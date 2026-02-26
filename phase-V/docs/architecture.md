# Architecture Diagram

This document provides a high-level overview of the application's architecture using a Mermaid diagram.

```mermaid
graph TD
    subgraph User Interface
        F[Frontend: Next.js]
    end

    subgraph Backend Services
        B[Backend: FastAPI]
        R[Recurring Task Service: FastAPI]
        N[Notification Service: FastAPI]
    end

    subgraph Dapr Building Blocks
        DS[Dapr State Store: PostgreSQL]
        DPS[Dapr Pub/Sub: Kafka]
        DKS[Dapr Kubernetes Secrets]
    end

    subgraph Infrastructure
        K8S[Kubernetes Cluster]
        Kafka[(Apache Kafka)]
        PG(PostgreSQL Database: Neon)
    end

    F --> B: API Calls
    B --> DS: State Management (Tasks, Users)
    B --> DKS: Secrets Retrieval (API Keys)
    B --> DPS: Publish (task.created, task.completed)

    R --x DPS: Subscribe (task.completed)
    R --> DPS: Publish (task.created)
    R --> DS: Create Recurring Tasks

    N --x DPS: Subscribe (reminders)
    N --> User: Send Notifications (Placeholder)

    K8S --- B
    K8S --- R
    K8S --- N
    K8S --- F

    DPS --- Kafka
    DS --- PG
```