---
id: 1
title: Create Phase 5 Advanced Cloud Plan
stage: plan
date: 2026-02-15
surface: agent
model: gemini-1.5-pro
feature: 001-phase5-advanced-cloud
branch: 001-phase5-advanced-cloud
user: Administrator
command: /sp.plan /sp.plan Create a comprehensive technical implementation plan for Phase 5 Advanced Cloud Deployment on Minikube: ...
labels: ["plan", "phase-5", "advanced-cloud", "todo-chatbot"]
links:
  spec: specs/001-phase5-advanced-cloud/spec.md
  ticket: null
  adr: null
  pr: null
files:
- specs/001-phase5-advanced-cloud/plan.md
- specs/001-phase5-advanced-cloud/research.md
- specs/001-phase5-advanced-cloud/data-model.md
- specs/001-phase5-advanced-cloud/contracts/api.yaml
- specs/001-phase5-advanced-cloud/quickstart.md
- specs/001-phase5-advanced-cloud/checklists/plan.md
tests:

## Prompt

/sp.plan /sp.plan

Create a comprehensive technical implementation plan for Phase 5 Advanced Cloud Deployment on Minikube:

## Tech Stack

### Core Technologies
- **Container Orchestration**: Kubernetes (Minikube v1.33+)
- **Package Manager**: Helm 3
- **Event Streaming**: Apache Kafka (Bitnami Helm Chart 30.x)
- **Distributed Runtime**: Dapr 1.16+ (dapr init -k)
- **Frontend**: Next.js 16 (App Router)
- **Backend**: Python 3.13 + FastAPI + SQLModel
- **AI**: OpenAI Agents SDK + Official MCP SDK
- **Database**: Neon Serverless PostgreSQL (external)
- **Authentication**: Better Auth (JWT)

### Development Tools
- **Docker**: Docker Desktop 4.35+ with Gordon AI (if available)
- **kubectl**: Kubernetes CLI
- **kubectl-ai** or **Kagent**: AI-assisted K8s operations
- **Dapr CLI**: dapr v1.16+
- **Helm**: v3.16+

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────────────┐
│                          MINIKUBE CLUSTER                                │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ Namespace: todo-app                                                │  │
│  │                                                                     │  │
│  │  ┌──────────────┐  ┌──────────────────────┐  ┌─────────────────┐ │  │
│  │  │   Frontend   │  │      Backend         │  │  Recurring Task │ │  │
│  │  │   (Next.js)  │──│  (FastAPI + MCP)    │  │    Service      │ │  │
│  │  │  + Dapr      │  │  + OpenAI Agents    │  │   + Dapr        │ │  │
│  │  │   Sidecar    │  │  + Dapr Sidecar     │  │    Sidecar      │ │  │
│  │  └──────────────┘  └──────────────────────┘  └─────────────────┘ │  │
│  │         │                    │                        │            │  │
│  │         └────────────────────┼────────────────────────┘            │  │
│  │                              │                                      │  │
│  │                       ┌──────▼──────┐                              │  │
│  │                       │ Notification │                              │  │
│  │                       │   Service    │                              │  │
│  │                       │  + Dapr      │                              │  │
│  │                       │   Sidecar    │                              │  │
│  │                       └──────────────┘                              │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                  │                                       │
│  ┌──────────────────────────────┼───────────────────────────────────┐  │
│  │ Namespace: kafka               │                                   │  │
│  │                                ▼                                   │  │
│  │  ┌─────────────────────────────────────────────────────────────┐ │  │
│  │  │  KAFKA CLUSTER (Bitnami Helm)                              │ │  │
│  │  │  Topics: task-events, reminders, task-updates              │ │  │
│  │  │  Brokers: 1 (Minikube), ZooKeeper: 1                        │ │  │
│  │  └─────────────────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ Namespace: dapr-system                                            │  │
│  │  - dapr-operator                                                  │  │
│  │  - dapr-sentry                                                    │  │
│  │  - dapr-sidecar-injector                                          │  │
│  │  - dapr-placement                                                 │  │
│  │  - dapr-dashboard                                                 │    │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ External: Neon DB (PostgreSQL)                                    │  │
│  │  Tables: users, tasks, conversations, messages                    │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Implementation Steps

