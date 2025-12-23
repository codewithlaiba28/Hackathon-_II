from typing import Dict, Any
from backend.services.agent_services.task_planner_agent import TaskPlannerAgent
from backend.services.agent_services.error_handling_agent import ErrorHandlingAgent
from sqlmodel import Session


class ChatService:
    """Service to coordinate chat processing using the agent services"""

    def __init__(self, session: Session):
        self.session = session
        self.task_planner_agent = TaskPlannerAgent(session)
        self.error_handler = ErrorHandlingAgent()

    def process_chat_message(self, user_id: str, message: str, conversation_id: str = None) -> Dict[str, Any]:
        """Process a chat message using the agent system"""
        try:
            # Validate input
            validation_result = self.error_handler.validate_input(
                {"user_id": user_id, "message": message},
                ["user_id", "message"]
            )
            if not validation_result["success"]:
                return validation_result

            # Process the user request using the task planner agent
            result = self.task_planner_agent.process_user_request(user_id, message, conversation_id)

            # Format the response to match the expected API structure
            formatted_result = {
                "conversation_id": result.get("conversation_id", conversation_id),
                "response": result.get("message", "I processed your request successfully."),
                "tool_calls": result.get("tool_calls", [])
            }

            return formatted_result

        except Exception as e:
            error_result = self.error_handler.handle_error(e, "processing chat message")
            return {
                "conversation_id": conversation_id,
                "response": error_result.get("message", "Sorry, I encountered an error processing your request."),
                "tool_calls": [],
                "error": True
            }

    def handle_complex_request(self, user_id: str, message: str, conversation_id: str = None) -> Dict[str, Any]:
        """Handle complex requests that might require multiple steps"""
        try:
            # Validate input
            validation_result = self.error_handler.validate_input(
                {"user_id": user_id, "message": message},
                ["user_id", "message"]
            )
            if not validation_result["success"]:
                return validation_result

            # Use the task planner agent to handle complex requests
            result = self.task_planner_agent.plan_complex_request(user_id, message, conversation_id)

            # Format the response
            formatted_result = {
                "conversation_id": result.get("conversation_id", conversation_id),
                "response": result.get("message", "I processed your complex request."),
                "tool_calls": result.get("tool_calls", [])
            }

            return formatted_result

        except Exception as e:
            error_result = self.error_handler.handle_error(e, "handling complex request")
            return {
                "conversation_id": conversation_id,
                "response": error_result.get("message", "Sorry, I encountered an error processing your complex request."),
                "tool_calls": [],
                "error": True
            }

    def create_new_conversation(self, user_id: str) -> Dict[str, Any]:
        """Create a new conversation for a user"""
        try:
            # Use the memory agent to create a new conversation
            result = self.task_planner_agent.memory_agent.store_conversation(user_id)
            if result["success"]:
                return {
                    "conversation_id": result["conversation_id"],
                    "message": "New conversation started successfully"
                }
            else:
                return result
        except Exception as e:
            return self.error_handler.handle_error(e, "creating new conversation")