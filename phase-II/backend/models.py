from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

# User model - aligned with Better Auth schema
class User(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)
    createdAt: datetime = Field(default_factory=datetime.utcnow, alias="createdAt")
    updatedAt: datetime = Field(default_factory=datetime.utcnow, alias="updatedAt")

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

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
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    title: str
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending")  # "pending", "completed", "in-progress"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: str = Field(foreign_key="user.id", index=True)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")