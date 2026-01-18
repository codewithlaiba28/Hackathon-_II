from typing import List, Optional
from sqlmodel import Session, select
from ..models.task import Task, TaskCreate, TaskUpdate
from uuid import UUID
from datetime import datetime


class TaskService:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, task_create: TaskCreate, user_id: UUID) -> Task:
        """
        Create a new task for a user
        """
        task = Task(
            description=task_create.description,
            is_completed=task_create.is_completed,
            user_id=user_id
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_user_tasks(self, user_id: UUID, status: str = "all") -> List[Task]:
        """
        Get all tasks for a user, optionally filtered by status
        """
        query = select(Task).where(Task.user_id == user_id)
        
        if status == "active":
            query = query.where(Task.is_completed == False)
        elif status == "completed":
            query = query.where(Task.is_completed == True)
            
        tasks = self.session.exec(query).all()
        return tasks

    def get_task_by_id(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """
        Get a specific task by ID for a user (ensures user owns the task)
        """
        task = self.session.exec(
            select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
        ).first()
        return task

    def update_task(self, task_id: UUID, task_update: TaskUpdate, user_id: UUID) -> Optional[Task]:
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
                
        task.updated_at = datetime.now()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: UUID, user_id: UUID) -> bool:
        """
        Delete a task for a user
        """
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return False
            
        self.session.delete(task)
        self.session.commit()
        return True

    def complete_task(self, task_id: UUID, user_id: UUID) -> Optional[Task]:
        """
        Mark a task as completed for a user
        """
        task = self.get_task_by_id(task_id, user_id)
        if not task:
            return None
            
        task.is_completed = True
        task.completed_at = datetime.now()
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
