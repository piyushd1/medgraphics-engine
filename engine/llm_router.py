import json
import logging
import litellm
import os

logger = logging.getLogger(__name__)

class LLMRouter:
    def __init__(self):
        """Initialize cost tracking."""
        self.cost_summary = {}
        self.last_model_used = None
        self.last_cost = {"total_cost": 0.0}

    def _track_cost(self, model_name: str, cost: float):
        if model_name not in self.cost_summary:
            self.cost_summary[model_name] = 0.0
        self.cost_summary[model_name] += cost
        self.last_cost["total_cost"] = cost

    def validate_model_setup(self, model_id: str) -> bool:
        """Run a minimal test API call to validate keys and model names."""
        if not model_id:
            return False

        try:
            logger.info(f"Validating model setup for {model_id}...")
            # Very small completion to minimize cost
            response = litellm.completion(
                model=model_id,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            logger.warning(f"Validation failed for {model_id}: {e}")
            return False

    def call(self, model_id: str, prompt: str, expect_json: bool = False, max_tokens: int = 4096) -> tuple[str, str, float]:
        """
        Route a prompt to the explicitly provided model.
        Returns tuple of (response_text, model_id, cost).
        """
        if not model_id:
            raise ValueError("model_id must be provided to LLMRouter.call")

        try:
            logger.info(f"Attempting {model_id}")
            self.last_model_used = model_id
            response = litellm.completion(
                model=model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            text = response.choices[0].message.content

            if expect_json and text:
                try:
                    clean_text = text.strip()
                    if clean_text.startswith("```json"):
                        clean_text = clean_text[7:]
                    if clean_text.endswith("```"):
                        clean_text = clean_text[:-3]
                    json.loads(clean_text)
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON response from {model_id}")

            cost = litellm.completion_cost(completion_response=response)
            if cost is None:
                cost = 0.0
            self._track_cost(model_id, cost)
            return text, model_id, cost

        except litellm.exceptions.AuthenticationError as e:
            msg = f"API Key missing or invalid for {model_id}. Please check your configuration."
            logger.error(msg)
            raise ValueError(msg)
        except Exception as e:
            logger.error(f"Error calling {model_id}: {e}")
            raise

    def image_generation(self, model_id: str, prompt: str) -> tuple[str, str, float]:
        """
        Generate an image using the specified model.
        Returns tuple of (image_url, model_id, cost).
        """
        if not model_id:
            raise ValueError("model_id must be provided to LLMRouter.image_generation")

        try:
            logger.info(f"Generating image with {model_id}")
            self.last_model_used = model_id
            response = litellm.image_generation(
                model=model_id,
                prompt=prompt
            )
            image_url = response.data[0].url

            cost = litellm.completion_cost(completion_response=response)
            if cost is None:
                cost = 0.0
            self._track_cost(model_id, cost)
            return image_url, model_id, cost

        except Exception as e:
            logger.error(f"Error generating image with {model_id}: {e}")
            raise

    def get_cost_summary(self) -> dict:
        """Return total costs per model for the session"""
        total = sum(self.cost_summary.values())
        return {
            "total_cost": total,
            "model_costs": self.cost_summary
        }
