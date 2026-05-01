import streamlit as st
import requests

st.set_page_config(page_title="ASX AI Broker", page_icon="📈")

st.title("🇦🇺 ASX Stock Analysis Agent")
st.markdown("Automated Broker Research powered by Oracle Cloud")

# THE BRAIN: Your Oracle Server IP
ORACLE_URL = "http://159.13.58.92:8000/agno/agent"

# Sidebar for simple security
with st.sidebar:
    st.header("Access Control")
    password = st.text_input("Enter Access Code", type="password")

if password == "ASX2026": # Change this to whatever you want
    query = st.text_area("What would you like to research?", 
                         placeholder="e.g., Analyze BHP and CBA. Give me a buy/sell recommendation.")

    if st.button("Run Broker Research"):
        if query:
            with st.spinner("Agent is searching ASX data and news..."):
                try:
                    response = requests.post(ORACLE_URL, json={"message": query})
                    if response.status_code == 200:
                        # Extract the message from Agno's response format
                        result = response.json().get("message", "No data returned")
                        st.markdown("### 🤖 Broker Recommendation")
                        st.write(result)
                    else:
                        st.error(f"Server Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")
        else:
            st.warning("Please enter a query.")
else:
    st.info("Please enter the correct access code in the sidebar to use the agent.")
