"""Browser demo for Friday's conversational AI, separate from the desktop voice app."""

import os

import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


def setting(name, default=None):
    value = os.getenv(name)
    if value:
        return value
    try:
        return st.secrets.get(name, default)
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return default


st.set_page_config(page_title="Friday AI Assistant", page_icon="🤖")
st.markdown(
    """
    <style>
    html {
        font-size: 20px !important;
    }
    .main h1 {
        font-size: 3.4rem !important;
        line-height: 1.15;
    }
    .main p, section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h2 {
        font-size: 1.25rem !important;
        line-height: 1.65;
    }
    [data-testid="stChatInput"] textarea {
        font-size: 1.2rem !important;
    }
    [data-testid="stChatInput"] button,
    section[data-testid="stSidebar"] button {
        font-size: 1.05rem !important;
    }
    section[data-testid="stSidebar"] button {
        min-height: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("Friday")
st.caption("A browser demo of Friday's AI conversation. The voice assistant runs on your desktop.")

api_key = setting("GROQ_API_KEY")
if not api_key:
    st.info("The demo is not configured yet. The project owner needs to add GROQ_API_KEY to the app's server-side secrets.")
    st.stop()

model = setting("AI_MODEL", "openai/gpt-oss-20b")
client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
system_message = {
    "role": "system",
    "content": "You are Friday, a polite, witty British AI assistant. Address the user as 'sir' occasionally. Keep replies concise, usually one to three sentences.",
}

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("About this demo")
    st.write("Try a conversation with Friday. Voice commands, timers, and desktop controls are available in the locally installed app.")
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask Friday something…")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    context = st.session_state.messages[-10:]
    try:
        with st.chat_message("assistant"):
            with st.spinner("Friday is thinking…"):
                result = client.chat.completions.create(
                    model=model,
                    messages=[system_message, *context],
                    timeout=30,
                )
                reply = result.choices[0].message.content or "I don't have a response just now."
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception:
        st.session_state.messages.pop()
        st.error("Friday couldn't reach the AI service. Please try again in a moment.")
