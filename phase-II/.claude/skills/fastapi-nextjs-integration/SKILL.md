---
name: fastapi-nextjs-integration
description: |
  This skill creates a comprehensive integration system between FastAPI backend and Next.js frontend with proper authentication, API routing, and data synchronization. Use this skill when you need to build full-stack applications with FastAPI and Next.js.
---

# FastAPI-Next.js Integration Skill

This skill should be used when users need to create a comprehensive integration system between FastAPI backend and Next.js frontend with proper authentication, API routing, and data synchronization.

## Skill Type: Builder

## Domain: Full-Stack Integration with FastAPI and Next.js

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, current API implementations, database schema |
| **Conversation** | User's specific requirements, constraints, preferences for data flow |
| **Skill References** | FastAPI and Next.js documentation, integration patterns, security considerations |
| **User Guidelines** | Project-specific conventions, team standards, deployment requirements |

Ensure all required context is gathered before implementing.

## Core Concepts

The FastAPI-Next.js integration involves:
- RESTful API design with FastAPI
- Next.js App Router for frontend routing
- Authentication synchronization between systems
- Database schema consistency
- CORS and security configuration
- API response normalization
- Error handling across stack

## Integration Architecture

The integration follows a microservice-like architecture where:
- FastAPI serves as the backend API server
- Next.js acts as the frontend application server
- Database layer shared between both systems
- Authentication system synchronized between frontend and backend
- API gateway patterns for request routing

## Implementation Steps

### 1. Backend Setup (FastAPI)

First, create the main FastAPI application with proper configuration:

```python
# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks, users  # Import your API routers
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI-Next.js Integration API",
    description="API for the integrated FastAPI-Next.js application",
    version="1.0.0"
)

# CORS configuration for Next.js development and production
allowed_origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://localhost:3001",  # Alternative Next.js dev server
    os.getenv("NEXT_PUBLIC_PROD_URL", ""),  # Production Next.js URL
]

# Remove empty strings from allowed_origins
allowed_origins = [origin for origin in allowed_origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "FastAPI-Next.js Integration API"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "api"}
```

### 2. Database Models and Schemas

Define consistent data models for both systems:

```python
# backend/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str

class User(UserBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

class UserRead(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    password: str

class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"  # pending, in-progress, completed
    priority: str = "medium"  # low, medium, high
    due_date: Optional[datetime] = None

class Task(TaskBase, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")

class TaskRead(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

class TaskCreate(TaskBase):
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
```

### 3. API Router Implementation

Create API endpoints with proper authentication:

```python
# backend/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from models import Task, TaskCreate, TaskRead, TaskUpdate, User
from db import get_session
from auth import get_current_user  # Assuming you have auth implemented

router = APIRouter()

@router.get("/", response_model=List[TaskRead])
def get_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    """
    tasks = session.exec(
        select(Task).where(Task.user_id == current_user.id)
    ).all()
    return tasks

@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    db_task = Task(
        **task.dict(),
        user_id=current_user.id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=TaskRead)
def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task by ID.
    """
    task = session.get(Task, task_id)
    if not task or task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.
    """
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task.
    """
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(db_task)
    session.commit()
    return {"success": True}
```

### 4. Frontend API Client Setup

Create a unified API client for Next.js:

```typescript
// frontend/lib/api-client.ts
import { getToken } from './auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

    // Get authentication token
    const token = await getToken();

    const config: RequestInit = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
    };

    console.log(`API Request: ${options.method || 'GET'} ${url}`);

    const response = await fetch(url, config);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = errorData.detail || `HTTP error! status: ${response.status}`;
      throw new Error(errorMessage);
    }

    // For DELETE requests, return success object instead of JSON
    if (options.method === 'DELETE') {
      return { success: true } as T;
    }

    return response.json();
  }

  // User endpoints
  getUsers = () => this.request<User[]>('/api/users');
  getUser = (id: string) => this.request<User>(`/api/users/${id}`);
  createUser = (userData: UserCreate) => this.request<User>('/api/users', {
    method: 'POST',
    body: JSON.stringify(userData),
  });

  // Task endpoints
  getTasks = () => this.request<Task[]>('/api/tasks');
  getTask = (id: string) => this.request<Task>(`/api/tasks/${id}`);
  createTask = (taskData: TaskCreate) => this.request<Task>('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(taskData),
  });
  updateTask = (id: string, taskData: TaskUpdate) => this.request<Task>(`/api/tasks/${id}`, {
    method: 'PUT',
    body: JSON.stringify(taskData),
  });
  deleteTask = (id: string) => this.request(`/api/tasks/${id}`, {
    method: 'DELETE',
  });
}

export const apiClient = new ApiClient();
```

