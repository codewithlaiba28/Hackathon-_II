# Implementation Tasks: Phase 5 Advanced Cloud Deployment for the Todo Chatbot

**Feature Branch**: `001-phase5-advanced-cloud`  
**Created**: 2026-02-15  
**Spec**: [specs/001-phase5-advanced-cloud/spec.md](specs/001-phase5-advanced-cloud/spec.md)  
**Plan**: [specs/001-phase5-advanced-cloud/plan.md](specs/001-phase5-advanced-cloud/plan.md)  

## Implementation Strategy

This implementation will follow an incremental delivery approach, prioritizing core functionalities before extending with intermediate and advanced features. The development will be structured around independently deployable and testable user stories, ensuring a stable foundation at each step. Deployment to Minikube will be conducted frequently to validate changes in a near-production environment.

## Phase 1: Setup & Environment

**Goal**: Establish the foundational environment and project structure for Phase 5 development.

- [ ] T001 Create Phase 5 directories as per project structure: `backend/src/services/recurring_tasks_service.py`, `backend/src/services/notification_service.py`, `dapr/components`, `kafka/`, `helm-charts/todo-app/`
- [ ] T002 Verify Minikube cluster is running and accessible (manual check/quickstart.md)
- [ ] T003 Install Dapr on Kubernetes cluster via `dapr init -k` (quickstart.md)
- [ ] T004 Install Kafka to Minikube via Bitnami Helm chart (quickstart.md)
- [ ] T005 Create Kubernetes namespaces: `todo-app`, `kafka`, `dapr-system` (quickstart.md)
- [ ] T006 Create Kubernetes Secret for Neon DB connection string in `todo-app` namespace (quickstart.md)

## Phase 2: Foundational Backend & Dapr Configuration

**Goal**: Implement core database schema changes, update backend models, and configure Dapr components.

- [ ] T007 Apply database schema extensions (ALTER TABLE, CREATE INDEX) to Neon DB (plan.md, `backend/create_tables.py` or migration script)
- [ ] T008 Update SQLModel `Task` model in `backend/src/models/task.py` with new fields (`priority`, `tags`, `due_date`, `recurring`, `recurring_frequency`, `parent_task_id`)
- [ ] T009 Define Dapr `kafka-pubsub` component YAML for Kafka in `dapr/components/kafka-pubsub.yaml`
- [ ] T010 Define Dapr `statestore` component YAML for PostgreSQL in `dapr/components/statestore.yaml`
- [ ] T011 Define Dapr `kubernetes-secrets` component YAML in `dapr/components/kubernetes-secrets.yaml`
- [ ] T012 Apply all Dapr component YAMLs to the `todo-app` namespace (quickstart.md)
- [ ] T013 Update base FastAPI application in `backend/src/main.py` to include Dapr client initialization

## Phase 3: User Story 1 - Create Recurring Tasks (P1)

**Goal**: Enable users to mark tasks as recurring with specified frequencies.
**Independent Test**: A user can create a "Daily Standup" task, mark it as recurring daily, and verify its recurrence settings via API.

- [ ] T014 [US1] Update `add_task` MCP tool in `backend/src/api/mcp_tools.py` to accept `is_recurring` and `recurring_frequency` parameters
- [ ] T015 [US1] Implement persistence logic for `is_recurring` and `recurring_frequency` in `backend/src/services/task_service.py`
- [ ] T016 [US1] Create or update API endpoint for task creation to handle recurring task parameters in `backend/src/api/routes/tasks.py`
- [ ] T017 [US1] Develop Frontend UI component for selecting recurrence frequency when creating/editing a task in `frontend/src/components/task_form.tsx`

## Phase 4: User Story 2 - Auto-create Next Recurring Task (P1)

**Goal**: Automatically generate the next instance of a recurring task upon completion.
**Independent Test**: Complete a daily recurring task, and verify a new instance appears for the next day via API.

