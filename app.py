import streamlit as st
import openai
import base64
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])
user_input = st.text_input("Ask me about this image:")

if uploaded_file and user_input:
    # Convert image to base64
    image_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{image_base64}"

    # Send text + image to GPT-4 with vision
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": user_input},
                {"type": "image_url", "image_url": image_url}
            ]
        }]
    )

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages
for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

    st.write(response.choices[0].message["content"])