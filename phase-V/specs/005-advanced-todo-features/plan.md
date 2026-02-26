# Advanced Todo Features Implementation Plan

## Technical Context

### Current Architecture
- **Frontend**: Next.js 16 with ChatKit
- **Backend**: FastAPI with SQLModel ORM
- **Database**: Neon PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Event System**: Planned Kafka integration
- **Service Mesh**: Planned Dapr integration

### Proposed Architecture
- **Frontend**: Next.js 16 + date-time picker component
- **Backend**: FastAPI + APScheduler for cron jobs
- **Event Bus**: Kafka on Minikube (Strimzi operator)
- **Dapr**: Version 1.16+ with all building blocks
- **Database**: Neon PostgreSQL (enhanced schema)

### Unknowns Requiring Clarification
- **NEEDS CLARIFICATION**: How will the timezone handling be implemented across frontend and backend?
- **NEEDS CLARIFICATION**: What specific notification mechanism will be used for reminders?
- **NEEDS CLARIFICATION**: How will the cron job scheduling be integrated with the existing FastAPI backend?

## Constitution Check

### Core Principles Compliance
- **SPEC-FIRST RULE**: All features specified in spec.md before implementation
- **MCP-COMPLIANT ARCHITECTURE**: MCP tools will be updated to handle new fields
- **STATELESS AUTHENTICATION**: Authentication remains JWT-based and stateless
- **ADVANCED FEATURE PRINCIPLES**: All requirements met (recurring tasks, due dates, priorities, tags, search)
- **EVENT-DRIVEN ARCHITECTURE PRINCIPLES**: Kafka integration for all state changes
- **DAPR INTEGRATION PRINCIPLES**: Following Dapr building blocks approach
- **PERFORMANCE & RELIABILITY PRINCIPLES**: Database indexes and proper error handling

### Gates Assessment
- [ ] All constitution principles satisfied
- [ ] No conflicts with existing architecture decisions
- [ ] Performance requirements achievable with proposed approach

## Phase 0: Research & Resolution

### Research Tasks

#### 1. Timezone Handling Research
**Decision**: Implement timezone handling using UTC storage in database with client-side conversion
**Rationale**: This follows industry best practices for handling timezones in distributed systems
**Alternatives considered**:
- Store in local timezones (problematic for data consistency)
- Server-side timezone conversion (increases server complexity)

#### 2. Notification Mechanism Research
**Decision**: Use WebSocket connections for real-time notifications with fallback to email/SMS
**Rationale**: Provides real-time experience for users while maintaining reliability
**Alternatives considered**:
- Polling mechanism (inefficient and high-latency)
- Push notifications via third-party service (dependency concerns)

#### 3. Cron Job Integration Research
**Decision**: Use APScheduler integrated with FastAPI and coordinated via Dapr Jobs API
**Rationale**: Combines Python's mature scheduling with Dapr's distributed coordination
**Alternatives considered**:
- Separate cron service (adds complexity)
- Database polling approach (inefficient)

## Phase 1: Design & Architecture

### Data Model Design

#### Enhanced Task Entity
```sql
-- Enhanced tasks table
ALTER TABLE tasks ADD COLUMN priority VARCHAR(10) DEFAULT 'medium';
ALTER TABLE tasks ADD COLUMN due_date TIMESTAMP WITH TIME ZONE;
ALTER TABLE tasks ADD COLUMN reminder_offset_minutes INTEGER;
ALTER TABLE tasks ADD COLUMN is_recurring BOOLEAN DEFAULT false;
ALTER TABLE tasks ADD COLUMN recurrence_pattern VARCHAR(50);
ALTER TABLE tasks ADD COLUMN parent_recurring_task_id INTEGER REFERENCES tasks(id);

-- Task tags junction table
CREATE TABLE task_tags (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    tag VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_priority ON tasks(priority);
CREATE INDEX idx_task_tags_tag ON task_tags(tag);
CREATE INDEX idx_task_tags_task_id ON task_tags(task_id);
```

#### Entity Relationships
- **Task** (1) → (0..*) **TaskTag** (Many-to-Many relationship via junction table)
- **Task** (1) → (0..*) **Task** (Parent-child relationship for recurring tasks)

### API Contract Design

#### New Endpoints
```
POST /api/{user_id}/tasks/recurring
  Request: {title, description, recurrence_pattern, ...}
  Response: {task, next_occurrence}

PUT /api/{user_id}/tasks/{task_id}/due-date
  Request: {due_date, reminder_offset_minutes}
  Response: {task}

GET /api/{user_id}/tasks/search
  Query: {q, priority, tag, status, due_date_from, due_date_to}
  Response: {tasks[], total_count, page_info}

GET /api/{user_id}/tasks/sort
  Query: {sort_by, order, filters...}
  Response: {tasks[]}
```

