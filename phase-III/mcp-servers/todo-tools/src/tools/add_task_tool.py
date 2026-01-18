from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional
import uuid
import sys
from sqlmodel import Session, create_engine, select
from models.task_models import Task, User


class AddTaskRequest(BaseModel):
    user_id: str = Field(..., description="The user's unique identifier")
    title: str = Field(..., description="The task title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="The task description", max_length=500)


class AddTaskResult(BaseModel):
    task_id: int
    status: str
    title: str


def create_add_task_tool(mcp: FastMCP, db_url: str):
    """Create the add_task MCP tool."""
    engine = create_engine(db_url)

    @mcp.tool(
        description="Create a new task",
    )
    def add_task(user_id: str, title: str, description: Optional[str] = None) -> AddTaskResult:
        """Create a new task."""
        print(f"DEBUG: add_task called for user {user_id}", file=sys.stderr)
        try:
            print("DEBUG: Opening session...", file=sys.stderr)
            with Session(engine) as session:
                # Create the task
                task = Task(
                    title=title,
                    description=description,
                    user_id=user_id,
                    completed=False
                )
                
                print("DEBUG: Adding task to session...", file=sys.stderr)
                session.add(task)
                print("DEBUG: Committing...", file=sys.stderr)
                session.commit()
                print("DEBUG: Refreshing...", file=sys.stderr)
                session.refresh(task)
                print("DEBUG: Task created successfully", file=sys.stderr)
                
                return AddTaskResult(
                    task_id=task.id, 
                    status="created", 
                    title=task.title
                )
        except Exception as e:
            import traceback
            print(f"ERROR in add_task: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            raise e

    return add_task
