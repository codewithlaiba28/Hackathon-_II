# Feature Specification: Phase 5 Advanced Cloud Deployment for the Todo Chatbot

**Feature Branch**: `001-phase5-advanced-cloud`  
**Created**: 2026-02-15  
**Status**: Draft  
**Input**: User description: "Build Phase 5 Advanced Cloud Deployment for the Todo Chatbot with the following features: ## Advanced Level Features ### 1. Recurring Tasks - User can mark a task as "recurring" with frequency: daily, weekly, monthly, yearly - When a recurring task is marked complete, automatically create next occurrence - Example: "Team standup" every weekday at 9 AM - Event-driven: Task completion publishes event → Recurring Task Service consumes → Creates next task ### 2. Due Dates & Time Reminders - User can set due date/time for any task - System sends reminder notification 1 hour before due time - Event-driven: Due date set → Publishes reminder event → Notification Service consumes - Use Dapr Jobs API to schedule exact reminder times (not cron polling) ## Intermediate Level Features ### 3. Priorities & Tags/Categories - Task priority levels: High, Medium, Low (default: Medium) - User can assign multiple tags to a task (work, personal, urgent, etc.) - Filter tasks by priority and/or tags - Tags stored as array in database, indexed for fast queries ### 4. Search & Filter - Full-text search across task titles and descriptions - Filter by: status (pending/completed), priority, tags, due date range - Combine multiple filters (e.g., "High priority + Work tag + Due this week") - Search via chatbot: "Show me high priority work tasks" ### 5. Sort Tasks - Sort by: creation date, due date, priority, title (alphabetical) - Default sort: Upcoming due dates first, then by priority - Maintain sort preference per user in database ## Event-Driven Architecture ### Kafka Topics 1. **task-events**: All task CRUD operations (create, update, delete, complete) 2. **reminders**: Scheduled reminder triggers from Dapr Jobs 3. **task-updates**: Real-time sync for multi-client updates ### Event Producers - Chat API (MCP Tools): Publishes to task-events on every task mutation - Dapr Jobs API: Publishes to reminders when job fires - Recurring Task Service: Publishes to task-events when creating next occurrence ### Event Consumers - **Recurring Task Service**: Consumes task-events (task.completed), creates next task - **Notification Service**: Consumes reminders, sends push/email notifications - **Audit Service** (optional): Consumes task-events, maintains activity log ## Dapr Building Blocks ### 1. Pub/Sub (Kafka Abstraction) - Component: Dapr Kafka Pub/Sub - Services publish/subscribe via Dapr API (no kafka-python library needed) - Swappable: Can switch to RabbitMQ/Redis by changing component YAML ### 2. State Management - Store conversation history in Dapr State Store (backed by PostgreSQL) - Store task cache for fast retrieval - Stateless services - all state externalized ### 3. Service Invocation - Frontend → Backend communication via Dapr service invocation - Built-in retries, circuit breakers, mTLS - Service discovery handled by Dapr ### 4. Jobs API (Reminders) - Schedule exact reminder times using Dapr Jobs API - Example: Task due at 2:00 PM → Schedule reminder job at 1:00 PM - When job fires, Dapr calls callback endpoint → Service publishes to reminders topic ### 5. Secrets Management - Store OpenAI API key, Neon DB credentials in Kubernetes Secrets - Access via Dapr Secrets API - No hardcoded credentials in code ## Deployment Architecture (Minikube) ### Namespaces - `todo-app`: Frontend, Backend, Recurring Task Service, Notification Service - `kafka`: Kafka broker and Zookeeper (Bitnami Helm chart) - `dapr-system`: Dapr control plane ### Services 1. **Frontend** (Next.js + ChatKit) - Deployment: 2 replicas - Service: ClusterIP, exposed via Ingress - Dapr sidecar: service invocation 2. **Backend** (FastAPI + MCP + OpenAI Agents SDK) - Deployment: 3 replicas - Service: ClusterIP - Dapr sidecar: Pub/Sub, State, Service Invocation, Jobs, Secrets 3. **Recurring Task Service** (Python FastAPI) - Deployment: 2 replicas - Subscribes to: task-events (task.completed filter) - Publishes to: task-events (task.created) - Dapr sidecar: Pub/Sub, State 4. **Notification Service** (Python FastAPI) - Deployment: 2 replicas - Subscribes to: reminders - Sends: Push notifications, emails - Dapr sidecar: Pub/Sub, Secrets 5. **Kafka** (Bitnami Helm Chart) - StatefulSet: 1 replica (Minikube) - Topics: task-events, reminders, task-updates - No authentication for local dev 6. **Neon DB** (External Managed Service) - Connection via Dapr State Store component - Tables: users, tasks, conversations, messages ### Helm Charts - `todo-app-chart`: Umbrella chart containing all services - `kafka-chart`: Bitnami Kafka (or Strimzi) - Dapr installed via `dapr init -k` ### Resource Specifications ```yaml resources: requests: memory: "256Mi" cpu: "100m" limits: memory: "512Mi" cpu: "500m" ``` ### Health Checks - Liveness probe: `/health/live` - Readiness probe: `/health/ready` - Startup probe: `/health/startup` (for slow-starting services) ## Acceptance Criteria ### Functional - [ ] User can create recurring tasks (daily/weekly/monthly/yearly) - [ ] Completed recurring task auto-creates next occurrence - [ ] User can set due date/time for tasks - [ ] System sends reminder 1 hour before due time - [ ] User can assign priority (High/Medium/Low) to tasks - [ ] User can add multiple tags to tasks - [ ] User can search tasks by title/description - [ ] User can filter by status, priority, tags, due date range - [ ] User can sort by date, priority, title - [ ] All features work via chatbot natural language ### Technical - [ ] All services deployed on Minikube - [ ] Kafka running on Minikube (Bitnami/Strimzi) - [ ] Dapr sidecars injected into all pods - [ ] Task events published to Kafka via Dapr Pub/Sub - [ ] Reminders scheduled via Dapr Jobs API - [ ] Conversation state stored in Dapr State Store - [ ] Secrets managed via Kubernetes Secrets + Dapr Secrets API - [ ] All services have health checks - [ ] Services have resource limits - [ ] Helm charts created for easy deployment - [ ] Zero-downtime rolling updates ### Observability - [ ] Structured logging with correlation IDs - [ ] Dapr dashboard accessible via port-forward - [ ] Kafka topics visible via kafka-console-consumer - [ ] Pod logs accessible via kubectl logs - [ ] Health check endpoints return proper status ## Out of Scope (Minikube Only, No Cloud) - ❌ DigitalOcean/Azure/GCP deployment - ❌ Ingress with real DNS/TLS - ❌ Horizontal Pod Autoscaling (HPA) - ❌ CI/CD pipeline (GitHub Actions) - ❌ Production monitoring (Prometheus/Grafana) - ✅ Focus: Everything running perfectly on local Minikube"

