<!-- SYNC IMPACT REPORT
Version change: N/A → 1.0.0
Modified principles: N/A
Added sections: All principles based on Phase 2 Todo App constitution
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ⚠ pending
Follow-up TODOs: None
-->

# Todo App Constitution

## Core Principles

### SPEC-FIRST RULE
Every feature must be written in /specs before Claude generates code. No coding without a specification.

### CLEAN BACKEND RULE
Laiba will paste her own Python files into the backend folder. After she pastes backend code, Claude must remove any extra or unused backend files. Keep only required FastAPI files: main.py, db.py, models.py, schemas.py, auth.py, routers/. Automatically clean duplicates, unused modules, old migrations, or leftover folders.

### TECHNOLOGY RULES
Backend: FastAPI + SQLModel + JWT authentication. Frontend: Next.js App Router + Tailwind + Better Auth + fully responsive + beautiful UI + landing page.

### AUTH RULE
Backend must accept JWT from Better Auth. JWT must contain `sub = user_id`. All endpoints must require Authorization: Bearer <token>.

### SECURITY RULE
Each user may ONLY access their own tasks (backend must verify user_id).

### MONOREPO RULE
The structure must remain:
   /phase-2/
   ├─ specs/
   ├─ backend/
   ├─ frontend/
   └─ CLAUDE.md

### UPDATE RULE
Any time Laiba updates specifications, Claude must regenerate or refactor code accordingly.

### SIMPLICITY & BEAUTY RULE
Code, folder structure, API, and frontend must remain simple, readable, fully responsive, and visually beautiful. Frontend MUST include a landing page with a clear **"Go to Todo" button** linking to the Todo dashboard.

## Additional Constraints

The project must maintain a clean, organized structure with clear separation between frontend and backend. All code must follow modern best practices for the specified technologies. The application must be fully responsive and accessible.

## Development Workflow

All development must follow the spec-first approach where specifications are created in the /specs directory before any implementation work begins. Code reviews must verify compliance with all constitution principles. Testing should be comprehensive with unit, integration, and end-to-end tests where appropriate.

## Governance

This constitution governs all development activities for the Todo App project. All code generation and modifications must comply with these principles. Amendments to this constitution require explicit approval and must be documented with clear rationale. All pull requests and code reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2025-12-09 | **Last Amended**: 2025-12-09
