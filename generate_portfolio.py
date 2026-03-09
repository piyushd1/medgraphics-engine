import os
import json
import logging
from engine.pipeline import MedGraphicsPipeline
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def generate_portfolio():
    os.makedirs("portfolio", exist_ok=True)
    pipeline = MedGraphicsPipeline()
    
    specialties = ["cardiology", "pediatrics", "obstetrics_gynecology"]
    templates = ["timeline", "comparison", "checklist", "flowchart", "info_card", "icon_grid"]
    formats = ["instagram_story", "instagram_post"]
    
    # We need a client profile for generation
    client_profile = {
        "name": "Demo Hospital",
        "theme": {
            "primary_color": "#0369a1",
            "secondary_color": "#e0f2fe",
            "accent_color": "#f59e0b",
            "heading_font": "Inter",
            "body_font": "Roboto"
        }
    }
    
    logger.info(f"Starting sample portfolio generation ({len(specialties) * len(templates) * len(formats)} combinations)...")
    
    for specialty in specialties:
        for fmt in formats:
            logger.info(f"Generating topics for {specialty} ({fmt})...")
            
            try:
                # Ask for 6 topics, mapping exactly 1 to each template
                topics = pipeline.generate_topics(
                    specialty_key=specialty,
                    keywords="evidence-based, patient education",
                    output_format=fmt,
                    num_topics=6
                )
                
                # Render each topic across the 6 templates manually to ensure matrix completion
                for template in templates:
                    # Find a topic suitable or just use the first one and override template
                    topic = next((t for t in topics if t["template_type"] == template), topics[0])
                    topic["template_type"] = template
                    
                    output_path = f"portfolio/{specialty}_{template}_{fmt}.png"
                    logger.info(f"Rendering: {output_path}")
                    
                    pipeline.run_full_pipeline(
                        specialty_key=specialty,
                        topic=topic,
                        client_profile=client_profile,
                        output_format=fmt,
                        output_path=output_path
                    )
                    
            except Exception as e:
                logger.error(f"Failed matrix branch for {specialty}/{fmt}: {e}")
                
    logger.info("Portfolio generation complete.")

if __name__ == "__main__":
    generate_portfolio()
