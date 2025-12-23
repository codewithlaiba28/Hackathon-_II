# Quickstart: AI Todo Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- OpenAI API key
- Better Auth account (or local setup)

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
git clone <repository-url>
cd todo-ai-chatbot
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create `.env` file with:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot
OPENAI_API_KEY=your_openai_api_key
NEON_DATABASE_URL=your_neon_database_url
BETTER_AUTH_SECRET=your_auth_secret
```

### 3. MCP Server Setup

```bash
cd mcp_server
pip install -r requirements.txt
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

Create `.env` file with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000
```

### 5. Database Setup

Run database migrations:
```bash
cd backend
python -m src.database.migrate
```

### 6. Run Development Servers

Start MCP server:
```bash
cd mcp_server
python -m src.server
```

Start backend:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

Start frontend:
```bash
cd frontend
npm run dev
```

## Architecture Overview

The system follows a layered architecture:

1. **Frontend (ChatKit UI)**: User interface for natural language interaction
2. **Backend (FastAPI)**: Chat endpoint and agent coordination
3. **MCP Server**: Exposes task operations as MCP tools
4. **Database (Neon PostgreSQL)**: Persistent storage for tasks and conversations

## Key Components

### Agent Services
- **Conversational Agent**: Processes user messages and extracts intent
- **Task Planner Agent**: Maps intent to appropriate MCP tool calls
- **MCP Tool Agent**: Executes MCP tools for task operations
- **Memory Agent**: Handles database read/write operations
- **Error Handling Agent**: Manages validation and error responses

### MCP Tools Available
- `add_task`: Create new tasks
- `list_tasks`: Retrieve user's tasks
- `complete_task`: Mark tasks as complete
- `delete_task`: Remove tasks
- `update_task`: Modify task details

## Testing the System

Once all services are running:

1. Navigate to the frontend (usually http://localhost:3000)
2. Authenticate using Better Auth
3. Try natural language commands like:
   - "Add a task: Buy groceries"
   - "What are my tasks?"
   - "Mark 'Buy groceries' as complete"
   - "Delete the meeting task"
   - "Update my shopping task to 'Buy milk and bread'"

## Configuration

### Environment Variables

**Backend (.env):**
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: OpenAI API key for agent functionality
- `NEON_DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Secret for Better Auth integration

**Frontend (.env):**
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Better Auth URL

## Troubleshooting

### Common Issues

1. **Database Connection Issues**: Ensure PostgreSQL is running and credentials are correct
2. **MCP Server Not Responding**: Verify MCP server is running on configured port
3. **Authentication Errors**: Check Better Auth setup and environment variables
4. **OpenAI API Errors**: Verify API key and account limits

### Development Tips

- Use `--reload` flag for auto-reload during development
- Check logs on all services when debugging
- Ensure all services are running before testing