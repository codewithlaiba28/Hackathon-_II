from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List, Optional
import auth
import models
import schemas
from db import get_session
from services.recurring_task_service import RecurringTaskService
from utils.event_publisher import event_publisher
from utils.time_utils import parse_natural_language_date
import logging

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(
    user_id: str,
    search: Optional[str] = Query(None, description="Search term for title or description"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    sort_by: Optional[str] = Query(None, description="Sort by field: due_date, priority, created_at"),
    order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user with search, filter, and sort capabilities.
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    logger.info(f"Fetching tasks for user ID: {user_id}")
    query = select(models.Task).where(models.Task.user_id == user_id)

    # Apply filters
    if search:
        search_term = f"%{search}%"
        query = query.where(
            (models.Task.title.ilike(search_term)) | 
            (models.Task.description.ilike(search_term))
        )
    
    if priority:
        query = query.where(models.Task.priority == priority)
        
    if status_filter:
        query = query.where(models.Task.status == status_filter)

    if tag:
        # Join with TaskTag to filter by tag
        query = query.join(models.TaskTag).where(models.TaskTag.tag == tag)

    # Apply sorting
    if sort_by:
        sort_column = getattr(models.Task, sort_by, None)
        if sort_column:
            if order.lower() == "desc":
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
    else:
        # Default sort by created_at desc
        query = query.order_by(models.Task.created_at.desc())

    tasks = session.exec(query).unique().all()
    logger.info(f"Retrieved {len(tasks)} tasks for user {user_id}")
    return tasks


@router.post("/{user_id}/tasks", response_model=schemas.TaskResponse)
async def create_task(
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

    # Create task excluding tags (handled separately)
    task_data = task.dict(exclude={"tags"})
    db_task = models.Task(
        **task_data,
        user_id=user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    # Handle tags
    if task.tags:
        for tag_name in task.tags:
            task_tag = models.TaskTag(task_id=db_task.id, tag=tag_name)
            session.add(task_tag)
        session.commit()
        session.refresh(db_task)

    # Publish event
    await event_publisher.publish_task_created_event(
        user_id, 
        db_task.id, 
        db_task.title, 
        db_task.priority
    )

    # If task has a due date, the notification service or a dapr job should handle it.
    # We could trigger a reminder scheduled event here if needed.

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
async def update_task(
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
    
    # Handle tags update if present
    if "tags" in update_data:
        tags = update_data.pop("tags")
        # Remove existing tags
        existing_tags = session.exec(select(models.TaskTag).where(models.TaskTag.task_id == task_id)).all()
        for tag in existing_tags:
            session.delete(tag)
        # Add new tags
        if tags:
            for tag_name in tags:
                task_tag = models.TaskTag(task_id=task_id, tag=tag_name)
                session.add(task_tag)

    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    # Publish event
    await event_publisher.publish_task_updated_event(
        user_id, 
        db_task.id, 
        update_data
    )

    return db_task


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=schemas.TaskResponse)
async def toggle_task_complete(
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

    logger.info(f"Toggling task {task_id} for user {user_id}")
    # Convert string task_id to int if necessary for database lookup
    try:
        db_task_id = int(task_id) if isinstance(task_id, str) else task_id
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid task ID format")
        
    db_task = session.get(models.Task, db_task_id)
    if not db_task or db_task.user_id != user_id:
        logger.warning(f"Task {task_id} not found for user {user_id}")
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = db_task.status
    # Toggle based on current status
    if db_task.status == "completed":
        db_task.status = "pending"
    else:
        db_task.status = "completed"
        # Publish completion event with recurrence data
        await event_publisher.publish_task_completed_event(
            user_id, 
            db_task_id, 
            is_recurring=db_task.is_recurring,
            recurrence_pattern=db_task.recurrence_pattern
        )
        
    logger.info(f"Task {task_id} status changing from {old_status} to {db_task.status}")
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{user_id}/tasks/{task_id}")
async def delete_task(
    user_id: str,
    task_id: str,
    current_user: models.User = Depends(auth.get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task.
    """
    if current_user.id != user_id:
        logger.warning(f"Auth mismatch: current_user.id ({current_user.id}) != user_id ({user_id})")
        raise HTTPException(status_code=403, detail="Not authorized")

    # Safety: Convert task_id to int explicitly for session.get
    try:
        db_task_id = int(str(task_id).strip())
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid task ID format")

    logger.info(f"Attempting to delete task {db_task_id} for user {user_id}")
    db_task = session.get(models.Task, db_task_id)
    if not db_task or db_task.user_id != user_id:
        logger.warning(f"Task {db_task_id} not found or owner mismatch")
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        # Explicitly delete associated tags first to avoid NotNullViolation
        # (the sa_column ForeignKey on TaskTag.task_id prevents ORM cascade from working)
        existing_tags = session.exec(
            select(models.TaskTag).where(models.TaskTag.task_id == db_task_id)
        ).all()
        for tag in existing_tags:
            session.delete(tag)
        
        # Also clear any child recurring tasks referencing this task
        child_tasks = session.exec(
            select(models.Task).where(models.Task.parent_recurring_task_id == db_task_id)
        ).all()
        for child in child_tasks:
            child.parent_recurring_task_id = None
            session.add(child)
        
        session.delete(db_task)
        session.commit()
        logger.info(f"Task {db_task_id} successfully deleted from database")
    except Exception as e:
        session.rollback()
        logger.error(f"Database error during deletion of task {db_task_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to delete task due to database error")
    
    # Publish event
    try:
        await event_publisher.publish_task_deleted_event(user_id, db_task_id)
    except Exception as e:
        logger.error(f"Event publishing failed for task {db_task_id} deletion: {str(e)}")
        # We don't raise 500 here since DB deletion was successful
    
    return {"success": True}
