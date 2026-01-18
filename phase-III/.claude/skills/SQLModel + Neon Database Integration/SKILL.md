---
name: sqlmodel-neon-integration
description: Design database schemas, implement CRUD operations with SQLModel ORM, connect to Neon Serverless PostgreSQL, and optimize queries for performance in production applications
---

### Purpose
Build robust data persistence layers using SQLModel with Neon's serverless PostgreSQL database for scalable, type-safe database operations.

### When to Use
- Building full-stack applications with persistent data
- Implementing multi-user systems with relational data
- Creating APIs that need database storage
- Deploying serverless applications with database needs

### Core Competencies

**1. Database Schema Design**
- Define SQLModel models for tasks, conversations, messages
- Set up foreign key relationships
- Create indexes for query optimization
- Implement timestamps and metadata
- Handle nullable fields correctly

**2. CRUD Operations**
- Create records with proper validation
- Read records with filtering and sorting
- Update records with partial updates
- Delete records (soft vs hard deletes)
- Handle transactions correctly

**3. Neon Connection Management**
- Configure connection strings
- Set up connection pooling
- Handle connection retries
- Implement health checks
- Manage environment variables

**4. Query Optimization**
- Use indexes effectively
- Implement pagination
- Optimize JOIN operations
- Cache frequently accessed data
- Monitor query performance

**5. Migrations**
- Create database migrations
- Version control schema changes
- Handle migration rollbacks
- Seed initial data
- Manage production deployments

### Implementation Guidelines

**Database Models**

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """User table managed by Better Auth."""
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
    conversations: list["Conversation"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    """Todo task model."""
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: User = Relationship(back_populates="tasks")

class Conversation(SQLModel, table=True):
    """Chat conversation session."""
    __tablename__ = "conversations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: User = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    """Chat message in a conversation."""
    __tablename__ = "messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    role: str = Field(regex="^(user|assistant)$")  # "user" or "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

**Database Connection**

```python
from sqlmodel import create_engine, Session, SQLModel
import os

# Get connection string from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,  # Connection pool size
    max_overflow=10  # Max overflow connections
)

def create_db_and_tables():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for FastAPI to get database session."""
    with Session(engine) as session:
        yield session
```

**CRUD Operations**

```python
from sqlmodel import Session, select
from fastapi import Depends

class TaskService:
    """Service layer for task operations."""
    
    def create_task(
        self,
        user_id: str,
        title: str,
        description: str | None,
        db: Session
    ) -> Task:
        """Create a new task."""
        task = Task(
            user_id=user_id,
            title=title,
            description=description
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    def get_tasks(
        self,
        user_id: str,
        status: str,
        db: Session
    ) -> list[Task]:
        """Get tasks filtered by status."""
        statement = select(Task).where(Task.user_id == user_id)
        
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)
        # status == "all" returns everything
        
        statement = statement.order_by(Task.created_at.desc())
        
        tasks = db.exec(statement).all()
        return tasks
    
    def update_task(
        self,
        user_id: str,
        task_id: int,
        title: str | None,
        description: str | None,
        db: Session
    ) -> Task | None:
        """Update task details."""
        task = db.get(Task, task_id)
        
        if not task or task.user_id != user_id:
            return None
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        
        task.updated_at = datetime.utcnow()
        
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    def complete_task(
        self,
        user_id: str,
        task_id: int,
        db: Session
    ) -> Task | None:
        """Mark task as complete."""
        task = db.get(Task, task_id)
        
        if not task or task.user_id != user_id:
            return None
        
        task.completed = True
        task.updated_at = datetime.utcnow()
        
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    def delete_task(
        self,
        user_id: str,
        task_id: int,
        db: Session
    ) -> bool:
        """Delete a task."""
        task = db.get(Task, task_id)
        
        if not task or task.user_id != user_id:
            return False
        
        db.delete(task)
        db.commit()
        return True
```

**FastAPI Integration**

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/api/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    status: str = "all",
    db: Session = Depends(get_session),
    auth: dict = Depends(verify_token)
):
    """Get user's tasks."""
    if auth["user_id"] != user_id:
        raise HTTPException(status_code=403)
    
    service = TaskService()
    tasks = service.get_tasks(user_id, status, db)
    return tasks

@app.post("/api/{user_id}/tasks")
async def create_task(
    user_id: str,
    request: TaskCreate,
    db: Session = Depends(get_session),
    auth: dict = Depends(verify_token)
):
    """Create a new task."""
    if auth["user_id"] != user_id:
        raise HTTPException(status_code=403)
    
    service = TaskService()
    task = service.create_task(
        user_id,
        request.title,
        request.description,
        db
    )
    return task
```

### Neon Configuration

**Environment Variables**

```bash
# .env
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require

# For Neon serverless, the connection string format is:
# postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require
```

**Connection Pooling Best Practices**

```python
# For serverless environments (Vercel, AWS Lambda)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=1,  # Small pool for serverless
    max_overflow=0,  # No overflow in serverless
    connect_args={
        "sslmode": "require",
        "connect_timeout": 10
    }
)

# For traditional servers (always-on)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600  # Recycle connections every hour
)
```

### Common Patterns

**Pagination**
```python
def get_tasks_paginated(
    user_id: str,
    page: int,
    page_size: int,
    db: Session
) -> tuple[list[Task], int]:
    """Get paginated tasks."""
    offset = (page - 1) * page_size
    
    statement = (
        select(Task)
        .where(Task.user_id == user_id)
        .offset(offset)
        .limit(page_size)
    )
    
    tasks = db.exec(statement).all()
    
    # Get total count
    count_statement = select(Task).where(Task.user_id == user_id)
    total = len(db.exec(count_statement).all())
    
    return tasks, total
```

**Soft Deletes**
```python
class Task(SQLModel, table=True):
    # ... other fields
    deleted_at: Optional[datetime] = None

def soft_delete_task(task_id: int, db: Session):
    task = db.get(Task, task_id)
    task.deleted_at = datetime.utcnow()
    db.add(task)
    db.commit()

# Exclude deleted tasks in queries
statement = select(Task).where(
    Task.user_id == user_id,
    Task.deleted_at == None
)
```

### Resources
- SQLModel Documentation
- Neon Database Guide
- PostgreSQL Best Practices

---