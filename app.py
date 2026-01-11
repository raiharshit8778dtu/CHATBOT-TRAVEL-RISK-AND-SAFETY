import streamlit as st
import openai
import os
import base64
from PIL import Image

# Load API key from Streamlit Secrets (recommended for Streamlit Cloud)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI setup
st.set_page_config(page_title="Image-Based Chatbot", layout="centered")
st.title("🖼️ Image-Based Chatbot")
st.write("Upload an image and ask a question about it. The chatbot will analyze the image and respond.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Image input
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
image_data = None
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    image_bytes = uploaded_image.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")
    image_data = f"data:image/png;base64,{base64_image}"

# Text input
user_input = st.chat_input("Ask a question about the image")
if user_input and image_data:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # GPT-4 Vision API call
    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions about uploaded images."
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_input},
                    {"type": "image_url", "image_url": {"url": image_data}}
                ]
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )

    reply = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

elif user_input and not image_data:
    st.warning("Please upload an image before asking a question.")