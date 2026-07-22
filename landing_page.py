import streamlit as st
from PIL import Image
import os
from pathlib import Path
from utils.standard_style import load_css
from utils.hide_streamlit_default import hide_default_info
from utils.page_config import setup_page_config
from utils.nav import draw_nav

# Gather variables
logo = "assets/wealthwiselogo.png"
currency_img = "assets/currency2.png"

# Make the nav bar and setup default style.
setup_page_config()
hide_default_info()
load_css()
draw_nav()

# --- (everything above here stays the same) -------------------------
with st.container(key="main"):
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown(
            "<h2 style='font-size:28px; font-weight:700;'>Discover Your Financial Fitness Level</h2>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            - **Personalized Feedback:** Receive honest insights into your financial knowledge.
            - **Tailored Learning Path:** Get a customized roadmap to enhance your financial skills.
            - **Empowerment:** Equip yourself with the tools to make informed financial decisions.
            """
        )

        if st.button("Get Started", type="primary", use_container_width=True):
            st.switch_page("pages/demographics.py")

    with right_col:
        st.image(currency_img, width=500)

# 🔄 NEW:  side-by-side graphics banner (replaces “Analytics Here”)
with st.container(key="feature-graphics"):
    col_l, col_r = st.columns(2, gap= "large")   # weights [1,1] = 50 / 50

    with col_l:
        st.image("assets/WW_ButtonClicked_Chart.png", use_container_width=True)

    with col_r:
        st.image("assets/WW_Finquiz_sentiments_Chart.png", use_container_width=True)

