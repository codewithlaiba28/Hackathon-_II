"""
Chat service for the Todo AI Chatbot
Implements the complete stateless chat request lifecycle using the new agent architecture
"""
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from datetime import datetime
import sys
import os
# Add the backend directory to the path so we can import the agent services
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from backend.services.agent_services.main_orchestrator import MainOrchestrator


async def process_chat_request(user_id: str, user_message: str, session: AsyncSession, conversation_id: int = None) -> Dict[str, Any]:
    """
    Complete chat request lifecycle using the new agent architecture
    """
    # Initialize the main orchestrator
    orchestrator = MainOrchestrator(session)

    # Process the request through the orchestrator
    result = await orchestrator.handle_request(user_id, user_message, conversation_id)

    # Return the structured response
    return {
        "conversation_id": result["conversation_id"],
        "message": result["response"],
        "timestamp": datetime.utcnow(),
        "tool_calls": result["tool_calls"]
    }