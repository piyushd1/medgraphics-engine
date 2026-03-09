import pytest
from unittest.mock import patch, MagicMock
import litellm

import sys
import os

# Ensure the root directory is on the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.llm_router import LLMRouter

def test_llm_router_authentication_error():
    """
    Tests that LLMRouter.call correctly handles AuthenticationError from litellm.
    It should catch the litellm AuthenticationError, log a clear message,
    and raise a ValueError with a helpful message about API keys.
    """
    # Initialize the router
    router = LLMRouter("config/models.yaml")

    # We expect a litellm AuthenticationError to be caught and re-raised as ValueError
    with patch('litellm.completion') as mock_completion:
        error_msg = "Invalid API Key"
        # Mocking an AuthenticationError
        mock_completion.side_effect = litellm.exceptions.AuthenticationError(
            message=error_msg,
            llm_provider="fake_provider",
            model="fake_model"
        )

        # We expect a ValueError to be raised with our custom message
        with pytest.raises(ValueError) as exc_info:
            router.call(task="topic_generation", prompt="Test prompt", tier="auto")

        # Verify the exception message contains the expected helpful text
        assert "API Key missing or invalid for" in str(exc_info.value)
        assert "Please check your .env file or environment variables" in str(exc_info.value)
