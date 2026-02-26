<!-- SYNC IMPACT REPORT
Version change: 2.0.0 → 2.1.0
Modified principles: Extensive update to align with user-provided Phase 5 Advanced Cloud Deployment principles.
Added sections: Cloud-Native Principles, Dapr Integration Principles, Kafka Event Streaming Principles, Deployment Principles, Security Principles, Development Workflow Principles, Code Quality Principles.
Removed sections: None (existing principles were integrated/retained).
Templates requiring updates:
  - .specify/templates/plan-template.md ⚠ pending (review for alignment)
  - .specify/templates/spec-template.md ⚠ pending (review for alignment)
  - .specify/templates/tasks-template.md ⚠ pending (review for alignment)
  - .specify/templates/commands/*.md ⚠ pending (review for alignment)
Follow-up TODOs: Manual review and update of dependent templates (.specify/templates/*.md) to ensure alignment with the new constitution principles.
-->

# Phase V – Advanced Cloud Deployment (Event-Driven, Dapr, Kafka) Constitution

## Purpose

Define global quality standards, architectural principles, and execution rules for building an advanced, event-driven AI Todo Chatbot with recurring tasks, due dates, reminders, and sophisticated features using Kafka, Dapr, and cloud deployment. The system must leverage Spec-Kit Plus and Claude Code for spec-driven development.

## Core Principles

### SPEC-FIRST RULE
Every feature must be written in /specs before Claude generates code. No coding without a specification. Specifications must include explicit tool contracts for MCP tools and clearly define intent mappings for AI agent behavior. All advanced features, event-driven architecture, and Dapr integration must be specified before implementation.

### MCP-COMPLIANT ARCHITECTURE RULE
All implementation must leverage Model Context Protocol (MCP) tools for database operations, business logic, and external service integrations. Claude must ensure all MCP tools have proper schemas, validation, and error handling. No direct database access from AI agents. MCP tools must integrate with event-driven architecture and Dapr services.

### MCP-AI INTEGRATION RULES
Backend: FastAPI + SQLModel + Neon PostgreSQL + MCP Server infrastructure. AI Logic: OpenAI Agents SDK with MCP tools. Frontend: Next.js App Router with MCP-powered chat interface. All components must integrate seamlessly with the MCP ecosystem, Kafka event streaming, and Dapr runtime.

### STATELESS AUTHENTICATION RULE
Backend must accept JWT from Better Auth. JWT must contain `sub = user_id`. All endpoints must require Authorization: Bearer <token>. All conversation state must persist in the database (no in-memory state). Sessions must be resumable after server restart. All services must authenticate consistently across the distributed system.

### MCP TOOL SECURITY RULE
Each user may ONLY access their own tasks through MCP tools (backend must verify user_id in all MCP tool calls). MCP tools must enforce proper authentication and authorization boundaries. No tool should allow cross-user data access. All Dapr services must maintain consistent security boundaries.

### PROJECT STRUCTURE RULE
The structure must remain:
   /phase-V/
   ├─ specs/
   ├─ backend/
   ├─ frontend/
   ├─ mcp-servers/
   ├─ kafka/
   ├─ dapr/
   ├─ k8s/
   ├─ helm/
   └─ CLAUDE.md

### SPEC-DRIVEN IMPLEMENTATION RULE
No manual coding is allowed; all implementation must occur via /sp.implement. Any updates to specifications must trigger corresponding code regeneration or refactoring through the Spec-Kit Plus workflow. All event-driven and Dapr integration specifications must follow the same process.

### PRODUCTION QUALITY RULE
Code, folder structure, API, and frontend must remain simple, readable, fully responsive, and production-ready. All MCP tools must include proper logging, error handling, and observability. System must support horizontal scalability with no in-memory state. All services must be resilient and fault-tolerant.

## Cloud-Native Principles
1. **Kubernetes-First**: All deployments must be Kubernetes-native using proper manifests.
   - Non-negotiable rule: Every component of the application must be designed and deployed to run natively on Kubernetes. This includes using Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets, etc.) or Helm charts for orchestration.
2. **Event-Driven Architecture**: Use Kafka for async communication, Dapr for service integration.
   - Non-negotiable rule: Asynchronous communication between microservices MUST be facilitated primarily through Kafka for event streaming and Dapr for robust service integration patterns.
3. **Local Development Parity**: Minikube setup must mirror production patterns.
   - Non-negotiable rule: The local development environment (e.g., using Minikube) MUST closely replicate the production Kubernetes environment, including Dapr and Kafka configurations, to ensure consistency and minimize "it works on my machine" issues.
4. **Infrastructure as Code**: All K8s resources defined in version-controlled YAML/Helm charts.
   - Non-negotiable rule: All Kubernetes resources, including deployments, services, Dapr components, and Kafka topics, MUST be defined as code (YAML manifests or Helm charts) and managed under version control.
5. **Observability**: Proper logging, health checks, and readiness probes.
   - Non-negotiable rule: Every deployed service MUST include structured logging, expose health checks (liveness and readiness probes), and emit metrics to ensure operational visibility.

## Dapr Integration Principles
1. **Loose Coupling**: Services communicate via Dapr building blocks (Pub/Sub, State, Service Invocation).
   - Non-negotiable rule: Services MUST interact through Dapr building blocks (e.g., Pub/Sub, State Management, Service Invocation) to ensure loose coupling and portability, avoiding direct service-to-service communication.
2. **Stateless Services**: Use Dapr State Store for conversation/task state.
   - Non-negotiable rule: Application services MUST remain stateless; any necessary conversational or task-specific state MUST be managed using the Dapr State Management building block.
3. **Jobs API**: Use Dapr Jobs API for scheduled reminders (not cron polling).
   - Non-negotiable rule: For scheduled operations like reminders, the Dapr Jobs API (or equivalent Dapr scheduling capabilities) MUST be utilized instead of traditional cron jobs or polling mechanisms.
4. **Component Abstraction**: Dapr components in YAML, swappable without code changes.
   - Non-negotiable rule: Dapr components (e.g., state stores, pub/sub brokers) MUST be defined externally in YAML configuration files, allowing them to be swapped without requiring application code changes.
5. **Sidecar Pattern**: Every service gets a Dapr sidecar.
   - Non-negotiable rule: All application services intended to use Dapr capabilities MUST be deployed with an accompanying Dapr sidecar container.

## Kafka Event Streaming Principles
1. **Event-Driven**: All task mutations (create/update/delete/complete) publish events.
   - Non-negotiable rule: Any mutation to a task (creation, update, deletion, completion) MUST trigger the publication of a corresponding event to Kafka.
2. **Topic Strategy**: Use topics: `task-events`, `reminders`, `task-updates`.
   - Non-negotiable rule: Kafka topics MUST be organized logically, specifically utilizing `task-events` for general task lifecycle events, `reminders` for reminder-related events, and `task-updates` for specific task attribute changes.
3. **Event Schema**: Consistent event structure with type, task_id, user_id, timestamp.
   - Non-negotiable rule: All events published to Kafka MUST adhere to a consistent schema, including essential fields such as `type`, `task_id`, `user_id`, and `timestamp`.
4. **Consumer Groups**: Proper consumer group naming for parallel processing.
   - Non-negotiable rule: Kafka consumers MUST belong to appropriately named consumer groups to enable parallel processing and ensure message delivery semantics.
5. **Local Kafka**: Use Bitnami Kafka Helm chart or Strimzi operator on Minikube.
   - Non-negotiable rule: For local development and testing with Minikube, Kafka MUST be deployed using either the Bitnami Kafka Helm chart or the Strimzi Kafka operator.

## Deployment Principles
1. **Helm Charts**: Package everything as Helm charts for easy deployment.
   - Non-negotiable rule: All application components, including services, Dapr configurations, and Kafka topics, MUST be packaged and deployed using Helm charts.
2. **Namespace Isolation**: Use dedicated namespaces (todo-app, kafka, dapr-system).
   - Non-negotiable rule: Deployments MUST utilize dedicated Kubernetes namespaces for logical isolation (e.g., `todo-app` for the application, `kafka` for Kafka components, `dapr-system` for Dapr infrastructure).
3. **Resource Limits**: Set memory/CPU requests and limits for all containers.
   - Non-negotiable rule: Every containerized service MUST define explicit memory and CPU requests and limits within its Kubernetes deployment configuration.
4. **Health Checks**: Liveness and readiness probes for all services.
   - Non-negotiable rule: All deployed services MUST implement both liveness and readiness probes to ensure Kubernetes can effectively manage their lifecycle and traffic routing.
5. **Rolling Updates**: Zero-downtime deployments with rolling update strategy.
   - Non-negotiable rule: Deployments MUST be configured to use a rolling update strategy to achieve zero-downtime application updates.

## Security Principles
1. **Secrets Management**: Use Kubernetes Secrets, never hardcode credentials.
   - Non-negotiable rule: Sensitive information and credentials MUST be managed using Kubernetes Secrets and NEVER hardcoded directly into configuration files or source code.
2. **RBAC**: Proper service accounts and role bindings.
   - Non-negotiable rule: Kubernetes Role-Based Access Control (RBAC) MUST be properly configured with dedicated service accounts and minimal necessary role bindings for all deployed components.
3. **Network Policies**: Restrict inter-pod communication.
   - Non-negotiable rule: Kubernetes Network Policies MUST be implemented to restrict unauthorized or unnecessary communication between pods.
4. **JWT Authentication**: Maintain Better Auth JWT validation from Phase III.
   - Non-negotiable rule: The system MUST continue to leverage and enforce the Better Auth JWT validation mechanisms established in Phase III for user authentication.
5. **Minimal Privileges**: Run containers as non-root users.
   - Non-negotiable rule: All containerized applications MUST be configured to run as non-root users with minimal necessary privileges.

## Development Workflow Principles
1. **Spec-Driven**: Follow /sp.specify → /sp.plan → /sp.tasks → /sp.implement.
   - Non-negotiable rule: All feature development MUST strictly adhere to the spec-driven workflow: `/sp.specify` for requirements, `/sp.plan` for architecture, `/sp.tasks` for detailed tasks, and `/sp.implement` for code generation.
2. **Incremental**: Deploy to Minikube after each feature completion.
   - Non-negotiable rule: After the completion of each significant feature or task, the changes MUST be deployed and tested on Minikube to ensure continuous integration and early detection of issues.
3. **Docker AI (Gordon)**: Use for intelligent Docker operations when available.
   - Non-negotiable rule: When available, AI tools like Docker AI (Gordon) SHOULD be utilized to optimize Dockerfile creation, image building, and container management.
4. **kubectl-ai / Kagent**: Use for AI-assisted Kubernetes operations.
   - Non-negotiable rule: When available, AI tools like `kubectl-ai` or `Kagent` SHOULD be leveraged for AI-assisted Kubernetes operations, manifest generation, and troubleshooting.
5. **Testing**: Test locally on Minikube before considering cloud deployment.
   - Non-negotiable rule: Comprehensive testing MUST be performed locally on Minikube to validate functionality, integration, and deployment before any consideration of cloud deployment.

## Code Quality Principles
1. **Error Handling**: Graceful degradation, retry logic, circuit breakers.
   - Non-negotiable rule: All services MUST implement robust error handling mechanisms, including graceful degradation, retry logic with exponential backoff, and circuit breakers for external dependencies.
2. **Logging**: Structured logging with correlation IDs.
   - Non-negotiable rule: All application and service logs MUST be structured (e.g., JSON format) and include correlation IDs for end-to-end traceability of requests.
3. **Async/Await**: Proper async patterns in Python FastAPI.
   - Non-negotiable rule: Python FastAPI services MUST utilize `async`/`await` patterns correctly for all asynchronous operations to ensure non-blocking I/O and optimal performance.
4. **Type Hints**: Full type annotations in Python code.
   - Non-negotiable rule: All Python code MUST include comprehensive type annotations to improve code readability, maintainability, and enable static analysis.
5. **Documentation**: README, architecture diagrams, deployment guides.
   - Non-negotiable rule: All repositories and significant components MUST include up-to-date documentation, including `README.md` files, architecture diagrams, and clear deployment guides.

## Global Rules

- Claude Code usage is MANDATORY for all phases.
- Claude Code Skills MUST be used where applicable.
- No manual coding; all implementation via /sp.implement.
- Stateless backend architecture is REQUIRED.
- All state must persist in the database (Neon PostgreSQL).
- Event-driven architecture must be implemented using Kafka.
- Dapr integration must follow all specified principles.
- Cloud deployment must follow Kubernetes best practices.

## Quality Standards

- Clear, testable specifications before implementation
- Explicit tool contracts for MCP tools
- Deterministic agent behavior for task operations
- Graceful error handling and user confirmation
- Production-ready security (JWT, auth boundaries)
- Horizontal scalability (no in-memory state)
- Proper containerization and orchestration standards
- Declarative infrastructure as code
- Event-driven architecture with Kafka
- Dapr integration following all specified principles
- Performance and reliability standards met

## AI Standards

- Use OpenAI Agents SDK for all AI logic
- Agent MUST use MCP tools (no direct DB access)
- Agent behavior MUST follow defined intent mappings
- Tool invocation MUST be logged and observable
- AI agents must interact with event-driven services appropriately
- MCP tools must be compatible with Dapr service invocation

## Success Criteria

- Advanced features (recurring tasks, due dates, reminders) work fully
- Event-driven architecture properly implemented with Kafka
- Dapr integration successful and follows all principles
- All filtering, search, and priority features work
- System passes event-driven request cycle validation
- Application deploys successfully with containerization
- Kubernetes manifests are properly configured
- Performance and reliability targets met
- Cloud deployment successful

## Non-Goals

- No manual UI logic for task parsing
- No frontend business logic duplication
- No state stored in memory or sessions
- No hardcoded infrastructure configurations
- No direct Kafka client usage (must use Dapr)
- No direct service-to-service calls (must use Dapr invocation)

## Additional Constraints

The project must maintain a clean, organized structure with clear separation between frontend, backend, MCP server, Kafka services, and Dapr components. All code must follow modern best practices for the specified technologies. The application must be fully responsive and accessible. MCP tools must be designed with explicit contracts and proper error handling. Containerization must follow Docker best practices, and Kubernetes manifests must adhere to established conventions. Event-driven architecture must be robust and fault-tolerant. Dapr integration must follow all specified principles.

## Development Workflow

All development must follow the spec-driven approach where specifications are created in the /specs directory before any implementation work begins. Code generation and MCP tool creation must comply with all constitution principles. Code reviews must verify compliance with all principles. Testing should be comprehensive with unit, integration, and end-to-end tests where appropriate, including MCP tool validation, event processing validation, and Dapr service integration testing. Container images must be scanned for security vulnerabilities, and Kubernetes deployments must be validated for best practices.

## Governance

This constitution governs all development activities for the Advanced Cloud Deployment project. All code generation, MCP tool creation, Kafka integration, Dapr integration, and modifications must comply with these principles. Amendments to this constitution require explicit approval and must be documented with clear rationale. All pull requests and code reviews must verify compliance with these principles.

**Version**: 2.1.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2026-02-15