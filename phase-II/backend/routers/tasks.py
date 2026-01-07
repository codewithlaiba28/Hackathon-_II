from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import auth
import models
import schemas
from db import get_session
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(
    user_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    logger.info(f"Fetching tasks for user ID: {user_id}")
    query = select(models.Task).where(models.Task.user_id == user_id)
    tasks = session.exec(query).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=schemas.TaskResponse)
def create_task(
    user_id: str,
    task: schemas.TaskCreate,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    db_task = models.Task(
        **task.dict(),
        user_id=user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/{user_id}/tasks/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    user_id: str,
    task_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve details of a specific task.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = session.get(models.Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return db_task


@router.put("/{user_id}/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    user_id: str,
    task_id: str,
    task_update: schemas.TaskUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = session.get(models.Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=schemas.TaskResponse)
def toggle_task_complete(
    user_id: str,
    task_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle a task's completion status.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = session.get(models.Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.status = "completed" if db_task.status != "completed" else "pending"
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db_task = session.get(models.Task, task_id)
    if not db_task or db_task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()
    return {"success": True}
