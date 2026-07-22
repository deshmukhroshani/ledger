import streamlit as st
from PIL import Image
import os
from utils.card import draw_course_card

st.set_page_config(page_title="WealthWise AI", layout="wide", initial_sidebar_state="collapsed")

# Session state init
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---- redirect guard -----------------------------------
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")
    st.stop()                                   # prevent flash of content


# --- Load assets --
logo = Image.open("assets/wealthwiselogo.png")

st.markdown("---")
st.button("🚀 Take the FinQuiz again!", use_container_width=True)
st.markdown("---")

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
            target_page="pages/budget_saving_course.py",
        )

    with col2:
        draw_course_card(
            title="Arrays 101",
            subtitle="Introduction to Data Structure",
            chapters=6,
            items=31,
            progress=0,
            target_page="pages/budget_saving_course.py",
        )

    with col3:
        draw_course_card(
            title="Budget Basics",
            subtitle="Saving on Any Income",
            chapters=8,
            items=42,
            progress=25,
            target_page="pages/budget_saving_course.py",
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