## User Scenarios & Testing

### User Story 1 - Create Recurring Tasks (Priority: P1)

Users need to mark tasks as recurring with specified frequencies (daily, weekly, monthly, yearly) so that routine activities are automatically managed.

**Why this priority**: Essential for automating repetitive tasks, a core advanced feature.

**Independent Test**: A user can create a "Daily Standup" task, mark it as recurring daily, and verify its recurrence settings.

**Acceptance Scenarios**:

1.  **Given** a user is creating a new task, **When** they specify a recurrence frequency (daily, weekly, monthly, yearly), **Then** the task is saved with the specified recurrence.
2.  **Given** an existing task, **When** a user modifies it to be recurring with a frequency, **Then** the task's recurrence setting is updated.

---

### User Story 2 - Auto-create Next Recurring Task (Priority: P1)

When a recurring task is completed, the system automatically generates the next instance of that task to maintain continuity of routine activities.

**Why this priority**: Critical for the automation aspect of recurring tasks, directly impacts user effort.

**Independent Test**: A user completes a daily recurring task, and a new instance of that task appears for the next day.

**Acceptance Scenarios**:

1.  **Given** a recurring task is marked as complete, **When** the completion event is processed, **Then** a new task occurrence is automatically created based on the defined frequency.
2.  **Given** a daily recurring task is completed, **When** the system processes the event, **Then** a new instance of the task is created for the next day.

