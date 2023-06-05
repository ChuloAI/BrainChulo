import os
import shutil
from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, desc
from models.all import Conversation, Message, ConversationWithMessages
from typing import List
from conversations.document_based import DocumentBasedConversation
from settings import load_config, logger
from plugins import load_plugins
from alembic import command
from alembic.config import Config

config = load_config()

sqlite_database_url = config.database_url
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_database_url, echo=True, connect_args=connect_args)

convo = DocumentBasedConversation()

def create_db_and_tables():
    migrations_config = Config("alembic.ini")
    command.upgrade(migrations_config, "head")

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()


# Load the plugins
load_plugins(app=app)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://0.0.0.0:5173",
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


@app.put('/conversations/{conversation_id}', response_model=Conversation)
def update_conversation(*, session: Session = Depends(get_session), conversation_id: int, payload: dict):
    """
    Update the title of a conversation.
    """
    conversation = session.get(Conversation, conversation_id)
    conversation.title = payload["title"]
    session.add(conversation)
    session.commit()
    session.refresh(conversation)

    return conversation

@app.delete("/conversations/{conversation_id}")
def delete_conversation(*, session: Session = Depends(get_session), conversation_id: int):
    """
    Delete a conversation.
    """
    conversation = session.get(Conversation, conversation_id)
    session.delete(conversation)
    session.commit()

    return conversation


@app.get("/conversations", response_model=List[Conversation])
def get_conversations(session: Session = Depends(get_session)):
    """
    Get all conversations.
    """
    return session.query(Conversation).order_by(desc(Conversation.id)).all()


@app.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation(conversation_id: int, session: Session = Depends(get_session)):
    """
    Get a conversation by id.
    """
    conversation = session.get(Conversation, conversation_id)

    return conversation

@app.post("/conversations/{conversation_id}/messages", response_model=Message)
def create_message(*, session: Session = Depends(get_session), conversation_id: int, message: Message):
    """
    Create a new message.
    """
    message = Message.from_orm(message)
    session.add(message)
    session.commit()
    session.refresh(message)

    return message

@app.post("/conversations/{conversation_id}/files", response_model=dict)
def upload_file(*, conversation_id: int, file: UploadFile):
    """
    Upload a file.
    """
    try:
        uploaded_file_name = file.filename
        filepath = os.path.join(
            os.getcwd(), "data", config.upload_path, uploaded_file_name
        )

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)

        convo.load_document(filepath, conversation_id)

        return {"text": f"{uploaded_file_name} has been loaded into memory for this conversation."}
    except Exception as e:
        logger.error(f"Error adding file to history: {e}")
        return f"Error adding file to history: {e}"

@app.post('/llm', response_model=str)
def llm(*, query: str):
    """
    Query the LLM
    """
    return convo.predict(query)

@app.post("/conversations/{conversation_id}/messages/{message_id}/upvote", response_model=Message)
def upvote_message(*, session: Session = Depends(get_session), conversation_id: int, message_id: int):
    """
    Upvote a message.
    """
    message = session.get(Message, message_id)
    message.rating = 1
    session.add(message)
    session.commit()
    session.refresh(message)

    return message

@app.post("/conversations/{conversation_id}/messages/{message_id}/downvote", response_model=Message)
def downvote_message(*, session: Session = Depends(get_session), conversation_id: int, message_id: int):
    """
    Downvote a message.
    """
    message = session.get(Message, message_id)
    message.rating = -1
    session.add(message)
    session.commit()
    session.refresh(message)

    return message

@app.post("/conversations/{conversation_id}/messages/{message_id}/resetVote", response_model=Message)
def reset_message_vote(*, session: Session = Depends(get_session), conversation_id: int, message_id: int):
    """
    Reset a message vote.
    """
    message = session.get(Message, message_id)
    message.rating = 0
    session.add(message)
    session.commit()
    session.refresh(message)

    return message

@app.post("/reset", response_model=dict)
def reset_all():
    """
    Reset the database.
    """
    SQLModel.metadata.drop_all(engine)
    print("Database has been reset.")
    SQLModel.metadata.create_all(engine)

    return {"text": "Database has been reset."}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=7865, reload=True)