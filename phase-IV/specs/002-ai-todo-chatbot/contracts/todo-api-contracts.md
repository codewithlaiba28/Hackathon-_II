# API Contracts: AI-Powered Todo Chatbot

## Overview
This document defines the API contracts for the AI-Powered Todo Chatbot, specifying the endpoints and data contracts based on the functional requirements in the feature specification.

## Authentication Contract

### JWT Token Requirements
**Header**: `Authorization: Bearer <token>`
**Claims Validation**:
- `sub`: Must contain user_id
- `exp`: Must not be expired
- `iat`: Must be valid

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Expired token or insufficient permissions

## Backend API Endpoints

### 1. Conversation Management

#### POST /api/v1/conversations/new
**Description**: Start a new conversation or resume existing
**Authentication**: Required
**Request Body**:
```json
{
  "message": "User's message to the AI",
  "conversation_id": "Optional: existing conversation ID"
}
```

**Response**:
```json
{
  "conversation_id": "UUID of the conversation",
  "response": "AI's response to the user",
  "timestamp": "ISO 8601 timestamp",
  "task_operations": [
    {
      "operation": "add|list|update|complete|delete",
      "task_id": "ID of affected task (if applicable)",
      "status": "success|partial|error"
    }
  ]
}
```

**Error Responses**:
- `400 Bad Request`: Invalid request format
- `401 Unauthorized`: Missing or invalid authentication
- `500 Internal Server Error`: AI processing failure

### 2. Task Management (Direct Endpoints)

#### GET /api/v1/tasks
**Description**: Get all tasks for the authenticated user
**Authentication**: Required
**Query Parameters**:
- `status` (optional): "all", "active", "completed" (default: "all")

**Response**:
```json
{
  "tasks": [
    {
      "id": "task UUID",
      "description": "Task description",
      "is_completed": true|false,
      "created_at": "ISO 8601 timestamp",
      "completed_at": "ISO 8601 timestamp or null"
    }
  ],
  "total_count": 5,
  "completed_count": 2
}
```

#### POST /api/v1/tasks
**Description**: Create a new task
**Authentication**: Required
**Request Body**:
```json
{
  "description": "Task description (required)"
}
```

**Response**:
```json
{
  "task": {
    "id": "new task UUID",
    "description": "Task description",
    "is_completed": false,
    "created_at": "ISO 8601 timestamp",
    "updated_at": "ISO 8601 timestamp"
  }
}
```

#### PUT /api/v1/tasks/{task_id}
**Description**: Update an existing task
**Authentication**: Required
**Path Parameter**: `task_id` (UUID)
**Request Body**:
```json
{
  "description": "New task description (optional)",
  "is_completed": true|false (optional)
}
```

**Response**:
```json
{
  "task": {
    "id": "task UUID",
    "description": "Updated task description",
    "is_completed": true|false,
    "created_at": "ISO 8601 timestamp",
    "updated_at": "ISO 8601 timestamp",
    "completed_at": "ISO 8601 timestamp or null"
  }
}
```

#### DELETE /api/v1/tasks/{task_id}
**Description**: Delete a task
**Authentication**: Required
**Path Parameter**: `task_id` (UUID)
**Response**: `204 No Content` on success

**Error Responses**:
- `404 Not Found`: Task doesn't exist or doesn't belong to user
- `400 Bad Request`: Invalid task ID format

## MCP Tool Contracts

### 1. add_task Tool
**Function Signature**:
```python
def add_task(description: str) -> dict:
    """
    Add a new task for the authenticated user

    Args:
        description: The task description

    Returns:
        dict: Contains 'success': bool, 'task_id': str, 'error': str (if failed)
    """
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "description": {
      "type": "string",
      "description": "The task description to add",
      "minLength": 1,
      "maxLength": 500
    }
  },
  "required": ["description"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "task_id": {"type": "string", "format": "uuid"},
    "error": {"type": "string"}
  },
  "required": ["success"]
}
```

### 2. list_tasks Tool
**Function Signature**:
```python
def list_tasks(status_filter: str = "all") -> dict:
    """
    List tasks for the authenticated user

    Args:
        status_filter: "all", "active", or "completed" (default: "all")

    Returns:
        dict: Contains 'tasks': list, 'total_count': int, 'error': str (if failed)
    """
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "status_filter": {
      "type": "string",
      "enum": ["all", "active", "completed"],
      "default": "all",
      "description": "Filter tasks by completion status"
    }
  }
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "tasks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string", "format": "uuid"},
          "description": {"type": "string"},
          "is_completed": {"type": "boolean"},
          "created_at": {"type": "string", "format": "date-time"},
          "completed_at": {"type": "string", "format": "date-time", "nullable": true}
        }
      }
    },
    "total_count": {"type": "integer"},
    "error": {"type": "string"}
  },
  "required": ["success", "tasks", "total_count"]
}
```

### 3. update_task Tool
**Function Signature**:
```python
def update_task(task_id: str, description: str = None, is_completed: bool = None) -> dict:
    """
    Update an existing task for the authenticated user

    Args:
        task_id: The ID of the task to update
        description: New description (optional)
        is_completed: New completion status (optional)

    Returns:
        dict: Contains 'success': bool, 'task': dict, 'error': str (if failed)
    """
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to update"
    },
    "description": {
      "type": "string",
      "minLength": 1,
      "maxLength": 500,
      "description": "New task description (optional)"
    },
    "is_completed": {
      "type": "boolean",
      "description": "New completion status (optional)"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "task": {
      "type": "object",
      "properties": {
        "id": {"type": "string", "format": "uuid"},
        "description": {"type": "string"},
        "is_completed": {"type": "boolean"},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "completed_at": {"type": "string", "format": "date-time", "nullable": true}
      }
    },
    "error": {"type": "string"}
  },
  "required": ["success"]
}
```

### 4. complete_task Tool
**Function Signature**:
```python
def complete_task(task_id: str) -> dict:
    """
    Mark a task as completed for the authenticated user

    Args:
        task_id: The ID of the task to mark as complete

    Returns:
        dict: Contains 'success': bool, 'task': dict, 'error': str (if failed)
    """
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to complete"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "task": {
      "type": "object",
      "properties": {
        "id": {"type": "string", "format": "uuid"},
        "description": {"type": "string"},
        "is_completed": {"type": "boolean"},
        "created_at": {"type": "string", "format": "date-time"},
        "updated_at": {"type": "string", "format": "date-time"},
        "completed_at": {"type": "string", "format": "date-time"}
      }
    },
    "error": {"type": "string"}
  },
  "required": ["success"]
}
```

### 5. delete_task Tool
**Function Signature**:
```python
def delete_task(task_id: str) -> dict:
    """
    Delete a task for the authenticated user

    Args:
        task_id: The ID of the task to delete

    Returns:
        dict: Contains 'success': bool, 'error': str (if failed)
    """
```

**Input Schema**:
```json
{
  "type": "object",
  "properties": {
    "task_id": {
      "type": "string",
      "format": "uuid",
      "description": "The ID of the task to delete"
    }
  },
  "required": ["task_id"]
}
```

**Output Schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "error": {"type": "string"}
  },
  "required": ["success"]
}
```

## Error Response Format
All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE_STRING",
    "message": "Human-readable error message",
    "details": "Optional detailed error information"
  }
}
```

## Validation Requirements
- All UUIDs must be valid RFC 4122 UUIDs
- All datetime strings must be in ISO 8601 format
- All text fields have appropriate length limits
- All requests must be authenticated with valid JWT
- MCP tools must validate user ownership of resources