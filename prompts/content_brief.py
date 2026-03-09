CONTENT_BRIEF_PROMPT = """
You are a medical content writer creating structured data for a patient education infographic.

Topic: {topic_title}
Description: {topic_description}
Template type: {template_type}
Specialty: {specialty_name}
Output format: {output_format} ({width}x{height})

Generate the COMPLETE structured content for this infographic. The content must be:
1. Medically accurate (suitable for patient education)
2. Written in simple, clear English (assume 8th-grade reading level)
3. Concise — infographics need SHORT text, not paragraphs
4. Positive/empowering tone, NOT fear-based

Generate content matching the template type's data structure.

For template_type="{template_type}", respond in JSON ONLY:
{template_data_schema}
"""

TEMPLATE_SCHEMAS = {
    "timeline": '''{
      "title": "string",
      "subtitle": "string (optional)",
      "timeline_items": [{"position": number, "icon": "emoji", "label": "short text"}],
      "highlight_range": {"start": number, "end": number, "label": "string"},
      "bullets": ["string"],
      "footer": "string"
    }''',
    
    "comparison": '''{
      "title": "string",
      "subtitle": "string",
      "left": {
        "heading": "string (positive framing)",
        "subheading": "string",
        "steps": [{"icon": "emoji", "label": "short text"}]
      },
      "right": {
        "heading": "string (alternative framing)",
        "subheading": "string",
        "steps": [{"icon": "emoji", "label": "short text"}]
      },
      "bottom_note": "string (balanced, non-alarming)",
      "footer_left": "string",
      "footer_right": "string"
    }''',
    
    "checklist": '''{
      "title": "string",
      "items": [
        {"icon": "emoji", "heading": "short text", "description": "brief explanation"}
      ],
      "footer": "string"
    }''',
    
    "flowchart": '''{
      "title": "string",
      "paths": [
        {
          "heading": "string (e.g., Regular Check-ups)",
          "color": "string (positive or negative)",
          "steps": ["short text step 1", "short text step 2", "short text step 3", "short text step 4"]
        }
      ]
    }''',
    
    "info_card": '''{
      "title": "short catchy title",
      "bullets": ["short bullet 1", "short bullet 2", "short bullet 3"],
      "illustration_placeholder": boolean,
      "background_style": "string (e.g., soft_gradient)"
    }''',
    
    "icon_grid": '''{
      "title": "short text title",
      "center": {"icon": "emoji", "label": "short text"},
      "cards": [
        {"icon": "emoji", "heading": "short text", "description": "brief explanation"}
      ]
    }'''
}
