# Data Model Design for Advanced Todo Features

## Enhanced Task Entity

### Fields
- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
  - Unique identifier for each task
  - Auto-generated sequence

- **user_id** (STRING, FOREIGN KEY)
  - References the user who owns the task
  - Indexed for performance

- **title** (STRING, NOT NULL)
  - Task title (1-200 characters)
  - Required field

- **description** (TEXT, OPTIONAL)
  - Detailed task description
  - Can be null

- **status** (STRING, DEFAULT 'pending')
  - Task status: 'pending', 'completed', 'in-progress'
  - Indexed for filtering

- **priority** (STRING, DEFAULT 'medium')
  - Task priority: 'low', 'medium', 'high', 'urgent'
  - Indexed for sorting and filtering

- **due_date** (TIMESTAMP WITH TIME ZONE, OPTIONAL)
  - Date and time when task is due
  - Supports timezone-aware storage

- **reminder_offset_minutes** (INTEGER, OPTIONAL)
  - Minutes before due_date to send reminder
  - Null if no reminder is set

- **is_recurring** (BOOLEAN, DEFAULT false)
  - Flag indicating if task is recurring
  - Indexed for performance

- **recurrence_pattern** (STRING, OPTIONAL)
  - Recurrence pattern (daily, weekly, monthly, custom cron)
  - Null if not recurring

- **recurrence_end_date** (TIMESTAMP WITH TIME ZONE, OPTIONAL)
  - Date when recurrence should stop
  - Null if no end date

- **parent_recurring_task_id** (INTEGER, FOREIGN KEY)
  - References parent recurring task
  - Null for original recurring task or non-recurring tasks

- **created_at** (TIMESTAMP WITH TIME ZONE, DEFAULT NOW())
  - Timestamp when task was created

- **updated_at** (TIMESTAMP WITH TIME ZONE, DEFAULT NOW())
  - Timestamp when task was last updated

### Relationships
- **User** (Many-to-One)
  - Task belongs to a single user
  - Foreign key: user_id → users.id

- **Parent Task** (Self-referencing Many-to-One)
  - Recurring task instances reference their parent
  - Foreign key: parent_recurring_task_id → tasks.id

- **Child Tasks** (One-to-Many)
  - Parent recurring task can have multiple instances
  - Reverse of parent relationship

## Task Tags Entity

### Fields
- **id** (INTEGER, PRIMARY KEY, AUTO_INCREMENT)
  - Unique identifier for each tag association

- **task_id** (INTEGER, FOREIGN KEY)
  - References the task this tag is associated with
  - Cascading delete when task is deleted

- **tag** (STRING, NOT NULL)
  - Tag value (e.g., "work", "work.meeting", "personal.health")
  - Length limited to 100 characters

- **created_at** (TIMESTAMP WITH TIME ZONE, DEFAULT NOW())
  - Timestamp when tag was added to task

### Relationships
- **Task** (Many-to-One)
  - Tag belongs to a single task
  - Foreign key: task_id → tasks.id

## Validation Rules

### Task Entity
- **Title**: Required, 1-200 characters
- **Description**: Optional, max 1000 characters
- **Priority**: Must be one of ['low', 'medium', 'high', 'urgent']
- **Due Date**: If set, must be a valid future date
- **Reminder Offset**: If set, must be positive number of minutes
- **Recurrence Pattern**: If is_recurring is true, pattern must be valid
- **Recurrence End Date**: If set, must be after the creation date
- **Parent Recurring Task ID**: Must reference an existing recurring task

### Task Tags Entity
- **Tag**: Required, 1-100 characters
- **Hierarchical Format**: Supports dot notation (e.g., "category.subcategory")
- **Uniqueness**: A task cannot have duplicate tags
- **Task Reference**: Must reference an existing task

## Indexes

### Primary Indexes
- **tasks.id**: Primary key index (auto-created)

### Secondary Indexes
- **idx_tasks_user_id**: Index on user_id for user-specific queries
- **idx_tasks_due_date**: Index on due_date for due date filtering
- **idx_tasks_priority**: Index on priority for priority-based sorting
- **idx_tasks_status**: Index on status for status filtering
- **idx_tasks_is_recurring**: Index on is_recurring for recurring task queries
- **idx_tasks_parent_recurring**: Index on parent_recurring_task_id for recurring task relationships

### Task Tags Indexes
- **idx_task_tags_task_id**: Index on task_id for task-specific tag queries
- **idx_task_tags_tag**: Index on tag for tag-based filtering
- **idx_task_tags_composite**: Composite index on (task_id, tag) for efficient joins

## State Transitions

### Task Status Transitions
- **pending** → **in-progress**: When user starts working on task
- **pending** → **completed**: When user marks task as complete
- **in-progress** → **completed**: When user finishes task
- **in-progress** → **pending**: When user decides to resume later
- **completed** → **pending**: When user reopens task

### Recurring Task Lifecycle
1. Original recurring task is created with recurrence pattern
2. When original/instance is completed, next occurrence is automatically created
3. New occurrence inherits all properties except:
   - Status (starts as 'pending')
   - Created/updated timestamps
   - Due date (adjusted according to recurrence pattern)
4. Recurrence continues until recurrence_end_date or user intervention

## Constraints

### Data Integrity
- Foreign key constraints to ensure referential integrity
- Check constraints for enum values (priority, status)
- Unique constraints where appropriate

### Business Logic
- A task cannot be both recurring and a child of another recurring task
- Due date must be set if reminder is configured
- Parent recurring task ID can only reference recurring tasks
- Recurrence pattern must be valid cron expression or predefined pattern

## Performance Considerations

### Query Optimization
- Most common queries should utilize indexes
- Consider materialized views for complex aggregations
- Pagination for large result sets

### Storage Efficiency
- Use appropriate data types to minimize storage
- Consider partitioning for large datasets
- Archive old completed tasks if needed