import streamlit as st
import json
import base64
from pathlib import Path

st.set_page_config(page_title="Client Profiles | MedGraphics", page_icon="🎨")

# Default fonts based on popular Google Fonts
FONT_OPTIONS = [
    "Inter", "Open Sans", "Roboto", "Lato", "Poppins",
    "Montserrat", "Playfair Display", "Merriweather", "Noto Sans"
]

def load_clients():
    clients_dir = Path("clients")
    if not clients_dir.exists():
        clients_dir.mkdir(parents=True)

    clients = {}
    for f in clients_dir.glob("*.json"):
        with open(f, "r", encoding="utf-8") as file:
            clients[f.stem] = json.load(file)
            clients[f.stem]["_filepath"] = str(f)
    return clients

def main():
    st.title("🎨 Client Profiles")
    st.markdown("Manage UI brand profiles for your medical graphics.")

    clients = load_clients()
    client_names = ["+ Create New Client"] + list(clients.keys())

    selected_profile = st.selectbox("Select Profile", options=client_names)

    st.divider()

    is_new = selected_profile == "+ Create New Client"

    with st.form("client_profile_form"):
        st.subheader("Brand Information")

        # Pre-fill data if editing
        current_data = clients.get(selected_profile, {}) if not is_new else {}

        name = st.text_input(
            "Client Name (Used as ID)",
            value=selected_profile if not is_new else "",
            disabled=not is_new
        )

        display_name = st.text_input("Display Name", value=current_data.get("name", ""))

        st.subheader("Brand Colors")
        col1, col2, col3 = st.columns(3)
        with col1:
            primary_color = st.color_picker("Primary Color", value=current_data.get("theme", {}).get("primary_color", "#2563eb"))
        with col2:
            secondary_color = st.color_picker("Secondary Color", value=current_data.get("theme", {}).get("secondary_color", "#1e40af"))
        with col3:
            accent_color = st.color_picker("Accent Color", value=current_data.get("theme", {}).get("accent_color", "#f59e0b"))

        st.subheader("Typography")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            heading_font = st.selectbox(
                "Heading Font",
                options=FONT_OPTIONS,
                index=FONT_OPTIONS.index(current_data.get("theme", {}).get("heading_font", "Inter")) if current_data.get("theme", {}).get("heading_font", "Inter") in FONT_OPTIONS else 0
            )
        with col_f2:
            body_font = st.selectbox(
                "Body Font",
                options=FONT_OPTIONS,
                index=FONT_OPTIONS.index(current_data.get("theme", {}).get("body_font", "Inter")) if current_data.get("theme", {}).get("body_font", "Inter") in FONT_OPTIONS else 0
            )

        st.subheader("Assets")
        logo_file = st.file_uploader("Upload Logo (PNG/SVG/JPG)", type=["png", "jpg", "jpeg", "svg"])

        if not is_new and current_data.get("logo"):
            st.image(current_data["logo"], width=150, caption="Current Logo")

        submitted = st.form_submit_button("Save Client Profile", type="primary")

        if submitted:
            if not name:
                st.error("Client Name is required.")
                return

            safe_id = "".join([c if c.isalnum() else "_" for c in name]).lower()

            logo_data = current_data.get("logo", "")
            if logo_file:
                # Read logo file as b64 data URI
                mime_type = logo_file.type
                b64_encoded = base64.b64encode(logo_file.read()).decode("utf-8")
                logo_data = f"data:{mime_type};base64,{b64_encoded}"

            new_profile = {
                "name": display_name or name,
                "theme": {
                    "primary_color": primary_color,
                    "secondary_color": secondary_color,
                    "accent_color": accent_color,
                    "heading_font": heading_font,
                    "body_font": body_font
                },
                "logo": logo_data
            }

            filepath = Path("clients") / f"{safe_id}.json"
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(new_profile, f, indent=2)

            st.success(f"Successfully saved profile for {name}!")
            st.rerun()

if __name__ == "__main__":
    main()
