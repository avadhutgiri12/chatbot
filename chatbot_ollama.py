import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Flux Chatbot", layout="centered")
st.title("Flux Chatbot")

GROQ_API_KEY = os.getenv("API_KEY") # Replace with your actual key
client = Groq(api_key=GROQ_API_KEY)

# required to maintain the chat history
if "messages" not in st.session_state:
    st.session_state.messages =[]
    
#Show the Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
#Default prompt or message
def userInput():
    prompt = st.chat_input("I am your AI Assistant. You can as me queries you like!!")
    if prompt:
        return prompt
    else:
        return "Hello!"
    

prompt = userInput()
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        
st.session_state.messages.append({"role":"user","content":prompt})

with st.chat_message("assistant"):
    response_placeholder =st.empty()
    full_response =""
    
    try:
        chat_complition = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        full_response = chat_complition.choices[0].message.content
        response_placeholder.markdown(full_response+ " ")
            
        response_placeholder.markdown(full_response)    
        st.session_state.messages.append({"role":"assistant","content" :full_response})
    except Exception as e:
        st.error(f'Error connecting ollama model : gemma:2b {e}')