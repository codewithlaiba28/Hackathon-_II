from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session, create_engine, select
from models.task_models import Task, User


class CompleteTaskResult(BaseModel):
    task_id: int
    status: str
    title: str


def create_complete_task_tool(mcp: FastMCP, db_url: str):
    """Create the complete_task MCP tool."""
    engine = create_engine(db_url)

    @mcp.tool(
        description="Mark a task as complete",
    )
    def complete_task(user_id: str, task_id: int) -> CompleteTaskResult:
        """Mark a task as complete."""
        with Session(engine) as session:
            # Get the task to complete
            task = session.exec(
                select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            ).first()
            
            if not task:
                raise Exception("Task not found")
            
            # Update task as completed
            task.completed = True
            
            session.add(task)
            session.commit()
            session.refresh(task)
            
            return CompleteTaskResult(
                task_id=task.id, 
                status="completed", 
                title=task.title
            )

    return complete_task
