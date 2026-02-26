from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime
import uuid


class ConversationBase(SQLModel):
    title: Optional[str] = Field(max_length=200, nullable=True)
    is_active: bool = Field(default=True)


class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now))


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(SQLModel):
    title: Optional[str] = Field(default=None, max_length=200)
    is_active: Optional[bool] = None


class ConversationPublic(ConversationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
