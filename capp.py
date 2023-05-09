import os
import base64
import aiohttp
import asyncio
import traceback
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components
from app.conversations.document_based import DocumentBasedConversation
from app.settings import load_config, logger
from datetime import datetime

# Set global variables
ROOT_DIR = './'
DEBUG = False
INITIAL_PROMPT = "Hello"

errors = []
config = load_config()

@st.cache_resource(show_spinner=False)
def conversation():
    # Load the document-based conversation by default.
    return DocumentBasedConversation()


@st.cache_data(show_spinner=False)
def get_local_img(file_path: str) -> str:
    # Load a byte image and return its base64 encoded string
    return base64.b64encode(open(file_path, "rb").read()).decode("utf-8")


@st.cache_data(show_spinner=False)
def get_favicon(file_path: str):
    # Load a byte image and return its favicon
    return Image.open(file_path)

@st.cache_data(show_spinner=False)
def get_css() -> str:
    # Read CSS code from style.css file
    with open(os.path.join(ROOT_DIR, "app", "assets", "style.css"), "r") as f:
        return f"<style>{f.read()}</style>"

@st.cache_data(show_spinner=False)
def get_js() -> str:
    with open(os.path.join(ROOT_DIR, "app", "assets", "app.js"), "r") as f:
        return f"<script>{f.read()}</script>"

def get_chat_message(
    contents: str = "",
    align: str = "left"
) -> str:
    # Formats the message in an chat fashion (user right, reply left)
    div_class = "AI-line"
    file_path = os.path.join(ROOT_DIR, "app", "assets", "AI_icon.png")
    src = f"data:image/gif;base64,{get_local_img(file_path)}"
    if align == "right":
        div_class = "human-line"
        if "USER" in st.session_state:
            src = st.session_state.USER.avatar_url
        else:
            file_path = os.path.join(ROOT_DIR, "app", "assets", "user_icon.png")
            src = f"data:image/gif;base64,{get_local_img(file_path)}"
    icon_code = f"<img class='chat-icon' src='{src}' width=32 height=32 alt='avatar'>"
    formatted_contents = f"""
    <div class="{div_class}">
        {icon_code}
        <div class="chat-bubble">
        &#8203;{contents}
        </div>
    </div>
    """
    return formatted_contents


async def main(human_prompt: str) -> dict:
    res = {'status': 0, 'message': "Success"}
    try:

        # Strip the prompt of any potentially harmful html/js injections
        human_prompt = human_prompt.replace("<", "&lt;").replace(">", "&gt;")

        # Update both chat log and the model memory
        st.session_state.LOG.append(f"Human: {human_prompt}")
        st.session_state.MEMORY.append({'role': "user", 'content': human_prompt})

        # Clear the input box after human_prompt is used
        # prompt_box.empty()

        with chat_box:
            # Write the latest human message first
            line = st.session_state.LOG[-1]
            contents = line.split("Human: ")[1]
            st.markdown(get_chat_message(contents, align="right"), unsafe_allow_html=True)

            reply_box = st.empty()
            reply_box.markdown(get_chat_message(), unsafe_allow_html=True)

            # This is one of those small three-dot animations to indicate the bot is "writing"
            writing_animation = st.empty()
            file_path = os.path.join(ROOT_DIR, "app", "assets", "loading.gif")
            writing_animation.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;<img src='data:image/gif;base64,{get_local_img(file_path)}' width=30 height=10>", unsafe_allow_html=True)

            reply_text = conversation().predict(human_prompt)
            
            reply_box.markdown(get_chat_message(reply_text), unsafe_allow_html=True)

            # Clear the writing animation
            writing_animation.empty()

            # Update the chat log and the model memory
            st.session_state.LOG.append(f"AI: {reply_text}")
            st.session_state.MEMORY.append({'role': "assistant", 'content': reply_text})

    except:
        res['status'] = 2
        res['message'] = traceback.format_exc()

    return res

### INITIALIZE AND LOAD ###

# Initialize page config
favicon = get_favicon(os.path.join(ROOT_DIR, "app", "assets", "AI_icon.png"))
st.set_page_config(
    page_title="BrainChulo - Smart Camelid Chatbox.",
    page_icon=favicon,
)

# Get query parameters
query_params = st.experimental_get_query_params()
if "debug" in query_params and query_params["debug"][0].lower() == "true":
    st.session_state.DEBUG = True

if "DEBUG" in st.session_state and st.session_state.DEBUG:
    DEBUG = True


# Initialize some useful class instances
st.spinner("Initializing App...")

### MAIN STREAMLIT UI STARTS HERE ###

# Define main layout
st.header("BrainChulo")
st.subheader("Smart Camelid Chatbox")

chat_box = st.container()
prompt_box = st.empty()
footer = st.container()

with footer:
    st.markdown("""
    <div id="footer"><small>
    GitHub <a href="https://github.com/CryptoRUSHGav/BrainChulo"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/CryptoRUSHGav/BrainChulo?style=social"></a>
    </small></div>
    """, unsafe_allow_html=True)

if DEBUG:
    with st.sidebar:
        st.subheader("Debug Area")


# Load CSS code
st.markdown(get_css(), unsafe_allow_html=True)
components.html(get_js(), height=0)

# Initialize/maintain a chat log and chat memory in Streamlit's session state
# Log is the actual line by line chat, while memory is limited by model's maximum token context length
if "MEMORY" not in st.session_state:
    st.session_state.MEMORY = [{'role': "system", 'content': INITIAL_PROMPT}]
    st.session_state.LOG = [INITIAL_PROMPT]


# Render chat history so far
with chat_box:
    for line in st.session_state.LOG[1:]:
        # For AI response
        if line.startswith("AI: "):
            contents = line.split("AI: ")[1]
            st.markdown(get_chat_message(contents), unsafe_allow_html=True)

        # For human prompts
        if line.startswith("Human: "):
            contents = line.split("Human: ")[1]
            st.markdown(get_chat_message(contents, align="right"), unsafe_allow_html=True)


# Define an input box for human prompts
with prompt_box:
    human_prompt = st.text_input("Prompt", value="", key=f"text_input_{len(st.session_state.LOG)}", placeholder="Type your prompt here...", label_visibility="hidden")


# Gate the subsequent chatbot response to only when the user has entered a prompt
if len(human_prompt) > 0:
    run_res = asyncio.run(main(human_prompt))
    if run_res['status'] == 0 and not DEBUG:
        st.experimental_rerun()

    else:
        if run_res['status'] != 0:
            st.error(run_res['message'])
        with prompt_box:
            st.experimental_rerun()