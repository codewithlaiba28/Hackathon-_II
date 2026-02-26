# Kafka Event Schemas

This document outlines the expected schemas for events published and consumed via Apache Kafka (leveraging Dapr Pub/Sub). These schemas ensure consistency and interoperability between microservices.

## 1. `task-events` Topic

This topic is used for events related to the lifecycle of a task.

### 1.1 `task.created` Event

Published when a new task is successfully created.

**Source:** Recurring Task Service, Backend Service
**Consumers:** Recurring Task Service (for parent task creation), Notification Service (for initial reminder setup)

```json
{
  "id": "integer (auto-generated)",
  "title": "string",
  "description": "string (optional)",
  "status": "string (enum: 'pending', 'completed')",
  "priority": "string (enum: 'High', 'Medium', 'Low')",
  "tags": "array of strings (optional)",
  "due_date": "datetime (ISO 8601 format, optional)",
  "reminder_offset_minutes": "integer (optional)",
  "is_recurring": "boolean",
  "recurring_frequency": "string (enum: 'daily', 'weekly', 'monthly', 'yearly', optional)",
  "recurrence_end_date": "datetime (ISO 8601 format, optional)",
  "parent_task_id": "integer (optional)",
  "user_id": "UUID (string)",
  "created_at": "datetime (ISO 8601 format)",
  "updated_at": "datetime (ISO 8601 format)"
}
```

**Corresponding Pydantic Schema (from `backend/schemas.py`):** `TaskResponse`

### 1.2 `task.completed` Event

Published when a task's status is changed to 'completed'.

**Source:** Backend Service
**Consumers:** Recurring Task Service (to potentially create a new occurrence)

```json
{
  "id": "integer",
  "title": "string",
  "description": "string (optional)",
  "status": "string (enum: 'completed')",
  "priority": "string (enum: 'High', 'Medium', 'Low')",
  "tags": "array of strings (optional)",
  "due_date": "datetime (ISO 8601 format, optional)",
  "reminder_offset_minutes": "integer (optional)",
  "is_recurring": "boolean",
  "recurring_frequency": "string (enum: 'daily', 'weekly', 'monthly', 'yearly', optional)",
  "recurrence_end_date": "datetime (ISO 8601 format, optional)",
  "parent_task_id": "integer (optional)",
  "user_id": "UUID (string)",
  "created_at": "datetime (ISO 8601 format)",
  "updated_at": "datetime (ISO 8601 format)"
}
```

**Corresponding Pydantic Schema (from `backend/schemas.py`):** `TaskResponse`

## 2. `reminders` Topic

This topic is used for scheduling and triggering task reminders.

### 2.1 `reminder.due` Event

Published when a reminder for a task becomes due. This event is typically triggered by the Dapr Jobs API scheduling mechanism.

**Source:** Dapr Jobs API (internally, via scheduled jobs)
**Consumers:** Notification Service

```json
{
  "task_id": "integer",
  "user_id": "UUID (string)",
  "title": "string",
  "description": "string (optional)",
  "due_date": "datetime (ISO 8601 format)",
  "reminder_time": "datetime (ISO 8601 format, the exact time the reminder is due)"
}
```