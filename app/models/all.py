from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    is_user: bool
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversation.id")
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