### Phase 5.1: Project Setup & Environment
1. Upgrade existing monorepo structure
2. Create Phase 5 directories
3. Set up Minikube cluster
4. Install Dapr on Kubernetes
5. Install Kafka via Helm

### Phase 5.2: Database Schema Updates
1. Add new fields to tasks table
2. Create migration scripts
3. Update SQLModel models

### Phase 5.3: Backend Enhancements
1. Update MCP tools for new features
2. Implement priority/tags logic
3. Implement search/filter/sort logic
4. Add Kafka event publishing
5. Integrate Dapr Pub/Sub
6. Integrate Dapr State Store
7. Integrate Dapr Jobs API
8. Add health check endpoints

### Phase 5.4: New Microservices
1. Create Recurring Task Service
2. Create Notification Service
3. Implement event consumers

### Phase 5.5: Frontend Updates
1. Update ChatKit UI for new features
2. Add priority/tags UI elements
3. Add search/filter/sort controls
4. Integrate with updated backend

### Phase 5.6: Containerization
1. Create Dockerfiles for all services
2. Build Docker images
3. Push to Minikube Docker daemon

### Phase 5.7: Kubernetes Manifests
1. Create Deployments
2. Create Services
3. Create ConfigMaps
4. Create Secrets
5. Create Dapr Components

### Phase 5.8: Helm Charts
1. Create umbrella Helm chart
2. Create subcharts for each service
3. Define values.yaml
4. Test chart installation

### Phase 5.9: Deployment & Testing
1. Deploy Kafka to Minikube
2. Deploy Dapr components
3. Deploy services via Helm
4. Test all features
5. Test event flows
6. Test failure scenarios

### Phase 5.10: Documentation
1. Update README with deployment instructions
2. Create architecture diagrams
3. Document event schemas
4. Create troubleshooting guide

## Detailed Component Specifications

### 1. Database Schema Extensions
```sql
-- Add columns to tasks table
ALTER TABLE tasks ADD COLUMN priority VARCHAR(10) DEFAULT 'medium';
ALTER TABLE tasks ADD COLUMN tags TEXT[];
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP;
ALTER TABLE tasks ADD COLUMN recurring BOOLEAN DEFAULT false;
ALTER TABLE tasks ADD COLUMN recurring_frequency VARCHAR(20);  -- daily, weekly, monthly, yearly
ALTER TABLE tasks ADD COLUMN parent_task_id INTEGER REFERENCES tasks(id);

-- Create indexes
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_tags ON tasks USING GIN(tags);
CREATE INDEX idx_tasks_search ON tasks USING GIN(to_tsvector('english', title || ' ' || COALESCE(description, '')));
```

### 2. MCP Tools Updates
```python
# Updated tools
- add_task: Add priority, tags, due_date, recurring params
- update_task: Support updating priority, tags, due_date
- list_tasks: Add filters (priority, tags, status, due_date_range), sorting
- search_tasks: Full-text search across title/description
- complete_task: Publish event for recurring task logic

# New tools
- set_reminder: Schedule reminder via Dapr Jobs API
- cancel_reminder: Cancel scheduled reminder
```

### 3. Kafka Event Schemas
```json
// task-events topic
{
  "event_type": "task.created" | "task.updated" | "task.completed" | "task.deleted",
  "task_id": 123,
  "user_id": "user_abc",
  "task_data": {
    "title": "Task title",
    "priority": "high",
    "tags": ["work", "urgent"],
    "due_date": "2026-02-01T14:00:00Z",
    "recurring": true,
    "recurring_frequency": "weekly"
  },
  "timestamp": "2026-01-18T10:30:00Z",
  "correlation_id": "uuid"
}

// reminders topic
{
  "event_type": "reminder.due",
  "task_id": 123,
  "user_id": "user_abc",
  "task_title": "Important meeting",
  "due_at": "2026-02-01T14:00:00Z",
  "remind_at": "2026-02-01T13:00:00Z",
  "timestamp": "2026-02-01T13:00:00Z"
}
```

