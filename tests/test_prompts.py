import sys
import os

# Ensure the root directory is on the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts.topic_generation import TOPIC_GENERATION_PROMPT

def test_prompts():
    print("Testing Topic Generation Prompt...")
    topic_prompt = TOPIC_GENERATION_PROMPT.format(
        specialty_name="Obstetrics & Gynecology",
        keywords="pregnancy scans, prenatal care",
        output_format="Instagram Story",
        width=1080,
        height=1920,
        num_topics=5
    )
    assert "Obstetrics & Gynecology" in topic_prompt
    
    print("All prompt formatting tests passed!")

if __name__ == "__main__":
    test_prompts()
