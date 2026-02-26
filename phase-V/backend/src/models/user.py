from sqlmodel import SQLModel, Field, Column, DateTime, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, max_length=255)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(unique=True, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now))
    sort_preference: Optional[str] = Field(default=None) # e.g., "due_date_asc", "priority_desc"

    # Relationships - Added missing back_populates if needed
    tasks: List["Task"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    pass

class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None, max_length=255)
    is_active: Optional[bool] = None

class UserPublic(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
