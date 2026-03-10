import os
import streamlit as st

PROVIDER_REGISTRY = {
    "openai": {
        "display_name": "OpenAI",
        "env_key": "OPENAI_API_KEY",
        "text_models": [
            {"id": "openai/gpt-4o-mini", "name": "GPT-4o Mini"},
            {"id": "openai/gpt-4o", "name": "GPT-4o"},
            {"id": "openai/o3-mini", "name": "o3-mini"}
        ],
        "image_models": [
            {"id": "dall-e-3", "name": "DALL-E 3"},
            {"id": "dall-e-2", "name": "DALL-E 2"}
        ]
    },
    "gemini": {
        "display_name": "Google Gemini",
        "env_key": "GEMINI_API_KEY",
        "text_models": [
            {"id": "gemini/gemini-2.0-flash", "name": "Gemini 2.0 Flash"},
            {"id": "gemini/gemini-2.5-pro", "name": "Gemini 2.5 Pro"}
        ],
        "image_models": [
            {"id": "gemini/imagen-3", "name": "Imagen 3"}
        ]
    },
    "anthropic": {
        "display_name": "Anthropic",
        "env_key": "ANTHROPIC_API_KEY",
        "text_models": [
            {"id": "anthropic/claude-3-5-sonnet-20241022", "name": "Claude 3.5 Sonnet"},
            {"id": "anthropic/claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku"},
            {"id": "anthropic/claude-3-opus-20240229", "name": "Claude 3 Opus"}
        ],
        "image_models": []
    },
    "huggingface": {
        "display_name": "Hugging Face",
        "env_key": "HUGGINGFACE_API_KEY",
        "text_models": [
            {"id": "huggingface/mistralai/Mistral-7B-Instruct-v0.3", "name": "Mistral 7B Instruct"}
        ],
        "image_models": [
            {"id": "huggingface/stabilityai/stable-diffusion-xl-base-1.0", "name": "Stable Diffusion XL"},
            {"id": "huggingface/black-forest-labs/FLUX.1-schnell", "name": "FLUX.1 Schnell"}
        ]
    },
    "groq": {
        "display_name": "Groq",
        "env_key": "GROQ_API_KEY",
        "text_models": [
            {"id": "groq/llama-3.3-70b-versatile", "name": "Llama 3.3 70B"},
            {"id": "groq/mixtral-8x7b-32768", "name": "Mixtral 8x7b"}
        ],
        "image_models": []
    },
    "openrouter": {
        "display_name": "OpenRouter",
        "env_key": "OPENROUTER_API_KEY",
        "text_models": [
            {"id": "openrouter/anthropic/claude-3.5-sonnet", "name": "Claude 3.5 Sonnet (OpenRouter)"},
            {"id": "openrouter/google/gemini-2.0-flash-exp:free", "name": "Gemini Flash Free (OpenRouter)"}
        ],
        "image_models": []
    }
}

def get_available_providers() -> list[str]:
    """Return provider keys that have an API key configured."""
    return [
        provider_id for provider_id, config in PROVIDER_REGISTRY.items()
        if os.environ.get(config["env_key"]) or st.session_state.get(f"api_key_{provider_id}")
    ]

def get_available_models(model_type: str = "text") -> list[dict]:
    """Return configured models from available providers.
    model_type should be 'text' or 'image'."""
    available = []
    model_key = "text_models" if model_type == "text" else "image_models"

    for provider_id in get_available_providers():
        for model in PROVIDER_REGISTRY[provider_id][model_key]:
            available.append({
                **model,
                "provider": provider_id,
                "provider_name": PROVIDER_REGISTRY[provider_id]["display_name"]
            })

    # Always add a custom option for arbitrary routing (e.g. for Groq/OpenRouter text or Replicate image)
    available.append({
        "id": "custom",
        "name": "Custom Model Input...",
        "provider": "custom",
        "provider_name": "Custom"
    })

    return available

def get_model_display_options(model_type: str = "text") -> dict:
    """Return {display_label: model_id} for use in st.selectbox."""
    models = get_available_models(model_type)
    return {
        f"{m['name']} ({m['provider_name']})": m["id"]
        for m in models
    }

def validate_provider_key(provider_id: str) -> bool:
    """Check if the provider's API key is configured."""
    env_key = PROVIDER_REGISTRY[provider_id]["env_key"]
    key = os.environ.get(env_key) or st.session_state.get(f"api_key_{provider_id}")
    return bool(key and len(key) > 5)
