import streamlit as st
import requests
import pandas as pd

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="SQL Text RAG",
    page_icon="🧠",
    layout="wide"
)

# =========================
# Custom CSS
# =========================
st.markdown(
    """
    <style>
    .main {
        background-color: #f5f7fa;
    }
     .stTextInput > div > div > input {
        border-radius: 10px;
    }

    .title {
        font-size: 40px;
        font-weight: bold;
        color: #1f4e79;
    }

    .subtitle {
        font-size: 18px;
        color: #555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    
# =========================
# Sidebar
# =========================
with st.sidebar:
    st.title("⚙️ Settings")

    groq_key = st.text_input(
        "Enter Groq API Key",
        type="password"
    )

    st.markdown("---")

    st.info(
        "Example Questions:\n\n"
        "- Show all customers\n"
        "- Which customer ordered Laptop?\n"
        "- Total sales amount\n"
        "- Show orders with customer names"
    )
    # =========================
# Main Page
# =========================
st.markdown('<p class="title">🧠 SQL Text RAG Application</p>', unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">Ask questions in plain English and get SQL-powered answers.</p>',
    unsafe_allow_html=True
)

st.markdown("---")

question = st.text_area(
    "Enter your question:",
    height=120,
    placeholder="Example: Which customer purchased Laptop?"
)

if st.button("Generate Answer"):

    if not groq_key:
        st.warning("Please enter Groq API key")

    elif not question:
        st.warning("Please enter a question")

    else:
     with st.spinner("Generating SQL and fetching result..."):

            payload = {
                "question": question,
                "groq_key": groq_key
            }

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/ask",
                    json=payload
                )

                data = response.json()

                if "error" in data:
                    st.error(data["error"])

                else:
                    st.success("Answer Generated Successfully")

                    st.subheader("Generated SQL Query")
                    st.code(data["generated_sql"], language="sql")

                    st.subheader("Result")

                    result = data["result"]

                    if result:
                        df = pd.DataFrame(result)
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No data found")

            except Exception as e:
                st.error(str(e))
