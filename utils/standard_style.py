from pathlib import Path
import streamlit as st

def load_css(name: str = "base.css"):
    css_path = Path("assets/styles/standard_style.css")
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.error(f"CSS {name} not found.")
