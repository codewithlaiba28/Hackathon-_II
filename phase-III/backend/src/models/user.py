from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, max_length=255)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now))


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    email: Optional[str] = Field(default=None, max_length=255)
    is_active: Optional[bool] = None


class UserPublic(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
