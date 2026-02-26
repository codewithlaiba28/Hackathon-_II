---
id: 1
title: Create Phase 5 Advanced Cloud Spec
stage: spec
date: 2026-02-15
surface: agent
model: gemini-1.5-pro
feature: 001-phase5-advanced-cloud
branch: 001-phase5-advanced-cloud
user: Administrator
command: /sp.specify Build Phase 5 Advanced Cloud Deployment for the Todo Chatbot with the following features: ...
labels: ["spec", "phase-5", "advanced-cloud", "todo-chatbot"]
links:
  spec: specs/001-phase5-advanced-cloud/spec.md
  ticket: null
  adr: null
  pr: null
files:
- specs/001-phase5-advanced-cloud/spec.md
- specs/001-phase5-advanced-cloud/checklists/requirements.md
tests:

## Prompt

/sp.specify Build Phase 5 Advanced Cloud Deployment for the Todo Chatbot with the following features: ## Advanced Level Features ### 1. Recurring Tasks - User can mark a task as "recurring" with frequency: daily, weekly, monthly, yearly - When a recurring task is marked complete, automatically create next occurrence - Example: "Team standup" every weekday at 9 AM - Event-driven: Task completion publishes event → Recurring Task Service consumes → Creates next task ### 2. Due Dates & Time Reminders - User can set due date/time for any task - System sends reminder notification 1 hour before due time - Event-driven: Due date set → Publishes reminder event → Notification Service consumes - Use Dapr Jobs API to schedule exact reminder times (not cron polling) ## Intermediate Level Features ### 3. Priorities & Tags/Categories - Task priority levels: High, Medium, Low (default: Medium) - User can assign multiple tags to a task (work, personal, urgent, etc.) - Filter tasks by priority and/or tags - Tags stored as array in database, indexed for fast queries ### 4. Search & Filter - Full-text search across task titles and descriptions - Filter by: status (pending/completed), priority, tags, due date range - Combine multiple filters (e.g., "High priority + Work tag + Due this week") - Search via chatbot: "Show me high priority work tasks" ### 5. Sort Tasks - Sort by: creation date, due date, priority, title (alphabetical) - Default sort: Upcoming due dates first, then by priority - Maintain sort preference per user in database ## Event-Driven Architecture ### Kafka Topics 1. **task-events**: All task CRUD operations (create, update, delete, complete) 2. **reminders**: Scheduled reminder triggers from Dapr Jobs 3. **task-updates**: Real-time sync for multi-client updates ### Event Producers - Chat API (MCP Tools): Publishes to task-events on every task mutation - Dapr Jobs API: Publishes to reminders when job fires - Recurring Task Service: Publishes to task-events when creating next occurrence ### Event Consumers - **Recurring Task Service**: Consumes task-events (task.completed), creates next task - **Notification Service**: Consumes reminders, sends push/email notifications - **Audit Service** (optional): Consumes task-events, maintains activity log ## Dapr Building Blocks ### 1. Pub/Sub (Kafka Abstraction) - Component: Dapr Kafka Pub/Sub - Services publish/subscribe via Dapr API (no kafka-python library needed) - Swappable: Can switch to RabbitMQ/Redis by changing component YAML ### 2. State Management - Store conversation history in Dapr State Store (backed by PostgreSQL) - Store task cache for fast retrieval - Stateless services - all state externalized ### 3. Service Invocation - Frontend → Backend communication via Dapr service invocation - Built-in retries, circuit breakers, mTLS - Service discovery handled by Dapr ### 4. Jobs API (Reminders) - Schedule exact reminder times using Dapr Jobs API - Example: Task due at 2:00 PM → Schedule reminder job at 1:00 PM - When job fires, Dapr calls callback endpoint → Service publishes to reminders topic ### 5. Secrets Management - Store OpenAI API key, Neon DB credentials in Kubernetes Secrets - Access via Dapr Secrets API - No hardcoded credentials in code ## Deployment Architecture (Minikube) ### Namespaces - `todo-app`: Frontend, Backend, Recurring Task Service, Notification Service - `kafka`: Kafka broker and Zookeeper (Bitnami Helm chart) - `dapr-system`: Dapr control plane ### Services 1. **Frontend** (Next.js + ChatKit) - Deployment: 2 replicas - Service: ClusterIP, exposed via Ingress - Dapr sidecar: service invocation 2. **Backend** (FastAPI + MCP + OpenAI Agents SDK) - Deployment: 3 replicas - Service: ClusterIP - Dapr sidecar: Pub/Sub, State, Service Invocation, Jobs, Secrets 3. **Recurring Task Service** (Python FastAPI) - Deployment: 2 replicas - Subscribes to: task-events (task.completed filter) - Publishes to: task-events (task.created) - Dapr sidecar: Pub/Sub, State 4. **Notification Service** (Python FastAPI) - Deployment: 2 replicas - Subscribes to: reminders - Sends: Push notifications, emails - Dapr sidecar: Pub/Sub, Secrets 5. **Kafka** (Bitnami Helm Chart) - StatefulSet: 1 replica (Minikube) - Topics: task-events, reminders, task-updates - No authentication for local dev 6. **Neon DB** (External Managed Service) - Connection via Dapr State Store component - Tables: users, tasks, conversations, messages ### Helm Charts - `todo-app-chart`: Umbrella chart containing all services - `kafka-chart`: Bitnami Kafka (or Strimzi) - Dapr installed via `dapr init -k` ### Resource Specifications ```yaml resources: requests: memory: "256Mi" cpu: "100m" limits: memory: "512Mi" cpu: "500m" ``` ### Health Checks - Liveness probe: `/health/live` - Readiness probe: `/health/ready` - Startup probe: `/health/startup` (for slow-starting services) ## Acceptance Criteria ### Functional - [ ] User can create recurring tasks (daily/weekly/monthly/yearly) - [ ] Completed recurring task auto-creates next occurrence - [ ] User can set due date/time for tasks - [ ] System sends reminder 1 hour before due time - [ ] User can assign priority (High/Medium/Low) to tasks - [ ] User can add multiple tags to tasks - [ ] User can search tasks by title/description - [ ] User can filter by status, priority, tags, due date range - [ ] User can sort by date, priority, title - [ ] All features work via chatbot natural language ### Technical - [ ] All services deployed on Minikube - [ ] Kafka running on Minikube (Bitnami/Strimzi) - [ ] Dapr sidecars injected into all pods - [ ] Task events published to Kafka via Dapr Pub/Sub - [ ] Reminders scheduled via Dapr Jobs API - [ ] Conversation state stored in Dapr State Store - [ ] Secrets managed via Kubernetes Secrets + Dapr Secrets API - [ ] All services have health checks - [ ] Services have resource limits - [ ] Helm charts created for easy deployment - [ ] Zero-downtime rolling updates ### Observability - [ ] Structured logging with correlation IDs - [ ] Dapr dashboard accessible via port-forward - [ ] Kafka topics visible via kafka-console-consumer - [ ] Pod logs accessible via kubectl logs - [ ] Health check endpoints return proper status ## Out of Scope (Minikube Only, No Cloud) - ❌ DigitalOcean/Azure/GCP deployment - ❌ Ingress with real DNS/TLS - ❌ Horizontal Pod Autoscaling (HPA) - ❌ CI/CD pipeline (GitHub Actions) - ❌ Production monitoring (Prometheus/Grafana) - ✅ Focus: Everything running perfectly on local Minikube

