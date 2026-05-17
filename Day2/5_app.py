import streamlit as st
import requests

st.title("FastAPI + Streamlit Integration")

# User input in Streamlit
user_input = st.text_input("Enter some text to process:")

if st.button("Send to API"):
    if user_input:
        # Prepare the payload and the URL
        payload = {"text": user_input}
        api_url = "http://127.0.0.1:8000/process"
        
        try:
            # Make the POST request to the FastAPI backend
            response = requests.post(api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json().get("message")
                st.success(f"Response from API: {result}")
            else:
                st.error("Failed to get a valid response from the API.")
        except requests.exceptions.ConnectionError:
            st.warning("Could not connect to the API. Is the backend running?")
    else:
        st.info("Please enter some text first.")