- [ ] T018 [US2] Create skeleton for `RecurringTaskService` in `backend/src/services/recurring_task_service.py`
- [ ] T019 [US2] Configure `RecurringTaskService` to subscribe to Dapr Pub/Sub for `task-events` (specifically `task.completed`) in `backend/src/services/recurring_task_service.py`
- [ ] T020 [US2] Implement event consumption logic in `RecurringTaskService` for `task.completed` events in `backend/src/services/recurring_task_service.py`
- [ ] T021 [US2] Implement logic in `RecurringTaskService` to create a new task occurrence based on recurrence frequency and publish `task.created` event via Dapr Pub/Sub in `backend/src/services/recurring_task_service.py`
- [ ] T022 [US2] Create Dockerfile for `RecurringTaskService` in `backend/Dockerfile.recurring_task_service`
- [ ] T023 [US2] Create Kubernetes Deployment and Service for `RecurringTaskService` in `helm-charts/todo-app/templates/recurring-service/`

## Phase 5: User Story 3 - Set Due Dates & Time Reminders (P1)

**Goal**: Enable users to set specific due dates and times for tasks.
**Independent Test**: User sets a due date/time for a task, and it's correctly saved and retrieved via API.

- [ ] T024 [US3] Update `add_task` MCP tool in `backend/src/api/mcp_tools.py` to accept `due_date` parameter
- [ ] T025 [US3] Update `update_task` MCP tool in `backend/src/api/mcp_tools.py` to allow modifying `due_date`
- [ ] T026 [US3] Implement persistence logic for `due_date` in `backend/src/services/task_service.py`
- [ ] T027 [US3] Develop Frontend UI component for setting due dates (calendar/time picker) in `frontend/src/components/task_form.tsx`

## Phase 6: User Story 4 - Receive Timely Reminder Notifications (P1)

**Goal**: Send reminder notifications one hour before a task's due time.
**Independent Test**: Set a task due for 2:00 PM, verify a reminder notification is received at 1:00 PM.

- [ ] T028 [US4] Implement `set_reminder` MCP tool in `backend/src/api/mcp_tools.py` to schedule reminders via Dapr Jobs API
- [ ] T029 [US4] Implement `cancel_reminder` MCP tool in `backend/src/api/mcp_tools.py` to cancel scheduled reminders
- [ ] T030 [US4] Integrate Dapr Jobs API client into `backend/src/services/dapr_service.py` (new file) for scheduling/cancelling jobs
- [ ] T031 [US4] Create skeleton for `NotificationService` in `backend/src/services/notification_service.py`
- [ ] T032 [US4] Configure `NotificationService` to subscribe to Dapr Pub/Sub for `reminders` topic in `backend/src/services/notification_service.py`
- [ ] T033 [US4] Implement event consumption logic in `NotificationService` for `reminder.due` events in `backend/src/services/notification_service.py`
- [ ] T034 [US4] Implement logic in `NotificationService` to send push/email notifications (placeholder implementation) in `backend/src/services/notification_service.py`
- [ ] T035 [US4] Create Dockerfile for `NotificationService` in `backend/Dockerfile.notification_service`
- [ ] T036 [US4] Create Kubernetes Deployment and Service for `NotificationService` in `helm-charts/todo-app/templates/notification-service/`
- [ ] T037 [US4] Frontend: Integrate calling `set_reminder` MCP tool when task with due date is created/updated in `frontend/src/components/task_form.tsx`

## Phase 7: User Story 5 - Assign Task Priorities (P2)

**Goal**: Enable users to assign priority levels (High, Medium, Low) to tasks.
**Independent Test**: User sets task to "High" priority, and it's reflected in task list API response.

- [ ] T038 [US5] Update `add_task` MCP tool in `backend/src/api/mcp_tools.py` to accept `priority` parameter
- [ ] T039 [US5] Update `update_task` MCP tool in `backend/src/api/mcp_tools.py` to allow modifying `priority`
- [ ] T040 [US5] Implement persistence logic for `priority` in `backend/src/services/task_service.py`
- [ ] T041 [US5] Develop Frontend UI component for selecting task priority in `frontend/src/components/task_form.tsx`

## Phase 8: User Story 6 - Assign Multiple Tags to Tasks (P2)

