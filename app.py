from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr

# Load environment variables
load_dotenv()

# Configure Google API key
genai.configure(api_key=os.getenv("AIzaSyAtTh00lG2oAzJnisLwijs81_OHOPeKhLE"))

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Function to load Gemini Pro-Model and get responses
model = genai.GenerativeModel("gemini-pro")

def get_gemini_response(question: str) -> str:
    response = model.generate_content(question)
    return response.text

# Function to convert text to speech
def text_to_speech(text: str):
    engine.say(text)
    engine.runAndWait()

# Function to convert speech to text
def speech_to_text() -> str:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, there was an error with the request."

# Initialize Streamlit application
st.set_page_config(page_title="Summer Internship ")
st.header("Chatbot")

# Input field for text
user_input = st.text_input("Input:", key="input")

# Button to submit the question
submit = st.button("Ask the Question:")

if submit and user_input:
    response = get_gemini_response(user_input)
    st.subheader("The Response is ")
    st.write(response)
    text_to_speech(response)

# Button to record voice input
if st.button("Record Voice Input"):
    voice_input = speech_to_text()
    st.text("Voice Input: " + voice_input)
    response = get_gemini_response(voice_input)
    st.subheader("The Response is ")
    st.write(response)
    text_to_speech(response)
