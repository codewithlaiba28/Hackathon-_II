# Implementation Plan: Phase 5 Advanced Cloud Deployment for the Todo Chatbot

**Branch**: `001-phase5-advanced-cloud` | **Date**: 2026-02-15 | **Spec**: [specs/001-phase5-advanced-cloud/spec.md](specs/001-phase5-advanced-cloud/spec.md)
**Input**: Feature specification from `/specs/001-phase5-advanced-cloud/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement advanced task management features (recurring tasks, due dates with reminders, priorities, tags, search, filter, sort) for the Todo Chatbot, leveraging an event-driven architecture with Kafka and Dapr on a Minikube-deployed Kubernetes cluster. The solution will involve updating existing backend services, creating new microservices (Recurring Task Service, Notification Service), and integrating with the Dapr distributed runtime and Kafka event streaming. Frontend updates will enable new UI elements and chatbot integration for these features.

## Technical Context

**Language/Version**: Python 3.13 (Backend services), JavaScript/TypeScript (Frontend - Next.js 16)  
**Primary Dependencies**: FastAPI, SQLModel, OpenAI Agents SDK, Next.js 16, Helm 3, Dapr 1.16+, Apache Kafka (Bitnami Helm Chart 30.x)  
**Storage**: Neon Serverless PostgreSQL (external) for core data, Dapr State Store (backed by PostgreSQL) for conversation history and task caching.  
**Testing**: `pytest` (Backend), `Jest`/`React Testing Library` (Frontend).  
**Target Platform**: Kubernetes (Minikube v1.33+)  
**Project Type**: Web application with distributed microservices architecture  
**Performance Goals**:
-   **SC-001**: Users can successfully create recurring tasks with any supported frequency (daily, weekly, monthly, yearly) and confirm the setting within 30 seconds.
-   **SC-002**: Upon completion of a recurring task, the next scheduled occurrence is automatically created and visible within 5 seconds.
-   **SC-003**: Reminder notifications are consistently delivered to users within 60 seconds of being due (1 hour before task due time).
-   **SC-004**: Users can filter tasks by any single or combination of criteria (status, priority, tags, due date range) and see results displayed within 2 seconds.
-   **SC-005**: Full-text searches across task titles and descriptions return relevant results within 3 seconds for datasets up to 10,000 tasks.
-   **SC-006**: Task sorting operations (by creation date, due date, priority, title) complete and re-render the list within 1 second.
**Constraints**:
-   Minikube-only deployment (no cloud, no production-grade monitoring/CI/CD).
-   Strict adherence to Dapr building blocks for inter-service communication, state management, and secrets.
-   Continued use of Better Auth JWT for user authentication.
-   All Kubernetes resources defined as Infrastructure as Code (Helm charts).
-   Stateless backend services.
**Scale/Scope**:
-   Designed for a single-user or small team Todo Chatbot.
-   Focus on functional completeness and robust local deployment patterns rather than massive horizontal scalability or enterprise-grade features.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **SPEC-FIRST RULE**: Passed. A detailed spec `specs/001-phase5-advanced-cloud/spec.md` was created.
-   **MCP-COMPLIANT ARCHITECTURE RULE**: Passed. Plan leverages MCP tools for backend interactions.
-   **MCP-AI INTEGRATION RULES**: Passed. Backend uses FastAPI/SQLModel, AI uses OpenAI Agents SDK, Frontend uses Next.js, all integrated with Dapr/Kafka.
-   **STATELESS AUTHENTICATION RULE**: Passed. Backend accepts JWT, conversation state in DB, services authenticate consistently.
-   **MCP TOOL SECURITY RULE**: Passed. MCP tools enforce user_id verification.
-   **PROJECT STRUCTURE RULE**: Passed. Plan adheres to the defined monorepo structure.
-   **SPEC-DRIVEN IMPLEMENTATION RULE**: Passed. This plan is derived directly from the spec.
-   **PRODUCTION QUALITY RULE**: Passed. Focus on logging, error handling, observability, scalability, resilience (within Minikube context).
-   **Cloud-Native Principles**: Passed. Embraces Kubernetes-First, Event-Driven, Local Development Parity, IaC, Observability.
-   **Dapr Integration Principles**: Passed. Adheres to Loose Coupling, Stateless Services (via Dapr State Store), Dapr Jobs API, Component Abstraction, Sidecar Pattern.
-   **Kafka Event Streaming Principles**: Passed. Follows Event-Driven, Topic Strategy, Event Schema, Consumer Groups, Local Kafka deployment.
-   **Deployment Principles**: Passed. Uses Helm Charts, Namespace Isolation, Resource Limits, Health Checks, Rolling Updates.
-   **Security Principles**: Passed. Includes Secrets Management, RBAC, Network Policies, JWT Authentication, Minimal Privileges.
-   **Development Workflow Principles**: Passed. Follows Spec-Driven, Incremental development, and leverages AI-assisted tools.
-   **Code Quality Principles**: Passed. Emphasizes Error Handling, Structured Logging, Async/Await patterns, Type Hints, and Documentation.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase5-advanced-cloud/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/           # SQLModel definitions
│   ├── services/         # Business logic, Dapr/Kafka interactions
│   ├── api/              # FastAPI endpoints, MCP tools
│   ├── routers/          # FastAPI routers
│   ├── utils/            # Utility functions
│   └── main.py           # FastAPI app entry
└── tests/                # Unit and integration tests

frontend/
├── src/
│   ├── components/       # React components
│   ├── pages/            # Next.js pages
│   ├── lib/              # Frontend utilities, API clients
│   └── app/              # Next.js App Router structure
└── tests/                # Frontend tests

mcp-servers/              # Potential Dapr-enabled MCP servers
kafka/                    # Kafka component definitions (Dapr, Helm)
dapr/                     # Dapr component definitions (YAML)
helm-charts/todo-app/     # Umbrella Helm chart
```

**Structure Decision**: The project will utilize a microservices-oriented structure with distinct `backend`, `frontend`, and new microservice directories within the existing monorepo. Dapr and Kafka configurations will reside in dedicated `dapr/` and `kafka/` directories respectively, and Helm charts will be managed under `helm-charts/todo-app/`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | N/A        | N/A                                 |
