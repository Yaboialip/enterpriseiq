import streamlit as st
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from agent.gemini_agent import chat

st.set_page_config(
    page_title="EnterpriseIQ",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 EnterpriseIQ — Smart Manufacturing Assistant")
st.caption("Powered by Gemini + MCP | SQL Database · ERP System · Documents")

# Sidebar
with st.sidebar:
    st.header("📊 Data Sources")
    st.success("✅ SQL Database")
    st.success("✅ ERP System")
    st.success("✅ Document Parser")
    st.divider()
    st.header("💡 Try asking:")
    examples = [
        "What is the current inventory?",
        "Show pending supplier orders",
        "What is production output today?",
        "Tampilkan status semua order",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state.pending_prompt = ex

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle sidebar button clicks
prompt = st.chat_input("Ask about your manufacturing data...")
if st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            response = chat(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()