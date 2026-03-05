import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
import time

# Load environment variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

def get_gemini_response(question):
    start_time = time.time()  # Start timing
    response = chat.send_message(question, stream=True)
    end_time = time.time()  # End timing
    execution_time = end_time - start_time  # Calculate execution time
    return response, execution_time

st.set_page_config("QnA_Application")
st.header("Gemini LLM Application")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("INPUT", key="input")
submit = st.button("Ask the Question")

if submit:
    response, execution_time = get_gemini_response(user_input)
    st.session_state["history"].append(("YOU", user_input))
    
    st.subheader("The response is ...")
    response_text = ""
    for chunk in response:
        response_text += chunk.text + " "
        st.write(chunk.text)
    
    st.session_state["history"].append(("BOT", response_text.strip()))
    
    st.subheader("Execution Time")
    st.write(f"⏱️ {execution_time:.2f} seconds")

st.subheader("The chat history is ...")
for role, text in st.session_state["history"]:
    st.write(f"{role}: {text}")
