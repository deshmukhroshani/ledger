import streamlit as st
from PIL import Image

def setup_page_config():
    st.set_page_config(
        page_title="WealthWise AI",
        page_icon = Image.open("assets/wealthwiselogo.png"),
        layout = "wide",
        initial_sidebar_state = "collapsed",
        menu_items = {'Get Help': None, 'Report a bug': None, 'About': None}
    )