**Goal**: Enable users to categorize tasks using multiple tags.
**Independent Test**: User assigns "work" and "urgent" tags to a task, and both are saved and retrieved via API.

- [ ] T042 [US6] Update `add_task` MCP tool in `backend/src/api/mcp_tools.py` to accept `tags` parameter
- [ ] T043 [US6] Update `update_task` MCP tool in `backend/src/api/mcp_tools.py` to allow modifying `tags`
- [ ] T044 [US6] Implement persistence logic for `tags` (array of strings) in `backend/src/services/task_service.py`
- [ ] T045 [US6] Develop Frontend UI component for adding/managing multiple tags in `frontend/src/components/task_form.tsx`

## Phase 9: User Story 7, 8, 9, 10, 11 - Search & Filter & Chatbot Integration (P2)

**Goal**: Provide comprehensive search and filtering capabilities, accessible via API and chatbot.
**Independent Test**: User performs a combined filter (e.g., "High priority + Work tag + Due this week") and a chatbot search ("Show me high priority work tasks"), verifying correct results via API and UI.

- [ ] T046 [US7, US8, US9, US10] Update `list_tasks` MCP tool in `backend/src/api/mcp_tools.py` to accept filter parameters (`status`, `priority`, `tags`, `due_date_start`, `due_date_end`)
- [ ] T047 [US7, US8, US9, US10] Implement filtering logic in `backend/src/services/task_service.py` to combine multiple criteria
- [ ] T048 [US7, US8, US9, US10] Implement full-text search logic in `backend/src/services/task_service.py` using `search_query`
- [ ] T049 [US7, US8, US9, US10] Create Frontend UI components for filter controls (status, priority, tags, date range) in `frontend/src/components/task_list.tsx`
- [ ] T050 [US11] Integrate chatbot NLP to map natural language queries to API filter/search parameters in `backend/src/services/chatbot_nlp.py` (new file)
- [ ] T051 [US11] Update chatbot frontend to send mapped filter/search requests to backend in `frontend/src/components/chatbot.tsx`

## Phase 10: User Story 12, 13 - Sort Tasks & Maintain Sort Preference (P3)

**Goal**: Allow users to sort tasks by various criteria and persist their preferences.
**Independent Test**: User sorts tasks by priority, closes/reopens app, and tasks remain sorted by priority.

- [ ] T052 [US12] Update `list_tasks` MCP tool in `backend/src/api/mcp_tools.py` to accept `sort_by` and `sort_order` parameters
- [ ] T053 [US12] Implement sorting logic in `backend/src/services/task_service.py`
- [ ] T054 [US12] Develop Frontend UI component for sort controls in `frontend/src/components/task_list.tsx`
- [ ] T055 [US13] Add `sortPreference` field to `User` model in `backend/src/models/user.py`
- [ ] T056 [US13] Implement logic to store and retrieve user's sort preference in `backend/src/services/user_service.py`
- [ ] T057 [US13] Frontend: Integrate saving/loading user's sort preference in `frontend/src/lib/user_settings.ts`

## Phase 11: Cross-Cutting Concerns & Deployment

**Goal**: Finalize containerization, Kubernetes manifests, Helm charts, and comprehensive testing.
**Independent Test**: Entire application stack deploys successfully on Minikube via Helm, all health checks pass, and basic functionality verified.

- [ ] T058 Create Dockerfile for Backend Service in `backend/Dockerfile`
- [ ] T059 Create Dockerfile for Frontend Service in `frontend/Dockerfile`
- [ ] T060 Update `helm-charts/todo-app/values.yaml` with image names, tags, and service configurations
- [ ] T061 Create Kubernetes Deployments for Frontend, Backend, Recurring Task Service, Notification Service in `helm-charts/todo-app/templates/`
- [ ] T062 Create Kubernetes Services for Frontend, Backend, Recurring Task Service, Notification Service in `helm-charts/todo-app/templates/`
- [ ] T063 Create Kubernetes ConfigMaps for application-specific configurations in `helm-charts/todo-app/templates/`
- [ ] T064 Define Health Check endpoints (`/health/live`, `/health/ready`) in Backend, Recurring Task Service, Notification Service (backend/src/main.py etc.)
- [ ] T065 Configure liveness, readiness, and startup probes in Kubernetes Deployments (helm-charts/todo-app/templates/...)
- [ ] T066 Implement structured logging with correlation IDs in all backend services (backend/src/utils/logging.py)
- [ ] T067 Update `quickstart.md` with final deployment instructions using Helm
- [ ] T068 Verify Dapr sidecar injection for all relevant pods in Helm charts
- [ ] T069 Update `README.md` with overall project setup and quickstart reference
- [ ] T070 Create architecture diagrams (e.g., Mermaid in `docs/`)
- [ ] T071 Document Kafka event schemas (already in plan, verify consistency)
- [ ] T072 Create basic troubleshooting guide (`docs/troubleshooting.md`)

