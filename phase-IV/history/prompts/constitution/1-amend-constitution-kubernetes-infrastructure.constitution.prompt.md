---
id: 1
title: Amend Constitution Kubernetes Infrastructure
stage: constitution
date_iso: 2026-02-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels:
  - constitution
  - kubernetes
  - containerization
  - infrastructure-as-code
link_spec: null
link_ticket: null
link_adr: null
link_pr: null
files_yaml:
  - .specify/memory/constitution.md
tests_yaml: []
---

# Prompt

```
Add Phase 4 specific principles:
- Containerization standards using Docker best practices
- Kubernetes manifest conventions
- Helm chart structure and values management
- Local development with Minikube requirements
- Health checks and readiness probes
- Resource limits and requests standards
- Environment variable management
- Secrets and ConfigMaps usage patterns
- Service mesh considerations (if using Dapr) ## Infrastructure as Code Principles
1. All infrastructure must be declarative (YAML manifests)
2. Use Helm for templating and reusability
3. Environment-specific values must be externalized
4. No hardcoded credentials or endpoints
5. All services must have health checks
6. Resource limits must be defined for all containers

## Containerization Standards
1. Multi-stage Docker builds for optimization
2. Non-root user in containers
3. Minimal base images (alpine/distroless)
4. .dockerignore for build efficiency
5. Layer caching optimization
6. Security scanning before deployment

## Kubernetes Best Practices
1. Namespace isolation for different environments
2. Labels and annotations for resource organization
3. ConfigMaps for configuration
4. Secrets for sensitive data
5. Liveness and readiness probes
6. Resource requests and limits
7. Rolling update strategy
```

# Response

Updated the constitution file at `.specify/memory/constitution.md` to version 1.3.0, changing the project to Phase IV with containerization and Kubernetes focus. Added three new principle sections:

1. Infrastructure as Code Principles
2. Containerization Standards
3. Kubernetes Best Practices

Also updated the project structure rule to include k8s and helm directories, and updated quality standards, success criteria, non-goals, additional constraints, and development workflow to reflect containerization and orchestration requirements.

The updated constitution now governs the containerized AI chatbot project with proper standards for Docker, Kubernetes, and infrastructure as code practices.