### 4. Dapr Components
```yaml
# dapr-pubsub-kafka.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka.kafka.svc.cluster.local:9092"
  - name: consumerGroup
    value: "todo-services"
  - name: authRequired
    value: "false"

# dapr-statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: todo-app
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: neon-db-secret
      key: connection-string

# dapr-secrets.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
  namespace: todo-app
spec:
  type: secretstores.kubernetes
  version: v1
```

### 5. Helm Chart Structure
```
helm/todo-app-chart/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── _helpers.tpl
│   ├── frontend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   ├── backend/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── secret.yaml
│   ├── recurring-service/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   ├── notification-service/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── configmap.yaml
│   ├── dapr-components/
│   │   ├── pubsub.yaml
│   │   ├── statestore.yaml
│   │   └── secrets.yaml
│   └── ingress.yaml
```

### 6. Resource Limits
```yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "100m"
  limits:
    memory: "512Mi"
    cpu: "500m"
```

### 7. Health Check Endpoints
```python
@app.get("/health/live")
async def liveness():
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    # Check DB connection
    # Check Kafka connection
    return {"status": "ready"}
```

## Technology Decisions Rationale

| Decision | Rationale |
|----------|-----------|
| Bitnami Kafka Helm | Easy setup, production-ready, well-maintained |
| Dapr Pub/Sub | Abstracts Kafka, swappable, built-in retries |
| Dapr Jobs API | Exact scheduling vs cron polling |
| Minikube only | Free, local development, no cloud costs |
| Helm charts | Repeatable deployments, easy upgrades |
| SQLModel + Neon | Async ORM, managed DB, no local maintenance |

## Success Criteria

- [ ] All services running on Minikube
- [ ] Kafka topics created and receiving events
- [ ] Dapr sidecars injected into all pods
- [ ] Advanced features (recurring, due dates, priorities, tags, search/filter/sort) working via chatbot
- [ ] Event-driven flows working (recurring tasks auto-create, reminders fire)
- [ ] Zero errors in logs
- [ ] Health checks passing
- [ ] Helm chart deploys successfully
- [ ] Can tear down and redeploy entire stack in under 5 minutes

## Response snapshot

The implementation plan for "Phase 5 Advanced Cloud Deployment for the Todo Chatbot" has been created and validated. The plan is located at `specs/001-phase5-advanced-cloud/plan.md`. Research findings, data model, API contracts, and a quickstart guide have also been generated. The agent's context has been updated with the new technology outlined in the plan.

## Outcome

- ✅ Impact: A comprehensive technical implementation plan has been generated, detailing the architecture, tech stack, implementation steps, and component specifications for Phase 5 Advanced Cloud Deployment.
- 🧪 Tests: No automated tests were run, but the plan passed all quality checks in `specs/001-phase5-advanced-cloud/checklists/plan.md`.
- 📁 Files:
  - `specs/001-phase5-advanced-cloud/plan.md` (created and populated)
  - `specs/001-phase5-advanced-cloud/research.md` (created and populated)
  - `specs/001-phase5-advanced-cloud/data-model.md` (created and populated)
  - `specs/001-phase5-advanced-cloud/contracts/api.yaml` (created and populated)
  - `specs/001-phase5-advanced-cloud/quickstart.md` (created and populated)
  - `specs/001-phase5-advanced-cloud/checklists/plan.md` (created and updated)
- 🔁 Next prompts: The implementation plan is ready for the next phase: `/sp.tasks`.
- 🧠 Reflection: The `setup-plan.sh` and `update-agent-context.sh` scripts exhibited unexpected behavior (empty output) when run via `run_shell_command`, requiring manual derivation of paths and confirmation of conceptual updates. Despite this, the plan generation process was successful, and all required artifacts were created.

## Evaluation notes (flywheel)

- Failure modes observed: The `setup-plan.sh` and `update-agent-context.sh` scripts did not output JSON as expected when run via `run_shell_command`, indicating a potential issue with script execution context or output redirection within the tool.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Investigate `setup-plan.sh` and `update-agent-context.sh` script execution within `run_shell_command` to ensure JSON output is captured.