---

### User Story 3 - Set Due Dates & Time Reminders (Priority: P1)

Users need to set specific due dates and times for tasks to manage deadlines effectively.

**Why this priority**: Fundamental for task management and organization, directly impacts user productivity.

**Independent Test**: A user sets a due date/time for a task and verifies it is displayed correctly.

**Acceptance Scenarios**:

1.  **Given** a user is creating or editing a task, **When** they specify a due date and time, **Then** the task is saved with the precise due date and time.
2.  **Given** a task with a due date/time, **When** the user views the task, **Then** the due date and time are accurately displayed.

---

### User Story 4 - Receive Timely Reminder Notifications (Priority: P1)

Users should receive reminder notifications one hour before a task's due time to help them stay on schedule.

**Why this priority**: Directly supports timely task completion and prevents missed deadlines.

**Independent Test**: A user sets a task due for 2:00 PM, and receives a reminder notification at 1:00 PM.

**Acceptance Scenarios**:

1.  **Given** a task with a set due date and time, **When** the time is exactly one hour before the due time, **Then** the system sends a reminder notification to the user.
2.  **Given** a task without a due time, **When** a due date is set, **Then** no time-based reminder is sent (only date-based reminders if applicable, which is out of scope for time reminders).

---

### User Story 5 - Assign Task Priorities (Priority: P2)

Users need to assign priority levels (High, Medium, Low) to tasks to help them focus on what's most important.

**Why this priority**: Improves user organization and task prioritization, enhancing productivity.

**Independent Test**: A user sets a task to "High" priority and sees it reflected in the task list.

**Acceptance Scenarios**:

1.  **Given** a user is creating or editing a task, **When** they select a priority level (High, Medium, Low), **Then** the task is saved with the chosen priority.
2.  **Given** an existing task, **When** its priority is updated, **Then** the new priority is displayed in the task list.

---

### User Story 6 - Assign Multiple Tags to Tasks (Priority: P2)

Users need to categorize tasks using multiple tags (e.g., work, personal, urgent) for better organization and searchability.

**Why this priority**: Enhances task categorization and filtering capabilities, improving task discovery.

**Independent Test**: A user assigns "work" and "urgent" tags to a task and verifies both tags are associated.

**Acceptance Scenarios**:

1.  **Given** a user is creating or editing a task, **When** they add multiple tags, **Then** all specified tags are associated with the task.
2.  **Given** a task with multiple tags, **When** the user views the task, **Then** all assigned tags are displayed.

---

### User Story 7 - Filter Tasks by Priority and Tags (Priority: P2)

Users need to filter tasks based on their assigned priority levels and tags to quickly find relevant tasks.

**Why this priority**: Improves task management efficiency and user focus.

**Independent Test**: A user filters tasks to show only "High" priority tasks with the "work" tag, and only matching tasks are displayed.

**Acceptance Scenarios**:

1.  **Given** a list of tasks with various priorities and tags, **When** the user filters by a specific priority, **Then** only tasks matching that priority are shown.
2.  **Given** a list of tasks, **When** the user filters by one or more tags, **Then** only tasks associated with all specified tags are displayed.

---

### User Story 8 - Full-text Search Tasks (Priority: P2)

Users need to perform full-text searches across task titles and descriptions to quickly locate tasks using keywords.

**Why this priority**: Essential for finding tasks without precise categorization, improving usability.

**Independent Test**: A user searches for a keyword present in a task's description and finds the task.

**Acceptance Scenarios**:

