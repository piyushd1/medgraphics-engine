import json
import yaml
import re
import logging
import requests
from pathlib import Path
from engine.llm_router import LLMRouter
from prompts.topic_generation import TOPIC_GENERATION_PROMPT

logger = logging.getLogger(__name__)

# Note: We now use a new set of prompts tailored to image generation.
# We'll define IMAGE_PROMPT_GENERATION_PROMPT directly here for simplicity since the templates/
# directory and content brief approach was removed.

IMAGE_PROMPT_GENERATION_PROMPT = """
You are an expert AI image prompt engineer specializing in medical infographics and creative assets.

Your task is to write a highly detailed, descriptive prompt for an AI image generator (like Midjourney, DALL-E 3)
to generate an image based on the following topic and specialty.

Topic: {topic_title}
Description: {topic_description}
Specialty: {specialty_name}
Format: {output_format}
Style Guidelines:
- Clean, professional medical style.
- Accurate but accessible visuals.
- Do NOT include text or words in the image (AI struggles with spelling). Focus on visual metaphors, diagrams, or photorealistic scenes.

Respond ONLY with the image generation prompt text. Do not wrap in quotes or code blocks.
"""

def clean_markdown_block(text: str) -> str:
    """Strip markdown code blocks if present"""
    text = text.strip()
    if text.startswith("```"):
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
        self.router = LLMRouter()
        
        # Load specialties and output formats config
        with open(f"{config_dir}/specialties.yaml", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
            
    def generate_topics(self, specialty_key: str, keywords: str, 
                        output_format: str, num_topics: int = 10, model_id: str = None) -> list[dict]:
        """Step 1: Generate topic suggestions"""
        if not model_id:
            raise ValueError("model_id is required for generate_topics")

        specialty = self.config["specialties"][specialty_key]
        format_config = self.config["output_formats"][output_format]
        
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
        
        response_text, model, cost = self.router.call(model_id, prompt, expect_json=True)
        return safe_json_parse(response_text)["topics"]
    
    def generate_image_prompt(self, topic: dict, specialty_key: str,
                              output_format: str, model_id: str = None) -> str:
        """Step 2: Generate an image prompt for the AI Image Generator"""
        if not model_id:
            raise ValueError("model_id is required for generate_image_prompt")

        specialty = self.config["specialties"][specialty_key]
        format_config = self.config["output_formats"][output_format]
        
        prompt = IMAGE_PROMPT_GENERATION_PROMPT.format(
            topic_title=topic["title"],
            topic_description=topic["description"],
            specialty_name=specialty["name"],
            output_format=format_config["name"]
        )
        
        response_text, model, cost = self.router.call(model_id, prompt, expect_json=False)
        return response_text.strip()
    
    def generate_image(self, image_prompt: str, model_id: str = None, output_path: str = None) -> str:
        """Step 3: Generate the actual image using an Image Generation Model"""
        if not model_id:
            raise ValueError("model_id is required for generate_image")

        image_url, model, cost = self.router.image_generation(model_id, image_prompt)
        
        # Download and save the image
        if output_path:
            response = requests.get(image_url)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return output_path

        return image_url
    
    def run_full_pipeline(self, specialty_key: str, topic: dict,
                          output_format: str, output_path: str,
                          topic_model: str, prompt_model: str, image_model: str) -> dict:
        """Run complete pipeline for one topic. Returns metadata."""
        
        logger.info(f"[{topic['title']}] Generating image prompt...")
        image_prompt = self.generate_image_prompt(
            topic, specialty_key, output_format, model_id=prompt_model
        )
        
        logger.info(f"[{topic['title']}] Generating image...")
        image_path = self.generate_image(
            image_prompt, model_id=image_model, output_path=output_path
        )
        
        return {
            "topic": topic["title"],
            "image_path": image_path,
            "image_prompt": image_prompt,
            "models_used": {
                "topic_gen": topic_model,
                "prompt_gen": prompt_model,
                "image_gen": image_model
            },
            "cost": sum(self.router.cost_summary.values()) # Total cost incurred so far
        }
