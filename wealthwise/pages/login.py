import streamlit as st
from pathlib import Path
from time import sleep

# Configuration for the page
st.set_page_config(page_title="WealthWise | Login", layout="centered")

# Load in CSS
css_path = Path("assets/styles/login.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
else:
    print("Path for css was not found")

# Redirect the user if they are already authenticated
if st.session_state.get("authenticated", False):
    # We will just go back to the landing page
    st.switch_page("pages\login_home_page.py")
    st.stop()
else:
    # Login form
    st.image("assets/wealthwiselogo.png", width=120)
    st.subheader("Sign in to WealthWise AI")

    # Temporary user for now
    USERS = {"demo": "hackathon123"}

    # Create a form
    with st.form("login_form", clear_on_submit=True):
        user = st.text_input(
            label = "Username",
            max_chars = 255
        )
        pwd = st.text_input(
            "Password",
            max_chars = 100,
            type="password"
        )
        submit = st.form_submit_button(
            label = "Login"
        )
        st.page_link("pages/signup.py", label = "Don't have an account? Register")

    # Log the user in if their password was correct
    if submit:
        st.session_state.logged_in = True          # unify on ONE flag
        st.session_state.username  = user          # remember user
        st.success("Login successful! Redirecting…")
        sleep(0.4)
        st.switch_page("pages/login_home_page.py") # use forward slash
    else:
        st.error("Invalid username or password")
