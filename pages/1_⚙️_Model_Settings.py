import streamlit as st
import os
import dotenv
from engine.llm_router import LLMRouter
from engine.model_registry import PROVIDER_REGISTRY, validate_provider_key, get_model_display_options

st.set_page_config(page_title="Model Settings | MedGraphics", page_icon="⚙️")

def load_env_file():
    env_path = ".env"
    if not os.path.exists(env_path):
        open(env_path, "a").close()
    return env_path

def main():
    st.title("⚙️ Model Settings")
    st.markdown("Configure your API keys and select models for each stage of the AI graphics pipeline.")
    
    env_path = load_env_file()
    dotenv.load_dotenv(env_path)
    
    st.header("1. API Keys")
    st.markdown("Enter API keys for providers you want to use. **Models will only appear if their provider is connected.**")

    for provider_id, config in PROVIDER_REGISTRY.items():
        name = config["display_name"]
        env_key = config["env_key"]

        col1, col2 = st.columns([3, 1])
        with col1:
            key_val = st.text_input(
                f"{name} API Key",
                value=st.session_state.get(f"api_key_{provider_id}", os.environ.get(env_key, "")),
                type="password",
                key=f"input_{env_key}"
            )
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if validate_provider_key(provider_id):
                st.success("Connected")
            else:
                st.caption("Not set")
        
        if key_val:
            os.environ[env_key] = key_val
            st.session_state[f"api_key_{provider_id}"] = key_val
            dotenv.set_key(env_path, env_key, key_val)
        elif env_key in os.environ and not key_val:
            os.environ.pop(env_key)
            if f"api_key_{provider_id}" in st.session_state:
                del st.session_state[f"api_key_{provider_id}"]
            dotenv.unset_key(env_path, env_key)

    # We don't need a Save button anymore since text_input changes instantly trigger a rerun and update os.environ

    st.divider()
    st.header("2. Pipeline Models")

    text_models = get_model_display_options("text")
    image_models = get_model_display_options("image")

    if not text_models or len(text_models) == 1:
        st.warning("⚠️ No API keys configured. Connect a provider above to see available models.")
    else:
        # ---- Topic Generation ----
        topic_idx = 0
        topic_options = list(text_models.values())
        if st.session_state.get("model_topic") in topic_options:
            topic_idx = topic_options.index(st.session_state["model_topic"])

        topic_model_selected = st.selectbox(
            "Topic Generation Model",
            options=topic_options,
            index=topic_idx,
            format_func=lambda x: [k for k, v in text_models.items() if v == x][0]
        )
        if topic_model_selected == "custom":
            topic_model_selected = st.text_input("Custom Topic Model ID", value=st.session_state.get("model_topic_custom", "openrouter/anthropic/claude-3-sonnet"))
            st.session_state["model_topic_custom"] = topic_model_selected

        # ---- Image Prompt Generation ----
        prompt_idx = 0
        prompt_options = list(text_models.values())
        if st.session_state.get("model_prompt") in prompt_options:
            prompt_idx = prompt_options.index(st.session_state["model_prompt"])

        prompt_model_selected = st.selectbox(
            "Image Prompt Generation Model",
            options=prompt_options,
            index=prompt_idx,
            format_func=lambda x: [k for k, v in text_models.items() if v == x][0]
        )
        if prompt_model_selected == "custom":
            prompt_model_selected = st.text_input("Custom Prompt Model ID", value=st.session_state.get("model_prompt_custom", "openai/gpt-4o"))
            st.session_state["model_prompt_custom"] = prompt_model_selected

        # ---- Image Generation ----
        img_idx = 0
        img_options = list(image_models.values())
        if st.session_state.get("model_image") in img_options:
            img_idx = img_options.index(st.session_state["model_image"])

        img_model_selected = st.selectbox(
            "Image Generation Model",
            options=img_options,
            index=img_idx,
            format_func=lambda x: [k for k, v in image_models.items() if v == x][0]
        )
        if img_model_selected == "custom":
            img_model_selected = st.text_input("Custom Image Model ID", value=st.session_state.get("model_image_custom", "dall-e-3"))
            st.session_state["model_image_custom"] = img_model_selected


        if st.button("Validate & Save Models", type="primary"):
            router = LLMRouter()
            with st.spinner("Validating..."):
                valid = True

                if not router.validate_model_setup(topic_model_selected):
                    st.error(f"Failed to validate Topic model: {topic_model_selected}")
                    valid = False
                if not router.validate_model_setup(prompt_model_selected):
                    st.error(f"Failed to validate Image Prompt model: {prompt_model_selected}")
                    valid = False

                if valid:
                    st.session_state.model_topic = topic_model_selected
                    st.session_state.model_prompt = prompt_model_selected
                    st.session_state.model_image = img_model_selected
                    st.success("Models validated and saved for this session!")

    st.divider()
    st.header("3. Session Cost Tracker")
    
    if "pipeline" in st.session_state:
        router = st.session_state.pipeline.router
        costs = router.get_cost_summary()
        st.metric("Total Session Cost", f"${costs['total_cost']:.4f}")
        
        if costs['model_costs']:
            st.subheader("Breakdown by Model")
            for model, cost in costs['model_costs'].items():
                st.write(f"- **{model}**: ${cost:.4f}")
        else:
            st.info("No API calls made yet in this session.")
    else:
        st.info("Start a generation run on the main page to track costs.")

if __name__ == "__main__":
    main()
