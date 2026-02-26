from typing import Optional, List
from datetime import datetime
import uuid

from sqlmodel import SQLModel, Field, Relationship, Column, String
from sqlalchemy.dialects.postgresql import ARRAY

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending")
    priority: Optional[str] = Field(default="Medium")  # High, Medium, Low
    tags: List[str] = Field(default_factory=list, sa_column=Column(ARRAY(String)))
    due_date: Optional[datetime] = Field(default=None)
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None) # daily, weekly, monthly
    recurrence_end_date: Optional[datetime] = Field(default=None)
    reminder_sent: bool = Field(default=False)
    reminder_offset_minutes: Optional[int] = Field(default=0)
    parent_recurring_task_id: Optional[int] = Field(default=None, foreign_key="task.id")

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id") # Link to the User model - Changed to str for consistency with root user.id
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}, nullable=False)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

    # Optional: Relationship to self for recurring tasks
    parent_task: Optional["Task"] = Relationship(back_populates="child_tasks", sa_relationship_kwargs={"remote_side": "Task.id"})
    child_tasks: List["Task"] = Relationship(back_populates="parent_task")

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
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
    reminder_offset_minutes: Optional[int] = None
    parent_recurring_task_id: Optional[int] = None

class TaskPublic(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime
