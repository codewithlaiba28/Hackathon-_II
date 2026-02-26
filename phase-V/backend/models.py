from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, ForeignKey

# User model - aligned with Better Auth schema
# Refinement: Added Relationship and List imports to ensure clean Dapr integration.
class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)
    createdAt: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updatedAt: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")
    conversations: List["Conversation"] = Relationship(back_populates="user")

# Session model - aligned with Better Auth schema
class Session(SQLModel, table=True):
    id: str = Field(primary_key=True)
    expiresAt: datetime
    ipAddress: Optional[str] = None
    userAgent: Optional[str] = None
    userId: str = Field(foreign_key="user.id", index=True)
    token: str = Field(unique=True, index=True)
    createdAt: datetime
    updatedAt: datetime

# Task model
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending")

    # New fields for advanced features
    priority: str = Field(default="medium")  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)
    reminder_sent: bool = Field(default=False)
    reminder_offset_minutes: int = Field(default=0)
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None)  # daily, weekly, monthly
    recurrence_end_date: Optional[datetime] = Field(default=None)
    parent_recurring_task_id: Optional[int] = Field(
        default=None, 
        sa_column=Column(Integer, ForeignKey("task.id", ondelete="CASCADE"), nullable=True)
    )

    @property
    def completed(self) -> bool:
        return self.status == "completed"

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")
    # Relationship for recurring task parent-child
    parent_task: Optional["Task"] = Relationship(
        back_populates="child_tasks", 
        sa_relationship_kwargs={"remote_side": "Task.id"}
    )
    child_tasks: List["Task"] = Relationship(back_populates="parent_task", sa_relationship_kwargs={"cascade": "all, delete-orphan", "passive_deletes": True})
    # Relationship for tags
    tags: List["TaskTag"] = Relationship(back_populates="task", sa_relationship_kwargs={"cascade": "all, delete-orphan", "passive_deletes": True})


class TaskTag(SQLModel, table=True):
    """Model for hierarchical tagging system"""
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    task_id: int = Field(
        sa_column=Column(Integer, ForeignKey("task.id", ondelete="CASCADE"), index=True, nullable=False)
    )
    tag: str = Field(max_length=100)  # e.g., "work", "work.meeting", "personal.health"
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to task
    task: "Task" = Relationship(back_populates="tags")

class Conversation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: Optional["User"] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    user_id: str = Field(foreign_key="user.id", index=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")