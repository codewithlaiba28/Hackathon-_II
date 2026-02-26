from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlmodel import Session, create_engine, select
from models.task_models import Task


class TaskInfo(BaseModel):
    id: int
    title: str
    completed: bool


def create_list_tasks_tool(mcp: FastMCP, db_url: str):
    """Create the list_tasks MCP tool."""
    engine = create_engine(db_url)

    @mcp.tool(
        description="Retrieve tasks from the list",
    )
    def list_tasks(user_id: str, status: Optional[str] = "all") -> List[TaskInfo]:
        """Retrieve tasks from the list."""
        with Session(engine) as session:
            query = select(Task).where(Task.user_id == user_id)
            
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)
            
            tasks = session.exec(query).all()
            
            task_items = [
                TaskInfo(
                    id=task.id,
                    title=task.title,
                    completed=task.completed
                )
                for task in tasks
            ]
            
            return task_items

    return list_tasks

    return list_tasks
