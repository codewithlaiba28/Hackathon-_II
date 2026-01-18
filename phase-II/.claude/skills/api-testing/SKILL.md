---
name: api-testing
description: |
  This skill creates comprehensive tests for FastAPI endpoints including authentication, CRUD operations, and error handling. Use this skill when you need to implement thorough testing for your FastAPI API endpoints.
---

# API Testing Skill

This skill should be used when users need to create comprehensive tests for FastAPI endpoints including authentication, CRUD operations, and error handling.

## Skill Type: Automation

## Domain: API Testing with FastAPI and Pytest

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing API endpoints, authentication system, models, and schemas |
| **Conversation** | User's specific testing requirements, coverage needs, and CI/CD constraints |
| **Skill References** | FastAPI testing documentation, Pytest best practices, test patterns |
| **User Guidelines** | Project-specific testing conventions, coverage thresholds, reporting requirements |

Ensure all required context is gathered before implementing.

## Core Concepts

API testing involves:
- Unit testing individual endpoint functions
- Integration testing of full request/response cycles
- Authentication and authorization testing
- Error handling verification
- Data validation testing
- Performance and load considerations

## Testing Workflow

The API testing process follows these steps:
1. Set up test database and fixtures
2. Create test clients for API interaction
3. Write tests for each endpoint
4. Verify authentication and authorization
5. Test error conditions and edge cases
6. Run tests and analyze results

## Implementation Steps

### 1. Setup Test Environment

First, create the test environment configuration:

```python
# backend/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool
from backend.main import app
from backend.db import get_session
from backend.models import User, Task
from unittest.mock import patch
from datetime import datetime

# Create an in-memory SQLite database for testing
@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    yield engine

@pytest.fixture(name="client")
def client_fixture(engine):
    def get_test_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpassword123"
    }

@pytest.fixture
def test_task():
    return {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending",
        "priority": "medium"
    }
```

### 2. Create Authentication Test Helpers

Create utilities for authentication testing:

```python
# backend/test_auth_helpers.py
from fastapi.testclient import TestClient
from backend.models import User
from backend.db import get_session
from sqlmodel import Session
from passlib.context import CryptContext
import pytest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_test_user(client: TestClient, user_data: dict) -> User:
    """Create a test user and return the user object"""
    from backend.models import UserCreate
    from backend.db import get_session
    from sqlmodel import Session

    # Hash the password
    hashed_password = pwd_context.hash(user_data["password"])

    # Create user in database
    with Session(get_session().bind) as session:
        user = User(
            email=user_data["email"],
            name=user_data["name"],
            hashed_password=hashed_password
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_auth_token(client: TestClient, email: str, password: str) -> str:
    """Get authentication token for a user"""
    response = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    return response.json()["access_token"]
```

### 3. Write Authentication Tests

Create comprehensive authentication tests:

```python
# backend/tests/test_auth.py
from fastapi.testclient import TestClient
import pytest
from backend.models import User

def test_user_registration(client: TestClient):
    """Test user registration endpoint"""
    user_data = {
        "email": "newuser@example.com",
        "name": "New User",
        "password": "securepassword123"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["name"] == user_data["name"]
    assert "id" in data
    assert "hashed_password" not in data  # Should not expose hashed password

def test_user_login_success(client: TestClient, test_user):
    """Test successful user login"""
    # First create the user
    client.post("/api/auth/register", json=test_user)

    # Then try to login
    login_data = {
        "email": test_user["email"],
        "password": test_user["password"]
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_user_login_invalid_credentials(client: TestClient, test_user):
    """Test login with invalid credentials"""
    # First create the user
    client.post("/api/auth/register", json=test_user)

    # Try to login with wrong password
    login_data = {
        "email": test_user["email"],
        "password": "wrongpassword"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401

def test_get_current_user(client: TestClient, test_user):
    """Test getting current user with valid token"""
    # Create and login user
    client.post("/api/auth/register", json=test_user)
    token = get_auth_token(client, test_user["email"], test_user["password"])

    # Get current user
    response = client.get("/api/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["name"] == test_user["name"]

def test_get_current_user_invalid_token(client: TestClient):
    """Test getting current user with invalid token"""
    response = client.get("/api/auth/me", headers={
        "Authorization": "Bearer invalidtoken"
    })
    assert response.status_code == 401
```

### 4. Write CRUD Operation Tests

Create comprehensive CRUD tests for your resources:

