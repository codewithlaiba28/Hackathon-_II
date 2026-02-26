---
id: 002
title: AdvancedFeaturesPlan
stage: plan
date_iso: 2026-02-10
surface: agent
model: Claude Sonnet 4.5
feature: advanced-todo-features
branch: 005-advanced-todo-features
user: Claude Code
command: sp.plan
labels: ["planning", "architecture", "advanced-features", "dapr", "kafka"]
links:
  spec: specs/005-advanced-todo-features/spec.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - specs/005-advanced-todo-features/plan.md
  - specs/005-advanced-todo-features/research.md
  - specs/005-advanced-todo-features/data-model.md
  - specs/005-advanced-todo-features/contracts/task-api-contracts.md
  - specs/005-advanced-todo-features/quickstart.md
tests_yaml: []
---

# Advanced Todo Features Implementation Plan

## Prompt Text
Create implementation plan for Advanced Features:

**Technology Stack Updates**:
- Frontend: Next.js 16 (existing) + date-time picker component
- Backend: FastAPI (existing) + APScheduler for cron jobs
- Event Bus: Kafka on Minikube (Strimzi operator)
- Dapr: Version 1.16+ with all building blocks
- Database: Neon PostgreSQL (add columns for new fields)

**Database Schema Updates**:
```sql
-- Add to tasks table
ALTER TABLE tasks ADD COLUMN priority VARCHAR(10) DEFAULT 'medium';
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP WITH TIME ZONE;
ALTER TABLE tasks ADD COLUMN reminder_offset_minutes INTEGER;
ALTER TABLE tasks ADD COLUMN is_recurring BOOLEAN DEFAULT false;
ALTER TABLE tasks ADD COLUMN recurrence_pattern VARCHAR(50);
ALTER TABLE tasks ADD COLUMN parent_recurring_task_id INTEGER REFERENCES tasks(id);

CREATE TABLE task_tags (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    tag VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_task_tags_tag ON task_tags(tag);
CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
```

**Kafka Topics**:
- `task-events`: All CRUD operations
- `task-reminders`: Scheduled reminder events
- `task-recurring`: Recurring task creation events
- `task-search-index`: Search index updates

**Dapr Components Required**:
1. **Pub/Sub**: Kafka component for event streaming
2. **State Store**: PostgreSQL for conversation/cache
3. **Jobs API**: For scheduled reminders (replaces cron polling)
4. **Secrets**: For API keys and DB credentials
5. **Configuration**: For feature flags and settings

**New Microservices**:
1. **Reminder Service**: Consumes `task-reminders`, sends notifications
2. **Recurring Task Service**: Consumes `task-events`, creates next occurrence
3. **Search Indexer Service**: Consumes `task-events`, updates search index

**MCP Tools Updates**:
- `add_task`: Add parameters for priority, due_date, tags, recurrence
- `update_task`: Support updating priority, due_date, tags
- `list_tasks`: Add filters for priority, due_date, tags, search query
- `search_tasks`: New tool for full-text search

## Response Text
Successfully created a comprehensive implementation plan for the advanced todo features including:

1. **Technical Context**: Defined current and proposed architecture with identified unknowns requiring clarification

2. **Research Resolution**: Created research document addressing timezone handling, notification mechanisms, and cron job integration

3. **Data Model Design**: Created detailed data model with enhanced Task entity, TaskTags entity, validation rules, indexes, and state transitions

4. **API Contracts**: Created comprehensive API contract documentation with endpoints for all new features including recurring tasks, due dates, priorities, tags, and search functionality

5. **Implementation Strategy**: Defined phased implementation approach with risk mitigation and success metrics

6. **Quickstart Guide**: Created developer quickstart guide with setup instructions and usage examples

All components are aligned with the project constitution and follow event-driven architecture, Dapr integration, and performance principles.

## Outcome
Implementation plan complete with all required design artifacts. Ready for task breakdown and implementation phase.