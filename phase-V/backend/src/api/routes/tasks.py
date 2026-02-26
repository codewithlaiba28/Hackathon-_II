from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ....db import get_session # Assuming db.py is at backend/db.py
from ...models.task import Task
from ...schemas import TaskCreate, TaskUpdate, TaskResponse # Using TaskResponse for output
from ...services.task_service import TaskService
from ...models.user import User # Assuming User model for authentication
from ...auth import get_current_user # Placeholder for auth dependency
import uuid # For UUID type

router = APIRouter(prefix="/tasks", tags=["tasks"])

# Dependency for TaskService
def get_task_service(session: Session = Depends(get_session)) -> TaskService:
    return TaskService(session)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user), # Authenticated user
    task_service: TaskService = Depends(get_task_service),
):
    """
    Create a new task with all parameters, including recurring task settings.
    """
    try:
        task = task_service.create_task(task_create=task_create, user_id=current_user.id)
        return task
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Placeholder for other task endpoints (list, get, update, delete, complete)
# These will be added in subsequent tasks.