from typing import Optional, List
from datetime import datetime
import uuid
from dapr.clients import DaprClient # New import
from ..services.dapr_service import DaprService # New import

# Assuming Task model is available
# from src.models.task import Task

# Placeholder for now, actual implementation will use TaskService
async def add_task(
    title: str,
    user_id: str,
    description: Optional[str] = None,
    status: str = "pending",
    priority: Optional[str] = "Medium",
    tags: Optional[List[str]] = None,
    due_date: Optional[datetime] = None,
    is_recurring: bool = False,
    recurrence_pattern: Optional[str] = None,
    parent_recurring_task_id: Optional[int] = None,
) -> dict: # Returning a dict for now, will be a Task object later
    """
    Adds a new task to the system.
    """
    # Placeholder for logic to add a task
    print(f"Adding task for user {user_id}: {title}")
    return {
        "title": title,
        "user_id": user_id,
        "description": description,
        "status": status,
        "priority": priority,
        "tags": tags,
        "due_date": due_date,
        "is_recurring": is_recurring,
        "recurrence_pattern": recurrence_pattern,
        "parent_recurring_task_id": parent_recurring_task_id,
        "id": 1 # Placeholder ID
    }

# Other MCP tools will be added here

async def update_task(
    task_id: int,
    user_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date: Optional[datetime] = None,
    is_recurring: Optional[bool] = None,
    recurrence_pattern: Optional[str] = None,
    recurrence_end_date: Optional[datetime] = None,
    reminder_offset_minutes: Optional[int] = None,
    parent_recurring_task_id: Optional[int] = None,
) -> dict: # Will return a Task object later
    """
    Updates an existing task in the system.
    """
    # Placeholder for logic to update a task
    print(f"Updating task {task_id} for user {user_id}")
    update_data = {
        "title": title,
        "description": description,
        "status": status,
        "priority": priority,
        "tags": tags,
        "due_date": due_date,
        "is_recurring": is_recurring,
        "recurrence_pattern": recurrence_pattern,
        "recurrence_end_date": recurrence_end_date,
        "reminder_offset_minutes": reminder_offset_minutes,
        "parent_recurring_task_id": parent_recurring_task_id,
    }
    # Filter out None values
    update_data = {k: v for k, v in update_data.items() if v is not None}

    # Placeholder: In a real implementation, this would call TaskService.update_task
    # and return the updated task.
    return {"id": task_id, "user_id": user_id, **update_data}

async def set_reminder(
    task_id: int,
    remind_at: datetime,
    user_id: str, # Changed from uuid.UUID to str
) -> dict:
    """
    Schedules a reminder for a task at a specific time using Dapr Jobs API.
    """
    print(f"Scheduling reminder for task {task_id} at {remind_at} for user {user_id}")
    dapr_client = DaprClient() # Instantiate DaprClient locally
    dapr_service = DaprService() # Instantiate DaprService (no longer takes client)
    success = await dapr_service.schedule_reminder_job(task_id, user_id, remind_at)
    if success:
        return {"task_id": task_id, "remind_at": remind_at.isoformat(), "status": "scheduled"}
    else:
        raise ValueError("Failed to schedule reminder")

async def cancel_reminder(
    task_id: int,
    user_id: str, # Changed from uuid.UUID to str
) -> dict:
    """
    Cancels a scheduled reminder for a task using Dapr Jobs API.
    """
    print(f"Cancelling reminder for task {task_id} for user {user_id}")
    dapr_client = DaprClient() # Instantiate DaprClient locally
    dapr_service = DaprService() # Instantiate DaprService
    success = await dapr_service.cancel_reminder_job(task_id)
    if success:
        return {"task_id": task_id, "status": "cancelled"}
    else:
        raise ValueError("Failed to cancel reminder")

async def list_tasks(
    user_id: str,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    due_date_start: Optional[datetime] = None,
    due_date_end: Optional[datetime] = None,
    search_query: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
) -> List[dict]:
    """
    Lists tasks for a user with optional filtering, searching, and sorting.
    """
    print(f"Listing tasks for user {user_id} with filters: status={status}, priority={priority}, tags={tags}, due_date_start={due_date_start}, due_date_end={due_date_end}, search_query={search_query}, sort_by={sort_by}, sort_order={sort_order}")
    # Placeholder: In a real implementation, this would call TaskService to retrieve filtered tasks.
    return []