### 5. Next.js Page Implementation

Create Next.js pages with proper data fetching:

```typescript
// frontend/app/tasks/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api-client';
import { Task } from '@/types/task';

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      const data = await apiClient.getTasks();
      setTasks(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-4">Loading tasks...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">My Tasks</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tasks.map((task) => (
          <div key={task.id} className="border rounded-lg p-4 shadow-sm">
            <h3 className="font-semibold">{task.title}</h3>
            <p className="text-gray-600 text-sm mt-1">{task.description}</p>
            <div className="flex justify-between items-center mt-2">
              <span className={`px-2 py-1 rounded text-xs ${
                task.status === 'completed' ? 'bg-green-100 text-green-800' :
                task.status === 'in-progress' ? 'bg-yellow-100 text-yellow-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {task.status}
              </span>
              <span className={`px-2 py-1 rounded text-xs ${
                task.priority === 'high' ? 'bg-red-100 text-red-800' :
                task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {task.priority}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 6. Environment Configuration

Set up environment variables for both systems:

```bash
# backend/.env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME="FastAPI-Next.js App"
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-nextauth-secret
```

### 7. Database Configuration

Set up database connections for both systems:

```python
# backend/db.py
from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    poolclass=StaticPool if DATABASE_URL.startswith("sqlite") else None,
)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    from models import User, Task
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)
```

### 8. Authentication Synchronization

Implement authentication that works across both systems:

```python
# backend/auth.py
import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session
from models import User
from db import get_session

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user
```

## Security Best Practices

1. **CORS Configuration**: Properly configure CORS to allow only trusted origins
2. **Authentication**: Implement secure JWT-based authentication
3. **Input Validation**: Use Pydantic models for request validation
4. **SQL Injection Prevention**: Use SQLAlchemy/SQLModel parameterized queries
5. **Environment Variables**: Store sensitive data in environment variables
6. **HTTPS**: Always use HTTPS in production environments
7. **Rate Limiting**: Implement rate limiting for API endpoints

## Error Handling Strategy

1. **Consistent Error Format**: Use consistent error response format across both systems
2. **Client-Side Error Handling**: Implement error boundaries and user-friendly messages
3. **Logging**: Log errors appropriately for debugging while protecting sensitive data
4. **Fallback Mechanisms**: Implement fallback UI states for network errors

## Testing the Integration

Create tests to verify the integration works properly:

```python
# backend/test_integration.py
import pytest
from fastapi.testclient import TestClient
from main import app
from db import create_db_and_tables, engine
from sqlmodel import SQLModel, Session

@pytest.fixture(scope="module")
def client():
    create_db_and_tables()
    with TestClient(app) as c:
        yield c

def test_api_health(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_create_task(client: TestClient):
    # This would require authentication, so we'll test with a mock token
    headers = {"Authorization": "Bearer fake-token"}
    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers=headers
    )
    # Expect 401 because token is invalid, but that's expected
    assert response.status_code in [200, 401]
```

## Validation Checklist

- [ ] FastAPI application properly configured with CORS
- [ ] Database models defined and consistent between systems
- [ ] API endpoints created with proper authentication
- [ ] Next.js API client implemented with proper error handling
- [ ] Environment variables configured for both systems
- [ ] Authentication system synchronized between frontend and backend
- [ ] Error handling implemented consistently
- [ ] Security best practices followed
- [ ] Database connection established and functional
- [ ] API endpoints tested and functional

## Deployment Considerations

1. **Production Environment**: Ensure proper environment configuration for production
2. **Database Migration**: Set up proper database migration system
3. **SSL/TLS**: Configure SSL certificates for secure connections
4. **Load Balancing**: Consider load balancing for high-traffic applications
5. **Monitoring**: Implement monitoring and logging for production systems

This skill provides a comprehensive approach to integrating FastAPI with Next.js, ensuring secure, scalable, and maintainable full-stack applications with proper data synchronization and authentication.