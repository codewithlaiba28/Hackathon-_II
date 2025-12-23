"""
Chat routes for the Todo AI Chatbot
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import uuid4
import json
from datetime import datetime

from ..database.database import get_async_session
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate
from ..schemas.chat import ChatRequest, ChatResponse, MessageResponse
from ..services.chat_service import process_chat_request
from ..services.agent_service import run_agent

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Main chat endpoint that handles the complete lifecycle:
    1. Fetch conversation history from DB
    2. Build message array for OpenAI Agents SDK
    3. Store user message
    4. Execute agent runner
    5. Capture MCP tool calls
    6. Store assistant response
    7. Return structured response
    """
    try:
        # Process the complete chat request lifecycle
        response = await process_chat_request(
            user_id=user_id,
            user_message=request.message,
            session=session
        )

        return ChatResponse(
            conversation_id=response["conversation_id"],
            message=response["message"],
            timestamp=response["timestamp"],
            tool_calls=response.get("tool_calls", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))