import streamlit as st
import os
import json
import yaml
from pathlib import Path
from engine.pipeline import MedGraphicsPipeline
from engine.llm_router import LLMRouter

st.set_page_config(page_title="MedGraphics Engine | New Campaign", page_icon="🏥", layout="wide")

def init_session_state():
    if "topics" not in st.session_state:
        st.session_state.topics = []
    if "generated_images" not in st.session_state:
        st.session_state.generated_images = []
    if "image_prompts" not in st.session_state:
        st.session_state.image_prompts = {}
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = MedGraphicsPipeline()
    if "model_topic" not in st.session_state:
        st.session_state.model_topic = "openai/gpt-4o-mini"
    if "model_prompt" not in st.session_state:
        st.session_state.model_prompt = "openai/gpt-4o"
    if "model_image" not in st.session_state:
        st.session_state.model_image = "dall-e-3"

def main():
    init_session_state()
    pipeline = st.session_state.pipeline

    st.title("🏥 MedGraphics AI Generator")
    st.markdown("Start a new AI image generation run.")

    has_keys = any([os.environ.get(k) for k in ["GEMINI_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "HUGGINGFACE_API_KEY", "GROQ_API_KEY", "OPENROUTER_API_KEY"]])
    if not has_keys:
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

    inspect_prompts = st.checkbox(
        "Inspect Prompts before generating",
        help="Pause before API calls to show the exact prompt being sent"
    )

    if st.button("✨ Step 1: Generate Topic Suggestions", use_container_width=True):
        with st.spinner(f"Generating topics using {st.session_state.model_topic}..."):
            try:
                topics = pipeline.generate_topics(
                    specialty_key=specialty_key,
                    keywords=val_keywords,
                    output_format=format_key,
                    num_topics=val_num_topics,
                    model_id=st.session_state.model_topic
                )
                st.session_state.topics = topics
                st.session_state.generated_images = []
                st.session_state.image_prompts = {}
                st.session_state.selected_specialty = specialty_key
                st.session_state.selected_format = format_key
                st.success(f"Generated {len(topics)} topics!")
            except Exception as e:
                st.error(f"Failed to generate topics: {e}")

    if st.session_state.topics:
        st.divider()
        st.subheader("Step 2: Generate Image Prompts for Topics")

        selected_topics = []
        for i, topic in enumerate(st.session_state.topics):
            checked = st.checkbox(
                f"**{topic['title']}** - *{topic['description']}*",
                value=True,
                key=f"topic_{i}"
            )
            if checked:
                selected_topics.append(topic)

        if st.button("🚀 Generate Prompts for Selected Topics", type="primary", use_container_width=True):
            if not selected_topics:
                st.warning("Please select at least one topic.")
                return

            progress_bar = st.progress(0, text="Starting prompt generation pipeline...")

            for i, topic in enumerate(selected_topics):
                progress_text = f"Generating prompt {i+1}/{len(selected_topics)}: {topic['title']}"
                progress_bar.progress(i / len(selected_topics), text=progress_text)

                try:
                    img_prompt = pipeline.generate_image_prompt(
                        topic=topic,
                        specialty_key=st.session_state.selected_specialty,
                        output_format=st.session_state.selected_format,
                        model_id=st.session_state.model_prompt
                    )
                    st.session_state.image_prompts[topic['title']] = {
                        "prompt": img_prompt,
                        "topic": topic
                    }
                except Exception as e:
                    st.error(f"Error generating prompt for '{topic['title']}': {e}")

            progress_bar.progress(1.0, text="Complete!")

    if st.session_state.image_prompts:
        st.divider()
        st.subheader("Step 3: Customize Image Prompts")
        st.markdown("Edit the generated prompts before sending them to the image model.")

        # We need a dictionary to store the user-edited prompts temporarily
        edited_prompts = {}
        for title, data in st.session_state.image_prompts.items():
            st.markdown(f"**Topic:** {title}")
            edited_prompts[title] = st.text_area(
                f"Prompt for {title}",
                value=data["prompt"],
                height=150,
                key=f"edit_prompt_{title}"
            )
            st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🖼️ Step 4: Generate Images", type="primary", use_container_width=True):

            progress_bar = st.progress(0, text="Generating images...")
            generated = []
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)

            titles = list(edited_prompts.keys())
            for i, title in enumerate(titles):
                progress_text = f"Generating image {i+1}/{len(titles)}: {title}"
                progress_bar.progress(i / len(titles), text=progress_text)

                final_prompt = edited_prompts[title]
                safe_title = "".join([c if c.isalnum() else "_" for c in title]).lower()
                output_path = f"{output_dir}/render_{safe_title}.png"

                try:
                    # Update the stored prompt to match what the user edited
                    st.session_state.image_prompts[title]["prompt"] = final_prompt

                    image_path = pipeline.generate_image(
                        final_prompt,
                        model_id=st.session_state.model_image,
                        output_path=output_path
                    )

                    generated.append({
                        "path": image_path,
                        "metadata": {
                            "topic": title,
                            "image_prompt": final_prompt,
                            "models_used": {
                                "topic_gen": st.session_state.model_topic,
                                "prompt_gen": st.session_state.model_prompt,
                                "image_gen": st.session_state.model_image
                            }
                        },
                        "topic": st.session_state.image_prompts[title]["topic"]
                    })
                except Exception as e:
                    st.error(f"Error generating image for '{title}': {e}")

            progress_bar.progress(1.0, text="All images generated!")
            st.session_state.generated_images = generated

    if st.session_state.generated_images:
        st.divider()
        st.subheader("Generated AI Images")

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
