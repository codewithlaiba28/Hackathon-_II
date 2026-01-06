"""
Stateless MCP Server for Todo Management Tools
Implements the required MCP tools for task operations with direct database interaction
"""
from typing import Dict, Any, Optional
import asyncio
from datetime import datetime
import uuid
from sqlmodel import create_engine, Session, select
from models.task import Task, TaskCreate, TaskUpdate
from models.conversation import Conversation
from models.message import Message
from config.settings import settings
from backend.db.session import engine


class TodoMCPStateManager:
    """
    State manager for the MCP server that handles database connections
    """
    def __init__(self):
        self.engine = engine

    def get_session(self):
        """Get a database session"""
        return Session(self.engine)


class TodoMCPServer:
    """
    Stateless MCP Server implementation for todo management tools
    Implements the required tools per the specification with direct database interaction:
    - add_task(user_id, title, description)
    - list_tasks(user_id, status)
    - complete_task(user_id, task_id)
    - delete_task(user_id, task_id)
    - update_task(user_id, task_id, title, description)
    """

    def __init__(self):
        self.state_manager = TodoMCPStateManager()

    async def add_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        MCP tool: Create a new task
        Specification:
        - Parameters: user_id (required), title (required), description (optional)
        - Returns: JSON object of the created task
        """
        try:
            # Validate required parameters
            if not user_id or not user_id.strip():
                return {
                    "status": "error",
                    "message": "user_id is required for add_task",
                    "data": None
                }

            if not title or not title.strip():
                return {
                    "status": "error",
                    "message": "title is required for add_task",
                    "data": None
                }

            with self.state_manager.get_session() as session:
                # Create a new task
                task = Task(
                    user_id=user_id,
                    title=title.strip(),
                    description=description.strip() if description else None,
                    completed=False  # Default to not completed
                )

                session.add(task)
                session.commit()
                session.refresh(task)

                # Convert to dict for response
                task_dict = {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }

                return {
                    "status": "success",
                    "data": task_dict,
                    "message": f"Task '{task.title}' created successfully"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to create task: {str(e)}",
                "data": None
            }

    async def list_tasks(
        self,
        user_id: str,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        MCP tool: Retrieve tasks based on filters
        Specification:
        - Parameters: user_id (required), status (optional: "all", "pending", "completed"; default "all")
        - Returns: List of Task objects
        """
        try:
            # Validate required parameter
            if not user_id or not user_id.strip():
                return {
                    "status": "error",
                    "message": "user_id is required for list_tasks",
                    "data": None
                }

            # Validate status parameter
            if status and status not in ["all", "pending", "completed"]:
                return {
                    "status": "error",
                    "message": "Status must be one of: all, pending, completed",
                    "data": None
                }

            # Default to "all" if not specified
            if not status:
                status = "all"

            with self.state_manager.get_session() as session:
                # Build query based on status filter
                query = select(Task).where(Task.user_id == user_id)

                if status == "pending":
                    query = query.where(Task.completed == False)
                elif status == "completed":
                    query = query.where(Task.completed == True)

                # Execute query
                tasks = session.exec(query).all()

                # Convert to dict format
                task_list = []
                for task in tasks:
                    task_dict = {
                        "id": task.id,
                        "user_id": task.user_id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None,
                        "updated_at": task.updated_at.isoformat() if task.updated_at else None
                    }
                    task_list.append(task_dict)

                return {
                    "status": "success",
                    "data": task_list,
                    "message": f"Retrieved {len(task_list)} tasks"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to list tasks: {str(e)}",
                "data": None
            }

    async def complete_task(
        self,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        MCP tool: Mark a task as complete
        Specification:
        - Parameters: user_id (required), task_id (required)
        - Returns: Updated Task object
        - Error: "Task not found" if ID is invalid
        """
        try:
            # Validate required parameters
            if not user_id or not user_id.strip():
                return {
                    "status": "error",
                    "message": "user_id is required for complete_task",
                    "data": None
                }

            if not task_id:
                return {
                    "status": "error",
                    "message": "task_id is required for complete_task",
                    "data": None
                }

            with self.state_manager.get_session() as session:
                # Find the task
                task = session.get(Task, task_id)

                if not task or task.user_id != user_id:
                    return {
                        "status": "error",
                        "message": "Task not found",
                        "data": None
                    }

                # Update the task to completed
                task.completed = True
                task.updated_at = datetime.utcnow()

                session.add(task)
                session.commit()
                session.refresh(task)

                # Convert to dict for response
                task_dict = {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }

                return {
                    "status": "success",
                    "data": task_dict,
                    "message": f"Task '{task.title}' marked as completed"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to complete task: {str(e)}",
                "data": None
            }

    async def delete_task(
        self,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        MCP tool: Permanently remove a task
        Specification:
        - Parameters: user_id (required), task_id (required)
        - Returns: {"success": true, "deleted_id": task_id}
        """
        try:
            # Validate required parameters
            if not user_id or not user_id.strip():
                return {
                    "status": "error",
                    "message": "user_id is required for delete_task",
                    "data": None
                }

            if not task_id:
                return {
                    "status": "error",
                    "message": "task_id is required for delete_task",
                    "data": None
                }

            with self.state_manager.get_session() as session:
                # Find the task
                task = session.get(Task, task_id)

                if not task or task.user_id != user_id:
                    return {
                        "status": "error",
                        "message": "Task not found",
                        "data": None
                    }

                # Delete the task
                session.delete(task)
                session.commit()

                return {
                    "status": "success",
                    "data": {
                        "success": True,
                        "deleted_id": task_id
                    },
                    "message": f"Task '{task.title}' deleted successfully"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete task: {str(e)}",
                "data": None
            }

    async def update_task(
        self,
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        MCP tool: Modify an existing task's details
        Specification:
        - Parameters: user_id (required), task_id (required), title (optional), description (optional)
        - Returns: Updated Task object
        """
        try:
            # Validate required parameters
            if not user_id or not user_id.strip():
                return {
                    "status": "error",
                    "message": "user_id is required for update_task",
                    "data": None
                }

            if not task_id:
                return {
                    "status": "error",
                    "message": "task_id is required for update_task",
                    "data": None
                }

            with self.state_manager.get_session() as session:
                # Find the task
                task = session.get(Task, task_id)

                if not task or task.user_id != user_id:
                    return {
                        "status": "error",
                        "message": "Task not found",
                        "data": None
                    }

                # Update fields if provided
                if title is not None:
                    task.title = title.strip()
                if description is not None:
                    task.description = description.strip()

                task.updated_at = datetime.utcnow()

                session.add(task)
                session.commit()
                session.refresh(task)

                # Convert to dict for response
                task_dict = {
                    "id": task.id,
                    "user_id": task.user_id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }

                return {
                    "status": "success",
                    "data": task_dict,
                    "message": f"Task '{task.title}' updated successfully"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update task: {str(e)}",
                "data": None
            }


# Global instance for use in other modules
todo_mcp_server = TodoMCPServer()