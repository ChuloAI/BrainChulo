from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
from models.all import Conversation, Message
import sqlite3
from settings import load_config

config = load_config()
router = APIRouter()


@router.post("/conversations", response_model=Conversation)
def create_conversation():
    conversation_id = Conversation()
    return conversation_id


@router.get("/conversations")
def get_conversations():
    conn = sqlite3.connect('brainchulo.db')
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve conversations
    cursor.execute(
        "SELECT * FROM conversations",
        (),
    )
    rows = cursor.fetchall()

    # Close the database connection
    conn.close()

    return rows


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    if conversation_id is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return retrieve_messages(conversation_id)


@router.post("/conversations/{conversation_id}/messages")
def add_message_to_conversation(conversation_id: str, message: str):
    if conversation_id is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    save_messages(conversation_id, [message])
