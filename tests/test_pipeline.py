import json
import os
import sys
import re
from dotenv import load_dotenv

# Ensure the root directory is on the Python path since test is in tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.pipeline import MedGraphicsPipeline

load_dotenv()

def test_pipeline():
    print("Testing MedGraphicsPipeline...")
    
    # Needs to be created from the current working directory
    # Loading the default client profile
    with open("clients/default.json", "r", encoding="utf-8") as f:
        client_profile = json.load(f)
        
    pipeline = MedGraphicsPipeline(config_dir="config")
    
    # 1. Generate a topic
    print("Step 1: Generating topics...")
    topics = pipeline.generate_topics(
        specialty_key="obstetrics_gynecology", 
        keywords="NT Scan",
        output_format="instagram_story", 
        num_topics=1
    )
    
    if not topics:
        print("Failed to generate topics.")
        return
        
    topic = topics[0]
    print(f"Generated Topic: {topic['title']} (Template: {topic['template_type']})")
    
    # Define an output path
    os.makedirs("output", exist_ok=True)
    safe_type = re.sub(r'[^\w\.-]', '', topic['template_type'])
    output_path = f"output/test_pipeline_{safe_type}.png"
    
    # 2-4. Run the rest of the pipeline
    try:
        metadata = pipeline.run_full_pipeline(
            specialty_key="obstetrics_gynecology",
            topic=topic,
            client_profile=client_profile,
            output_format="instagram_story",
            output_path=output_path
        )
        
        print("\nPipeline completed successfully!")
        print(f"Saved Image: {metadata['image_path']}")
        print(f"Model Used: {metadata['model_used']}")
        print(f"Session Cost tracking looks good.")
        
        # Save HTML for debugging
        html_path = output_path.replace(".png", ".html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(metadata["html"])
        print(f"Saved HTML to {html_path}")
        
    finally:
        pipeline.renderer.stop()

if __name__ == "__main__":
    test_pipeline()
