# Quickstart Guide: AI-Powered Todo Chatbot

## Overview
This guide provides instructions for setting up and running the AI-Powered Todo Chatbot locally, including all necessary components: backend API, MCP server, and frontend interface.

## Prerequisites
- Python 3.11+
- Node.js 18+ and npm/yarn
- PostgreSQL (or access to Neon PostgreSQL)
- OpenAI API key
- Better Auth compatible environment

## Environment Setup

### 1. Clone and Navigate to Repository
```bash
git clone <repository-url>
cd <repository-root>
```

### 2. Install Backend Dependencies
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
# or
yarn install
```

### 4. Set Up MCP Server Dependencies
```bash
# Navigate to MCP server directory
cd mcp-servers/todo-tools

# Activate the same virtual environment
source ../../../backend/venv/bin/activate  # On Windows: ..\..\..\backend\venv\Scripts\activate

# Install MCP server dependencies
pip install -r requirements.txt
```

## Environment Variables

### Backend (.env file in backend/)
```env
# Database Configuration
DATABASE_URL="postgresql://username:password@localhost:5432/todo_chatbot"
NEON_DATABASE_URL="your_neon_database_url_here"

# OpenAI Configuration
OPENAI_API_KEY="your_openai_api_key_here"

# Better Auth Configuration
BETTER_AUTH_SECRET="your_auth_secret_here"
BETTER_AUTH_URL="http://localhost:3000"

# JWT Configuration
JWT_SECRET="your_jwt_secret_here"
JWT_ALGORITHM="HS256"
JWT_EXPIRATION_MINUTES=1440  # 24 hours

# Application Settings
APP_ENV="development"
DEBUG=true
```

### Frontend (.env.local file in frontend/)
```env
# Backend API Configuration
NEXT_PUBLIC_BACKEND_URL="http://localhost:8000"
NEXT_PUBLIC_MCP_SERVER_URL="http://localhost:8001"

# Better Auth Configuration
NEXTAUTH_URL="http://localhost:3000"
NEXTAUTH_SECRET="your_auth_secret_here"
```

## Database Setup

### 1. Set Up PostgreSQL Database
```bash
# Using SQLModel for database setup
cd backend
source venv/bin/activate

# Create and run database migrations
python -m src.db.init_db
```

### 2. Verify Database Connection
```bash
# Run database health check
python -m src.db.health_check
```

## Running the Application

### 1. Start the MCP Server
```bash
cd mcp-servers/todo-tools
source ../../../backend/venv/bin/activate

# Start the MCP server
python -m src.main
```
Expected output: MCP server running on http://localhost:8001

### 2. Start the Backend API
```bash
cd backend
source venv/bin/activate

# Start the FastAPI backend
uvicorn src.api.main:app --reload --port 8000
```
Expected output: Server running on http://localhost:8000

### 3. Start the Frontend
```bash
cd frontend

# Start the development server
npm run dev
# or
yarn dev
```
Expected output: Frontend running on http://localhost:3000

## Testing the Setup

### 1. Verify Backend API
```bash
curl -H "Authorization: Bearer <valid_jwt_token>" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/tasks
```

### 2. Verify MCP Server
```bash
# Check MCP server health
curl http://localhost:8001/health
```

### 3. Test the Application
1. Open http://localhost:3000 in your browser
2. Authenticate using Better Auth
3. Try creating a task with natural language: "Add a task to buy groceries"
4. Verify the task appears in the task list

## Common Issues and Solutions

### Issue: Database connection fails
**Solution**:
- Verify DATABASE_URL in .env file
- Ensure PostgreSQL server is running
- Check credentials and database name

### Issue: MCP server not connecting to backend
**Solution**:
- Verify MCP server is running on correct port
- Check that backend can reach MCP server
- Confirm tool definitions are properly registered

### Issue: OpenAI API errors
**Solution**:
- Verify OPENAI_API_KEY is set correctly
- Check API key has required permissions
- Ensure sufficient quota available

### Issue: Authentication fails
**Solution**:
- Verify Better Auth configuration
- Check JWT secret matches between services
- Ensure auth middleware is properly configured

## Development Workflow

### Running Tests
```bash
# Backend tests
cd backend
source venv/bin/activate
pytest

# Frontend tests
cd frontend
npm test

# MCP server tests
cd mcp-servers/todo-tools
source ../../../backend/venv/bin/activate
pytest
```

### Code Formatting
```bash
# Backend formatting
cd backend
source venv/bin/activate
black src/
flake8 src/

# Frontend formatting
cd frontend
npm run format
```

## Production Deployment Notes

### Environment Variables for Production
```env
# Production-specific settings
APP_ENV="production"
DEBUG=false
LOG_LEVEL="INFO"

# Production database URL
DATABASE_URL="postgresql://..."

# Production OpenAI settings
OPENAI_API_KEY="..."
OPENAI_MODEL="gpt-4-turbo"  # Use more capable model in prod

# Production security
JWT_EXPIRATION_MINUTES=720   # 12 hours for production
```

### Docker Deployment (Optional)
```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.prod.yml up --build
```

## Troubleshooting Tips

1. **Check Logs**: Monitor logs for all components when troubleshooting
2. **Verify Ports**: Ensure no port conflicts between services
3. **Token Expiry**: JWT tokens expire - refresh authentication if needed
4. **Network Connectivity**: Ensure all services can communicate with each other
5. **Rate Limits**: Be aware of OpenAI API rate limits during development

## Next Steps

1. Customize the AI agent's behavior in `backend/src/agents/todo_agent.py`
2. Extend MCP tools in `mcp-servers/todo-tools/src/tools/`
3. Modify the UI components in `frontend/src/components/`
4. Add new features by extending the data models and API endpoints