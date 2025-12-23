# Todo AI Chatbot - Setup Instructions

This document provides comprehensive setup instructions for the Todo AI Chatbot application.

## Prerequisites

Before setting up the application, ensure you have the following installed:

### Backend Requirements
- Python 3.9 or higher
- pip (Python package installer)
- Virtual environment tool (venv, virtualenv, or conda)
- PostgreSQL 12 or higher
- Git

### Frontend Requirements
- Node.js 18 or higher
- npm or yarn package manager

### Optional (for deployment)
- Docker and Docker Compose
- Redis server

## Quick Setup (Recommended)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd todo-ai-chatbot
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Or if using Poetry:
poetry install
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# Or if using yarn:
yarn install
```

### 4. Database Setup
```bash
# Navigate to backend directory
cd backend

# Create database tables (if using SQLModel/SQLAlchemy)
alembic upgrade head
```

### 5. Environment Configuration
```bash
# Copy environment example file
cp .env.example .env

# Edit the .env file with your configuration
# See Environment Variables section below
```

## Detailed Setup

### Backend Setup in Detail

#### 1. Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

#### 2. Install Backend Dependencies
```bash
# Using pip
pip install -r requirements.txt

# Or using Poetry (if available)
poetry install

# Or install dependencies manually
pip install fastapi uvicorn sqlmodel python-multipart python-jose[cryptography] passlib[bcrypt] asyncpg redis python-socketio python-dotenv
```

#### 3. Database Setup
Choose one of the following database options:

**Option A: PostgreSQL (Production)**
1. Install PostgreSQL
2. Create a database: `CREATE DATABASE todo_chatbot;`
3. Update DATABASE_URL in .env file
4. Run migrations: `alembic upgrade head`

**Option B: SQLite (Development)**
1. No installation needed
2. Update DATABASE_URL in .env file to: `sqlite:///./todo_chatbot.db`

### Frontend Setup in Detail

#### 1. Install Node.js Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Or using yarn
yarn install
```

#### 2. Frontend Environment Variables
Create a `.env` file in the frontend directory:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TITLE=Todo AI Chatbot
```

### MCP Server Setup
If using MCP servers:
```bash
# Navigate to MCP servers directory
cd mcp_servers

# Install MCP dependencies
pip install mcp
```

## Environment Variables

Create `.env` files in both backend and frontend directories:

### Backend .env
```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_chatbot

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# JWT
JWT_SECRET_KEY=your_jwt_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=Todo AI Chatbot
APP_VERSION=1.0.0
DEBUG=true

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Redis (for caching and sessions)
REDIS_URL=redis://localhost:6379/0

# Email configuration (optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# MCP Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=3001

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

### Frontend .env
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_TITLE=Todo AI Chatbot
REACT_APP_DEBUG=false
```

## Running the Application

### Development Mode

#### Backend
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Navigate to backend directory
cd backend

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using poetry
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
# Navigate to frontend directory
cd frontend

# Start development server
npm start
# Or using yarn
yarn start
```

### Production Mode

#### Backend
```bash
# Navigate to backend directory
cd backend

# Run with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000

# Or using gunicorn (for production)
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

#### Frontend
```bash
# Navigate to frontend directory
cd frontend

# Build for production
npm run build

# Serve build files
npx serve -s build
```

### Docker Setup
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

## Database Migrations

### Setting up Alembic (if using SQLAlchemy)
```bash
# Initialize alembic (first time only)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Downgrade migrations
alembic downgrade -1
```

## Testing

### Backend Tests
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_module.py

# Run tests with verbose output
pytest -v
```

### Frontend Tests
```bash
# Run all tests
npm test

# Run tests once
npm test -- --watchAll=false

# Run tests with coverage
npm test -- --coverage
```

## Development Tools

### Code Formatting
```bash
# Format Python code with Black
black .

# Sort imports with isort
isort .

# Format JavaScript/TypeScript with Prettier
npm run format
```

### Linting
```bash
# Python linting
flake8 .
mypy .

# JavaScript/TypeScript linting
npm run lint
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Check if another process is using the port: `lsof -i :8000` (macOS/Linux) or `netstat -ano | findstr :8000` (Windows)
   - Kill the process or use a different port

2. **Database connection errors**
   - Verify PostgreSQL is running
   - Check DATABASE_URL in .env file
   - Ensure database exists and user has permissions

3. **Missing dependencies**
   - Activate virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **Frontend build errors**
   - Clear node_modules: `rm -rf node_modules package-lock.json` then `npm install`
   - Check Node.js version compatibility

### Debugging Tips
- Set `DEBUG=true` in environment for detailed error messages
- Check logs in console and log files
- Use browser developer tools for frontend issues
- Verify API endpoints using tools like Postman

## Next Steps

After successful setup:

1. Run the application in development mode
2. Access the API documentation at `http://localhost:8000/docs`
3. Set up your OpenAI API key for AI features
4. Configure authentication for production use
5. Set up monitoring and logging for production
6. Review security settings before production deployment