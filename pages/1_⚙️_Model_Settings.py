import streamlit as st
import os
import dotenv

st.set_page_config(page_title="Model Settings | MedGraphics", page_icon="⚙️")

def load_env_file():
    env_path = ".env"
    if not os.path.exists(env_path):
        open(env_path, "a").close()
    return env_path

def main():
    st.title("⚙️ Model Settings")
    st.markdown("Configure your AI models and track API usage costs for this session.")

    st.header("API Keys")

    env_path = load_env_file()
    dotenv.load_dotenv(env_path)

    col1, col2 = st.columns([3, 1])
    with col1:
        gemini_key = st.text_input("Gemini API Key", value=os.environ.get("GEMINI_API_KEY", ""), type="password")
        openai_key = st.text_input("OpenAI API Key", value=os.environ.get("OPENAI_API_KEY", ""), type="password")
        anthropic_key = st.text_input("Anthropic API Key", value=os.environ.get("ANTHROPIC_API_KEY", ""), type="password")
        hf_key = st.text_input("HuggingFace API Key", value=os.environ.get("HUGGINGFACE_API_KEY", ""), type="password")

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("✅ Connected" if os.environ.get("GEMINI_API_KEY") else "❌ Not set")
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("✅ Connected" if os.environ.get("OPENAI_API_KEY") else "❌ Not set")
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("✅ Connected" if os.environ.get("ANTHROPIC_API_KEY") else "❌ Not set")
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("✅ Connected" if os.environ.get("HUGGINGFACE_API_KEY") else "❌ Not set")

    if st.button("Save API Keys", type="primary"):
        keys_to_save = {
            "GEMINI_API_KEY": gemini_key,
            "OPENAI_API_KEY": openai_key,
            "ANTHROPIC_API_KEY": anthropic_key,
            "HUGGINGFACE_API_KEY": hf_key,
        }
        for k, v in keys_to_save.items():
            if v:
                os.environ[k] = v
                dotenv.set_key(env_path, k, v)
            elif k in os.environ:
                # Need to clear it if it was emptied
                os.environ.pop(k)
                dotenv.unset_key(env_path, k)
        st.success("API keys saved successfully!")
        st.rerun()

    st.divider()
    st.header("Cost Tracker")

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
