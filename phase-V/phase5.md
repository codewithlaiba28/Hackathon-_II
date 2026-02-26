# Phase V: Advanced Cloud Deployment

## Objective
Implement advanced features and deploy first on Minikube locally and then to production-grade Kubernetes.

## Core Requirements

### Part A: Advanced Features
*   **Advanced Level Features**:
    *   Recurring Tasks
    *   Due Dates & Reminders
*   **Intermediate Level Features**:
    *   Priorities
    *   Tags
    *   Search, Filter, Sort
*   **Event-Driven Architecture**:
    *   Use Dapr for distributed application runtime.
    *   **Modification**: Use **Redis** for Pub/Sub instead of Kafka for the initial implementation/simplicity, as per user instruction.
*   **Dapr Integration**:
    *   Pub/Sub
    *   State Management
    *   Bindings (cron)
    *   Secrets
    *   Service Invocation

### Part B: Local Deployment
*   Deploy to **Minikube**.
*   Deploy Dapr on Minikube with full components (Pub/Sub, State, Bindings, Secrets, Service Invocation).

### Part C: Cloud Deployment (Future)
*   Deploy to Azure (AKS) / Google Cloud (GKE).
*   Deploy Dapr on GKE/AKS.
*   Use Kafka (Confluent/Redpanda) or Dapr PubSub.
*   CI/CD with Github Actions.
*   Monitoring and Logging.

## Architecture Overview
*   **Frontend**: Next.js
*   **Backend**: FastAPI
*   **Middleware/Runtime**: Dapr
*   **Message Broker**: Redis (Local), Kafka (Prod/Cloud)
*   **Database**: Neon DB (Postgres) / Local Postgres
