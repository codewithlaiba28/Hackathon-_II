"""
Conversation Memory Agent
Role: Manages long-term persistence of the chat session.
"""
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from models.conversation import Conversation
from models.message import Message


class ConversationMemoryAgent:
    """
    Conversation Memory Agent
    Role: Manages long-term persistence of the chat session.

    Responsibility:
    - Fetch conversation context before processing.
    - Append new user messages and assistant responses to the database.

    Skills: fetch_history, append_message
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def fetch_history(self, user_id: str, session_id: str = None) -> List[Dict[str, str]]:
        """
        Skill: Fetch History
        Fetches conversation history for a user, either for a specific session or the most recent one.

        Input Schema: {"user_id": "string", "session_id": "string" (optional)}
        Output Schema: List of Message objects with role and content
        """
        try:
            # If session_id is provided, get messages for that specific conversation
            if session_id:
                statement = select(Message).where(
                    Message.conversation_id == session_id
                ).order_by(Message.created_at)
            else:
                # Get the most recent conversation for the user
                conversation_statement = select(Conversation).where(
                    Conversation.user_id == user_id
                ).order_by(Conversation.updated_at.desc()).limit(1)

                result = await self.session.execute(conversation_statement)
                conversation = result.first()

                if not conversation:
                    return []  # No conversation found for user

                conversation_id = conversation[0].id if isinstance(conversation, tuple) else conversation.id

                # Get messages for this conversation
                statement = select(Message).where(
                    Message.conversation_id == conversation_id
                ).order_by(Message.created_at)

            result = await self.session.execute(statement)
            messages = result.scalars().all()

            # Convert to the required format
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

            return formatted_messages

        except Exception as e:
            print(f"Error fetching conversation history: {str(e)}")
            return []

    async def append_message(self, user_id: str, session_id: str, role: str, content: str) -> Dict[str, Any]:
        """
        Skill: Append Message
        Appends a message to the conversation history in the database.

        Input Schema: {"user_id": "string", "session_id": "string", "role": "string", "content": "string"}
        Output Schema: {"success": "boolean", "message_id": "string", "message": "string"}
        """
        try:
            # First, verify that the conversation exists and belongs to the user
            conversation_statement = select(Conversation).where(
                Conversation.id == session_id,
                Conversation.user_id == user_id
            )

            result = await self.session.execute(conversation_statement)
            conversation = result.first()

            if not conversation:
                return {
                    "success": False,
                    "message_id": None,
                    "message": "Conversation not found or doesn't belong to user"
                }

            # Create and store the new message
            message = Message(
                role=role,
                content=content,
                conversation_id=session_id
            )

            self.session.add(message)
            await self.session.commit()
            await self.session.refresh(message)

            return {
                "success": True,
                "message_id": str(message.id),
                "message": "Message added successfully"
            }

        except Exception as e:
            print(f"Error appending message: {str(e)}")
            return {
                "success": False,
                "message_id": None,
                "message": f"Failed to append message: {str(e)}"
            }

    async def create_conversation(self, user_id: str) -> Dict[str, Any]:
        """
        Creates a new conversation for the user.
        """
        try:
            conversation = Conversation(
                user_id=user_id
            )

            self.session.add(conversation)
            await self.session.commit()
            await self.session.refresh(conversation)

            return {
                "success": True,
                "conversation_id": conversation.id,
                "message": "Conversation created successfully"
            }

        except Exception as e:
            print(f"Error creating conversation: {str(e)}")
            return {
                "success": False,
                "conversation_id": None,
                "message": f"Failed to create conversation: {str(e)}"
            }