import streamlit as st

# Set page config FIRST, before any other Streamlit commands
st.set_page_config(page_title="MedGraphics Engine", page_icon="🏥", layout="wide")

st.markdown("Redirecting to New Campaign...")

# Streamlit redirects to the first page in the pages/ folder if we just switch
st.switch_page("pages/0_🏥_New_Campaign.py")
