import os
import streamlit as st
from app.conversations.document_based import DocumentBasedConversation
from app.settings import load_config, logger
from datetime import datetime

config = load_config()

# Load the document-based conversation by default.
# Eventually, we'll want to load the conversation from UI selection
convo = DocumentBasedConversation()

if "history" not in st.session_state:
    st.session_state["history"] = []

# Function to upload a file
def upload_file():
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        file_name = uploaded_file.name
        with open(f"data/{file_name}", "wb") as f:
            f.write(file_contents)
        st.write(f"{file_name} has been uploaded")
        return file_name

# Function to update the votes for a response
def update_votes(key, rating):
    # history = st.session_state['history', []]

    # print(history[response], response, rating)
    # if history[response] and history[response]["rating"] is not None:
    #     history[response]["rating"] = rating
    # elif history[response]:
    #     history[response] = {"rating": [rating]}
    
    st.session_state["history"][key]['rating'] = rating

# Function to render the chat history in a chat window
def render_history(history):
    for key, interaction in enumerate(history):
        st.write(f"User: {interaction['user_input']}")
        st.write(f"Bot: {interaction['response']}")
        st.write(f"Rating: {interaction['rating']}")

        # Update the votes for the AI response
        col1, col2 = st.columns(2)
        with col1:
            upvote_button = st.button("Upvote", key=f"upvote_{key}", on_click=update_votes, args=(key, 1))
        with col2:
            downvote_button = st.button("Downvote", key=f"downvote_{key}", on_click=update_votes, args=(key, 0))        
        st.write("-" * 30)


def add_message(user_input):
    history = st.session_state.get("history", [])

    # Call the predict function with the user input
    response = convo.predict(user_input)
    rating = 0.5

    history.append({
        "user_input": user_input,
        "response": response,
        "rating": rating
    })
    st.session_state["history"] = history

# Set the app title
st.title("Chatbot")

with st.container():
    render_history(st.session_state["history"])

# Add a textbox for user input
user_input = st.text_input("Enter your message here:", key="input_message")

# Add a button to submit the user input
if st.button("Submit"):
    add_message(user_input)

# Add a file upload option
file_name = upload_file()

# Add a file upload option
if file_name is not None:
    st.write(f"You uploaded {file_name}")

# Add a button to clear the chat history
if st.button("Clear History"):
    history.clear()


