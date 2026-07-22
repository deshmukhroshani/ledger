import streamlit as st
from PIL import Image
import os
from utils.card import draw_course_card
from utils.standard_style import load_css
from utils.hide_streamlit_default import hide_default_info
from utils.page_config import setup_page_config
from utils.nav import draw_nav
from backend.get_user_info import fetch_quiz_questions, fetch_demographics
from backend.roadmap_db import fetch_roadmap


# Load in standard css
setup_page_config()
hide_default_info()
load_css()
draw_nav()

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.username is not None:
    st.session_state.quiz_questions = fetch_quiz_questions(st.session_state.username)
    st.session_state.demographics = fetch_demographics(st.session_state.username)
    st.session_state.roadmap_data = fetch_roadmap(st.session_state.username)
    if st.session_state.quiz_questions is not None and st.session_state.demographics and st.button("🚀 Take the FinQuiz again!", use_container_width=True):
        st.switch_page("pages/fin_quiz_retake.py")
    if st.session_state.roadmap_data is not None and st.button("🗺️ Your Personalized Financial Roadmap", use_container_width=True):
        st.switch_page("pages/roadmap.py")
else:
    st.button("🚀 Take the FinQuiz again!", use_container_width=True, disabled=True)
    st.button("🗺️ Your Personalized Financial Roadmap", use_container_width=True, disabled=True)

# ---- redirect guard -----------------------------------
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()                                   # prevent flash of content


# --- Load assets --
logo = Image.open("assets/wealthwiselogo.png")

# --- Main dashboard layout ---
left, right = st.columns([4, 1])

with left:
    st.markdown("### 📚 Explore Courses")

    col1, col2, col3 = st.columns(3)

    with col1:
        draw_course_card(
            title="Graph",
            subtitle="Detailed Explanation of",
            chapters=6,
            items=56,
            progress=0,
            target_page="pages/roadmap.py",
        )

with right:
    st.markdown("### 🎁 My Rewards")
    st.warning("You’ve earned 300 points. Redeem soon!")

st.markdown("---")
st.markdown("### 📈 Analytics")
st.line_chart({"Savings": [200, 300, 250, 400, 500], "Investments": [100, 200, 300, 350, 450]})

# --- Chat bubble ---
st.markdown("""
<style>
#chat-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #2e7bcf;
    color: white;
    border-radius: 50%;
    width: 60px;
    height: 60px;
    text-align: center;
    font-size: 30px;
    line-height: 60px;
    cursor: pointer;
    z-index: 1000;
}
</style>
<div id="chat-button" onclick="alert('Chat feature coming soon!')">💬</div>
""", unsafe_allow_html=True)
