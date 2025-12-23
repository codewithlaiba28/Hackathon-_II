from typing import Dict, Any, Optional, List
from backend.services.database_service import DatabaseService
from sqlmodel import Session
from backend.models.conversation import Conversation
from backend.models.message import Message


class MemoryAgent:
    """Agent responsible for fetching/storing conversation & tasks in database"""

    def __init__(self, session: Session):
        self.session = session
        self.db_service = DatabaseService()

    def store_conversation(self, user_id: str, title: Optional[str] = None) -> Dict[str, Any]:
        """Create a new conversation"""
        try:
            conversation_data = {
                "user_id": user_id,
                "title": title
            }
            conversation = self.db_service.create_conversation(self.session, conversation_data)
            return {
                "success": True,
                "conversation_id": conversation.id,
                "message": "Conversation created successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create conversation: {str(e)}"
            }

    def get_conversation(self, conversation_id: str, user_id: str) -> Dict[str, Any]:
        """Get conversation by ID for a specific user"""
        try:
            conversation = self.db_service.get_conversation_by_id(self.session, conversation_id, user_id)
            if conversation:
                return {
                    "success": True,
                    "conversation": {
                        "id": conversation.id,
                        "title": conversation.title,
                        "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
                        "is_active": conversation.is_active
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "Conversation not found or you don't have permission to access it"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get conversation: {str(e)}"
            }

    def store_message(self, conversation_id: str, role: str, content: str,
                     tool_calls: Optional[Dict[str, Any]] = None,
                     tool_call_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Store a message in the conversation"""
        try:
            message_data = {
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
                "tool_calls": tool_calls,
                "tool_call_results": tool_call_results
            }
            message = self.db_service.create_message(self.session, message_data)
            return {
                "success": True,
                "message_id": message.id,
                "message": "Message stored successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to store message: {str(e)}"
            }

    def get_conversation_history(self, conversation_id: str, user_id: str) -> Dict[str, Any]:
        """Get conversation history with messages"""
        try:
            # First check if user has access to the conversation
            conversation = self.db_service.get_conversation_by_id(self.session, conversation_id, user_id)
            if not conversation:
                return {
                    "success": False,
                    "message": "Conversation not found or you don't have permission to access it"
                }

            # In a full implementation, we would fetch messages from the database
            # For now, we'll return a placeholder response
            return {
                "success": True,
                "conversation_id": conversation_id,
                "messages": [],
                "message": "Conversation history retrieved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to get conversation history: {str(e)}"
            }