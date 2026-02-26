# Research Findings for Phase 5 Advanced Cloud Deployment

## Decision: Frontend Testing Frameworks

- **What was chosen**: `Jest` for JavaScript testing framework and `React Testing Library` for testing React components.
- **Rationale**: These are standard choices for Next.js applications, offering robust features for unit, integration, and UI testing in a React environment. They align with modern best practices for testing frontend applications.
- **Alternatives considered**: Cypress (for E2E testing, but not needed for initial unit/integration focus), Enzyme (older React testing utility, less aligned with modern React practices).

## Decision: Scale/Scope for Todo Chatbot

- **What was chosen**: Initial development targets a single-user or small team Todo Chatbot.
- **Rationale**: This scope allows for focused development on the core advanced features and the complex distributed architecture patterns (Dapr, Kafka, Kubernetes) without immediate concern for extreme horizontal scalability or enterprise-level user management complexities. It aligns with the "Minikube-only, no cloud" constraint for this phase.
- **Alternatives considered**: Designing for large-scale enterprise usage from the outset (rejected due to increased complexity, cost, and deviation from current phase focus).

