import streamlit as st
import requests

st.set_page_config(
    page_title="RAG Document Finder",
    layout="wide"
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.title("Document Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


st.sidebar.title("Groq API Key")

groq_key = st.sidebar.text_input(
    "Enter Groq API Key",
    type="password"
)

# -------------------------------------------------
# Upload Button
# -------------------------------------------------

if uploaded_file is not None:

    if st.sidebar.button("Upload Document"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )

        if response.status_code == 200:
            st.sidebar.success("Document uploaded successfully")
        else:
            st.sidebar.error("Upload failed")

# -------------------------------------------------
# Main Chat UI
# -------------------------------------------------

st.title("RAG Document Finder / Chatbot")

question = st.text_input(
    "Ask question from uploaded document"
)

# -------------------------------------------------
# Ask Button
# -------------------------------------------------

if st.button("Ask"):

    if not groq_key:
        st.warning("Please enter Groq API Key")

    elif not question:
        st.warning("Please enter question")

    else:

        payload = {
            "question": question,
            "groq_key": groq_key
        }

        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json=payload
        )

        if response.status_code == 200:

            answer = response.json()["answer"]

            st.subheader("Answer")
            st.write(answer)

        else:
            st.error("API Error")