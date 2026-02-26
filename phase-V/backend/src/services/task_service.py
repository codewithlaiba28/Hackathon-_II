from typing import List, Optional
from sqlmodel import Session, select, or_
from ..models.task import Task
from ..schemas import TaskCreate, TaskUpdate
from uuid import UUID
from datetime import datetime, UTC


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task_create: TaskCreate, user_id: str) -> Task:
        """
        Create a new task for a user
        """
        task = Task(
            title=task_create.title,
            description=task_create.description,
            status=task_create.status,
            priority=task_create.priority,
            tags=task_create.tags,
            due_date=task_create.due_date,
            is_recurring=task_create.is_recurring,
            recurrence_pattern=task_create.recurrence_pattern,
            recurrence_end_date=task_create.recurrence_end_date,
            reminder_offset_minutes=task_create.reminder_offset_minutes,
            parent_recurring_task_id=task_create.parent_recurring_task_id,
            user_id=user_id
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_user_tasks(
        self, 
        user_id: str, 
        status: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        due_date_start: Optional[datetime] = None,
        due_date_end: Optional[datetime] = None,
        search_query: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: Optional[str] = None,
    ) -> List[Task]:
        """
        Get all tasks for a user, optionally filtered by multiple criteria and sorted.
        """
        query = select(Task).where(Task.user_id == user_id)
        
        if status == "active":
            query = query.where(Task.status != "completed")
        elif status == "completed":
            query = query.where(Task.status == "completed")
        elif status is not None:
            query = query.where(Task.status == status)

        if priority:
            query = query.where(Task.priority == priority)

        if tags:
            for tag in tags:
                query = query.where(Task.tags.contains([tag]))

        if due_date_start:
            query = query.where(Task.due_date >= due_date_start)

        if due_date_end:
            query = query.where(Task.due_date <= due_date_end)

        if search_query:
            query = query.where(or_(
                Task.title.ilike(f"%{search_query}%"),
                Task.description.ilike(f"%{search_query}%")
            ))
        
        # Sorting logic
        if sort_by:
            if hasattr(Task, sort_by):
                sort_column = getattr(Task, sort_by)
                if sort_order == "desc":
                    query = query.order_by(sort_column.desc())
                else:
                    query = query.order_by(sort_column.asc())
            else:
                print(f"Warning: Attempted to sort by unknown column '{sort_by}'")
            
        tasks = self.session.exec(query).all()
        return tasks

    def get_task_by_id(self, task_id: int, user_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for a user (ensures user owns the task)
        """
        task = self.session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()
        return task

    def update_task(self, task_id: int, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        """
        Update a task for a user
        """
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None
            
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(task, field):
                setattr(task, field, value)
                
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: int, user_id: str) -> bool:
        """
        Delete a task for a user
        """
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return False
            
        self.session.delete(task)
        self.session.commit()
        return True

    def complete_task(self, task_id: int, user_id: str) -> Optional[Task]:
        """
        Mark a task as completed for a user
        """
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None
            
        task.status = "completed"
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
