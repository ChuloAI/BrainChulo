import os
import shutil
from fastapi import FastAPI, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, desc
from models.all import Conversation, Message, ConversationWithMessages, Flow, FlowRead, FlowCreate, FlowUpdate
from typing import List
from settings import load_config, logger
from plugins import load_plugins
from alembic import command
from alembic.config import Config
from configparser import ConfigParser

config = load_config()

sqlite_database_url = config.database_url
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_database_url, echo=True, connect_args=connect_args)

# Introducing a new feature flag
# So GuidanceLLaMAcpp can coexist with FlowAgents

if config.use_flow_agents:
    logger.info("Using (experimental) flow agents")
    from conversations.document_based_flow import DocumentBasedConversationFlowAgent

    convo = DocumentBasedConversationFlowAgent()
else:
    logger.info("Using experimental Guidance LLaMA cpp implementation.")
    from conversations.document_based import DocumentBasedConversation

    convo = DocumentBasedConversation()


def create_db_and_tables():
    confparser = ConfigParser()
    confparser.read(f"{config.backend_root_path}/alembic.ini")
    confparser.set('alembic', 'script_location', f"{config.backend_root_path}/migrations")
    confparser.set('alembic', 'prepend_sys_path', config.backend_root_path)

    migrations_config_path = os.path.join(config.backend_root_path, "generated_alembic.ini")

    with open(migrations_config_path, 'w') as config_file:
        confparser.write(config_file)

    migrations_config = Config(migrations_config_path)
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post('/llm/query/', response_model=str)
def llm_query(*, query: str, session: Session = Depends(get_session)):
    """
    Query the LLM
    """
    return convo.predict(query, [])


@app.post("/conversations", response_model=Conversation)
def create_conversation(*, session: Session = Depends(get_session), conversation: Conversation):
    """
    Create a new conversation.
    """
    conversation = Conversation.from_orm(conversation)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    print(str(conversation))
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
        filepath = os.path.join(os.getcwd(), "data", config.upload_path, uploaded_file_name)

        os.makedirs(os.path.dirname(filepath), mode=0o777, exist_ok=True)

        with open(filepath, "wb") as f:
            shutil.copyfileobj(file.file, f)

        convo.load_document(filepath, conversation_id)

        return {"text": f"{uploaded_file_name} has been loaded into memory for this conversation."}
    except Exception as e:
        logger.error(f"Error adding file to history: {e}")
        return f"Error adding file to history: {e}"


@app.post('/llm/{conversation_id}/', response_model=str)
def llm(*, conversation_id: str, query: str, session: Session = Depends(get_session)):
    """
    Query the LLM
    """
    conversation_data = get_conversation(conversation_id, session)
    history = conversation_data.messages

    return convo.predict(query, conversation_id)

    # we could also work from history only
    # return convo.predict(query, history)


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


@app.get("/flows", response_model=List[Flow])
def read_flows(session: Session = Depends(get_session)):
    return session.query(Flow).order_by(desc(Flow.id)).all()


@app.get("/flows/{flow_id}", response_model=FlowRead)
def read_flow(flow_id: int):
    pass


@app.post("/flows", response_model=FlowRead)
def create_flow(*, session: Session = Depends(get_session), flow: FlowCreate):
    flow = Flow.from_orm(flow)
    session.add(flow)
    session.commit()
    session.refresh(flow)
    print(str(flow))
    return flow


@app.put("/flows/{flow_id}", response_model=FlowRead)
def update_flow(*, session: Session = Depends(get_session), flow_id: int, flow: FlowUpdate):
    db_flow = session.get(Flow, flow_id)
    db_flow.name = flow.name
    session.add(db_flow)
    session.commit()
    session.refresh(db_flow)
    return db_flow


@app.delete("/flows/{flow_id}")
def delete_flow(*, session: Session = Depends(get_session), flow_id: int):
    flow = session.get(Flow, flow_id)
    if not flow:
        raise HTTPException(404, detail="Flow not found")

    session.delete(flow)
    session.commit()

    return {"text": "Flow deleted."}


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

    uvicorn.run("main:app", host="0.0.0.0", port=7865, reload=False)
