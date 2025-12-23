"""
MCP Server for Todo Management Tools
Implements the required MCP tools for task operations according to the Phase III Design
"""
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import asyncio
from datetime import datetime, date
import uuid


class Task(BaseModel):
    id: str
    user_id: str
    description: str  # According to spec: 'description' is the main content field
    due_date: Optional[str] = None  # ISO 8601 date string (optional)
    priority: str = "medium"  # "low", "medium", "high" (optional, default "medium")
    status: str = "pending"  # "pending", "completed" (default "pending")
    created_at: datetime
    updated_at: datetime
    conversation_id: Optional[str] = None


class TodoMCPServer:
    """
    MCP Server implementation for todo management tools
    Implements the required tools per the specification:
    - add_task
    - list_tasks
    - complete_task
    - delete_task
    - update_task
    """

    def __init__(self):
        # In a real implementation, this would connect to a database
        # For simulation purposes, we'll use in-memory storage
        self.tasks: List[Task] = []

    async def add_task(
        self,
        description: str,
        user_id: str,
        due_date: Optional[str] = None,
        priority: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        MCP tool: Create a new Todo item
        Specification:
        - Parameters: description (required), due_date (optional), priority (optional)
        - Returns: JSON object of the created task (including assigned ID)
        """
        try:
            # Validate required parameter
            if not description or not description.strip():
                return {
                    "status": "error",
                    "message": "Description is required for add_task",
                    "data": None
                }

            # Validate priority if provided
            if priority and priority not in ["low", "medium", "high"]:
                return {
                    "status": "error",
                    "message": "Priority must be one of: low, medium, high",
                    "data": None
                }

            # Use default priority if not provided
            if not priority:
                priority = "medium"

            task = Task(
                id=str(uuid.uuid4()),
                user_id=user_id,
                description=description.strip(),
                due_date=due_date,
                priority=priority,
                status="pending",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.tasks.append(task)

            return {
                "status": "success",
                "data": task.dict(),
                "message": f"Task '{task.description}' created successfully"
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
        status: Optional[str] = None,
        limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        MCP tool: Retrieve tasks based on filters
        Specification:
        - Parameters: status (optional: "pending", "completed", "all"; default "pending")
        - Parameters: limit (optional: max results; default 10)
        - Returns: List of Task objects
        """
        try:
            # Validate status parameter
            if status and status not in ["pending", "completed", "all"]:
                return {
                    "status": "error",
                    "message": "Status must be one of: pending, completed, all",
                    "data": None
                }

            # Default to "pending" if not specified
            if not status:
                status = "pending"

            # Filter tasks by user_id
            user_tasks = [task for task in self.tasks if task.user_id == user_id]

            # Apply status filter
            if status != "all":
                user_tasks = [task for task in user_tasks if task.status == status]

            # Apply limit if provided
            if limit:
                user_tasks = user_tasks[:limit]

            # Convert to dict format
            task_list = [task.dict() for task in user_tasks]

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
        task_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        MCP tool: Mark a task as finished
        Specification:
        - Parameters: task_id (required)
        - Returns: Updated Task object
        - Error: "Task not found" if ID is invalid
        """
        try:
            task = None
            task_index = None
            for i, t in enumerate(self.tasks):
                if t.id == task_id and t.user_id == user_id:
                    task = t
                    task_index = i
                    break

            if not task:
                return {
                    "status": "error",
                    "message": "Task not found",
                    "data": None
                }

            # Update the task to completed
            updated_task = task.copy(update={
                "status": "completed",
                "updated_at": datetime.utcnow()
            })

            # Replace the task in the list
            self.tasks[task_index] = updated_task

            return {
                "status": "success",
                "data": updated_task.dict(),
                "message": f"Task '{updated_task.description}' marked as completed"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to complete task: {str(e)}",
                "data": None
            }

    async def delete_task(
        self,
        task_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        MCP tool: Permanently remove a task
        Specification:
        - Parameters: task_id (required)
        - Returns: {"success": true, "deleted_id": 123}
        """
        try:
            task_index = None
            for i, task in enumerate(self.tasks):
                if task.id == task_id and task.user_id == user_id:
                    task_index = i
                    break

            if task_index is None:
                return {
                    "status": "error",
                    "message": "Task not found",
                    "data": None
                }

            deleted_task = self.tasks.pop(task_index)
            return {
                "status": "success",
                "data": {
                    "success": True,
                    "deleted_id": deleted_task.id
                },
                "message": f"Task '{deleted_task.description}' deleted successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to delete task: {str(e)}",
                "data": None
            }

    async def update_task(
        self,
        task_id: str,
        user_id: str,
        description: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        MCP tool: Modify an existing task's details
        Specification:
        - Parameters: task_id (required), description (optional), status (optional)
        - Returns: Updated Task object
        """
        try:
            # Validate status parameter if provided
            if status and status not in ["pending", "completed"]:
                return {
                    "status": "error",
                    "message": "Status must be one of: pending, completed",
                    "data": None
                }

            task = None
            task_index = None
            for i, t in enumerate(self.tasks):
                if t.id == task_id and t.user_id == user_id:
                    task = t
                    task_index = i
                    break

            if not task:
                return {
                    "status": "error",
                    "message": "Task not found",
                    "data": None
                }

            # Prepare update data
            update_data = task.dict()
            if description is not None:
                update_data["description"] = description.strip()
            if status is not None:
                update_data["status"] = status
            update_data["updated_at"] = datetime.utcnow()

            # Create updated task
            updated_task = Task(**update_data)

            # Replace the task in the list
            self.tasks[task_index] = updated_task

            return {
                "status": "success",
                "data": updated_task.dict(),
                "message": f"Task '{updated_task.description}' updated successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to update task: {str(e)}",
                "data": None
            }


# Global instance for use in other modules
todo_mcp_server = TodoMCPServer()