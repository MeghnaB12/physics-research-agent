import streamlit as st
import sys
import os

# Add backend to path so we can import the agent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend/app")))

from agent.gemini_agent import PhysicsAgent

st.set_page_config(page_title="Physics Insight Agent", page_icon="⚛️")

# Initialize Agent (Cached so it doesn't reload on every click)
@st.cache_resource
def load_agent():
    return PhysicsAgent()

agent = load_agent()

# Header
st.title("⚛️ Physics-Informed Research Agent")
st.markdown("""
This agent can **read** research papers and **solve** the math inside them.
* **Search:** Ask about "limiting absorption principle" or "wave operators".
* **Solve:** Ask it to solve equations found in the text.
""")

# Chat History Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your research paper..."):
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get Agent Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking (Searching & Solving)..."):
            response_text = agent.ask(prompt)
            st.markdown(response_text)
    
    # 3. Save Assistant Message
    st.session_state.messages.append({"role": "assistant", "content": response_text})