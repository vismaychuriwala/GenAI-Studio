import streamlit as st
import os
import yaml
from dotenv import load_dotenv
from agents import BasicAgent

load_dotenv()

# Load configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Set page config
st.set_page_config(
    page_title=config["app"]["page_title"],
    page_icon=config["app"]["icon"]
)

st.title(f"{config['app']['icon']} {config['app']['title']}")

if "agent" not in st.session_state:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set OPENAI_API_KEY in your .env file")
        st.stop()

    # Build system prompt path
    system_prompt_path = os.path.join("prompts", config["agent"]["system_prompt_file"])

    st.session_state.agent = BasicAgent(
        api_key=api_key,
        model=config["agent"]["model"],
        temperature=config["agent"]["temperature"],
        system_prompt_path=system_prompt_path,
        reasoning_effort=config["agent"].get("reasoning_effort")
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.session_state.agent.clear_history()
    st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.chat(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
