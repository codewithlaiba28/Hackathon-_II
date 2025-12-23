<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Added sections: 6 principles based on AI Todo Chatbot architecture
- Templates requiring updates: ✅ All templates checked for alignment
- Follow-up TODOs: None
-->
# Todo AI Chatbot Constitution

## Core Principles

### I. Agent-First Architecture
Every feature starts with a designated agent responsibility; Agents must be purpose-driven with clearly defined skills and responsibilities; Each agent has a single, well-defined purpose in the system.

### II. Stateless Design
All application state must be persisted in the database; Servers hold no state between requests; Scalability and resilience are achieved through stateless server design with all data stored in Neon PostgreSQL DB.

### III. MCP-Driven Operations (NON-NEGOTIABLE)
All task operations must be exposed as MCP (Model Context Protocol) tools; Every user action maps to a specific MCP tool call; Tools must be standardized and well-defined (add_task, list_tasks, complete_task, delete_task, update_task).

### IV. Natural Language Processing Priority
User interactions must be processed through conversational AI; Intent extraction and understanding is the primary interface; All user commands must be interpretable through NLU capabilities.

### V. Layered Agent Architecture
System must implement a clear agent hierarchy: Conversational Agent → Task Planner Agent → MCP Tool Agent → Memory Agent → Error Handling Agent; Each layer has specific responsibilities and communication protocols.

### VI. Database-First State Management
All conversation and task data must be stored in Neon PostgreSQL DB; No in-memory state that can be lost; Memory Agent is responsible for all data persistence and retrieval operations.

## System Architecture Requirements

The system follows a clear architecture pattern: ChatKit UI → FastAPI Chat Endpoint → OpenAI Agents SDK → MCP Server → Neon PostgreSQL DB; Each layer communicates through well-defined interfaces; Scalable, resilient, and horizontally distributable design is mandatory.

## Development Workflow

All features must implement the agent-based architecture pattern; Each agent implementation requires clear skill definitions; MCP tool integration is mandatory for all task operations; State management must follow the database-first principle.

## Governance

This constitution supersedes all other development practices; All code reviews must verify compliance with agent-first architecture and stateless design principles; Complexity must be justified with clear architectural benefits; New features must align with the defined agent hierarchy and MCP tool requirements.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): Original adoption date unknown | **Last Amended**: 2025-12-22