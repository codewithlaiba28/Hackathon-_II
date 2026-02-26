from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Dict, Any
import os
from datetime import datetime

from db import engine, DATABASE_URL
from models import Conversation, Message, Task
from schemas import ChatRequest, ChatResponse
# Lazy import TodoAgent inside endpoints

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
    from src.custom_agents.todo_agent import TodoAgent
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

@router.post("/{user_id}/chat/stream")
async def chat_stream_endpoint(
    user_id: str,
    chat_req: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Streaming version of the chat endpoint.
    """
    from fastapi.responses import StreamingResponse
    import json
    
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

    # 2. Fetch history
    history_query = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at.asc())
    history_messages = session.exec(history_query).all()
    formatted_history = [{"role": m.role, "content": m.content} for m in history_messages]

    # 3. Store user message
    user_msg = Message(user_id=user_id, conversation_id=conversation.id, role="user", content=chat_req.message)
    session.add(user_msg)
    session.commit()

    async def event_generator():
        print(f"DEBUG: [Stream] Starting generator for user {user_id}", flush=True)
        from src.custom_agents.todo_agent import TodoAgent
        import asyncio
        
        try:
            # Send initial metadata
            yield f"data: {json.dumps({'conversation_id': conversation.id, 'type': 'metadata'})}\n\n"
            yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': datetime.utcnow().isoformat()})}\n\n"
            
            print(f"DEBUG: [Stream] Initializing TodoAgent for user {user_id}", flush=True)
            todo_agent = TodoAgent(user_id=user_id, db_url=DATABASE_URL)
            
            # Use non-streaming run() with a timeout — more reliable for tool calls
            print(f"DEBUG: [Stream] Using non-streaming run() with 90s timeout...", flush=True)
            try:
                agent_result = await asyncio.wait_for(
                    todo_agent.run(chat_req.message, formatted_history),
                    timeout=90.0
                )
                full_response = agent_result.get("response", "")
                tool_calls = agent_result.get("tool_calls", [])
                
                print(f"DEBUG: [Stream] Agent run completed. Response: {full_response[:100]}...", flush=True)
                
                # Send tool call notifications
                for tc in tool_calls:
                    yield f"data: {json.dumps({'tool_call': tc.get('name', 'unknown'), 'type': 'tool_call'})}\n\n"
                
                # Send response as content chunks (simulate streaming for frontend compatibility)
                if full_response:
                    # Send in small chunks for a streaming feel
                    chunk_size = 20
                    for i in range(0, len(full_response), chunk_size):
                        chunk = full_response[i:i+chunk_size]
                        yield f"data: {json.dumps({'content': chunk, 'type': 'content'})}\n\n"
                else:
                    yield f"data: {json.dumps({'content': 'I processed your request but had no text to display.', 'type': 'content'})}\n\n"
                    full_response = "I processed your request but had no text to display."
                    
            except asyncio.TimeoutError:
                print(f"CRITICAL ERROR: Agent timed out after 90s", flush=True)
                full_response = "Sorry, the request timed out. Please try again."
                yield f"data: {json.dumps({'content': full_response, 'type': 'content'})}\n\n"
            
            # Store assistant response
            from db import engine
            with Session(engine) as final_session:
                assistant_msg = Message(
                    user_id=user_id,
                    conversation_id=conversation.id,
                    role="assistant",
                    content=full_response
                )
                final_session.add(assistant_msg)
                
                db_conv = final_session.get(Conversation, conversation.id)
                if db_conv:
                    db_conv.updated_at = datetime.utcnow()
                    final_session.add(db_conv)
                
                final_session.commit()
                print(f"DEBUG: [Stream] Response saved to DB for conv {conversation.id}", flush=True)
            
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
        except Exception as e:
            import traceback
            print(f"CRITICAL ERROR in Stream: {str(e)}")
            traceback.print_exc()
            yield f"data: {json.dumps({'error': str(e), 'type': 'error'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
