from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import auth
from auth import get_current_user
import models
import schemas
from db import get_session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[schemas.TaskResponse])
def get_tasks(
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    This function implements the data filtering step in the authentication flow.
    """
    logger.info(f"Fetching tasks for user ID: {current_user.id}")

    # Ensure each user can only access their own tasks (Security Rule)
    query = select(models.Task).where(models.Task.user_id == current_user.id)
    tasks = session.exec(query).all()

    logger.info(f"Returning {len(tasks)} tasks for user ID: {current_user.id}")
    return tasks


@router.post("/", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    # Create task with the authenticated user's ID
    db_task = models.Task(
        **task.dict(),
        user_id=current_user.id  # Assign task to current user
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: str,
    task_update: schemas.TaskUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.
    This function implements the data filtering step in the authentication flow.
    """
    logger.info(f"Updating task ID: {task_id} for user ID: {current_user.id}")

    # Get the task and verify it belongs to the current user
    db_task = session.get(models.Task, task_id)

    if not db_task:
        logger.warning(f"Task with ID {task_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Security check: ensure user can only update their own tasks
    if db_task.user_id != current_user.id:
        logger.warning(f"User {current_user.id} attempted to update task {task_id} belonging to user {db_task.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    logger.info(f"User {current_user.id} authorized to update task {task_id}")

    # Update task fields
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Update the updated_at timestamp
    db_task.updated_at = db_task.updated_at  # This will be updated automatically by SQLModel

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    logger.info(f"Successfully updated task {task_id}")
    return db_task


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task.
    This function implements the data filtering step in the authentication flow.
    """
    logger.info(f"Deleting task ID: {task_id} for user ID: {current_user.id}")

    # Get the task and verify it belongs to the current user
    db_task = session.get(models.Task, task_id)

    if not db_task:
        logger.warning(f"Task with ID {task_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Security check: ensure user can only delete their own tasks
    if db_task.user_id != current_user.id:
        logger.warning(f"User {current_user.id} attempted to delete task {task_id} belonging to user {db_task.user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    logger.info(f"User {current_user.id} authorized to delete task {task_id}")
    session.delete(db_task)
    session.commit()
    logger.info(f"Successfully deleted task {task_id}")
    return {"success": True}