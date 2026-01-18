from sqlmodel import SQLModel, Field, Column, DateTime, JSON
from typing import Optional
from datetime import datetime
import uuid


class MessageBase(SQLModel):
    conversation_id: uuid.UUID
    sender_type: str = Field(regex="^(user|ai)$")  # Enum-like validation
    content: str = Field(min_length=1, max_length=5000)
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))


class Message(MessageBase, table=True):
    __tablename__ = "messages"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id", index=True)
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now))
    metadata: Optional[dict] = Field(default=None, sa_column=Column(JSON))


class MessageCreate(MessageBase):
    pass


class MessageUpdate(SQLModel):
    content: Optional[str] = Field(default=None, min_length=1, max_length=5000)
    metadata: Optional[dict] = Field(default=None)


class MessagePublic(MessageBase):
    id: uuid.UUID
    timestamp: datetime
