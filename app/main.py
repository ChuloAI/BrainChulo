from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session
from models.all import Conversation, Message
from typing import List
from conversations.document_based import DocumentBasedConversation
from datetime import datetime

sqlite_database_url = "sqlite:///data/brainchulo.db"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_database_url, echo=True, connect_args=connect_args)

convo = DocumentBasedConversation()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/conversations", response_model=Conversation)
def create_conversation(*, session: Session = Depends(get_session), conversation: Conversation):
    """
    Create a new conversation.
    """
    conversation = Conversation.from_orm(conversation)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    return conversation


@app.get("/conversations", response_model=List[Conversation])
def get_conversations(session: Session = Depends(get_session)):
    """
    Get all conversations.
    """
    return session.query(Conversation).all()


@app.get("/conversations/{conversation_id}", response_model=Conversation)
def get_conversation(conversation_id: int, session: Session = Depends(get_session)):
    """
    Get a conversation by id.
    """
    conversation = session.get(Conversation, conversation_id)

    return conversation

@app.post("/conversations/{conversation_id}/messages", response_model=Message)
def create_message(*, session: Session = Depends(get_session), conversation_id: int, message: Message):
    """
    Create a new message. Then query for a response
    """
    message = Message.from_orm(message)
    session.add(message)

    response = convo.predict(message.text)
    response_message = Message(text=response, is_user=False, conversation_id=conversation_id, created_at=datetime.utcnow())
    session.add(response_message)
    session.commit()
    session.refresh(response_message)

    return response_message



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=7865, reload=True)


# import os
# from fastapi import FastAPI, UploadFile, File
# from tempfile import _TemporaryFileWrapper
# import shutil
# from pydantic import BaseModel
# from conversations.document_based import DocumentBasedConversation
# from settings import load_config, logger

# config = load_config()
# convo = DocumentBasedConversation()

# app = FastAPI()


# class Text(BaseModel):
#     text: str


# @app.post("/add_text")
# def add_text(history: list, text: Text):
#     if text.text != "":
#         history = history + [(text.text, None)]
#     return {"history": history, "response": ""}


# @app.post("/add_file")
# def add_file(history: list, file: UploadFile = File(...)):
#     if isinstance(file.file, _TemporaryFileWrapper):
#         try:
#             uploaded_file_name = file.filename
#             filepath = os.path.join(
#                 os.getcwd(), "data", config.upload_path, uploaded_file_name
#             )

#             os.makedirs(os.path.dirname(filepath), exist_ok=True)

#             with open(filepath, "wb") as f:
#                 shutil.copyfileobj(file.file, f)

#             convo.load_document(filepath)

#             return {
#                 "history": history
#                 + [(f"{uploaded_file_name} has been loaded into memory.", None)]
#             }
#         except Exception as e:
#             logger.error(f"Error adding file to history: {e}")
#             updated_history = history
#     else:
#         updated_history = history

#     return {"history": updated_history}


# @app.post("/bot")
# def bot(history: list):
#     if history and len(history) > 0:
#         input = history[-1][0]
#         response = convo.predict(input=input)
#         history[-1][1] = response
#     return {"history": history}


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run("main:app", host="0.0.0.0", port=7865, reload=True)
