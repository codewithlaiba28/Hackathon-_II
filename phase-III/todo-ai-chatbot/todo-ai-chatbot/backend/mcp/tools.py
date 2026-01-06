from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.task import Task
from datetime import datetime

class TodoTools:
    @staticmethod
    async def add_task(session: AsyncSession, user_id: str, title: str, description: str = "") -> dict:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return {"task_id": task.id, "status": "created", "title": task.title}

    @staticmethod
    async def list_tasks(session: AsyncSession, user_id: str, status: Optional[str] = "all") -> List[dict]:
        query = select(Task).where(Task.user_id == user_id)
        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)
        
        results = await session.execute(query)
        tasks = results.scalars().all()
        return [{"id": t.id, "title": t.title, "completed": t.completed} for t in tasks]

    @staticmethod
    async def complete_task(session: AsyncSession, user_id: str, task_id: int) -> dict:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()
        if not task:
            return {"error": "Task not found"}
        
        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return {"task_id": task.id, "status": "completed", "title": task.title}

    @staticmethod
    async def delete_task(session: AsyncSession, user_id: str, task_id: int) -> dict:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()
        if not task:
            return {"error": "Task not found"}
        
        await session.delete(task)
        await session.commit()
        return {"task_id": task_id, "status": "deleted", "title": task.title}

    @staticmethod
    async def update_task(session: AsyncSession, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> dict:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()
        if not task:
            return {"error": "Task not found"}
        
        if title:
            task.title = title
        if description:
            task.description = description
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return {"task_id": task.id, "status": "updated", "title": task.title}