#### Updated MCP Tool Contracts
```python
# Enhanced MCP tools
add_task(user_id: str, title: str, description: str, priority: str, due_date: str, tags: List[str], recurrence_pattern: str) -> Dict
update_task(user_id: str, task_id: int, priority: str, due_date: str, tags: List[str]) -> Dict
list_tasks(user_id: str, priority: str, tag: str, due_date_range: Tuple, status: str) -> List[Dict]
search_tasks(user_id: str, query: str, filters: Dict) -> List[Dict]
```

### Dapr Component Configuration

#### 1. Pub/Sub Component (Kafka)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka:9092"
  - name: consumerGroup
    value: "todo-service"
```

#### 2. State Store Component (PostgreSQL)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgresql-state
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "postgresql://user:password@postgres:5432/todo_db"
```

#### 3. Secret Store Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kubernetes-secrets
spec:
  type: secretstores.kubernetes
  version: v1
```

### Kafka Topic Design

#### Topic Specifications
- **task-events**: All CRUD operations on tasks (partitioned by user_id)
- **task-reminders**: Scheduled reminder events (partitioned by reminder_time)
- **task-recurring**: Recurring task creation events (partitioned by recurrence_pattern)
- **task-search-index**: Search index updates (partitioned by task_id)

### Microservices Architecture

#### 1. Reminder Service
- **Responsibility**: Process reminder events and send notifications
- **Technology**: Python/FastAPI with Dapr sidecar
- **Triggers**: Kafka consumer for `task-reminders` topic
- **Outputs**: WebSocket notifications, email/SMS as fallback

#### 2. Recurring Task Service
- **Responsibility**: Process recurring task events and create new occurrences
- **Technology**: Python/FastAPI with Dapr sidecar
- **Triggers**: Kafka consumer for `task-recurring` topic
- **Outputs**: New task records in database

#### 3. Search Indexer Service
- **Responsibility**: Update search index based on task changes
- **Technology**: Python/FastAPI with Dapr sidecar
- **Triggers**: Kafka consumer for `task-search-index` topic
- **Outputs**: Updated search index

## Phase 2: Implementation Strategy

### Implementation Order
1. **Database Schema Updates** - Add new fields and tables
2. **Backend API Extensions** - Update FastAPI endpoints
3. **MCP Tool Enhancements** - Update existing tools and add new ones
4. **Event Infrastructure** - Set up Kafka and Dapr
5. **Microservices** - Implement reminder, recurring, and search services
6. **Frontend Updates** - Add UI components for new features
7. **Integration Testing** - End-to-end testing of all features

### Risk Mitigation
- **Database Migration Risk**: Implement gradual schema changes with rollback capability
- **Event Processing Risk**: Implement dead letter queues and retry mechanisms
- **Performance Risk**: Monitor query performance and optimize indexes
- **Notification Reliability**: Implement multiple delivery mechanisms with fallbacks

### Success Metrics
- Recurring tasks generate next occurrence with 99.9% reliability
- Reminders delivered within 5 minutes of scheduled time (95% of cases)
- Search operations complete in under 1 second (95% of queries)
- System maintains sub-200ms response times under normal load

## Phase 3: Deployment Strategy

### Local Development Setup
- Minikube cluster with Kafka (via Strimzi operator)
- Dapr runtime installed and initialized
- Helm charts for all services
- Local PostgreSQL for development

### Cloud Deployment
- AKS/GKE cluster preparation
- Managed Kafka service (Confluent Cloud or Redpanda)
- Dapr production configuration
- Monitoring and observability setup

### Rollout Plan
1. **Phase 1**: Deploy database schema changes
2. **Phase 2**: Deploy backend API extensions
3. **Phase 3**: Deploy event infrastructure and microservices
4. **Phase 4**: Deploy frontend updates
5. **Phase 5**: Full system integration and testing

## Quality Assurance

### Testing Strategy
- Unit tests for all new components
- Integration tests for event processing
- End-to-end tests for user workflows
- Performance tests for search and filtering
- Chaos engineering for resilience testing

### Monitoring & Observability
- Distributed tracing across services
- Metrics for event processing rates
- Alerts for failed reminders or recurring tasks
- Performance dashboards for search and filtering

## Post-Design Constitution Check
- [x] All constitution principles satisfied
- [x] Event-driven architecture principles followed
- [x] Dapr integration principles adhered to
- [x] Performance & reliability principles addressed
- [x] No conflicts with existing architecture decisions