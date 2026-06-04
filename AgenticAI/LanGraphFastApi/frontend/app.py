import streamlit as st
import requests

st.set_page_config(
    layout="wide"
)

st.title(
    "LangGraph Database Agent"
)

left, right = st.columns([1,3])

with left:

    st.subheader("Tables")

    st.write("customers")
    st.write("orders")
    st.write("products")

with right:

    prompt = st.text_area(
        "Ask anything"
    )

    if st.button("Submit"):

        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "query": prompt
            }
        )

        st.write(
            response.json()["response"]
        )
        
       

