import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Stop if API key is missing
if not api_key:
    st.error("API key not found. Please add OPENAI_API_KEY to your .env or Streamlit Secrets.")
    st.stop()

# Initialize OpenAI client
openai.api_key = api_key

# Streamlit UI
st.set_page_config(page_title="Travel Risk & Safety Chatbot", layout="centered")
st.title("🧳 Travel Risk & Safety Chatbot")
st.write("Ask me about travel safety, health risks, political stability, or natural hazards anywhere in the world.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Where are you traveling to or what safety info do you need?")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a travel safety expert. Provide accurate, up-to-date information about travel risks, health advisories, political stability, and natural hazards."},
            *st.session_state.messages
        ],
        temperature=0.7
    )

    reply = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)