```python
# backend/tests/test_tasks.py
from fastapi.testclient import TestClient
import pytest

def test_create_task(client: TestClient, test_user, test_task):
    """Test creating a new task"""
    # Create and login user
    client.post("/api/auth/register", json=test_user)
    token = get_auth_token(client, test_user["email"], test_user["password"])

    response = client.post(
        "/api/tasks",
        json=test_task,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == test_task["title"]
    assert data["description"] == test_task["description"]
    assert data["status"] == test_task["status"]
    assert data["priority"] == test_task["priority"]
    assert "id" in data
    assert "user_id" in data

def test_get_tasks(client: TestClient, test_user, test_task):
    """Test getting all tasks for a user"""
    # Create and login user
    client.post("/api/auth/register", json=test_user)
    token = get_auth_token(client, test_user["email"], test_user["password"])

    # Create a task
    client.post(
        "/api/tasks",
        json=test_task,
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get all tasks
    response = client.get("/api/tasks", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == test_task["title"]

def test_get_task_by_id(client: TestClient, test_user, test_task):
    """Test getting a specific task by ID"""
    # Create and login user
    client.post("/api/auth/register", json=test_user)
    token = get_auth_token(client, test_user["email"], test_user["password"])

    # Create a task and get its ID
    response = client.post(
        "/api/tasks",
        json=test_task,
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = response.json()["id"]

    # Get the specific task
    response = client.get(f"/api/tasks/{task_id}", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == test_task["title"]

def test_update_task(client: TestClient, test_user, test_task):
    """Test updating an existing task"""
    # Create and login user
    client.post("/api/auth/register", json=test_user)
    token = get_auth_token(client, test_user["email"], test_user["password"])

    # Create a task and get its ID
    response = client.post(
        "/api/tasks",
        json=test_task,
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Task Title",
        "status": "completed"
    }

    response = client.put(
        f"/api/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["status"] == update_data["status"]

def test_delete_task(client: TestClient, test_user, test_task):
    """Test deleting a task"""
    # Create and login user
    client.post("/api/auth/register", json=test_user)
    token = get_auth_token(client, test_user["email"], test_user["password"])

    # Create a task and get its ID
    response = client.post(
        "/api/tasks",
        json=test_task,
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = response.json()["id"]

    # Delete the task
    response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Verify the task is deleted
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404

def test_task_authorization(client: TestClient, test_user):
    """Test that users can only access their own tasks"""
    # Create first user and task
    user1_data = {**test_user, "email": "user1@example.com"}
    client.post("/api/auth/register", json=user1_data)
    token1 = get_auth_token(client, user1_data["email"], user1_data["password"])

    task_data = {
        "title": "User 1's Task",
        "description": "This belongs to user 1",
        "status": "pending",
        "priority": "medium"
    }

    response = client.post(
        "/api/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token1}"}
    )
    task_id = response.json()["id"]
    assert response.status_code == 200

    # Create second user
    user2_data = {**test_user, "email": "user2@example.com"}
    client.post("/api/auth/register", json=user2_data)
    token2 = get_auth_token(client, user2_data["email"], user2_data["password"])

    # Try to access user1's task with user2's token
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 404  # Should not find the task
```

### 5. Write Error Handling Tests

Create tests for error conditions:

```python
# backend/tests/test_error_handling.py
from fastapi.testclient import TestClient

def test_invalid_input_validation(client: TestClient, test_user):
    """Test validation of invalid input data"""
    # Create and login user
    client.post("/api/auth/register", json=test_user)
    token = get_auth_token(client, test_user["email"], test_user["password"])

    # Try to create a task with invalid data
    invalid_task = {
        "title": "",  # Empty title should fail validation
        "description": "Valid description",
        "status": "invalid_status",  # Invalid status
        "priority": "medium"
    }

    response = client.post(
        "/api/tasks",
        json=invalid_task,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Validation error

def test_nonexistent_task_access(client: TestClient, test_user):
    """Test accessing a non-existent task"""
    # Create and login user
    client.post("/api/auth/register", json=test_user)
    token = get_auth_token(client, test_user["email"], test_user["password"])

    # Try to access a task that doesn't exist
    fake_task_id = "nonexistent_task_id"
    response = client.get(
        f"/api/tasks/{fake_task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404

def test_unauthorized_access(client: TestClient, test_user, test_task):
    """Test accessing protected endpoints without authentication"""
    # Create a task without authentication (should fail)
    response = client.post("/api/tasks", json=test_task)
    assert response.status_code == 401  # Unauthorized

    # Try to get tasks without authentication
    response = client.get("/api/tasks")
    assert response.status_code == 401  # Unauthorized

def test_rate_limiting(client: TestClient, test_user):
    """Test rate limiting functionality (if implemented)"""
    # This would require rate limiting middleware to be in place
    # For now, just ensure the basic functionality works
    pass
```

### 6. Create Test Configuration

Set up pytest configuration:

```ini
# backend/pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -ra
    -v
    --tb=short
    --strict-markers
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    auth: marks tests related to authentication
    crud: marks tests related to CRUD operations
    error: marks tests related to error handling
```

### 7. Create Test Run Scripts

Create scripts to run different types of tests:

```bash
# backend/scripts/run_tests.sh
#!/bin/bash

# Run all tests
echo "Running all tests..."
python -m pytest tests/ -v

# Run only authentication tests
echo "Running authentication tests..."
python -m pytest tests/ -m auth -v

# Run only CRUD tests
echo "Running CRUD tests..."
python -m pytest tests/ -m crud -v

# Run with coverage
echo "Running tests with coverage..."
python -m pytest tests/ --cov=backend --cov-report=html --cov-report=term
```

### 8. Integration Testing

Create integration tests that test multiple components together:

```python
# backend/tests/test_integration.py
from fastapi.testclient import TestClient
import pytest

@pytest.mark.integration
def test_full_user_workflow(client: TestClient):
    """Test the complete user workflow: register, login, create task, update, delete"""
    # Step 1: Register user
    user_data = {
        "email": "integration@example.com",
        "name": "Integration Test User",
        "password": "integrationpassword123"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Step 2: Login user
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Step 3: Create task
    task_data = {
        "title": "Integration Test Task",
        "description": "Task created during integration test",
        "status": "pending",
        "priority": "high"
    }

    response = client.post(
        "/api/tasks",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    task_id = response.json()["id"]

    # Step 4: Get the task
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == task_id

    # Step 5: Update the task
    update_data = {
        "status": "completed",
        "priority": "low"
    }

    response = client.put(
        f"/api/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

    # Step 6: Delete the task
    response = client.delete(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Step 7: Verify task is deleted
    response = client.get(
        f"/api/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404

@pytest.mark.integration
def test_multiple_users_isolation(client: TestClient):
    """Test that multiple users have isolated data"""
    # Create first user
    user1_data = {
        "email": "user1@example.com",
        "name": "User 1",
        "password": "password123"
    }

    client.post("/api/auth/register", json=user1_data)
    token1 = get_auth_token(client, user1_data["email"], user1_data["password"])

    # Create second user
    user2_data = {
        "email": "user2@example.com",
        "name": "User 2",
        "password": "password123"
    }

    client.post("/api/auth/register", json=user2_data)
    token2 = get_auth_token(client, user2_data["email"], user2_data["password"])

    # User 1 creates a task
    task1_data = {
        "title": "User 1's Task",
        "description": "Belongs to user 1",
        "status": "pending",
        "priority": "medium"
    }

    response = client.post(
        "/api/tasks",
        json=task1_data,
        headers={"Authorization": f"Bearer {token1}"}
    )
    task1_id = response.json()["id"]
    assert response.status_code == 200

    # User 2 creates a task
    task2_data = {
        "title": "User 2's Task",
        "description": "Belongs to user 2",
        "status": "pending",
        "priority": "medium"
    }

    response = client.post(
        "/api/tasks",
        json=task2_data,
        headers={"Authorization": f"Bearer {token2}"}
    )
    task2_id = response.json()["id"]
    assert response.status_code == 200

    # User 1 should only see their own task
    response = client.get("/api/tasks", headers={
        "Authorization": f"Bearer {token1}"
    })
    user1_tasks = response.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["id"] == task1_id

    # User 2 should only see their own task
    response = client.get("/api/tasks", headers={
        "Authorization": f"Bearer {token2}"
    })
    user2_tasks = response.json()
    assert len(user2_tasks) == 1
    assert user2_tasks[0]["id"] == task2_id

    # Each user should not be able to access the other's task
    response = client.get(
        f"/api/tasks/{task2_id}",
        headers={"Authorization": f"Bearer {token1}"}
    )
    assert response.status_code == 404

    response = client.get(
        f"/api/tasks/{task1_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 404
```

## Best Practices

1. **Use fixtures** to set up common test data
2. **Test both positive and negative cases** for each endpoint
3. **Use parameterized tests** for testing multiple input variations
4. **Isolate tests** so they don't depend on each other
5. **Use appropriate test markers** to categorize tests
6. **Test authentication and authorization** for all protected endpoints
7. **Verify data integrity** after operations
8. **Test error responses** have appropriate status codes and messages

## Test Coverage Checklist

- [ ] Authentication endpoints tested (register, login, logout)
- [ ] CRUD operations tested for all resources
- [ ] Authorization tested (users can only access their own data)
- [ ] Input validation tested (both valid and invalid inputs)
- [ ] Error handling tested (404, 401, 422, etc.)
- [ ] Integration tests cover complete workflows
- [ ] Edge cases tested (empty inputs, maximum lengths, etc.)
- [ ] Database transaction tests (rollbacks, etc.)

## Running Tests

```bash
# Run all tests
pytest

# Run tests with specific markers
pytest -m auth  # Run only authentication tests
pytest -m crud  # Run only CRUD tests
pytest -m integration  # Run only integration tests

# Run tests with coverage
pytest --cov=backend --cov-report=html

# Run tests in parallel (if you have pytest-xdist installed)
pytest -n auto
```

This skill provides a comprehensive approach to API testing for FastAPI applications, ensuring thorough testing of authentication, CRUD operations, and error handling scenarios.