1.  **Given** a list of tasks, **When** the user enters a search term, **Then** tasks with titles or descriptions containing the search term are displayed.
2.  **Given** a search term, **When** no tasks match the term, **Then** the system indicates no results found.

---

### User Story 9 - Filter by Status, Priority, Tags, Due Date Range (Priority: P2)

Users need comprehensive filtering options including status, priority, tags, and due date range to refine their task views.

**Why this priority**: Provides granular control over task visibility, enabling focused work.

**Independent Test**: A user filters for "completed" tasks, "High" priority, with "personal" tag, due "this month", and only matching tasks are shown.

**Acceptance Scenarios**:

1.  **Given** a list of tasks, **When** the user filters by task status (pending/completed), **Then** only tasks matching the selected status are displayed.
2.  **Given** a list of tasks, **When** the user filters by a specific due date range, **Then** only tasks falling within that range are displayed.

---

### User Story 10 - Combine Multiple Filters (Priority: P2)

Users need to apply multiple filters simultaneously (e.g., "High priority + Work tag + Due this week") to create highly specific task views.

**Why this priority**: Enhances the power of filtering, allowing users to drill down to very specific task sets.

**Independent Test**: A user applies filters for "High priority", "Work tag", and "Due this week", and only tasks satisfying all three conditions are shown.

**Acceptance Scenarios**:

1.  **Given** a list of tasks, **When** the user applies multiple filters (e.g., status AND priority AND tags), **Then** only tasks that satisfy ALL selected filter criteria are displayed.
2.  **Given** a set of combined filters, **When** no tasks match all criteria, **Then** the system displays no results.

---

### User Story 11 - Chatbot Integration for Search & Filter (Priority: P2)

Users need to perform search and filter operations through natural language commands in the chatbot interface.

**Why this priority**: Improves accessibility and user experience for interacting with advanced features.

**Independent Test**: A user types "Show me high priority work tasks" in the chatbot and sees the correctly filtered list.

**Acceptance Scenarios**:

1.  **Given** the chatbot is active, **When** the user issues a natural language command to search for tasks (e.g., "find tasks about meeting"), **Then** the system interprets the command and displays matching tasks.
2.  **Given** the chatbot is active, **When** the user issues a natural language command to filter tasks (e.g., "show me tasks due tomorrow"), **Then** the system interprets the command and applies the specified filters.

---

### User Story 12 - Sort Tasks by Various Criteria (Priority: P3)

Users need to sort their task lists by creation date, due date, priority, or title to organize their view according to their current needs.

**Why this priority**: Provides flexibility in task organization and personal preference.

**Independent Test**: A user sorts tasks by due date (ascending) and observes the list reordering correctly.

**Acceptance Scenarios**:

1.  **Given** a list of tasks, **When** the user selects a sort criterion (creation date, due date, priority, title), **Then** the task list reorders according to the selected criterion.
2.  **Given** tasks with the same sort key (e.g., same due date), **When** a secondary sort key is implied (e.g., then by priority), **Then** the tasks are correctly sorted based on the secondary key.

---

### User Story 13 - Maintain User Sort Preference (Priority: P3)

The system should remember each user's preferred sort order across sessions.

**Why this priority**: Enhances user convenience and personalization.

**Independent Test**: A user sorts their tasks by priority, closes the application, reopens it, and sees tasks still sorted by priority.

**Acceptance Scenarios**:

1.  **Given** a user sets a preferred sort order, **When** they close and reopen the application, **Then** their previous sort preference is automatically applied.
2.  **Given** a user has a saved sort preference, **When** they manually change the sort order, **Then** the new sort order becomes the active preference for subsequent sessions.

---

### Edge Cases

-   **Recurring tasks without end date**: How long do they recur? (Indefinitely unless explicitly stopped)
-   **Reminders for tasks without specific time**: When is the reminder sent? (e.g., default to 9 AM on due date or no time reminder if only date is set)
-   **Conflicting filters**: What happens if filters exclude all tasks? (Display "No tasks found")
-   **Search with no results**: What is the user feedback? (Display "No tasks found for your search")
-   **Task deletion impacting recurring series**: Does deleting one instance delete all future ones or just that one? (Just that one, with option to delete series)

