from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Dict, Any
import os
from datetime import datetime

from db import engine, DATABASE_URL
from models import Conversation, Message, Task
from schemas import ChatRequest, ChatResponse
from src.custom_agents.todo_agent import TodoAgent

router = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    chat_req: ChatRequest,
    session: Session = Depends(get_session)
):
    # 1. Fetch or create conversation
    if chat_req.conversation_id:
        conversation = session.get(Conversation, chat_req.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # 2. Fetch conversation history
    history_query = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc())
    history_messages = session.exec(history_query).all()
    
    formatted_history = [
        {"role": m.role, "content": m.content}
        for m in history_messages
    ]

    # 3. Store user message in database
    user_msg = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=chat_req.message
    )
    session.add(user_msg)
    
    # 4. Run agent with MCP tools
    todo_agent = TodoAgent(user_id=user_id, db_url=DATABASE_URL)
    
    print(f"DEBUG: Starting agent run for user {user_id} with message: {chat_req.message}")
    try:
        agent_result = await todo_agent.run(chat_req.message, formatted_history)
        print(f"DEBUG: Agent run completed. Response length: {len(agent_result.get('response', ''))}")
        
        # 5. Store assistant response in database
        assistant_msg = Message(
            user_id=user_id,
            conversation_id=conversation.id,
            role="assistant",
            content=agent_result["response"]
        )
        session.add(assistant_msg)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        
        session.commit()
        
        return ChatResponse(
            conversation_id=conversation.id,
            response=agent_result["response"],
            tool_calls=agent_result["tool_calls"]
        )
        
    except Exception as e:
        session.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
