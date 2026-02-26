import sys
import os
import logging

# Configure logging
# On Vercel, we can't write to files, so we use stream logging only
IS_VERCEL = os.getenv("VERCEL_REGION") is not None

if not IS_VERCEL:
    # Configure file logging at the very top before other imports
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_debug.log")

    # Create file handler
    fh = logging.FileHandler(log_file)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO) # Use INFO for root to avoid asyncio debug spam
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    root_logger.addHandler(fh)

    # Redirect stderr to the log file as well
    class StderrLogger:
        def write(self, message):
            if message.strip():
                root_logger.error(f"STDERR: {message.strip()}")
        def flush(self):
            pass

    sys.stderr = StderrLogger()
else:
    # On Vercel, just use basic logging to stdout/stderr
    logging.basicConfig(level=logging.INFO)

import asyncio

# Fix for Windows asyncio loop with httpx/ssl
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field, Session, create_engine, select
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger("mcp-server")
logger.info(f"DEBUG: MCP script starting, log file: {log_file}")

# Model - table=True must be set for SQLModel to use it as a table
class Task(SQLModel, table=True):
    __tablename__ = "task" # Match backend model table name
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    user_id: str = Field(index=True)
    title: str
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending")
    priority: str = Field(default="medium")  # New field
    due_date: Optional[datetime] = Field(default=None)  # New field
    is_recurring: bool = Field(default=False)  # New field
    recurrence_pattern: Optional[str] = Field(default=None)  # New field
    recurrence_end_date: Optional[datetime] = Field(default=None)  # New field
    parent_recurring_task_id: Optional[int] = Field(default=None)  # New field
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def completed(self) -> bool:
        return self.status == "completed"

# Request/Result Models
class AddTaskResult(BaseModel):
    task_id: int
    status: str
    title: str
    priority: str
    due_date: Optional[str] = None

class TaskInfo(BaseModel):
    id: int
    title: str
    completed: bool
    status: str
    priority: str = "medium"
    due_date: Optional[str] = None

class UpdateTaskResult(BaseModel):
    task_id: int
    status: str
    title: str

class CompleteTaskResult(BaseModel):
    task_id: int
    status: str
    title: str

class DeleteTaskResult(BaseModel):
    task_id: int
    status: str
    title: str

# Server Initialization
mcp = FastMCP("todo-mcp-server")
db_url = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Neon/PostgreSQL frequently requires SSL
if db_url.startswith("postgresql") and "sslmode" not in db_url:
    if "?" in db_url:
        db_url += "&sslmode=require"
    else:
        db_url += "?sslmode=require"

logger.info(f"Using DB URL: {db_url}")
engine = create_engine(db_url)

