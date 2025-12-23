from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any
from pydantic import BaseModel
from backend.services.chat_service import ChatService
from backend.db.session import get_session
from sqlmodel import Session


# Define request/response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: list = []


# Create router
router = APIRouter()


@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session)
) -> ChatResponse:
    """
    Process user message and return AI response
    """
    try:
        # Initialize chat service
        chat_service = ChatService(session)

        # Process the chat message
        result = chat_service.process_chat_message(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )

        # Check if there was an error in processing
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["response"])

        # Return the formatted response
        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result.get("tool_calls", [])
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle any other exceptions
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/api/users/{user_id}/tasks")
async def list_tasks_endpoint(
    user_id: str,
    status: Optional[str] = None,
    session: Session = Depends(get_session)
):
    """
    List user's tasks with optional filtering
    """
    try:
        from backend.services.agent_services.mcp_tool_agent import MCPToolAgent

        # Initialize MCP tool agent
        mcp_agent = MCPToolAgent(session)

        # List tasks for the user
        result = mcp_agent.list_tasks(user_id, status)

        if result["success"]:
            return {"tasks": result["tasks"]}
        else:
            raise HTTPException(status_code=400, detail=result["message"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")