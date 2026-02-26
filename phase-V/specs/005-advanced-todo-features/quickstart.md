# Advanced Todo Features Quickstart Guide

## Overview
This guide provides a quick introduction to implementing and using the advanced features in the Todo application: recurring tasks, due dates & reminders, priorities & tags, and search & filtering.

## Prerequisites
- Python 3.11+ with uv installed
- Node.js 18+ for frontend development
- Docker and Docker Compose
- Minikube or access to a Kubernetes cluster
- Dapr installed and initialized
- Kafka cluster (local or managed)

## Local Development Setup

### 1. Clone and Initialize the Project
```bash
git clone <repository-url>
cd <project-directory>
cd backend
uv venv  # Create virtual environment
source .venv/bin/activate  # Activate virtual environment (Linux/Mac) or venv\Scripts\Activate.ps1 (Windows)
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
SECRET_KEY=your-secret-key-here
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001
KAFKA_BROKERS=localhost:9092
OPENAI_API_KEY=your-openai-api-key
```

### 3. Database Setup
```bash
# Run database migrations to add new fields
cd backend
python -m db migrate
```

### 4. Dapr Setup
```bash
# Initialize Dapr (if not already done)
dapr init

# Run the application with Dapr
dapr run --app-id todo-backend --app-port 8000 -- uvicorn main:app --reload
```

### 5. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```

## Key Feature Implementation

### 1. Enhanced Task Model
The task model has been extended with new fields:

```python
# In models.py
class Task(SQLModel, table=True):
    # ... existing fields ...
    priority: str = Field(default="medium")  # low, medium, high, urgent
    due_date: Optional[datetime] = Field(default=None)
    reminder_offset_minutes: Optional[int] = Field(default=None)
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None)  # daily, weekly, monthly, custom cron
    recurrence_end_date: Optional[datetime] = Field(default=None)
    parent_recurring_task_id: Optional[int] = Field(default=None, foreign_key="task.id")

    # Relationship for tags
    tags: List["TaskTag"] = Relationship(back_populates="task")
```

### 2. Creating a Recurring Task
```python
# Example API call to create a recurring task
POST /api/{user_id}/tasks
{
  "title": "Daily exercise",
  "description": "Go for a 30-minute run",
  "priority": "medium",
  "is_recurring": true,
  "recurrence_pattern": "daily",
  "recurrence_end_date": "2026-12-31T23:59:59Z",
  "tags": ["health", "fitness"]
}
```

### 3. Setting Due Dates and Reminders
```python
# Example API call to set due date and reminder
PUT /api/{user_id}/tasks/{task_id}
{
  "due_date": "2026-02-15T10:00:00Z",
  "reminder_offset_minutes": 60  # Send reminder 1 hour before due time
}
```

### 4. Using Priority and Tagging
```python
# Example API call to update priority and tags
PUT /api/{user_id}/tasks/{task_id}
{
  "priority": "high",
  "tags": ["work", "important", "deadline"]
}
```

### 5. Advanced Search and Filtering
```python
# Example API call for advanced search
POST /api/{user_id}/tasks/search
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
  "order": "asc"
}
```

## Kafka Event Processing

### Setting up Kafka Topics
```bash
# Create required Kafka topics
kafka-topics --create --topic task-events --bootstrap-server localhost:9092
kafka-topics --create --topic task-reminders --bootstrap-server localhost:9092
kafka-topics --create --topic task-recurring --bootstrap-server localhost:9092
kafka-topics --create --topic task-search-index --bootstrap-server localhost:9092
```

### Event Producer Example (using Dapr)
```python
import httpx

# Publish task event via Dapr
async def publish_task_event(task_data, event_type):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"http://localhost:3500/v1.0/publish/kafka-pubsub/task-{event_type}",
            json={
                "event_type": event_type,
                "task_id": task_data["id"],
                "user_id": task_data["user_id"],
                "data": task_data,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```

## Dapr Integration

### Dapr Components Configuration
Place these files in the `dapr/components` directory:

**pubsub.yaml**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "localhost:9092"
  - name: consumerGroup
    value: "todo-service"
```

**statestore.yaml**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgresql-state
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "postgresql://user:password@localhost:5432/todo_db"
```

## MCP Tool Updates

### Enhanced MCP Tools
The MCP tools have been updated to support new features:

```python
# Example enhanced add_task tool
async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    is_recurring: bool = False,
    recurrence_pattern: Optional[str] = None
) -> Dict:
    # Implementation using Dapr for event publishing
    # ...
```

## Running the Services

### Local Development
```bash
# Terminal 1: Start Dapr with the backend
cd backend
dapr run --app-id todo-backend --app-port 8000 -- uvicorn main:app --reload

# Terminal 2: Start the reminder service
cd services/reminder-service
dapr run --app-id reminder-service -- uvicorn main:app

# Terminal 3: Start the recurring task service
cd services/recurring-task-service
dapr run --app-id recurring-task-service -- uvicorn main:app

# Terminal 4: Start the frontend
cd frontend
npm run dev
```

### With Docker Compose
```bash
# Start all services with Docker Compose
docker-compose up --build
```

### In Kubernetes
```bash
# Deploy to Kubernetes with Helm
helm install todo-app ./helm-charts/todo-app --values ./helm-charts/values-dev.yaml
```

## Testing the Features

### 1. Test Recurring Tasks
- Create a recurring task via the API
- Complete the task and verify that the next occurrence is created
- Check that recurrence follows the specified pattern

### 2. Test Due Dates & Reminders
- Create a task with a due date and reminder
- Verify that reminders are sent at the correct time
- Check that overdue tasks are highlighted in the UI

### 3. Test Priority & Tagging
- Create tasks with different priority levels
- Apply hierarchical tags to tasks
- Verify filtering by priority and tags works correctly

### 4. Test Search & Filtering
- Create tasks with various attributes
- Perform searches and apply filters
- Verify that results match the search criteria

## Common Issues and Solutions

### Dapr Sidecar Not Starting
- Ensure Dapr is properly initialized: `dapr init`
- Check that ports 3500 and 50001 are available
- Verify component files are in the correct location

### Kafka Connection Issues
- Ensure Kafka is running and accessible
- Check that the broker address in configuration matches the running instance
- Verify that required topics exist

### Database Migration Issues
- Run migrations in the correct order
- Check that the database connection string is correct
- Verify that the user has sufficient privileges

## Next Steps

1. **Production Deployment**: Set up cloud infrastructure with AKS/GKE
2. **Monitoring**: Implement metrics and logging with Prometheus and Grafana
3. **Security**: Add additional authentication and authorization layers
4. **Performance**: Optimize queries and add caching where appropriate
5. **Testing**: Implement comprehensive test suites for all new features

## Resources

- [API Documentation](./contracts/task-api-contracts.md)
- [Data Model](./data-model.md)
- [Implementation Plan](./plan.md)
- [Dapr Documentation](https://docs.dapr.io)
- [Kafka Documentation](https://kafka.apache.org/documentation/)