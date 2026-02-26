from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import uuid
# Note: models import is not needed in schemas, removing relative import issue

# User schemas
class UserBase(BaseModel):
    email: str
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserResponse(UserBase):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = Field(default="pending", description="Task status",
                        json_schema_extra={"enum": ["pending", "completed"]})
    priority: str = Field(default="medium", description="Task priority",
                          json_schema_extra={"enum": ["high", "medium", "low"]})
    tags: Optional[List[str]] = Field(default_factory=list, description="List of tags")
    due_date: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = Field(default=None, description="Recurrence pattern",
                                               json_schema_extra={"enum": ["daily", "weekly", "monthly"]})
    recurrence_end_date: Optional[datetime] = None
    parent_recurring_task_id: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurrence_pattern: Optional[str] = None
    recurrence_end_date: Optional[datetime] = None
    parent_recurring_task_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: str
    tags: Optional[List[str]] = []

    @field_validator('tags', mode='before')
    @classmethod
    def serialize_tags(cls, v):
        if not v:
            return []
        # If it's a list of strings, return as is
        if isinstance(v, list) and len(v) > 0 and isinstance(v[0], str):
            return v
        # If it's a list of TaskTag objects (SQLModel/SQLAlchemy)
        return [item.tag for item in v] if v else []

    class Config:
        from_attributes = True


# TaskTag schemas
class TaskTagBase(BaseModel):
    tag: str  # e.g., "work", "work.meeting", "personal.health"


class TaskTagCreate(TaskTagBase):
    task_id: int


class TaskTagResponse(TaskTagBase):
    id: int
    task_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Auth schemas
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class LoginResponse(BaseModel):
    token: str
    user: UserResponse

class LogoutRequest(BaseModel):
    token: str

class LogoutResponse(BaseModel):
    success: bool

class TokenData(BaseModel):
    user_id: str

class BetterAuthSyncRequest(BaseModel):
    email: str
    name: Optional[str] = None

# Chat schemas
class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[dict]