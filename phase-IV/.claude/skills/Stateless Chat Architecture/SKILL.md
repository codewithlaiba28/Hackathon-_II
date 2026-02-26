---
name: stateless-chat-architecture
description: Design and implement stateless conversational systems that persist state to databases, enabling horizontal scalability, resilience, and conversation resumption across server restarts
---

### Purpose
Build scalable chat systems where servers hold no state, all conversation context is stored in databases, and any server instance can handle any request.

### When to Use
- Building production chat applications
- Implementing horizontally scalable systems
- Creating resilient conversational interfaces
- Designing cloud-native chat backends

### Core Competencies

**1. Database-Backed State**
- Store conversation history in PostgreSQL
- Persist messages with roles (user/assistant)
- Manage conversation sessions
- Implement conversation resumption
- Handle concurrent updates

**2. Stateless Request Handling**
- Build stateless endpoints (POST /api/{user_id}/chat)
- Fetch context from database per request
- Construct message arrays dynamically
- Store responses immediately
- Enable horizontal scaling

**3. Session Management**
- Create unique conversation IDs
- Associate conversations with users
- Track conversation metadata
- Implement session expiration
- Handle cleanup and archival

**4. Conversation Flow**
- Receive user message
- Fetch conversation history
- Build message array for agent
- Store user message in DB
- Run agent with MCP tools
- Store assistant response
- Return response to client
- Server ready for next request (stateless)

### Implementation Guidelines

```python
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from datetime import datetime

app = FastAPI()

@app.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    # 1. Get or create conversation
    if request.conversation_id:
        conversation = db.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404)
    else:
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    
    # 2. Fetch conversation history from database
    messages = db.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    ).all()
    
    # 3. Build message array
    message_history = [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
    
    # 4. Store user message
    user_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message,
        created_at=datetime.utcnow()
    )
    db.add(user_msg)
    db.commit()
    
    # 5. Run agent with full history
    agent_response = todo_agent.run(
        messages=message_history + [
            {"role": "user", "content": request.message}
        ],
        context={"user_id": user_id}
    )
    
    # 6. Store assistant response
    assistant_msg = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=agent_response.content,
        created_at=datetime.utcnow()
    )
    db.add(assistant_msg)
    db.commit()
    
    # 7. Return response (server holds NO state)
    return {
        "conversation_id": conversation.id,
        "response": agent_response.content,
        "tool_calls": agent_response.tool_calls
    }
```

### Database Models

```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)
    role: str  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Architecture Benefits

**Scalability**
- Any server handles any request
- Horizontal scaling behind load balancer
- No sticky sessions required
- Independent scaling of components

**Resilience**
- Server restarts don't lose state
- Conversation continues after failures
- Database is single source of truth
- Automatic recovery

**Testability**
- Each request is independent
- Reproducible test scenarios
- Easy to mock database
- Clear input/output contracts

### Common Patterns
- Conversation ID in request/response
- History fetching per request
- Immediate persistence after agent run
- Optimistic UI updates on frontend
- Retry logic for database failures

### Resources
- Stateless Architecture Patterns
- Database Session Management
- Horizontal Scaling Best Practices

---