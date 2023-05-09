import os
from tempfile import _TemporaryFileWrapper
import gradio as gr
from app.conversations.document_based import DocumentBasedConversation
from app.settings import load_config, logger

config = load_config()

# Load the document-based conversation by default.
# Eventually, we'll want to load the conversation from UI selection
convo = DocumentBasedConversation()


def add_text(history, text):
    """
    Adds text to a history list.

    Args:
        history (list): A list of tuples containing strings and None.
        text (str): A string to add to the history list.

    Returns:
        list: The updated history list with the new text appended.
        str: An empty string.

    Example:
        >>> add_text([], "hello")
        ([("hello", None)], "")
    """

    if text != "":
        history = history + [(text, None)]
    return history, ""


def add_file(history, new_file):
    """
    Adds a new file to the history and returns the updated history.

    :param history: list of tuples representing the conversation history
    :param new_file: the file to be added
    :return: updated history
    """
    if isinstance(new_file, _TemporaryFileWrapper):
        try:
            # Save the file to disk
            uploaded_file_name = os.path.basename(new_file.name)
            filepath = os.path.join(
                os.getcwd(),
                "data",
                config.upload_path,
                uploaded_file_name)

            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, "wb") as file:
                # Copy the contents of the file object to the new file
                with open(new_file.name, "rb") as new_file_contents:
                    for line in new_file_contents:
                        file.write(line)

            # Load the document into the conversation
            convo.load_document(filepath)

            uploaded_file_name = os.path.basename(new_file.name)
            # Do not update the history but return the event
            return history + \
                [(f"{uploaded_file_name} has been loaded into memory.", None)]
        except Exception as e:
            logger.error(f"Error adding file to history: {e}")
            updated_history = history
    else:
        updated_history = history

    return updated_history


def bot(history):
    """
    Given a history of conversations, predict the response for the latest input.

    :param history: A list of tuples containing the input and response of previous conversations.
    :type history: list

    :return: The updated history with the predicted response added.
    :rtype: list
    """
    if history and len(history) > 0:
        input = history[-1][0]
        response = convo.predict(input=input)
        history[-1][1] = response
    return history

def launch_app():
    with gr.Blocks() as app:
        chatbot = gr.Chatbot([], elem_id="chatbot").style(
            height="auto")

        with gr.Row():
            with gr.Column(scale=0.9):
                txt = gr.Textbox(
                    show_label=False,
                    placeholder="Enter text and press enter, or upload a text file",
                ).style(
                    container=False)
            with gr.Column(scale=0.05):
                btn_submit = gr.Button("✉️").style(container=False)
            with gr.Column(scale=0.05):
                btn = gr.UploadButton("📁", file_types=["text"]).style(
                    container=False)

        btn_submit.click(add_text, [chatbot, txt], [chatbot, txt]).then(
            bot, chatbot, chatbot
        )
        txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
            bot, chatbot, chatbot
        )
        btn.upload(add_file, [chatbot, btn], [chatbot])

    app.launch(server_port=7865, server_name="0.0.0.0", debug=True)

if __name__ == "__main__":
    launch_app()