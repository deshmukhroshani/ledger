# utils/chatbot.py
import streamlit as st
from backend.app import generate_chat_response

def render_chatbot():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("## 💬 Ask WealthWise AI", unsafe_allow_html=True)

    # Display previous Q&A
    for i, (q, a) in enumerate(st.session_state.chat_history):
        with st.expander(f"Q{i+1}: {q}", expanded=False):
            st.markdown(a, unsafe_allow_html=True)

    # Chat input
    user_query = st.text_input("Type your question:", key="chat_input")
    if st.button("Ask", key="chat_ask_button") and user_query.strip():
        with st.spinner("Thinking..."):
            response = generate_chat_response(user_query)
            st.session_state.chat_history.append((user_query, response))

