from prompts.topic_generation import TOPIC_GENERATION_PROMPT
from prompts.content_brief import CONTENT_BRIEF_PROMPT, TEMPLATE_SCHEMAS
from prompts.html_generation import HTML_GENERATION_PROMPT

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
    
    print("Testing Content Brief Prompt...")
    brief_prompt = CONTENT_BRIEF_PROMPT.format(
        topic_title="Anomaly Scan Window",
        topic_description="Why the anomaly scan is done between 20-24 weeks",
        template_type="timeline",
        specialty_name="Obstetrics & Gynecology",
        output_format="Instagram Story",
        width=1080,
        height=1920,
        template_data_schema=TEMPLATE_SCHEMAS["timeline"]
    )
    assert "Anomaly Scan Window" in brief_prompt
    assert "timeline_items" in brief_prompt
    
    print("Testing HTML Generation Prompt...")
    html_prompt = HTML_GENERATION_PROMPT.format(
        content_json='{"title": "Test Box"}',
        template_type="timeline",
        width=1080,
        height=1920,
        primary_color="#FFAA00",
        secondary_color="#00AAFF",
        accent_color="#FF00AA",
        font_heading="Inter",
        font_body="Roboto"
    )
    assert '{"title": "Test Box"}' in html_prompt
    
    print("All prompt formatting tests passed!")

if __name__ == "__main__":
    test_prompts()