## Response snapshot

The feature specification for "Phase 5 Advanced Cloud Deployment for the Todo Chatbot" has been created and validated. The branch `001-phase5-advanced-cloud` was created, and the specification is located at `specs/001-phase5-advanced-cloud/spec.md`. All specification quality checks have passed.

## Outcome

- ✅ Impact: A detailed feature specification has been created for Phase 5 Advanced Cloud Deployment, covering recurring tasks, due dates, reminders, priorities, tags, search, filter, sort, event-driven architecture with Kafka, Dapr building blocks, and Minikube deployment.
- 🧪 Tests: No automated tests were run, but the specification passed all quality checks in `specs/001-phase5-advanced-cloud/checklists/requirements.md`.
- 📁 Files:
  - `specs/001-phase5-advanced-cloud/spec.md` (created and populated)
  - `specs/001-phase5-advanced-cloud/checklists/requirements.md` (created and updated)
- 🔁 Next prompts: The specification is ready for the next phase: `/sp.plan`.
- 🧠 Reflection: The `create-new-feature.sh` script exhibited unexpected behavior (empty output), requiring manual creation of the branch and feature directory. The specification generation and validation process was successful despite this.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-new-feature.sh` script did not output JSON as expected when run via `run_shell_command`, indicating a potential issue with script execution context or output redirection within the tool.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Investigate `create-new-feature.sh` script execution within `run_shell_command` to ensure JSON output is captured.
