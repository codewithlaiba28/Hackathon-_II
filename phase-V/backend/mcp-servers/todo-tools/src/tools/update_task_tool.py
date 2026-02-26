from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session, create_engine, select
from datetime import datetime
from models.task_models import Task


class UpdateTaskResult(BaseModel):
    task_id: int
    status: str
    title: str


def create_update_task_tool(mcp: FastMCP, db_url: str):
    """Create the update_task MCP tool."""
    engine = create_engine(db_url)

    @mcp.tool(
        description="Modify task title or description",
    )
    def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> UpdateTaskResult:
        """Modify task title or description."""
        with Session(engine) as session:
            # Get the task to update
            task = session.exec(
                select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            ).first()
            
            if not task:
                raise Exception("Task not found")
            
            # Update fields if provided
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            
            task.updated_at = datetime.utcnow()
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return UpdateTaskResult(
                task_id=task.id, 
                status="updated", 
                title=task.title
            )

    return update_task
