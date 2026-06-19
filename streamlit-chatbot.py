import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# .env file se variables ko system environment mein load karein
load_dotenv()

# System environment se GOOGLE_API_KEY nikalein
api_key = os.getenv("GOOGLE_API_KEY")

# Agar .env se na mile toh check karein kya kisi aur naam se hai
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

# Agar phir bhi na mile toh safe check ke liye Streamlit secrets dekhein bina crash kiye
if not api_key and hasattr(st, "secrets"):
    api_key = st.secrets.get("GOOGLE_API_KEY")

# Check karein ke API Key mili ya nahi
if not api_key:
    st.error("Error: Boss, aapki .env file mein 'GOOGLE_API_KEY' nahi mili. Please file check karein!")
    st.stop()

# Gemini ko configure karein (Fast model: gemini-1.5-flash)
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

st.title("My Gemini AI Chatbot 🤖")

# Chat history initialize karein
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani chat screen par dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User se input lene ke liye box
user_query = st.chat_input("Boss, Gemini AI se kuch bhi poocho...")

if user_query:
    # 1. User ka message screen par dikhao
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. Gemini AI se jawab lena
    with st.chat_message("assistant"):
        try:
            response = model.generate_content(user_query)
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Gemini API Error: {e}")