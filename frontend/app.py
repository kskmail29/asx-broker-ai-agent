import streamlit as st
import requests

# --- CONFIGURATION ---
ORACLE_IP = st.secrets["ORACLE_IP"]
ACCESS_CODE = st.secrets["ACCESS_CODE"]
AGENT_ID = "global-alpha-broker"
ORACLE_URL = f"http://{ORACLE_IP}/api/agents/{AGENT_ID}/runs"

st.set_page_config(page_title="Global Alpha Broker", page_icon="📈", layout="wide")

# --- UI HEADER ---
st.title("🌏 Global Alpha Stock Broker")
st.markdown("**Markets covered:** 🇦🇺 ASX &nbsp;|&nbsp; 🇮🇳 NSE India &nbsp;|&nbsp; 🇺🇸 US (NYSE / NASDAQ)")

# --- SIDEBAR SECURITY & SETTINGS ---
with st.sidebar:
    st.header("🔐 Access Control")
    access_code = st.text_input("Enter Access Code", type="password")
    
    st.divider()
    st.info("""
    **Instructions:**
    1. Enter the access code.
    2. Ask about ASX, Indian NSE, or US stocks.
    3. If connection fails, allow 'Insecure Content' in your browser settings.
    """)

# --- MAIN INTERFACE ---
if access_code == ACCESS_CODE:
    user_query = st.text_area(
        "What is your investment research request?",
        placeholder="e.g. Analyse BHP on ASX, Reliance on NSE India, and Apple on NASDAQ — give me a buy/sell rating.",
        height=150
    )

    if st.button("🚀 Run Professional Research"):
        if user_query:
            with st.spinner("Broker is researching market data and news across agents..."):
                # Agno AgentOS expects data as Form-Data (application/x-www-form-urlencoded)
                payload = {
                    "message": user_query,
                    "stream": "false",
                    "monitor": "true"
                }
                
                try:
                    # We use 'data=' for form-encoding instead of 'json='
                    response = requests.post(ORACLE_URL, data=payload, timeout=60)
                    
                    if response.status_code == 200:
                        # Agno returns a JSON object; 'content' contains the markdown answer
                        raw_data = response.json()
                        answer = raw_data.get("content", "No content returned from agent.")
                        
                        st.divider()
                        st.markdown("### 🤖 Broker Analysis Report")
                        st.markdown(answer)
                    
                    elif response.status_code == 404:
                        st.error("Error 404: Agent ID not found. Check if the Agent Name in broker.py matches.")
                    else:
                        st.error(f"Server returned {response.status_code}: {response.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("🚨 **Connection Failed.** This is usually the 'Mixed Content' block. Please click the lock/settings icon in your browser URL bar and 'Allow Insecure Content' for this site.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter a research query first.")
else:
    st.warning("Please enter the correct access code in the sidebar to unlock the Broker.")

# --- FOOTER ---
st.divider()
st.caption("Powered by Agno multi-agent framework, Claude Sonnet, and Oracle Cloud Infrastructure.")
