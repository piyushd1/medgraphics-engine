import streamlit as st
import os
import json
import yaml
from pathlib import Path
from engine.pipeline import MedGraphicsPipeline

# Set page config FIRST, before any other Streamlit commands
st.set_page_config(page_title="MedGraphics Engine | New Campaign", page_icon="🏥", layout="wide")

def init_session_state():
    if "topics" not in st.session_state:
        st.session_state.topics = []
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = MedGraphicsPipeline()

def load_config():
    with open("config/specialties.yaml", "r", encoding="utf-8") as f:
        specialties_config = yaml.safe_load(f)
    with open("config/specialties.yaml", "r", encoding="utf-8") as f:
        # Load output_formats from the same file as per original instructions, or models if separated
        # We know output_formats is in specialties.yaml
        pass

    # Actually pipeline has config loaded already.
    return specialties_config

def get_clients():
    clients_dir = Path("clients")
    # if it doesn't exist, use config/clients
    if not clients_dir.exists():
        clients_dir = Path("config/clients")

    client_files = list(clients_dir.glob("*.json"))
    clients = {}
    for f in client_files:
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            clients[f.stem] = data
    return clients

def main():
    init_session_state()
    pipeline = st.session_state.pipeline

    st.title("🏥 MedGraphics Engine")
    st.markdown("Start a new graphic generation run.")

    # Ensure API keys are set or warn
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("OPENAI_API_KEY") and not os.environ.get("HUGGINGFACE_API_KEY"):
        st.warning("⚠️ No API keys found! Please go to **Model Settings** in the sidebar to configure them before generating.")

    col1, col2 = st.columns(2)

    specialties_config = pipeline.config.get("specialties", {})
    output_formats = pipeline.config.get("output_formats", {})

    specialty_options = {k: v["name"] for k, v in specialties_config.items()}
    format_options = {k: v["name"] for k, v in output_formats.items()}

    with col1:
        specialty_key = st.selectbox("Medical Specialty", options=list(specialty_options.keys()), format_func=lambda x: specialty_options[x])
        val_keywords = st.text_input("Keywords (optional)", help="e.g. 'pregnancy nutrition, safe exercises'")
    with col2:
        format_key = st.selectbox("Output Format", options=list(format_options.keys()), format_func=lambda x: format_options[x])
        val_num_topics = st.number_input("How many topics?", min_value=1, max_value=20, value=3)

    clients = get_clients()
    client_options = {k: v.get("name", k) for k, v in clients.items()}
    selected_client_key = st.selectbox("Client Profile", options=list(client_options.keys()), format_func=lambda x: client_options[x])

    if st.button("✨ Generate Topic Suggestions", use_container_width=True):
        with st.spinner("Generating topics..."):
            try:
                topics = pipeline.generate_topics(
                    specialty_key=specialty_key,
                    keywords=val_keywords,
                    output_format=format_key,
                    num_topics=val_num_topics
                )
                st.session_state.topics = topics
                # Reset previous generations
                st.session_state.generated_images = []
                st.session_state.selected_specialty = specialty_key
                st.session_state.selected_format = format_key
                st.session_state.selected_client = selected_client_key
                st.success(f"Generated {len(topics)} topics!")
            except Exception as e:
                st.error(f"Failed to generate topics: {e}")

    if st.session_state.topics:
        st.divider()
        st.subheader("Select Topics to Generate")

        selected_topics = []
        for i, topic in enumerate(st.session_state.topics):
            # Checkbox for each topic
            checked = st.checkbox(
                f"**{topic['title']}** ({topic['template_type']}) - *{topic['description']}*",
                value=True,
                key=f"topic_{i}"
            )
            if checked:
                selected_topics.append(topic)

        if st.button("🚀 Generate Graphics for Selected Topics", type="primary", use_container_width=True):
            if not selected_topics:
                st.warning("Please select at least one topic.")
                return

            progress_bar = st.progress(0, text="Starting rendering pipeline...")

            client_profile = clients[st.session_state.selected_client]

            generated = []
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)

            for i, topic in enumerate(selected_topics):
                progress_text = f"Generating {i+1}/{len(selected_topics)}: {topic['title']}"
                progress_bar.progress(i / len(selected_topics), text=progress_text)

                safe_title = "".join([c if c.isalnum() else "_" for c in topic['title']]).lower()
                output_path = f"{output_dir}/render_{safe_title}.png"

                try:
                    metadata = pipeline.run_full_pipeline(
                        specialty_key=st.session_state.selected_specialty,
                        topic=topic,
                        client_profile=client_profile,
                        output_format=st.session_state.selected_format,
                        output_path=output_path
                    )
                    generated.append({
                        "path": output_path,
                        "metadata": metadata,
                        "topic": topic
                    })
                except Exception as e:
                    st.error(f"Error generating '{topic['title']}': {e}")

            progress_bar.progress(1.0, text="Complete!")
            st.session_state.generated_images = generated

    if st.session_state.generated_images:
        st.divider()
        st.subheader("Generated Graphics")

        cols = st.columns(3)
        for i, img_data in enumerate(st.session_state.generated_images):
            col = cols[i % 3]
            with col:
                st.image(img_data["path"], caption=img_data["topic"]["title"], use_container_width=True)
                with open(img_data["path"], "rb") as file:
                    st.download_button(
                        label="⬇️ Download",
                        data=file,
                        file_name=os.path.basename(img_data["path"]),
                        mime="image/png",
                        key=f"dl_{i}"
                    )

if __name__ == "__main__":
    main()
