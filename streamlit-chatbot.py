import os
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv() 

client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

st.title("Hello Streamlit!")

st.write("This is a simple Streamlit app.")

# Sliders, Buttons , CChatbot form

st.slider("Select Pay Range", 0, 100, 50)

st.button("Click Me!")

# Chatbot form - Query Input, Submit Button, Response Display

st.subheader("Chatbot Form")
user_input = st.text_input("Enter your query:")
user_age = st.number_input(
    "Enter your age", 
    min_value=0, 
    max_value=120, 
    value=25
)

user_resume = st.file_uploader(
    "Upload Resume", 
    type=["pdf", "docx"]
)

if st.checkbox("I agree to the terms and conditions"):
    st.write("Thank you for agreeing to the terms and conditions")
if st.button("Submit"):
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents=user_input
    )
    st.write(response.text) 