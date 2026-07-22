import streamlit as st

st.set_page_config(page_title="Financial Roadmap", layout="wide")
st.title("🗺️ Your Personalized Financial Roadmap")
st.markdown("## 📈 Structured Path from Beginner to Financial Expert")

# --- Check if roadmap exists ---
if "roadmap_data" not in st.session_state:
    st.warning("🚧 Please complete the quiz to generate your roadmap.")
    st.stop()

roadmap = st.session_state.roadmap_data

# --- Track completion ---
if "completed_steps" not in st.session_state:
    st.session_state.completed_steps = {}

# --- Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    for section, section_data in roadmap.items():
        st.markdown(f"### {section}")
        if "subtitle" in section_data and section_data["subtitle"]:
            st.caption(section_data["subtitle"])

        for idx, step in enumerate(section_data.get("topics", [])):
            step_key = f"{section}_{idx}"
            if step_key not in st.session_state.completed_steps:
                st.session_state.completed_steps[step_key] = False

            is_checked = st.checkbox(step["label"], key=step_key)
            st.session_state.completed_steps[step_key] = is_checked

            with st.expander(f"ℹ️ {step['label']}"):
                st.write(step["summary"])
                if step["resources"]:
                    st.markdown("**Resources:**")
                    for title, url in step["resources"]:
                        st.markdown(f"- [{title}]({url})")

with col2:
    st.markdown("### ✅ Completed")
    completed = [k for k, v in st.session_state.completed_steps.items() if v]
    if completed:
        for key in completed:
            section, idx = key.rsplit("_", 1)
            label = roadmap[section]["topics"][int(idx)]["label"]
            st.write(f"✔️ {label}")
    else:
        st.info("No steps completed yet.")

