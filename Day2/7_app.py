import streamlit as st
import requests

st.set_page_config(page_title="AI Research Lab", layout="wide")

st.title("🧪 AI Document Intelligence Lab")
st.markdown("---")

# Sidebar for configuration
st.sidebar.header("Settings")
analysis_mode = st.sidebar.selectbox("Analysis Mode", ["Summary", "Entities", "Sentiment"])
api_base_url = "http://127.0.0.1:8000"

# Main UI layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Input Data")
    text_input = st.text_area("Paste your document content here:", height=300)
    run_button = st.button("Run Intelligence Analysis", type="primary")

with col2:
    st.subheader("Results")
    if run_button:
        if text_input:
            with st.spinner("Communicating with FastAPI Backend..."):
                try:
                    # Constructing the payload
                    payload = {
                        "content": text_input,
                        "analysis_type": analysis_mode
                    }
                    
                    response = requests.post(f"{api_base_url}/analyze", json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Displaying Metrics
                        m1, m2 = st.columns(2)
                        metrics = data["metrics"]
                        m1.metric("Sentiment", metrics["sentiment"])
                        m2.metric("Complexity Score", metrics["complexity_score"])
                        
                        st.info(data["analysis"])
                        st.write("**System Tags:**", data["tags"])
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")
        else:
            st.warning("Please enter text to analyze.")