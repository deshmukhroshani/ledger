import streamlit as st
import re
from backend.app import generate_roadmap

st.set_page_config(page_title="Financial Quiz", layout="centered")
st.title("🧠 Your Personalized Financial Quiz")

# --- Ensure Required Data ---
if "demographics" not in st.session_state or "quiz_output" not in st.session_state:
    st.warning("Please fill out your demographics first.")
    st.stop()

demographics = st.session_state.demographics
quiz_output = st.session_state.quiz_output

# --- Initialize Reset State ---
if "quiz_key_version" not in st.session_state:
    st.session_state.quiz_key_version = 0

# --- Quiz Rendering ---
pattern = r"## (.*?)\n(.*?)(?=\n## |\Z)"
matches = re.findall(pattern, quiz_output, re.DOTALL)
responses = {}

st.markdown("### 📝 Answer the Following Questions:")
for section, questions_block in matches:
    st.subheader(section.strip())
    questions = re.findall(r"\d+\.\s+(.*)", questions_block)
    for idx, q in enumerate(questions):
        key_base = f"{section.strip()}_{idx}"
        # Append version to key to clear selection on reset
        key = f"{key_base}_v{st.session_state.quiz_key_version}"
        responses[key_base] = st.radio(q.strip(), ["Yes", "No"], key=key, index=None)

# --- Submit Answers and Generate Roadmap ---
if st.button("📨 Submit Quiz Answers"):
    st.session_state.quiz_responses = responses
    st.success("✅ Responses submitted! Generating your personalized roadmap...")

    # Generate and store roadmap
    roadmap = generate_roadmap(demographics, responses)
    st.session_state.roadmap_data = roadmap

    st.switch_page("pages/roadmap.py")

# --- Reset Quiz Selections ---
if st.button("🔄 Reset Quiz"):
    st.session_state.quiz_key_version += 1  # Forces radio button widget keys to update
    st.rerun()

# Optional: Back to Demographics
if st.button("🔙 Go Back"):
    st.switch_page("pages/demographics.py")
