# utils/card.py  – overwrite the previous version
import streamlit as st
from pathlib import Path
import textwrap

def draw_course_card(
    title: str,
    subtitle: str,
    chapters: int,
    items: int,
    progress: int,
    target_page: str,
):
    """
    Render a “LeetCode-style” course card and make its play button navigate
    to another Streamlit page.
    """

    _inject_css()

    html = f"""\
    <div class="course-card">
      <div class="card-top">
        <div class="card-text">
          <h4>{subtitle}</h4>
          <h2>{title}</h2>
        </div>
      </div>

      <div class="card-bottom">
        <div><span class="big">{chapters}</span><br><span class="label">Chapters</span></div>
        <div><span class="big">{items}</span><br><span class="label">Items</span></div>
        <div><span class="big">{progress}%</span><br><span class="label">Complete</span></div>
      </div>
    </div>"""

    st.markdown(html, unsafe_allow_html=True)

    with st.container():
        st.page_link(
            target_page,
            label="Resume the Course!",
        )

def _inject_css():
    css_path = Path("assets/styles/cards.css")
    css = css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
