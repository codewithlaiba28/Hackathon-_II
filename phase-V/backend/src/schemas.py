from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
import uuid

# Task schemas - Aligned with root models.py and schemas.py
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = Field(default="pending")
    priority: str = Field(default="medium")
    tags: Optional[List[str]] = Field(default_factory=list)
    due_date: Optional[datetime] = None
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = Field(default=None) # daily, weekly, monthly
    recurrence_end_date: Optional[datetime] = None
    reminder_sent: bool = False
    parent_recurring_task_id: Optional[int] = None
    reminder_offset_minutes: Optional[int] = Field(default=0)

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
    reminder_sent: Optional[bool] = None
    parent_recurring_task_id: Optional[int] = None
    reminder_offset_minutes: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    user_id: str

    class Config:
        from_attributes = True

# Event Payload schemas for Dapr Pub/Sub
class TaskEventPayload(BaseModel):
    event_type: str
    task_id: int
    user_id: str
    title: Optional[str] = None
    is_recurring: Optional[bool] = False
    recurrence_pattern: Optional[str] = None
    due_date: Optional[str] = None
