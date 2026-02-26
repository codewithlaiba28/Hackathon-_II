<!-- SYNC IMPACT REPORT
Version change: 1.2.0 → 1.3.0
Modified principles: Updated project name to Phase IV and added containerization, Kubernetes, and infrastructure as code principles
Added sections: Infrastructure as Code Principles, Containerization Standards, Kubernetes Best Practices
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ✅ updated
Follow-up TODOs: None
-->

# Phase IV – Containerized AI Chatbot (Kubernetes, Infrastructure as Code) Constitution

## Purpose

Define global quality standards, architectural principles, and execution rules for building a stateless, MCP-powered AI Todo Chatbot using Spec-Kit Plus and Claude Code, deployed with containerization and Kubernetes orchestration.

## Core Principles

### SPEC-FIRST RULE
Every feature must be written in /specs before Claude generates code. No coding without a specification. Specifications must include explicit tool contracts for MCP tools and clearly define intent mappings for AI agent behavior.

### MCP-COMPLIANT ARCHITECTURE RULE
All implementation must leverage Model Context Protocol (MCP) tools for database operations, business logic, and external service integrations. Claude must ensure all MCP tools have proper schemas, validation, and error handling. No direct database access from AI agents.

### MCP-AI INTEGRATION RULES
Backend: FastAPI + SQLModel + Neon PostgreSQL + MCP Server infrastructure. AI Logic: OpenAI Agents SDK with MCP tools. Frontend: Next.js App Router with MCP-powered chat interface. All components must integrate seamlessly with the MCP ecosystem.

### STATELESS AUTHENTICATION RULE
Backend must accept JWT from Better Auth. JWT must contain `sub = user_id`. All endpoints must require Authorization: Bearer <token>. All conversation state must persist in the database (no in-memory state). Sessions must be resumable after server restart.

### MCP TOOL SECURITY RULE
Each user may ONLY access their own tasks through MCP tools (backend must verify user_id in all MCP tool calls). MCP tools must enforce proper authentication and authorization boundaries. No tool should allow cross-user data access.

### PROJECT STRUCTURE RULE
The structure must remain:
   /phase-IV/
   ├─ specs/
   ├─ backend/
   ├─ frontend/
   ├─ mcp-servers/
   ├─ k8s/
   ├─ helm/
   └─ CLAUDE.md

### SPEC-DRIVEN IMPLEMENTATION RULE
No manual coding is allowed; all implementation must occur via /sp.implement. Any updates to specifications must trigger corresponding code regeneration or refactoring through the Spec-Kit Plus workflow.

### PRODUCTION QUALITY RULE
Code, folder structure, API, and frontend must remain simple, readable, fully responsive, and production-ready. All MCP tools must include proper logging, error handling, and observability. System must support horizontal scalability with no in-memory state.

### INFRASTRUCTURE AS CODE PRINCIPLES
1. All infrastructure must be declarative (YAML manifests)
2. Use Helm for templating and reusability
3. Environment-specific values must be externalized
4. No hardcoded credentials or endpoints
5. All services must have health checks
6. Resource limits must be defined for all containers

### CONTAINERIZATION STANDARDS
1. Multi-stage Docker builds for optimization
2. Non-root user in containers
3. Minimal base images (alpine/distroless)
4. .dockerignore for build efficiency
5. Layer caching optimization
6. Security scanning before deployment

### KUBERNETES BEST PRACTICES
1. Namespace isolation for different environments
2. Labels and annotations for resource organization
3. ConfigMaps for configuration
4. Secrets for sensitive data
5. Liveness and readiness probes
6. Resource requests and limits
7. Rolling update strategy

## Global Rules

- Claude Code usage is MANDATORY for all phases.
- Claude Code Skills MUST be used where applicable.
- No manual coding; all implementation via /sp.implement.
- Stateless backend architecture is REQUIRED.
- All state must persist in the database (Neon PostgreSQL).

## Quality Standards

- Clear, testable specifications before implementation
- Explicit tool contracts for MCP tools
- Deterministic agent behavior for task operations
- Graceful error handling and user confirmation
- Production-ready security (JWT, auth boundaries)
- Horizontal scalability (no in-memory state)
- Proper containerization and orchestration standards
- Declarative infrastructure as code

## AI Standards

- Use OpenAI Agents SDK for all AI logic
- Agent MUST use MCP tools (no direct DB access)
- Agent behavior MUST follow defined intent mappings
- Tool invocation MUST be logged and observable

## Success Criteria

- Todo management works fully via natural language
- Conversations resume after server restart
- MCP tools correctly manage task lifecycle
- System passes stateless request cycle validation
- Application deploys successfully with containerization
- Kubernetes manifests are properly configured

## Non-Goals

- No manual UI logic for task parsing
- No frontend business logic duplication
- No state stored in memory or sessions
- No hardcoded infrastructure configurations

## Additional Constraints

The project must maintain a clean, organized structure with clear separation between frontend, backend, and MCP server components. All code must follow modern best practices for the specified technologies. The application must be fully responsive and accessible. MCP tools must be designed with explicit contracts and proper error handling. Containerization must follow Docker best practices, and Kubernetes manifests must adhere to established conventions.

## Development Workflow

All development must follow the spec-driven approach where specifications are created in the /specs directory before any implementation work begins. Code generation and MCP tool creation must comply with all constitution principles. Code reviews must verify compliance with all principles. Testing should be comprehensive with unit, integration, and end-to-end tests where appropriate, including MCP tool validation. Container images must be scanned for security vulnerabilities, and Kubernetes deployments must be validated for best practices.

## Governance

This constitution governs all development activities for the Todo AI Chatbot project. All code generation, MCP tool creation, and modifications must comply with these principles. Amendments to this constitution require explicit approval and must be documented with clear rationale. All pull requests and code reviews must verify compliance with these principles.

**Version**: 1.3.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2026-02-06