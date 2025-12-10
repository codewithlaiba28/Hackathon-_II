# API Contracts: UI Components

## Authentication Endpoints

### POST /api/auth/login
**Description**: Authenticate user and return JWT token
- **Request**: `{ email: string, password: string }`
- **Response**: `{ token: string, user: { id, email, name } }`
- **Headers**: `Content-Type: application/json`
- **Authentication**: None (public endpoint)

### POST /api/auth/logout
**Description**: Logout user and invalidate session
- **Request**: `{ token: string }`
- **Response**: `{ success: boolean }`
- **Headers**: `Content-Type: application/json`
- **Authentication**: Required (Bearer token)

## Task Management Endpoints

### GET /api/tasks
**Description**: Get all tasks for the authenticated user
- **Response**: `{ tasks: [{ id, title, description, status, createdAt, updatedAt, userId }] }`
- **Headers**: `Authorization: Bearer {token}`
- **Authentication**: Required (Bearer token)

### POST /api/tasks
**Description**: Create a new task
- **Request**: `{ title: string, description?: string, status?: string }`
- **Response**: `{ task: { id, title, description, status, createdAt, updatedAt, userId } }`
- **Headers**: `Content-Type: application/json`, `Authorization: Bearer {token}`
- **Authentication**: Required (Bearer token)

### PUT /api/tasks/{id}
**Description**: Update an existing task
- **Request**: `{ title?: string, description?: string, status?: string }`
- **Response**: `{ task: { id, title, description, status, createdAt, updatedAt, userId } }`
- **Headers**: `Content-Type: application/json`, `Authorization: Bearer {token}`
- **Authentication**: Required (Bearer token)

### DELETE /api/tasks/{id}
**Description**: Delete a task
- **Response**: `{ success: boolean }`
- **Headers**: `Authorization: Bearer {token}`
- **Authentication**: Required (Bearer token)

## API Client Integration

### Request Format
- All requests use JSON format
- Authentication via Bearer token in Authorization header
- Error responses follow format: `{ error: string, message: string }`

### Response Format
- Success responses: `{ data?: any, message?: string }`
- Error responses: `{ error: string, message: string }`
- All dates in ISO 8601 format