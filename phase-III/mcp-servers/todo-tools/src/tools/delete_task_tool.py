from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Session, create_engine, select
from models.task_models import Task


class DeleteTaskResult(BaseModel):
    task_id: int
    status: str
    title: str


def create_delete_task_tool(mcp: FastMCP, db_url: str):
    """Create the delete_task MCP tool."""
    engine = create_engine(db_url)

    @mcp.tool(
        description="Remove a task from the list",
    )
    def delete_task(user_id: str, task_id: int) -> DeleteTaskResult:
        """Remove a task from the list."""
        with Session(engine) as session:
            # Get the task to delete
            task = session.exec(
                select(Task).where(Task.id == task_id).where(Task.user_id == user_id)
            ).first()
            
            if not task:
                raise Exception("Task not found")
            
            task_id_val = task.id
            title_val = task.title
            
            # Delete the task
            session.delete(task)
            session.commit()
            
            return DeleteTaskResult(
                task_id=task_id_val, 
                status="deleted", 
                title=title_val
            )

    return delete_task
