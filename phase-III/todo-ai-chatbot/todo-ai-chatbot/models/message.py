"""
Message model for the Todo AI Chatbot
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import String, DateTime, Index, ForeignKey
from pydantic import BaseModel


class MessageBase(SQLModel):
    user_id: str = Field(index=True)
    role: str = Field(max_length=20)
    content: str = Field(max_length=5000)
    conversation_id: int = Field(foreign_key="conversations.id")

class Message(MessageBase, table=True):
    __tablename__ = "messages"
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))

    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")

class MessageCreate(BaseModel):
    user_id: str
    role: str
    content: str
    conversation_id: int

class MessageResponse(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True