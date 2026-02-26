# Task API Contracts for Advanced Features

## Enhanced Task Endpoints

### GET /api/{user_id}/tasks
**Purpose**: Retrieve tasks with advanced filtering and sorting capabilities

**Query Parameters**:
- `priority` (optional): Filter by priority level (low, medium, high, urgent)
- `tag` (optional): Filter by tag (can be used multiple times for AND logic)
- `status` (optional): Filter by status (pending, completed, in-progress)
- `due_date_from` (optional): Filter tasks with due date after this date
- `due_date_to` (optional): Filter tasks with due date before this date
- `search` (optional): Full-text search across title, description, and tags
- `sort_by` (optional): Sort field (due_date, priority, created_at, title, status)
- `order` (optional): Sort order (asc, desc) - default: asc
- `page` (optional): Page number for pagination - default: 1
- `limit` (optional): Number of items per page - default: 20, max: 100

**Response**:
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user-123",
      "title": "Complete project proposal",
      "description": "Finish the project proposal document",
      "status": "pending",
      "priority": "high",
      "due_date": "2026-02-15T10:00:00Z",
      "reminder_offset_minutes": 60,
      "is_recurring": true,
      "recurrence_pattern": "weekly",
      "parent_recurring_task_id": null,
      "tags": ["work", "important"],
      "created_at": "2026-02-10T08:00:00Z",
      "updated_at": "2026-02-10T08:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "has_next": true,
    "has_prev": false
  }
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized
- 403: Forbidden (trying to access other user's tasks)

### POST /api/{user_id}/tasks
**Purpose**: Create a new task with advanced features

**Request Body**:
```json
{
  "title": "Team meeting",
  "description": "Weekly team sync meeting",
  "priority": "medium",
  "due_date": "2026-02-12T14:00:00Z",
  "reminder_offset_minutes": 30,
  "is_recurring": true,
  "recurrence_pattern": "weekly",
  "recurrence_end_date": "2026-12-31T23:59:59Z",
  "tags": ["work", "meeting", "team"]
}
```

**Response**:
```json
{
  "id": 1,
  "user_id": "user-123",
  "title": "Team meeting",
  "description": "Weekly team sync meeting",
  "status": "pending",
  "priority": "medium",
  "due_date": "2026-02-12T14:00:00Z",
  "reminder_offset_minutes": 30,
  "is_recurring": true,
  "recurrence_pattern": "weekly",
  "recurrence_end_date": "2026-12-31T23:59:59Z",
  "parent_recurring_task_id": null,
  "tags": ["work", "meeting", "team"],
  "created_at": "2026-02-10T09:00:00Z",
  "updated_at": "2026-02-10T09:00:00Z"
}
```

**Status Codes**:
- 201: Created
- 400: Invalid request data
- 401: Unauthorized

### PUT /api/{user_id}/tasks/{task_id}
**Purpose**: Update an existing task with advanced features

**Request Body** (partial updates allowed):
```json
{
  "title": "Updated team meeting",
  "priority": "high",
  "due_date": "2026-02-13T15:00:00Z",
  "tags": ["work", "meeting", "urgent"],
  "recurrence_pattern": "daily"
}
```

**Response**:
```json
{
  "id": 1,
  "user_id": "user-123",
  "title": "Updated team meeting",
  "description": "Weekly team sync meeting",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-02-13T15:00:00Z",
  "reminder_offset_minutes": 30,
  "is_recurring": true,
  "recurrence_pattern": "daily",
  "recurrence_end_date": "2026-12-31T23:59:59Z",
  "parent_recurring_task_id": null,
  "tags": ["work", "meeting", "urgent"],
  "created_at": "2026-02-10T09:00:00Z",
  "updated_at": "2026-02-10T10:00:00Z"
}
```

**Status Codes**:
- 200: Updated
- 400: Invalid request data
- 401: Unauthorized
- 404: Task not found

### POST /api/{user_id}/tasks/search
**Purpose**: Search tasks with full-text search and advanced filtering

**Request Body**:
```json
{
  "query": "project",
  "filters": {
    "priority": ["high", "urgent"],
    "status": ["pending"],
    "due_date_range": {
      "from": "2026-02-01T00:00:00Z",
      "to": "2026-02-28T23:59:59Z"
    },
    "tags": ["work"]
  },
  "sort_by": "due_date",
  "order": "asc",
  "page": 1,
  "limit": 20
}
```

**Response**:
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user-123",
      "title": "Complete project proposal",
      "description": "Finish the project proposal document",
      "status": "pending",
      "priority": "high",
      "due_date": "2026-02-15T10:00:00Z",
      "tags": ["work", "important"],
      "relevance_score": 0.95
    }
  ],
  "total_found": 5,
  "query_execution_time_ms": 45
}
```

**Status Codes**:
- 200: Success
- 400: Invalid search query
- 401: Unauthorized

### PUT /api/{user_id}/tasks/{task_id}/priority
**Purpose**: Update only the priority of a task

**Request Body**:
```json
{
  "priority": "urgent"
}
```

**Response**:
```json
{
  "id": 1,
  "priority": "urgent",
  "updated_at": "2026-02-10T11:00:00Z"
}
```

**Status Codes**:
- 200: Success
- 400: Invalid priority value
- 401: Unauthorized
- 404: Task not found

### PUT /api/{user_id}/tasks/{task_id}/tags
**Purpose**: Update only the tags of a task

**Request Body**:
```json
{
  "tags": ["work", "important", "deadline"]
}
```

**Response**:
```json
{
  "id": 1,
  "tags": ["work", "important", "deadline"],
  "updated_at": "2026-02-10T11:00:00Z"
}
```

**Status Codes**:
- 200: Success
- 400: Invalid tags
- 401: Unauthorized
- 404: Task not found

### GET /api/{user_id}/tasks/overdue
**Purpose**: Get all overdue tasks for the user

**Query Parameters**:
- `include_today` (optional): Include tasks due today (default: false)

**Response**:
```json
{
  "overdue_tasks": [
    {
      "id": 1,
      "title": "Submit report",
      "due_date": "2026-02-09T17:00:00Z",
      "priority": "high",
      "tags": ["work", "report"]
    }
  ]
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized

### GET /api/{user_id}/tasks/upcoming
**Purpose**: Get upcoming tasks for the next week/month

**Query Parameters**:
- `period` (optional): "week", "month" (default: week)

**Response**:
```json
{
  "upcoming_tasks": [
    {
      "id": 2,
      "title": "Team meeting",
      "due_date": "2026-02-12T14:00:00Z",
      "priority": "medium",
      "tags": ["work", "meeting"]
    }
  ]
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized

## Recurring Task Endpoints

### POST /api/{user_id}/tasks/recurring
**Purpose**: Create a new recurring task

**Request Body**:
```json
{
  "title": "Daily standup",
  "description": "Daily team standup meeting",
  "priority": "medium",
  "due_time": "09:00:00", // Time of day for recurring tasks
  "recurrence_pattern": "daily",
  "recurrence_end_date": "2026-12-31T23:59:59Z",
  "tags": ["work", "meeting", "daily"]
}
```

**Response**:
```json
{
  "id": 1,
  "user_id": "user-123",
  "title": "Daily standup",
  "description": "Daily team standup meeting",
  "status": "pending",
  "priority": "medium",
  "due_date": "2026-02-11T09:00:00Z", // Next occurrence
  "is_recurring": true,
  "recurrence_pattern": "daily",
  "recurrence_end_date": "2026-12-31T23:59:59Z",
  "tags": ["work", "meeting", "daily"],
  "created_at": "2026-02-10T11:30:00Z",
  "updated_at": "2026-02-10T11:30:00Z"
}
```

**Status Codes**:
- 201: Created
- 400: Invalid recurrence pattern
- 401: Unauthorized

### PUT /api/{user_id}/tasks/{task_id}/recurrence
**Purpose**: Update recurrence settings for a recurring task

**Request Body**:
```json
{
  "recurrence_pattern": "weekly",
  "recurrence_end_date": "2026-12-31T23:59:59Z"
}
```

**Response**:
```json
{
  "id": 1,
  "recurrence_pattern": "weekly",
  "recurrence_end_date": "2026-12-31T23:59:59Z",
  "updated_at": "2026-02-10T12:00:00Z"
}
```

**Status Codes**:
- 200: Success
- 400: Invalid recurrence settings
- 401: Unauthorized
- 404: Task not found or not recurring

## Tag Management Endpoints

### GET /api/{user_id}/tags
**Purpose**: Get all tags used by the user

**Response**:
```json
{
  "tags": [
    {
      "name": "work",
      "usage_count": 25,
      "hierarchical_path": "work"
    },
    {
      "name": "meeting",
      "usage_count": 12,
      "hierarchical_path": "work.meeting"
    },
    {
      "name": "health",
      "usage_count": 8,
      "hierarchical_path": "personal.health"
    }
  ]
}
```

**Status Codes**:
- 200: Success
- 401: Unauthorized

## Error Response Format

All error responses follow this format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request data is invalid",
    "details": [
      {
        "field": "priority",
        "issue": "Value must be one of: low, medium, high, urgent"
      }
    ]
  }
}
```

## Common Headers

- **Authorization**: Bearer {jwt_token}
- **Content-Type**: application/json
- **Accept**: application/json

## Rate Limiting

- Standard endpoints: 100 requests/minute per user
- Search endpoints: 50 requests/minute per user
- Bulk operations: 10 requests/minute per user