## Requirements

### Functional Requirements

-   **FR-001 (Recurring Tasks)**: System MUST allow users to mark a task as recurring with frequencies: daily, weekly, monthly, yearly.
-   **FR-002 (Recurring Tasks)**: System MUST automatically create the next occurrence of a recurring task when the current instance is marked complete.
-   **FR-003 (Due Dates)**: System MUST allow users to set a due date and time for any task.
-   **FR-004 (Reminders)**: System MUST send a reminder notification to the user 1 hour before a task's due time.
-   **FR-005 (Priorities)**: System MUST allow users to assign priority levels (High, Medium, Low) to tasks (default: Medium).
-   **FR-006 (Tags)**: System MUST allow users to assign multiple tags to a task.
-   **FR-007 (Filtering)**: System MUST allow filtering tasks by status (pending/completed), priority, tags, and due date range.
-   **FR-008 (Filtering)**: System MUST support combining multiple filter criteria.
-   **FR-009 (Search)**: System MUST support full-text search across task titles and descriptions.
-   **FR-010 (Sort)**: System MUST allow sorting tasks by creation date, due date, priority, and title (alphabetical).
-   **FR-011 (Sort Preference)**: System MUST maintain user-specific sort preferences in the database.
-   **FR-012 (Chatbot Integration)**: All search, filter, and sort functionalities MUST be accessible and controllable via natural language commands through the chatbot interface.

### Event-Driven Architecture Requirements

-   **EDA-001 (Kafka Topics)**: System MUST utilize Kafka topics: `task-events` (for CRUD), `reminders` (for scheduled triggers), `task-updates` (for real-time sync).
-   **EDA-002 (Event Producers)**: Chat API (MCP Tools) MUST publish events to `task-events` on every task mutation.
-   **EDA-003 (Event Producers)**: Dapr Jobs API MUST publish events to `reminders` when a scheduled job fires.
-   **EDA-004 (Event Producers)**: Recurring Task Service MUST publish events to `task-events` when creating the next occurrence of a task.
-   **EDA-005 (Event Consumers)**: Recurring Task Service MUST consume `task-events` (filtered for `task.completed`) to create subsequent recurring tasks.
-   **EDA-006 (Event Consumers)**: Notification Service MUST consume `reminders` to send push/email notifications.
-   **EDA-007 (Event Consumers - Optional)**: An optional Audit Service MAY consume `task-events` to maintain an activity log.

### Dapr Building Blocks Requirements

-   **DAPR-001 (Pub/Sub)**: Services MUST publish and subscribe to events via Dapr Pub/Sub API, abstracting Kafka.
-   **DAPR-002 (State Management)**: Conversation history and task cache MUST be stored in Dapr State Store (backed by PostgreSQL).
-   **DAPR-003 (Service Invocation)**: Frontend and Backend communication MUST utilize Dapr Service Invocation for features like retries, circuit breakers, and mTLS.
-   **DAPR-004 (Jobs API)**: Scheduled reminders MUST be implemented using the Dapr Jobs API.
-   **DAPR-005 (Secrets Management)**: Sensitive credentials (e.g., OpenAI API key, Neon DB credentials) MUST be stored in Kubernetes Secrets and accessed via the Dapr Secrets API.

### Deployment Architecture Requirements (Minikube)

