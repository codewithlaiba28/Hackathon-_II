---
id: 1
title: Update Project Constitution
stage: constitution
date: 2025-12-22
surface: agent
model: claude-sonnet-4-5-20250929
feature: ai-todo-chatbot
branch: 001-ai-todo-chatbot
user: Claude User
command: /sp.constitution
labels: [constitution, architecture, agents, mcp]
links:
  spec: specs/001-ai-todo-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

  Architecture Overview:

ChatKit UI → FastAPI Chat Endpoint → OpenAI Agents SDK → MCP Server → Neon PostgreSQL DB


Agents & Sub-Agents:

Agent/Sub-Agent    Responsibility    Skills
Conversational Agent    Understand user messages & intent    NLU, intent extraction
Task Planner Agent    Map intent → MCP tool    Decision making
MCP Tool Agent  dd_task, list_tasks, complete_task, delete_task, update_task
Memory Agent    Fetch/store conversation & tasks    DB read/write
Error Handling Agent    Confirm actions & handle errors    Validation, friendly responses

Stateless Design:

Server holds l data in DB

Scalable, resilient, horizontally distributableno state, al  Execute MCP tools    a

## Response snapshot

Updated the project constitution to reflect the AI Todo Chatbot architecture. The new constitution includes 6 core principles based on the agent-first architecture:

1. Agent-First Architecture - Each feature starts with a designated agent responsibility
2. Stateless Design - All state persisted in database, no server state
3. MCP-Driven Operations - All operations as MCP tools (non-negotiable)
4. Natural Language Processing Priority - Conversational AI as primary interface
5. Layered Agent Architecture - Clear agent hierarchy and responsibilities
6. Database-First State Management - All data in Neon PostgreSQL DB

Also updated System Architecture Requirements, Development Workflow, and Governance sections to align with the agent-based architecture and MCP-driven approach. Version updated from 1.0.0 to 1.1.0 as this adds significant new architectural principles.

## Outcome

- ✅ Impact: Updated constitution with agent-based architecture principles
- 🧪 Tests: null
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Proceed with development following new architectural principles
- 🧠 Reflection: Constitution now properly reflects the AI Todo Chatbot architecture

## Evaluation notes (flywheel)

- Failure modes observed: null
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null