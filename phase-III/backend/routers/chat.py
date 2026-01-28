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
        todo_agent = TodoAgent(user_id=user_id, db_url=DATABASE_URL)
        full_response = ""
        
        try:
            # Send initial conversation info
            yield f"data: {json.dumps({'conversation_id': conversation.id, 'type': 'metadata'})}\n\n"
            
            async for event in todo_agent.run_streamed(chat_req.message, formatted_history):
                # The event is a StreamEvent from openai-agents
                if event.type == "raw_response_event":
                    data = event.data
                    # Handle text deltas
                    # Note: Depending on the model, it might be ResponseTextDeltaEvent or similar
                    if hasattr(data, "delta") and isinstance(data.delta, str):
                        content = data.delta
                        full_response += content
                        yield f"data: {json.dumps({'content': content, 'type': 'content'})}\n\n"
                    elif hasattr(data, "type") and data.type == "text_delta":
                        content = data.text
                        full_response += content
                        yield f"data: {json.dumps({'content': content, 'type': 'content'})}\n\n"
                    elif hasattr(data, "choices") and len(data.choices) > 0:
                        choice = data.choices[0]
                        if hasattr(choice, "delta") and hasattr(choice.delta, "content") and choice.delta.content:
                            content = choice.delta.content
                            full_response += content
                            yield f"data: {json.dumps({'content': content, 'type': 'content'})}\n\n"
                
                elif event.type == "run_item_stream_event":
                    if event.name == "tool_called":
                        # Tool call detected
                        tool_name = event.item.raw_item.name if hasattr(event.item, "raw_item") else "unknown"
                        yield f"data: {json.dumps({'tool_call': tool_name, 'type': 'tool_call'})}\n\n"

            # 5. Store assistant response when done
            # We need a new session or use the existing one carefully (async)
            # For simplicity in this generator, we use a fresh session
            from db import engine
            with Session(engine) as final_session:
                assistant_msg = Message(
                    user_id=user_id,
                    conversation_id=conversation.id,
                    role="assistant",
                    content=full_response
                )
                final_session.add(assistant_msg)
                
                # Update conversation timestamp
                db_conv = final_session.get(Conversation, conversation.id)
                if db_conv:
                    db_conv.updated_at = datetime.utcnow()
                    final_session.add(db_conv)
                
                final_session.commit()
            
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            
        except Exception as e:
            print(f"Error in stream: {e}")
            yield f"data: {json.dumps({'error': str(e), 'type': 'error'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
