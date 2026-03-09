import streamlit as st
import os
import glob
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Output Gallery | MedGraphics", page_icon="🖼️")

def get_generated_images(output_dir="output"):
    if not os.path.exists(output_dir):
        return []

    # Get all PNGs
    files = glob.glob(os.path.join(output_dir, "*.png"))

    # Sort by creation time (newest first)
    files.sort(key=os.path.getmtime, reverse=True)

    # Metadata parsing (basic)
    images = []
    for f in files:
        filename = os.path.basename(f)
        mtime = os.path.getmtime(f)
        date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")

        images.append({
            "path": f,
            "filename": filename,
            "date": date_str,
            "timestamp": mtime
        })

    return images

def main():
    st.title("🖼️ Output Gallery")
    st.markdown("Browse and download previously generated graphics.")

    images = get_generated_images()

    if not images:
        st.info("No generated images found in the output folder. Go to New Campaign to create some!")
        return

    st.write(f"Found **{len(images)}** images.")

    # Optional search/filter
    search_query = st.text_input("Search by filename", "")

    if search_query:
        images = [img for img in images if search_query.lower() in img["filename"].lower()]

    st.divider()

    # Layout in a grid
    cols_per_row = 3
    for i in range(0, len(images), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(images):
                img = images[i + j]
                with cols[j]:
                    st.image(img["path"], caption=img["filename"], use_container_width=True)
                    st.caption(f"Created: {img['date']}")

                    with open(img["path"], "rb") as file:
                        st.download_button(
                            label="⬇️ Download",
                            data=file,
                            file_name=img["filename"],
                            mime="image/png",
                            key=f"dl_{img['filename']}_{i+j}"
                        )
                    st.markdown("<br>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
