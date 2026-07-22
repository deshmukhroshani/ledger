import streamlit as st
import pycountry
import re
from backend.persist_to_db import persist_to_cloud_sql
from backend.fetch_from_db import fetch_from_cloud_sql
from backend.app import generate_quiz

st.set_page_config(page_title="Demographic Form", layout="centered")
st.title("👤 Tell Us About You")

# --- Session State Initialization ---
if "quiz_output" not in st.session_state:
    st.session_state.quiz_output = None
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "last_submitted_data" not in st.session_state:
    st.session_state.last_submitted_data = {}
if "submit_error" not in st.session_state:
    st.session_state.submit_error = None
if "quiz_key_version" not in st.session_state:
    st.session_state.quiz_key_version = 0

# --- Country Selection ---
countries = [""] + sorted([country.name for country in pycountry.countries])
selected_country = st.selectbox("🌍 Where are you located?", countries, index=0)

# --- Age Range ---
age_ranges_dict = {age_label: age_id for age_id, age_label in fetch_from_cloud_sql('age_range')}
selected_age_label = st.selectbox("🎂 Age Range", [""] + list(age_ranges_dict.keys()), index=0)
selected_age_id = age_ranges_dict.get(selected_age_label) if selected_age_label else None

# --- Sex ---
sex_options = ["", "Male", "Female", "Other"]
selected_sex = st.selectbox("🧑 Sex", sex_options, index=0)
selected_sex_id = selected_sex[0].upper() if selected_sex else None

# --- Education Level ---
education_levels_dict = {label: id for id, label in fetch_from_cloud_sql('education_level')}
selected_education_label = st.selectbox("🎓 Education Level", [""] + list(education_levels_dict.keys()), index=0)
selected_education_id = education_levels_dict.get(selected_education_label) if selected_education_label else None

# --- Employment Status ---
employment_statuses_dict = {label: id for id, label in fetch_from_cloud_sql('employment_status')}
selected_employment_label = st.selectbox("💼 Employment Status", [""] + list(employment_statuses_dict.keys()), index=0)
selected_employment_id = employment_statuses_dict.get(selected_employment_label) if selected_employment_label else None

# --- Estimated Annual Income ---
estimated_annual_income_dict = {label: id for id, label in fetch_from_cloud_sql('estimated_annual_income')}
selected_income_label = st.selectbox("💰 Estimated Annual Income", [""] + list(estimated_annual_income_dict.keys()), index=0)
selected_income_id = estimated_annual_income_dict.get(selected_income_label) if selected_income_label else None

# --- Form Validation ---
all_filled = all([
    selected_country.strip(),
    selected_age_id is not None,
    selected_education_id is not None,
    selected_employment_id is not None,
    selected_income_id is not None,
    selected_sex_id is not None,
])

# --- Current form data for comparison ---
current_form_data = {
    'country': selected_country.strip(),
    'age_range_id': selected_age_id,
    'education_level_id': selected_education_id,
    'employment_status_id': selected_employment_id,
    'estimated_annual_income_id': selected_income_id,
    'gender': selected_sex_id
}

# --- Show Submit Button ---
if all_filled:
    if st.button("✅ Submit"):
        try:
            persist_to_cloud_sql(current_form_data, 'user_demographics')
        except Exception as e:
            st.session_state.submit_error = str(e)

        demographics = {
            "Country": selected_country,
            "Age Range": selected_age_label,
            "Gender": selected_sex,
            "Education": selected_education_label,
            "Employment Status": selected_employment_label,
            "Estimated Income": selected_income_label,
        }
        st.session_state.demographics = demographics
        st.session_state.quiz_output = generate_quiz(demographics)
        st.session_state.quiz_responses = {}
        st.switch_page("pages/fin_quiz.py")  # Requires Streamlit >= 1.31
else:
    st.button("✅ Submit", disabled=True)