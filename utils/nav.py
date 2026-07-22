import streamlit as st
from pathlib import Path
from utils.standard_style import load_css

def draw_nav():
    load_css()
    _inject_nav_css()

    HOME_PAGE = "landing_page.py"

    # this container becomes the sticky bar
    with st.container(key="nav") as bar:
        col_logo, col_brand, col_login, col_signup = st.columns(
            [1, 6, 1.2, 1.2], gap="small"
        )

        with col_logo:
            st.image("assets/wealthwiselogo.png", width=34)

        with col_brand:
            if st.button("WealthWise", key="brand_btn",
                         type="secondary", help="Home",
                         use_container_width=True):
                st.switch_page(HOME_PAGE)


        with col_login:
            st.page_link("pages/login.py", label="Log in", use_container_width=True)

        with col_signup:
            st.page_link("pages/signup.py", label="Sign up", use_container_width=True)

def _inject_nav_css():
    css = Path("assets/styles/landing_page.css").read_text("utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
