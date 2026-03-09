import json
import yaml
import re
import logging
from pathlib import Path
from engine.llm_router import LLMRouter
from engine.template_engine import TemplateEngine
from engine.renderer import Renderer
from prompts.topic_generation import TOPIC_GENERATION_PROMPT
from prompts.content_brief import CONTENT_BRIEF_PROMPT, TEMPLATE_SCHEMAS
from prompts.html_generation import HTML_GENERATION_PROMPT

logger = logging.getLogger(__name__)

def clean_markdown_block(text: str) -> str:
    """Strip markdown code blocks if present"""
    text = text.strip()
    if text.startswith("```"):
        # Find the first newline after ``` to strip language identifier like json or html
        newline_idx = text.find("\n")
        if newline_idx != -1 and newline_idx < 15:
            text = text[newline_idx+1:]
        else:
            text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def safe_json_parse(text: str) -> dict:
    """Parse JSON from LLM response, handling common issues"""
    text = clean_markdown_block(text)
    return json.loads(text)

class MedGraphicsPipeline:
    def __init__(self, config_dir="config"):
        self.router = LLMRouter(f"{config_dir}/models.yaml")
        self.template_engine = TemplateEngine("templates")
        self.renderer = Renderer()

        # Load specialties and output formats config
        with open(f"{config_dir}/specialties.yaml", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

    def generate_topics(self, specialty_key: str, keywords: str,
                        output_format: str, num_topics: int = 10) -> list[dict]:
        """Step 1: Generate topic suggestions"""
        specialty = self.config["specialties"][specialty_key]
        format_config = self.config["output_formats"][output_format]

        # Prevent prompt injection by heavily sanitizing keywords
        raw_keywords = keywords or specialty.get("topics_hint", "")
        safe_keywords = re.sub(r'[^\w\s,\.-]', '', raw_keywords)

        prompt = TOPIC_GENERATION_PROMPT.format(
            specialty_name=specialty["name"],
            keywords=safe_keywords,
            output_format=format_config["name"],
            width=format_config["width"],
            height=format_config["height"],
            num_topics=num_topics
        )

        response_text, model, cost = self.router.call_with_fallback("topic_generation", prompt, expect_json=True)
        return safe_json_parse(response_text)["topics"]

    def generate_content(self, topic: dict, specialty_key: str,
                         output_format: str) -> dict:
        """Step 2: Generate structured content for a topic"""
        specialty = self.config["specialties"][specialty_key]
        format_config = self.config["output_formats"][output_format]
        template_type = topic["template_type"]

        prompt = CONTENT_BRIEF_PROMPT.format(
            topic_title=topic["title"],
            topic_description=topic["description"],
            template_type=template_type,
            specialty_name=specialty["name"],
            output_format=format_config["name"],
            width=format_config["width"],
            height=format_config["height"],
            template_data_schema=TEMPLATE_SCHEMAS.get(template_type, "{}")
        )

        response_text, model, cost = self.router.call_with_fallback("content_brief", prompt, expect_json=True)
        return safe_json_parse(response_text)

    def generate_html(self, content: dict, template_type: str,
                      client_profile: dict, output_format: str) -> str:
        """Step 3: Generate complete HTML"""
        format_config = self.config["output_formats"][output_format]

        prompt = HTML_GENERATION_PROMPT.format(
            content_json=json.dumps(content, indent=2),
            template_type=template_type,
            width=format_config["width"],
            height=format_config["height"],
            primary_color=client_profile["theme"]["primary_color"],
            secondary_color=client_profile["theme"]["secondary_color"],
            accent_color=client_profile["theme"]["accent_color"],
            font_heading=client_profile["theme"]["font_heading"],
            font_body=client_profile["theme"]["font_body"]
        )

        # HTML generation doesn't return JSON
        response_text, model, cost = self.router.call_with_fallback("html_generation", prompt, expect_json=False)

        # Cleanup markdown formatting around HTML using shared helper
        return clean_markdown_block(response_text)

    def render_image(self, html: str, output_path: str,
                     output_format: str) -> str:
        """Step 4: Render HTML to PNG"""
        format_config = self.config["output_formats"][output_format]
        return self.renderer.render_html_to_png(
            html, output_path,
            format_config["width"], format_config["height"]
        )

    def run_full_pipeline(self, specialty_key: str, topic: dict,
                          client_profile: dict, output_format: str,
                          output_path: str) -> dict:
        """Run complete pipeline for one topic. Returns metadata."""

        logger.info(f"[{topic['title']}] Generating structured content...")
        content = self.generate_content(topic, specialty_key, output_format)

        logger.info(f"[{topic['title']}] Generating HTML code...")
        html = self.generate_html(content, topic["template_type"], client_profile, output_format)

        logger.info(f"[{topic['title']}] Rendering PNG...")
        # Start renderer if not started
        if not self.renderer.browser:
            self.renderer.start()
        image_path = self.render_image(html, output_path, output_format)

        return {
            "topic": topic["title"],
            "template_type": topic["template_type"],
            "image_path": image_path,
            "html": html,  # Save for debugging/editing
            "model_used": self.router.last_model_used,
            "cost": self.router.last_cost.get("total_cost", 0.0)
        }
