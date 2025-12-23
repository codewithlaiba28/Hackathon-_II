from typing import Dict, Any, Optional
import logging
from datetime import datetime


class ErrorHandlingAgent:
    """Agent responsible for confirming actions & handling errors with validation and friendly responses"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """Handle an error and return a user-friendly response"""
        error_msg = str(error)
        self.logger.error(f"Error in {context}: {error_msg}", exc_info=True)

        # Create a user-friendly error message
        user_friendly_msg = self._create_user_friendly_message(error_msg, context)

        return {
            "success": False,
            "message": user_friendly_msg,
            "error_code": "INTERNAL_ERROR",
            "timestamp": datetime.utcnow().isoformat()
        }

    def _create_user_friendly_message(self, error_msg: str, context: str) -> str:
        """Create a user-friendly error message based on the error type"""
        error_msg_lower = error_msg.lower()

        if "connection" in error_msg_lower or "database" in error_msg_lower:
            return "I'm having trouble connecting to the database. Please try again in a moment."
        elif "not found" in error_msg_lower or "404" in error_msg_lower:
            return "I couldn't find what you're looking for. Could you check the details and try again?"
        elif "permission" in error_msg_lower or "unauthorized" in error_msg_lower:
            return "You don't have permission to perform this action. Please check your access rights."
        elif "validation" in error_msg_lower or "invalid" in error_msg_lower:
            return "The information you provided seems to be invalid. Please check and try again."
        elif "timeout" in error_msg_lower:
            return "The request took too long to process. Please try again."
        else:
            return "Something went wrong while processing your request. Please try again or contact support if the issue persists."

    def confirm_action(self, action: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Confirm an action with appropriate response based on the result"""
        if result.get("success", False):
            # Create a confirmation message based on the action
            confirmation_msg = self._create_confirmation_message(action, result)
            return {
                "success": True,
                "message": confirmation_msg,
                "result": result,
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            # Return the error result as-is
            return result

    def _create_confirmation_message(self, action: str, result: Dict[str, Any]) -> str:
        """Create a confirmation message based on the action and result"""
        action_lower = action.lower()

        if "create" in action_lower or "add" in action_lower:
            if "task" in action_lower:
                return result.get("message", "Task created successfully!")
            elif "conversation" in action_lower:
                return result.get("message", "Conversation started successfully!")
            else:
                return result.get("message", "Item created successfully!")
        elif "update" in action_lower or "complete" in action_lower:
            if "task" in action_lower:
                return result.get("message", "Task updated successfully!")
            else:
                return result.get("message", "Item updated successfully!")
        elif "delete" in action_lower:
            return result.get("message", "Item deleted successfully!")
        elif "list" in action_lower or "get" in action_lower:
            count = result.get("count", 0) if isinstance(result.get("count"), int) else len(result.get("tasks", []))
            if "task" in action_lower:
                return f"I found {count} tasks for you."
            else:
                return result.get("message", f"Retrieved {count} items successfully!")
        else:
            return result.get("message", "Action completed successfully!")

    def validate_input(self, input_data: Dict[str, Any], required_fields: list) -> Dict[str, Any]:
        """Validate input data has required fields"""
        missing_fields = []
        for field in required_fields:
            if field not in input_data or input_data[field] is None or input_data[field] == "":
                missing_fields.append(field)

        if missing_fields:
            return {
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}",
                "error_code": "VALIDATION_ERROR",
                "missing_fields": missing_fields
            }

        return {"success": True}

    def validate_task_data(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate task-specific data"""
        # Check if title is provided and not empty
        title = task_data.get("title", "").strip()
        if not title:
            return {
                "success": False,
                "message": "Task title is required",
                "error_code": "VALIDATION_ERROR"
            }

        # Check title length
        if len(title) > 255:
            return {
                "success": False,
                "message": "Task title must be 255 characters or less",
                "error_code": "VALIDATION_ERROR"
            }

        # Check description length if provided
        description = task_data.get("description", "")
        if len(description) > 1000:
            return {
                "success": False,
                "message": "Task description must be 1000 characters or less",
                "error_code": "VALIDATION_ERROR"
            }

        return {"success": True}