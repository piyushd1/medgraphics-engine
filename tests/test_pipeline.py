import pytest
from engine.pipeline import MedGraphicsPipeline, safe_json_parse

def test_safe_json_parse():
    text = "```json\n{\"topics\": []}\n```"
    parsed = safe_json_parse(text)
    assert parsed == {"topics": []}
