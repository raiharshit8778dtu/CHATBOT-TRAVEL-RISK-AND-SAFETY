import streamlit as st
from openai import OpenAI
import base64
import os
# Load API key safely
api_key = st.secrets.get("OPENAI_API_KEY", None)
if not api_key:
    st.error("API key not found. Please add OPENAI_API_KEY to Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", "content": "You are a helpful travel safety chatbot."}]

# Display uploaded image preview
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Chat input
user_input = st.chat_input("Ask me about this image:")

if uploaded_file and user_input:
    # Convert image to base64
    image_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{image_base64}"

    # Add user message to history
    st.session_state["messages"].append({
        "role": "user",
        "content": [
            {"type": "text", "text": user_input},
            {"type": "image_url", "image_url": image_url}
        ]
    })

    # Send full conversation to GPT-4 Vision
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=st.session_state["messages"]
    )

    bot_reply = response.choices[0].message.content

    # Add assistant reply to history
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Display assistant reply
    st.chat_message("assistant").write(bot_reply)