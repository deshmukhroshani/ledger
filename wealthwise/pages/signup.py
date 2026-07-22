import streamlit as st
from time import sleep
from pathlib import Path
import datetime as dt
import re
import pycountry

from backend.db_utils import insert_user

# -------- PAGE CONFIG --------
st.set_page_config(page_title="WealthWise | Sign-up", layout="centered")

gender_options = ["", "Male", "Female", "Other", "Prefer not to say"]
countries = sorted([country.name for country in pycountry.countries])

# -------- NAV REDIRECT --------
if st.session_state.get("authenticated"):
    st.switch_page("../landing_page.py")   # already signed-in

# TODO Later replace with a real DB / Auth service
USERS = st.session_state.setdefault("user_store", {})

# -------- SIGN-UP FORM --------
st.title("Create your WealthWise account")

# Create the form
with st.form("signup", clear_on_submit=False):

    # Put the first/last name columns side by side
    col1, col2 = st.columns(2)
    first = col1.text_input("First name", max_chars = 40, placeholder = "John")
    last = col2.text_input("Last name",  max_chars = 40, placeholder = "Doe")

    sex = st.selectbox(
        "Sex / Gender identity",
        options = gender_options,
        index = 0  # prepopulate
    )

    # Get where the user is from
    country = st.selectbox("Country", options=countries, index=countries.index("United States"))

    # Get the user's birthday
    dob = st.date_input(
        "Date of birth",
        value = dt.date.today(),
        min_value = dt.date(1900, 1, 1),
        max_value = dt.date.today(),
    )

    email = st.text_input("Email", max_chars=120, placeholder="you@example.com")

    pwd  = st.text_input("Password", type="password", max_chars=100,
                         help="≥ 8 characters, one number & letter")
    pwd2 = st.text_input("Confirm password", type="password", max_chars=100)

    accept = st.checkbox("I accept the Terms & Privacy Policy")
    submit = st.form_submit_button("Create account")

# Validate the email through regex
def valid_email(x:str) -> bool:
    return re.fullmatch(r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+", x) is not None

# This is what happens when the user presses create account
if submit:
    # Store the potential errors
    errors = []

    # Check for all errors
    if email in USERS:
        errors.append("email already exists.")
    if not valid_email(email):
        errors.append("Email address is not valid.")
    if len(pwd) < 8 or re.search(r"\d", pwd) is None or re.search(r"[A-Za-z]", pwd) is None:
        errors.append("Password must be ≥ 8 chars and contain letters & numbers.")
    if pwd != pwd2:
        errors.append("Passwords do not match.")
    if not accept:
        errors.append("You must accept the Terms.")

    # If errors are found, then print them to the user
    if errors:
        for e in errors:
            st.error(e)

    # Otherwise we will make a new user with their information
    # Here is where we will see what each user has. This will need
    # to match the JSON we define for an end user.
    else:
       # USERS[email] = {"password": pwd, "email": email, "first": first, "last": last}
        result = insert_user(first, last, email, pwd, sex[0], country, dob)
        if result["status"] == "success":
            st.success("Account created! Redirecting to login …")
            sleep(0.6)
            st.switch_page("pages/login.py")
        else:
            st.error(result["message"])