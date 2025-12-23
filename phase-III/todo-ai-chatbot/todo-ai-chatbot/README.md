# Todo AI Chatbot

An AI-powered todo management system that allows users to manage tasks through natural language conversation.

## Architecture Overview

The system follows a sub-agent architecture as specified in the Phase III Design:

### Sub-Agent Architecture
- **Conversational Agent (Router)**: Handles user interaction and intent classification
- **Task Planner Agent (Orchestrator)**: Breaks down user goals into executable steps
- **Tool Execution Agent (Executor)**: Executes MCP tools safely
- **Conversation Memory Agent**: Manages conversation persistence

### Technology Stack
- **Frontend**: OpenAI ChatKit
- **Backend**: Python FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth

## Components

### MCP Tools
The system implements the following MCP tools:
- `add_task`: Create a new task
- `list_tasks`: Retrieve tasks with optional filtering
- `complete_task`: Mark a task as complete
- `delete_task`: Remove a task
- `update_task`: Modify task details

### API Endpoints
- `POST /api/{user_id}/chat`: Main chat endpoint for natural language interaction
- `GET /api/users/{user_id}/tasks`: List user's tasks

## Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL (or Neon Serverless PostgreSQL account)
- OpenAI API key

### Setup

1. Clone the repository
2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install MCP server dependencies:
   ```bash
   cd mcp_servers
   pip install -r requirements.txt
   ```

4. Create `.env` file with required environment variables:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot
   OPENAI_API_KEY=your_openai_api_key
   ```

### Running the Services

1. Start the MCP server:
   ```bash
   cd mcp_servers
   python -m uvicorn main:app --reload --port 8001
   ```

2. Start the backend API:
   ```bash
   cd backend
   python -m uvicorn main:app --reload --port 8000
   ```

## Natural Language Commands

The system supports various natural language commands:

| User Says | Agent Action |
|-----------|--------------|
| "Add a task to buy groceries" | Call add_task |
| "Show me all my tasks" | Call list_tasks with status: all |
| "What's pending?" | Call list_tasks with status: pending |
| "Mark task 3 as complete" | Call complete_task with task_id: 3 |
| "Delete the meeting task" | Call list_tasks → delete_task |
| "Change task 1 to 'Call mom tonight'" | Call update_task with new title |
| "I need to remember to pay bills" | Call add_task with title "Pay bills" |
| "What have I completed?" | Call list_tasks with status: completed |

## Features

- **Natural Language Processing**: Understands and processes natural language task management commands
- **Stateless Design**: All state is persisted in the database
- **Scalable Architecture**: Horizontally scalable with separate MCP server
- **Persistent Conversations**: Maintains conversation context across sessions
- **User Isolation**: Each user has isolated task management

## Design Principles

- **Agent-First Architecture**: Every feature starts with a designated agent responsibility
- **Stateless Design**: All application state persisted in database
- **MCP-Driven Operations**: All task operations exposed as MCP tools
- **Layered Agent Architecture**: Clear hierarchy with specific responsibilities
- **Database-First State Management**: All data stored in Neon PostgreSQL DB

## Project Structure

```
todo-ai-chatbot/
├── backend/
│   ├── models/          # Database models
│   ├── services/        # Business logic services
│   │   └── agent_services/  # Agent implementations
│   ├── api/             # API endpoints
│   └── requirements.txt # Backend dependencies
├── mcp_servers/         # MCP server implementation
│   ├── todo_management/ # Todo-specific MCP tools
│   └── requirements.txt # MCP server dependencies
├── frontend/            # Frontend implementation
└── specs/               # Specification documents
    └── phase-iii-design.md # Architecture specification
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Specify your license here]