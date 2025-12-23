from typing import Dict, Any, Optional
from backend.services.database_service import DatabaseService
from sqlmodel import Session
import json


class MCPToolAgent:
    """Agent responsible for executing MCP tools for task operations"""

    def __init__(self, session: Session):
        self.session = session
        self.db_service = DatabaseService()

    def add_task(self, user_id: str, title: str, description: str = "", conversation_id: str = None) -> Dict[str, Any]:
        """Create a new task"""
        try:
            task_data = {
                "user_id": user_id,
                "title": title,
                "description": description,
                "conversation_id": conversation_id
            }
            task = self.db_service.create_task(self.session, task_data)
            return {
                "success": True,
                "task_id": task.id,
                "message": f"Task '{task.title}' created successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create task: {str(e)}"
            }

    def list_tasks(self, user_id: str, status: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve tasks for a user with optional status filtering"""
        try:
            tasks = self.db_service.get_tasks_by_user(self.session, user_id, status)
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None
                })
            return {
                "success": True,
                "tasks": task_list,
                "count": len(task_list)
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to list tasks: {str(e)}"
            }

    def complete_task(self, task_id: str, user_id: str, completed: bool = True) -> Dict[str, Any]:
        """Mark a task as complete or incomplete"""
        try:
            update_data = {"completed": completed}
            task = self.db_service.update_task(self.session, task_id, user_id, update_data)
            if task:
                status_text = "completed" if completed else "marked as incomplete"
                return {
                    "success": True,
                    "message": f"Task '{task.title}' {status_text} successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Task not found or you don't have permission to update it"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update task: {str(e)}"
            }

    def delete_task(self, task_id: str, user_id: str) -> Dict[str, Any]:
        """Remove a task"""
        try:
            success = self.db_service.delete_task(self.session, task_id, user_id)
            if success:
                return {
                    "success": True,
                    "message": "Task deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Task not found or you don't have permission to delete it"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to delete task: {str(e)}"
            }

    def update_task(self, task_id: str, user_id: str, title: Optional[str] = None,
                   description: Optional[str] = None) -> Dict[str, Any]:
        """Modify task title/description"""
        try:
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description

            if not update_data:
                return {
                    "success": False,
                    "message": "No fields to update provided"
                }

            task = self.db_service.update_task(self.session, task_id, user_id, update_data)
            if task:
                return {
                    "success": True,
                    "message": f"Task updated successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Task not found or you don't have permission to update it"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update task: {str(e)}"
            }