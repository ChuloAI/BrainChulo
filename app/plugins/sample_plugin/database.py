from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from models.all import Conversation

class SamplePluginModelBase(SQLModel):
    """A base model for SamplePluginModel"""
    # __tablename__: str = 'sample_plugin_model'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    title: Optional[str]
    conversation_id: Optional[int] = Field(default=None, foreign_key="conversation.id")

class SamplePluginModel(SamplePluginModelBase, table=True):
    """A model for SamplePlugin"""
    id: Optional[int] = Field(default=None, primary_key=True)
    conversations: List["Conversation"] = Relationship(back_populates="SamplePluginModel")

class SamplePluginModelRead(SamplePluginModelBase):
    """A read model for SamplePlugin"""
    id: int
