from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class ConversationBase(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    title: Optional[str]

class Conversation(ConversationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    messages: List["Message"] = Relationship(back_populates="conversation")

class ConversationRead(ConversationBase):
    id: int

class MessageBase(SQLModel):
    text: str
    is_user: bool
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversation.id")
    rating: int = 0 # -1, 0, 1
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

class MessageRead(MessageBase):
    id: int

class ConversationWithMessages(ConversationRead):
    messages: List[MessageRead] = []