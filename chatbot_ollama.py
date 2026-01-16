import streamlit as st
import ollama

st.set_page_config(page_title="SKAI Technologies Chatbot", layout="centered")
st.title("SKAI Technologies Chatbot")

# required to maintain the chat history
if "messages" not in st.session_state:
    st.session_state.messages =[]
    
#Show the Chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
#Default prompt or message

prompt = st.chat_input("I am your AI Assistant. You can as me queries you like!!")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
        
st.session_state.messages.append({"role":"user","content":prompt})

#Fetch the response from ollama model
with st.chat_message("assistant"):
    response_placeholder =st.empty()
    full_response =""
    
    try:
        stream = ollama.chat(
            model='gemma:2b',
            messages= st.session_state.messages,
            stream=True
        )
        
        for chunk in stream:
            content = chunk['message']['content']
            full_response +=content
            response_placeholder.markdown(full_response+ " ")
            
        response_placeholder.markdown(full_response)    
        st.session_state.messages.append({"role":"assistant","content" :full_response})
    except Exception as e:
        st.error(f'Error connecting ollama model : gemma:2b {e}')