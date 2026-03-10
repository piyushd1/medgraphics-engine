import pytest
from engine.llm_router import LLMRouter

def test_llm_router_initialization():
    router = LLMRouter()
    assert router.cost_summary == {}
    
def test_validate_model_setup(mocker):
    mocker.patch("engine.llm_router.litellm.completion", return_value=True)
    router = LLMRouter()
    assert router.validate_model_setup("openai/gpt-4o-mini") is True
