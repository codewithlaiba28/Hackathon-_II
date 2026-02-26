# Data Model: AI-Powered Todo Chatbot

## Overview
This document defines the data models for the AI-Powered Todo Chatbot, based on the entities identified in the feature specification and requirements.

## Entity Definitions

### 1. User
**Description**: Represents an authenticated user in the system
**Fields**:
- `id` (UUID/Integer): Unique identifier for the user
- `email` (String): User's email address (unique, validated)
- `created_at` (DateTime): Timestamp when user account was created
- `updated_at` (DateTime): Timestamp when user account was last updated
- `is_active` (Boolean): Whether the user account is active

**Relationships**:
- One-to-many with Task (user has many tasks)
- One-to-many with Conversation (user has many conversations)

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Created_at and updated_at are automatically managed

### 2. Task
**Description**: Represents a todo item created by a user
**Fields**:
- `id` (UUID/Integer): Unique identifier for the task
- `user_id` (UUID/Integer): Foreign key linking to the owning user
- `description` (String): The task description text (required)
- `is_completed` (Boolean): Whether the task is marked as complete (default: False)
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated
- `completed_at` (DateTime, nullable): Timestamp when task was marked as complete

**Relationships**:
- Many-to-one with User (task belongs to one user)
- User can have many tasks

**Validation Rules**:
- Description cannot be empty or only whitespace
- User_id must reference an existing, active user
- completed_at can only be set when is_completed is True
- Task cannot be marked as incomplete after being completed (append-only for completion)

**State Transitions**:
- New task: `is_completed = False`, `completed_at = null`
- Task completed: `is_completed = True`, `completed_at = current_timestamp`
- Completed task cannot return to incomplete state

### 3. Conversation
**Description**: Represents a chat session between user and AI agent
**Fields**:
- `id` (UUID/Integer): Unique identifier for the conversation
- `user_id` (UUID/Integer): Foreign key linking to the user
- `title` (String, nullable): Auto-generated or user-provided title for the conversation
- `created_at` (DateTime): Timestamp when conversation was initiated
- `updated_at` (DateTime): Timestamp when conversation was last updated
- `is_active` (Boolean): Whether conversation is currently active (default: True)

**Relationships**:
- Many-to-one with User (conversation belongs to one user)
- One-to-many with Message (conversation has many messages)

**Validation Rules**:
- User_id must reference an existing, active user
- Title can be auto-generated from first message if not provided
- Updated_at automatically updates when new messages are added

### 4. Message
**Description**: Represents a single message in a conversation (either from user or AI)
**Fields**:
- `id` (UUID/Integer): Unique identifier for the message
- `conversation_id` (UUID/Integer): Foreign key linking to the conversation
- `sender_type` (Enum: 'user' | 'ai'): Indicates who sent the message
- `content` (Text): The message content/text
- `timestamp` (DateTime): When the message was sent/received
- `metadata` (JSON, nullable): Additional data about the message (e.g., tool calls, intent classification)

**Relationships**:
- Many-to-one with Conversation (message belongs to one conversation)
- Conversation has many messages (ordered by timestamp)

**Validation Rules**:
- Conversation_id must reference an existing, active conversation
- Sender_type must be either 'user' or 'ai'
- Content cannot be empty
- Timestamp must be within reasonable bounds

## Database Schema Relationships

```
Users (1) -----> (*) Tasks
Users (1) -----> (*) Conversations
Conversations (1) -----> (*) Messages
```

## Indexing Strategy

### Primary Indexes
- All id fields (primary keys)
- User email (unique)

### Secondary Indexes
- Tasks.user_id (foreign key, for user isolation queries)
- Tasks.created_at (for chronological sorting)
- Conversations.user_id (foreign key, for user isolation queries)
- Conversations.updated_at (for recent conversations)
- Messages.conversation_id (foreign key, for conversation retrieval)
- Messages.timestamp (for chronological ordering)

## Access Control & Isolation

### User Isolation Rules
- All queries must filter by user_id to prevent cross-user data access
- MCP tools must validate that requested operations belong to the authenticated user
- No direct access to another user's tasks or conversations is permitted

### Query Patterns
- Get user's tasks: `SELECT * FROM tasks WHERE user_id = ?`
- Get user's conversations: `SELECT * FROM conversations WHERE user_id = ?`
- Get conversation messages: `SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp`

## Data Lifecycle

### Task Lifecycle
1. User creates task → Task created with `is_completed = False`
2. User marks task complete → Task updated with `is_completed = True`, `completed_at = timestamp`
3. Task remains in user's list but marked as completed
4. User may delete task → Task soft-deleted (or permanently deleted based on requirements)

### Conversation Lifecycle
1. New chat initiated → Conversation created
2. Messages exchanged → Messages added to conversation
3. Session ends → Conversation remains for continuity
4. User returns → Same conversation resumed or new one created based on context

## Performance Considerations

### Query Optimization
- Most frequent operations: getting user's tasks, adding new tasks
- Queries should leverage indexes on user_id and timestamp fields
- Pagination for conversations with many messages

### Storage Efficiency
- Text fields should have reasonable length limits
- JSON metadata should be kept concise
- Consider archiving very old conversations if needed