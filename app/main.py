from fastapi import FastAPI, UploadFile, File
from tempfile import _TemporaryFileWrapper
import shutil
from pydantic import BaseModel
from conversations.document_based import DocumentBasedConversation
from settings import load_config, logger

config = load_config()
convo = DocumentBasedConversation()

app = FastAPI()


class Text(BaseModel):
    text: str


@app.post("/add_text")
def add_text(history: list, text: Text):
    if text.text != "":
        history = history + [(text.text, None)]
    return {"history": history, "response": ""}


@app.post("/add_file")
def add_file(history: list, file: UploadFile = File(...)):
    if isinstance(file.file, _TemporaryFileWrapper):
        try:
            uploaded_file_name = file.filename
            filepath = os.path.join(
                os.getcwd(), "data", config.upload_path, uploaded_file_name
            )

            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, "wb") as f:
                shutil.copyfileobj(file.file, f)

            convo.load_document(filepath)

            return {
                "history": history
                + [(f"{uploaded_file_name} has been loaded into memory.", None)]
            }
        except Exception as e:
            logger.error(f"Error adding file to history: {e}")
            updated_history = history
    else:
        updated_history = history

    return {"history": updated_history}


@app.post("/bot")
def bot(history: list):
    if history and len(history) > 0:
        input = history[-1][0]
        response = convo.predict(input=input)
        history[-1][1] = response
    return {"history": history}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=7865, reload=True)