-   **DEP-001 (Namespaces)**: Deployment MUST use dedicated Kubernetes namespaces: `todo-app`, `kafka`, `dapr-system`.
-   **DEP-002 (Services)**: Frontend, Backend, Recurring Task Service, and Notification Service MUST be deployed as Kubernetes Deployments with specified replicas and service types.
-   **DEP-003 (Kafka Deployment)**: Kafka (broker and Zookeeper) MUST be deployed on Minikube, preferably via Bitnami Helm chart or Strimzi operator.
-   **DEP-004 (Neon DB)**: The application MUST connect to an external Neon DB instance via the Dapr State Store component.
-   **DEP-005 (Helm Charts)**: All application components MUST be packaged as Helm charts (`todo-app-chart`, `kafka-chart`).
-   **DEP-006 (Resource Specs)**: All containers MUST define Kubernetes `resources` (requests and limits for memory and CPU).
-   **DEP-007 (Health Checks)**: All services MUST implement liveness, readiness, and startup probes (`/health/live`, `/health/ready`, `/health/startup`).
-   **DEP-008 (Dapr Sidecars)**: Dapr sidecars MUST be injected into relevant pods (e.g., Frontend for service invocation, Backend for Pub/Sub, State, Service Invocation, Jobs, Secrets).

### Key Entities

-   **Task**: Represents a single task with attributes like `title`, `description`, `status` (pending/completed), `priority` (High, Medium, Low), `tags` (array of strings), `dueDate`, `dueTime`, `isRecurring`, `recurrenceFrequency` (daily, weekly, monthly, yearly), `userId`.
-   **User**: Represents a user with attributes like `userId`, `username`, `email`, `sortPreference`.
-   **Conversation**: Represents a user's interaction with the chatbot.
-   **Message**: Represents a single message within a conversation.
-   **Tag**: Represents a categorization label for tasks.

## Dependencies and Assumptions

-   **External Services**: Reliance on external managed services for PostgreSQL (Neon DB).
-   **Dapr Runtime**: Assumption that the Dapr runtime is correctly installed and configured in the Kubernetes cluster (Minikube).
-   **Kafka Deployment**: Assumption that Kafka (Bitnami Helm chart or Strimzi) is deployed and operational in Minikube.
-   **Better Auth JWT**: Continued use of the existing Better Auth JWT validation for user authentication.
-   **Minikube Environment**: All development and testing will be conducted within a Minikube environment, mirroring production patterns as closely as possible.
-   **Chatbot Framework**: The existence of a chatbot framework (e.g., ChatKit) that can integrate with the backend for natural language processing.

## Success Criteria

### Measurable Outcomes

-   **SC-001**: Users can successfully create recurring tasks with any supported frequency (daily, weekly, monthly, yearly) and confirm the setting within 30 seconds.
-   **SC-002**: Upon completion of a recurring task, the next scheduled occurrence is automatically created and visible within 5 seconds.
-   **SC-003**: Reminder notifications are consistently delivered to users within 60 seconds of being due (1 hour before task due time).
-   **SC-004**: Users can filter tasks by any single or combination of criteria (status, priority, tags, due date range) and see results displayed within 2 seconds.
-   **SC-005**: Full-text searches across task titles and descriptions return relevant results within 3 seconds for datasets up to 10,000 tasks.
-   **SC-006**: Task sorting operations (by creation date, due date, priority, title) complete and re-render the list within 1 second.
-   **SC-007**: User sort preferences are persistently saved and automatically applied upon subsequent application access.
-   **SC-008**: All deployed services on Minikube maintain an uptime of 99.9% over a 24-hour period during local testing.
-   **SC-009**: All Kafka events (task mutations, reminders) are published and consumed without loss, and processed by consumers within 5 seconds of being produced.
-   **SC-010**: Dapr building blocks (Pub/Sub, State, Service Invocation, Jobs, Secrets) are correctly integrated and function as expected, as verified by Dapr metrics and logs.

## Out of Scope (Minikube Only, No Cloud)

-   ❌ DigitalOcean/Azure/GCP deployment
-   ❌ Ingress with real DNS/TLS
-   ❌ Horizontal Pod Autoscaling (HPA)
-   ❌ CI/CD pipeline (GitHub Actions)
-   ❌ Production monitoring (Prometheus/Grafana)
-   ✅ Focus: Everything running perfectly on local Minikube