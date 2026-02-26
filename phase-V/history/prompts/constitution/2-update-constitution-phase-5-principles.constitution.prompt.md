---
id: 2
title: Update Constitution Phase 5 Principles
stage: constitution
date: 2026-02-15
surface: agent
model: gemini-1.5-pro
feature: none
branch: null
user: Administrator
command: /sp.constitution /sp.constitution
labels: ["constitution", "phase-5", "cloud-deployment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:

---

## Prompt

/sp.constitution /sp.constitution

Create a Phase 5 constitution for Advanced Cloud Deployment with these principles:

## Cloud-Native Principles
1. **Kubernetes-First**: All deployments must be Kubernetes-native using proper manifests
2. **Event-Driven Architecture**: Use Kafka for async communication, Dapr for service integration
3. **Local Development Parity**: Minikube setup must mirror production patterns
4. **Infrastructure as Code**: All K8s resources defined in version-controlled YAML/Helm charts
5. **Observability**: Proper logging, health checks, and readiness probes

## Dapr Integration Principles
1. **Loose Coupling**: Services communicate via Dapr building blocks (Pub/Sub, State, Service Invocation)
2. **Stateless Services**: Use Dapr State Store for conversation/task state
3. **Jobs API**: Use Dapr Jobs API for scheduled reminders (not cron polling)
4. **Component Abstraction**: Dapr components in YAML, swappable without code changes
5. **Sidecar Pattern**: Every service gets a Dapr sidecar

## Kafka Event Streaming Principles
1. **Event-Driven**: All task mutations (create/update/delete/complete) publish events
2. **Topic Strategy**: Use topics: `task-events`, `reminders`, `task-updates`
3. **Event Schema**: Consistent event structure with type, task_id, user_id, timestamp
4. **Consumer Groups**: Proper consumer group naming for parallel processing
5. **Local Kafka**: Use Bitnami Kafka Helm chart or Strimzi operator on Minikube

## Deployment Principles
1. **Helm Charts**: Package everything as Helm charts for easy deployment
2. **Namespace Isolation**: Use dedicated namespaces (todo-app, kafka, dapr-system)
3. **Resource Limits**: Set memory/CPU requests and limits for all containers
4. **Health Checks**: Liveness and readiness probes for all services
5. **Rolling Updates**: Zero-downtime deployments with rolling update strategy

## Security Principles
1. **Secrets Management**: Use Kubernetes Secrets, never hardcode credentials
2. **RBAC**: Proper service accounts and role bindings
3. **Network Policies**: Restrict inter-pod communication
4. **JWT Authentication**: Maintain Better Auth JWT validation from Phase III
5. **Minimal Privileges**: Run containers as non-root users

## Development Workflow Principles
1. **Spec-Driven**: Follow /sp.specify → /sp.plan → /sp.tasks → /sp.implement
2. **Incremental**: Deploy to Minikube after each feature completion
3. **Docker AI (Gordon)**: Use for intelligent Docker operations when available
4. **kubectl-ai / Kagent**: Use for AI-assisted Kubernetes operations
5. **Testing**: Test locally on Minikube before considering cloud deployment

## Code Quality Principles
1. **Error Handling**: Graceful degradation, retry logic, circuit breakers
2. **Logging**: Structured logging with correlation IDs
3. **Async/Await**: Proper async patterns in Python FastAPI
4. **Type Hints**: Full type annotations in Python code
5. **Documentation**: README, architecture diagrams, deployment guides

## Response snapshot

The project constitution at `.specify/memory/constitution.md` has been updated to version 2.1.0, incorporating new principles for Cloud-Native, Dapr Integration, Kafka Event Streaming, Deployment, Security, Development Workflow, and Code Quality. The `LAST_AMENDED_DATE` has been set to 2026-02-15.

## Outcome

- ✅ Impact: The project constitution was updated to reflect new Phase 5 principles for advanced cloud deployment, Dapr, and Kafka integration.
- 🧪 Tests: No tests were executed as part of this constitution update.
- 📁 Files: The `.specify/memory/constitution.md` file was modified.
- 🔁 Next prompts: Review and update dependent templates (`plan-template.md`, `spec-template.md`, `tasks-template.md`, `commands/*.md`) for alignment.
- 🧠 Reflection: Successfully updated the constitution based on user-provided principles, ensuring version and date consistency. Noted required manual follow-ups for dependent templates.

## Evaluation notes (flywheel)

- Failure modes observed: The `create-phr.sh` script did not create a new PHR file as expected, requiring manual PHR creation.
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
