import json
import logging
import litellm
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)

class LLMRouter:
    def __init__(self, config_path="config/models.yaml"):
        """Load model configs from YAML and initialize cost tracking."""
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        self.cost_summary = {}

        # Pre-compute model lookup for performance
        self._models_by_name = {}
        self._models_by_tier_and_task = {}

        for tier, models in self.config.get("models", {}).items():
            for m in models:
                self._models_by_name[m["name"]] = m

                # Pre-compute tier and task combinations
                for task in m.get("use_for", []):
                    key = (tier, task)
                    if key not in self._models_by_tier_and_task:
                        self._models_by_tier_and_task[key] = []
                    self._models_by_tier_and_task[key].append(m)

    def _track_cost(self, model_name: str, cost: float):
        if model_name not in self.cost_summary:
            self.cost_summary[model_name] = 0.0
        self.cost_summary[model_name] += cost

    def _get_model_config(self, model_name: str) -> dict:
        return self._models_by_name.get(model_name)

    def _get_models_for_task(self, task: str, tier: str) -> list:
        """Returns all models in a specific tier that support the given task."""
        return self._models_by_tier_and_task.get((tier, task), [])

    def call(self, task: str, prompt: str, tier: str = "auto") -> str:
        """
        Route a prompt to the appropriate model based on tier.
        If tier='auto', uses the default model for the task.
        """
        model_name = None
        max_tokens = 4096

        if tier == "auto":
            # Get default from config
            model_name = self.config.get("defaults", {}).get(task)
            if not model_name:
                raise ValueError(f"No default model configured for task '{task}'")
        else:
            task_models = self._get_models_for_task(task, tier)
            if not task_models:
                raise ValueError(f"No model found in tier '{tier}' for task '{task}'")
            model_name = task_models[0]["name"]

        model_cfg = self._get_model_config(model_name)
        if model_cfg:
            max_tokens = model_cfg.get("max_tokens", 4096)

        try:
            response = litellm.completion(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens
            )
            text = response.choices[0].message.content
            cost = litellm.completion_cost(completion_response=response)
            if cost is None:
                cost = 0.0
            self._track_cost(model_name, cost)
            return text
        except litellm.exceptions.AuthenticationError as e:
            msg = f"API Key missing or invalid for {model_name}. Please check your .env file or environment variables."
            logger.error(msg)
            raise ValueError(msg)
        except Exception as e:
            logger.error(f"Error calling {model_name}: {e}")
            raise

    def call_with_fallback(self, task: str, prompt: str, expect_json: bool = False) -> tuple[str, str, float]:
        """
        Always starts at free tier, escalates on failure.
        """
        tiers_to_try = ["free", "mid", "premium"]

        for tier in tiers_to_try:
            task_models = self._get_models_for_task(task, tier)
            for model_cfg in task_models:
                model_name = model_cfg["name"]
                max_tokens = model_cfg.get("max_tokens", 4096)

                try:
                    logger.info(f"Attempting {model_name} for {task} (tier: {tier})")
                    response = litellm.completion(
                        model=model_name,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=max_tokens
                    )
                    text = response.choices[0].message.content

                    if not text or not text.strip():
                        logger.warning(f"Empty response from {model_name}, escalating...")
                        continue

                    if expect_json:
                        try:
                            clean_text = text.strip()
                            if clean_text.startswith("```json"):
                                clean_text = clean_text[7:]
                            if clean_text.endswith("```"):
                                clean_text = clean_text[:-3]
                            json.loads(clean_text)
                        except json.JSONDecodeError:
                            logger.warning(f"Invalid JSON response from {model_name}, escalating...")
                            continue

                    cost = litellm.completion_cost(completion_response=response)
                    if cost is None:
                        cost = 0.0
                    self._track_cost(model_name, cost)
                    return text, model_name, cost

                except litellm.exceptions.AuthenticationError as e:
                    # Missing API key shouldn't be blindly skipped if it's a hard requirement, but for fallback
                    # we might escalate purely to try another provider the user DID configure.
                    logger.warning(f"Authentication setup error for {model_name}: {e}, escalating...")
                    continue
                except Exception as e:
                    logger.warning(f"API Error from {model_name}: {e}, escalating...")
                    continue

        raise RuntimeError(f"All fallback models failed for task '{task}'")

    def get_cost_summary(self) -> dict:
        """Return total costs per model for the session"""
        return self.cost_summary
