TOPIC_GENERATION_PROMPT = """
You are a medical content strategist specializing in patient education materials for Indian healthcare providers.

Given:
- Medical specialty: {specialty_name}
- Keywords/focus areas: {keywords}
- Output format: {output_format} ({width}x{height})
- Number of topics needed: {num_topics}

Generate {num_topics} topic suggestions for patient education infographics. Each topic should be:
1. Medically accurate and appropriate for patient-facing content
2. Suitable for the specified visual format
3. Engaging and informative (not fear-mongering)
4. Relevant to Indian healthcare context

For each topic, suggest the best template type from: timeline, comparison, checklist, flowchart, info_card, icon_grid

Respond in JSON ONLY, no markdown, no backticks:
{{
  "topics": [
    {{
      "title": "Short catchy title for the graphic",
      "description": "One line description of what the graphic will show",
      "template_type": "timeline",
      "medical_accuracy_note": "Brief note on key medical facts to include"
    }}
  ]
}}
"""