@mcp.tool(description="Create a new task with optional priority, due date, and recurrence settings")
def add_task(
    user_id: str, 
    title: str, 
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
    is_recurring: bool = False,
    recurrence_pattern: Optional[str] = None
) -> AddTaskResult:
    """
    Add a new task to the user's list.
    
    Args:
        user_id: The user's ID
        title: Task title (required)
        description: Task description (optional)
        priority: Priority level - 'low', 'medium', or 'high' (default: 'medium')
        due_date: Due date in ISO format like '2026-02-17T21:00:00' (optional)
        is_recurring: Whether this is a recurring task (default: False)
        recurrence_pattern: Recurrence pattern - 'daily', 'weekly', or 'monthly' (optional, only if is_recurring=True)
    """
    logger.info(f"add_task tool called for user {user_id}: {title} (priority={priority}, due_date={due_date})")
    try:
        with Session(engine) as session:
            # Parse due_date if provided
            parsed_due_date = None
            if due_date:
                try:
                    # Clean up the date string (remove potential extra whitespace or 'Z')
                    clean_due_date = due_date.strip().replace('Z', '+00:00')
                    # Try built-in fromisoformat first
                    parsed_due_date = datetime.fromisoformat(clean_due_date)
                    logger.info(f"Successfully parsed ISO date: {parsed_due_date}")
                except Exception as e:
                    logger.warning(f"ISO parse failed for '{due_date}': {e}. Trying dateutil...")
                    try:
                        from dateutil import parser as date_parser
                        parsed_due_date = date_parser.parse(due_date)
                        logger.info(f"Successfully parsed date with dateutil: {parsed_due_date}")
                    except Exception as e2:
                        logger.error(f"All date parsing failed for '{due_date}': {e2}")
                        parsed_due_date = None
            
            task = Task(
                title=title, 
                description=description, 
                user_id=user_id, 
                status="pending",
                priority=priority,
                due_date=parsed_due_date,
                is_recurring=is_recurring,
                recurrence_pattern=recurrence_pattern if is_recurring else None
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            logger.info(f"Task created with ID {task.id}")
            return AddTaskResult(
                task_id=task.id, 
                status=task.status, 
                title=task.title,
                priority=task.priority,
                due_date=task.due_date.isoformat() if task.due_date else None
            )
    except Exception as e:
        logger.error(f"Error in add_task: {str(e)}", exc_info=True)
        raise

@mcp.tool(description="Retrieve tasks from the list")
def list_tasks(user_id: str, status: Optional[str] = "all") -> List[TaskInfo]:
    logger.info(f"list_tasks tool called for user {user_id}, status {status}")
    try:
        with Session(engine) as session:
            # Force fresh read from database (no cached data)
            session.expire_all()
            
            query = select(Task).where(Task.user_id == user_id)
            if status == "pending":
                query = query.where(Task.status == "pending")
            elif status == "completed":
                query = query.where(Task.status == "completed")
            tasks = session.exec(query).all()
            return [
                TaskInfo(
                    id=task.id, 
                    title=task.title, 
                    completed=(task.status == "completed"), 
                    status=task.status,
                    priority=task.priority,
                    due_date=task.due_date.isoformat() if task.due_date else None
                ) 
                for task in tasks
            ]
    except Exception as e:
        logger.error(f"Error in list_tasks: {str(e)}", exc_info=True)
        raise

@mcp.tool(description="Modify task title or description")
def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> UpdateTaskResult:
    logger.info(f"update_task tool called for user {user_id}, task {task_id}")
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        if not task:
            raise Exception("Task not found")
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return UpdateTaskResult(task_id=task.id, status=task.status, title=task.title)

@mcp.tool(description="Mark a task as complete")
def complete_task(user_id: str, task_id: int) -> CompleteTaskResult:
    logger.info(f"complete_task tool called for user {user_id}, task {task_id}")
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        if not task:
            raise Exception("Task not found")
        task.status = "completed"
        session.add(task)
        session.commit()
        session.refresh(task)
        return CompleteTaskResult(task_id=task.id, status=task.status, title=task.title)

@mcp.tool(description="Remove a task from the list")
def delete_task(user_id: str, task_id: int) -> DeleteTaskResult:
    logger.info(f"delete_task tool called for user {user_id}, task {task_id}")
    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.id == task_id).where(Task.user_id == user_id)).first()
        if not task:
            raise Exception("Task not found")
        tid, title = task.id, task.title
        session.delete(task)
        session.commit()
        return DeleteTaskResult(task_id=tid, status="deleted", title=title)

if __name__ == "__main__":
    try:
        # Redirect stdout/stderr purely for safety, although logging handles it
        # sys.stdout = open(os.devnull, 'w') # DANGER: FastMCP needs stdout!
        
        # FastMCP uses stdout for communication, so we MUST NOT print anything else
        logger.info("Starting MCP server...")
        mcp.run()
    except Exception as e:
        logger.critical(f"Server crashed: {e}", exc_info=True)
        # Even on crash, don't print to stdout if possible, or print properly formatted error if protocol allows
        sys.exit(1)
