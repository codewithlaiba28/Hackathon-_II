# Data Model: AI Todo Chatbot

## Task Entity

**Fields:**
- id: UUID (Primary Key, auto-generated)
- title: String (required, max 255 characters)
- description: String (optional, max 1000 characters)
- completed: Boolean (default: false)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated)
- user_id: UUID (Foreign Key to User, required)
- conversation_id: UUID (Foreign Key to Conversation, required)

**Validation Rules:**
- Title must not be empty
- Title length must be 1-255 characters
- User must exist
- Conversation must exist

**State Transitions:**
- Created with completed=false
- Can transition to completed=true via complete_task operation
- Can transition back to completed=false if needed
- Can be deleted via delete_task operation

## Conversation Entity

**Fields:**
- id: UUID (Primary Key, auto-generated)
- user_id: UUID (Foreign Key to User, required)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated)
- title: String (optional, auto-generated from first message, max 255 characters)
- is_active: Boolean (default: true)

**Validation Rules:**
- User must exist
- Title length must be 0-255 characters if provided

## Message Entity

**Fields:**
- id: UUID (Primary Key, auto-generated)
- conversation_id: UUID (Foreign Key to Conversation, required)
- role: String (required, values: "user", "assistant", "system")
- content: String (required, max 10000 characters)
- timestamp: DateTime (auto-generated)
- tool_calls: JSON (optional, for storing MCP tool calls)
- tool_call_results: JSON (optional, for storing MCP tool results)

**Validation Rules:**
- Conversation must exist
- Role must be one of allowed values
- Content must not be empty

## User Entity

**Fields:**
- id: UUID (Primary Key, auto-generated)
- email: String (required, unique, max 255 characters)
- name: String (optional, max 255 characters)
- created_at: DateTime (auto-generated)
- updated_at: DateTime (auto-generated)
- auth_provider_id: String (optional, for Better Auth integration)

**Validation Rules:**
- Email must be valid email format
- Email must be unique
- Email length must be 1-255 characters

## Relationships

**User → Conversation:**
- One-to-many (User can have multiple conversations)
- Cascade delete: Conversations are deleted when user is deleted

**Conversation → Task:**
- One-to-many (Conversation can have multiple tasks)
- Cascade delete: Tasks are deleted when conversation is deleted

**Conversation → Message:**
- One-to-many (Conversation can have multiple messages)
- Cascade delete: Messages are deleted when conversation is deleted

## Indexes

**Task:**
- Index on user_id for efficient user task queries
- Index on conversation_id for efficient conversation task queries
- Composite index on (user_id, completed) for efficient task listing

**Conversation:**
- Index on user_id for efficient user conversation queries
- Index on is_active for efficient active conversation queries

**Message:**
- Index on conversation_id for efficient conversation message queries
- Index on timestamp for chronological message ordering