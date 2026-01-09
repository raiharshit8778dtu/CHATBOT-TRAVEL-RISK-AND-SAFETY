import streamlit as st
import openai
import base64
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# 👉 STEP 1: Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages in chat format
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

uploaded_file = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])
user_input = st.chat_input("Ask me about this image:")   # 👈 replaced text_input with chat_input

if uploaded_file and user_input:
    # Convert image to base64
    image_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{image_base64}"

    # Add user message to history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Send text + image to GPT-4 Vision
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a helpful travel safety chatbot."},
            {"role": "user", "content": [
                {"type": "text", "text": user_input},
                {"type": "image_url", "image_url": image_url}
            ]}
        ]
    )

    bot_reply = response.choices[0].message["content"]

    # Add assistant reply to history
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Show assistant reply in chat UI
    st.chat_message("assistant").write(bot_reply)