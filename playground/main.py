import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("SmartCookie AI Wellness Buddy")
st.subheader("Enter a health question and get a response from your AI Wellness Buddy")
cache = "The following question is from an elderly patient with a history of hypertension and diabetes question:"
question = st.text_input("Enter your question here")

if question:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=cache+question,
        temperature=0.3,
        max_tokens=256,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=0,
    )

    st.write(response.choices[0].text)  # Print the response from GPT-3