## Dependency Graph (User Story Completion Order)

1.  **P1 Stories**:
    *   User Story 1 (Create Recurring Tasks)
    *   User Story 3 (Set Due Dates & Time Reminders)
    *   User Story 4 (Receive Timely Reminder Notifications) - Depends on US3
    *   User Story 2 (Auto-create Next Recurring Task) - Depends on US1

2.  **P2 Stories**:
    *   User Story 5 (Assign Task Priorities)
    *   User Story 6 (Assign Multiple Tags to Tasks)
    *   User Story 7 (Filter Tasks by Priority and Tags) - Depends on US5, US6
    *   User Story 8 (Full-text Search Tasks)
    *   User Story 9 (Filter by Status, Priority, Tags, Due Date Range) - Depends on US7, US8
    *   User Story 10 (Combine Multiple Filters) - Depends on US9
    *   User Story 11 (Chatbot Integration for Search & Filter) - Depends on US10

3.  **P3 Stories**:
    *   User Story 12 (Sort Tasks by Various Criteria)
    *   User Story 13 (Maintain User Sort Preference) - Depends on US12

## Parallel Execution Examples

### Example 1: Core Recurring Task & Due Date Features (P1)

Tasks T014-T017 (US1), T024-T027 (US3) can be developed in parallel after foundational tasks.

### Example 2: Notifications & Auto-Recurring (P1)

Tasks T018-T023 (US2) and T028-T037 (US4) can be developed in parallel once US1 and US3 are stable.

### Example 3: Priorities & Tags (P2)

Tasks T038-T041 (US5) and T042-T045 (US6) can be developed in parallel.

## Suggested MVP Scope

The absolute Minimum Viable Product (MVP) should focus on **User Story 1 (Create Recurring Tasks)**, **User Story 3 (Set Due Dates & Time Reminders)**, **User Story 4 (Receive Timely Reminder Notifications)**, and **User Story 2 (Auto-create Next Recurring Task)**. This provides the core advanced functionality.

## Independent Test Criteria per User Story

-   **User Story 1 (Create Recurring Tasks)**: A user can create a "Daily Standup" task, mark it as recurring daily, and verify its recurrence settings via API.
-   **User Story 2 (Auto-create Next Recurring Task)**: Complete a daily recurring task, and verify a new instance appears for the next day via API.
-   **User Story 3 (Set Due Dates & Time Reminders)**: User sets a due date/time for a task, and it's correctly saved and retrieved via API.
-   **User Story 4 (Receive Timely Reminder Notifications)**: Set a task due for 2:00 PM, verify a reminder notification is received at 1:00 PM.
-   **User Story 5 (Assign Task Priorities)**: User sets task to "High" priority, and it's reflected in task list API response.
-   **User Story 6 (Assign Multiple Tags to Tasks)**: User assigns "work" and "urgent" tags to a task, and both are saved and retrieved via API.
-   **User Story 7, 8, 9, 10, 11 (Search & Filter & Chatbot Integration)**: User performs a combined filter (e.g., "High priority + Work tag + Due this week") and a chatbot search ("Show me high priority work tasks"), verifying correct results via API and UI.
-   **User Story 12, 13 (Sort Tasks & Maintain Sort Preference)**: User sorts tasks by priority, closes/reopens app, and tasks remain sorted by priority.
