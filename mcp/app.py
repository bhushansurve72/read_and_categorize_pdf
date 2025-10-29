import streamlit as st
from mcp_agent import run_agent

st.set_page_config(page_title="MCP Agent Demo", layout="centered")

st.title("💳 Mock MCP Operations Agent")
st.markdown("""
Type a command like:
- "Activate card 9876-4321-5555-1111"
- "Update address for account 12345 to 42 Elm Street, NY"
- "Close account 54321"
""")

# --- Maintain logs in session state ---
if "logs" not in st.session_state:
    st.session_state.logs = []

# --- Input box ---
user_input = st.text_area("Your request:", height=100, placeholder="Enter a command for the agent...")

# --- Run agent ---
if st.button("Run Agent"):
    if user_input.strip():
        with st.spinner("🤖 Processing your request..."):
            try:
                result = run_agent(user_input)
                st.success(result)
                st.session_state.logs.append(f"🟢 {result}")
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.logs.append(f"🔴 Error: {e}")
    else:
        st.warning("Please enter a valid instruction.")

# --- Display log history ---
st.divider()
st.subheader("📜 API Logs")

if st.session_state.logs:
    for entry in reversed(st.session_state.logs):
        st.write(entry)
else:
    st.info("No logs yet. Submit a command to see activity.")
