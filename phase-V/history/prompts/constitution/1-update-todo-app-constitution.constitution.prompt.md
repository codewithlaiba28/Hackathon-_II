---
id: 1
title: Update Todo App Constitution
stage: constitution
date: 2025-12-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Laiba Khan
command: /sp.constitution
labels: [constitution, todo-app, phase-2]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
 # Phase 2 – Constitution (Todo App)

This constitution defines how all code must be generated and maintained during Phase 2.
Claude AI MUST follow these rules strictly:

1. SPEC-FIRST RULE
   Every feature must be written in /specs before Claude generates code.
   No coding without a specification.

2. CLEAN BACKEND RULE (IMPORTANT BY LAIBA KHAN)
   Laiba will paste her own Python files into the backend folder.
   AFTER she pastes backend code, Claude MUST:
   - Remove any extra or unused backend files.
   - Keep only required FastAPI files: main.py, db.py, models.py, schemas.py, auth.py, routers/.
   - Automatically clean duplicates, unused modules, old migrations, or leftover folders.

3. TECHNOLOGY RULES
   - Backend: FastAPI + SQLModel + JWT authentication.
   - Frontend: Next.js App Router + Tailwind + Better Auth + fully responsive + beautiful UI + landing page.

4. AUTH RULE
   Backend must accept JWT from Better Auth.
   JWT must contain `sub = user_id`.
   All endpoints must require Authorization: Bearer <token>.

5. SECURITY RULE
   Each user may ONLY access their own tasks (backend must verify user_id).

6. MONOREPO RULE
   The structure must remain:
      /phase-2/
      ├─ specs/
      ├─ backend/
      ├─ frontend/
      └─ CLAUDE.md

7. UPDATE RULE
   Any time Laiba updates specifications, Claude must regenerate or refactor code accordingly.

8. SIMPLICITY & BEAUTY RULE
   Code, folder structure, API, and frontend must remain simple, readable, fully responsive, and visually beautiful.
   Frontend MUST include a landing page with a clear **"Go to Todo" button** linking to the Todo dashboard.
```

## Response snapshot

Updated the constitution file with the specific rules and principles for the Phase 2 Todo App project. The new constitution includes 8 core principles covering spec-first development, clean backend maintenance, technology stack requirements, authentication rules, security requirements, monorepo structure, update procedures, and simplicity/beauty standards. The constitution now serves as the authoritative guide for all development activities in the project.

## Outcome

- ✅ Impact: Updated project constitution with specific Phase 2 Todo App rules
- 🧪 Tests: none required for constitution update
- 📁 Files: Modified .specify/memory/constitution.md with new principles
- 🔁 Next prompts: Development should now follow the new constitution guidelines
- 🧠 Reflection: Constitution now properly reflects the project requirements and will guide all future development

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not applicable
- Prompt variant (if applicable): not applicable
- Next experiment (smallest change to try): begin implementing features following the new constitution