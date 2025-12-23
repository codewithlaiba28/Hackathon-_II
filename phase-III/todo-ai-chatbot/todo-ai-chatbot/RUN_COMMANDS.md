# Todo AI Chatbot - Run Commands

This document provides all the necessary commands to run, test, and manage the Todo AI Chatbot application.

## Backend Commands

### Development
```bash
# Start backend server with auto-reload
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Start with specific log level
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Start with custom workers (production)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Poetry (if configured)
```bash
# Run with poetry
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests with poetry
poetry run pytest

# Run specific test
poetry run pytest tests/test_module.py
```

### Database Commands
```bash
# Run database migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Downgrade to previous migration
alembic downgrade -1

# Check current migration status
alembic current
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run tests with detailed output
pytest -v

# Run specific test file
pytest tests/test_module.py

# Run tests matching pattern
pytest -k "test_function_name"

# Run tests and generate coverage report
pytest --cov=. --cov-report=html
```

### Code Quality
```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Lint code with Flake8
flake8 .

# Type check with MyPy
mypy .

# Run all code quality checks
black . && isort . && flake8 . && mypy .
```

## Frontend Commands

### Development
```bash
# Start development server
cd frontend
npm start

# Or using yarn
yarn start
```

### Build
```bash
# Create production build
npm run build

# Create production build with analysis
npm run build --analyze

# Create development build
npm run build:dev
```

### Testing
```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests once
npm test -- --watchAll=false

# Run tests with coverage
npm test -- --coverage

# Run specific test file
npm test -- tests/Component.test.js
```

### Code Quality
```bash
# Lint code
npm run lint

# Format code with Prettier
npm run format

# Check for type errors
npm run type-check

# Run all quality checks
npm run lint && npm run format && npm run type-check
```

## Docker Commands

### Build and Run
```bash
# Build and start all services
docker-compose up --build

# Build and start in detached mode
docker-compose up --build -d

# Start without building
docker-compose up

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Individual Services
```bash
# Build only backend
docker-compose build backend

# Build only frontend
docker-compose build frontend

# Start only backend
docker-compose up backend

# Start only database
docker-compose up db
```

### Docker Management
```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs backend

# Execute command in container
docker-compose exec backend bash
```

## MCP Server Commands

### Starting MCP Servers
```bash
# Start MCP server for todo management
python -m mcp_servers.todo_management

# Start MCP server for NLP processing
python -m mcp_servers.nlp_processing

# Start all MCP servers
bash scripts/start_mcp_servers.sh
```

## Production Commands

### Deployment
```bash
# Deploy to production (example)
bash scripts/deploy.sh production

# Deploy specific environment
bash scripts/deploy.sh staging
```

### Monitoring
```bash
# Check application health
curl http://localhost:8000/health

# Monitor logs
tail -f logs/app.log

# Check resource usage
htop
# Or on macOS
top
```

### Maintenance
```bash
# Clear cache
redis-cli flushall

# Clean up old migrations
alembic history --verbose

# Backup database (PostgreSQL)
pg_dump todo_chatbot > backup.sql

# Restore database (PostgreSQL)
psql todo_chatbot < backup.sql
```

## Common Workflows

### Full Development Start
```bash
# Terminal 1: Start backend
cd backend && source venv/bin/activate && uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend && npm start

# Terminal 3: Start MCP servers (if needed)
cd mcp_servers && python -m todo_management
```

### Full Production Start (Docker)
```bash
# Build and start all services
docker-compose up --build -d

# Check if all services are running
docker-compose ps

# View application logs
docker-compose logs -f
```

### Testing Workflow
```bash
# Run all tests with coverage
pytest --cov=.

# Run frontend tests
cd frontend && npm test -- --watchAll=false

# Run backend tests
cd backend && pytest

# Run both frontend and backend tests
cd backend && pytest && cd ../frontend && npm test -- --watchAll=false
```

### Code Quality Workflow
```bash
# Before committing code
cd backend
black . && isort . && flake8 . && mypy .
cd ../frontend
npm run lint && npm run format && npm run type-check
```

### Database Workflow
```bash
# When adding new models
cd backend
alembic revision --autogenerate -m "Add new model"
alembic upgrade head

# When updating existing models
cd backend
alembic revision --autogenerate -m "Update existing model"
alembic upgrade head

# Check database status
alembic current
```

## Troubleshooting Commands

### Process Management
```bash
# Find processes using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process by PID
kill -9 PID

# Kill all Python processes
pkill -f python
```

### Environment Management
```bash
# Activate Python virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

# Deactivate virtual environment
deactivate

# Create new virtual environment
python -m venv venv

# Reinstall dependencies
pip install -r requirements.txt
```

### Git Commands
```bash
# Before starting work
git pull origin main

# After making changes
git add .
git commit -m "Brief description of changes"
git push origin feature-branch

# Check status
git status

# Check differences
git diff
```

These commands provide a comprehensive reference for running and managing the Todo AI Chatbot application in various scenarios.