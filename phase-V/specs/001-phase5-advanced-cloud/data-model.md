# Data Model for Phase 5 Advanced Cloud Deployment

## Entities

### User

Represents a user of the Todo Chatbot.

-   `userId`: Unique identifier for the user (Primary Key).
-   `username`: User's chosen username.
-   `email`: User's email address.
-   `sortPreference`: Stores the user's preferred task sorting order (e.g., `due_date_asc`, `priority_desc`).

### Task

Represents a single task managed by the user.

-   `id`: Unique identifier for the task (Primary Key).
-   `title`: Short description of the task.
-   `description`: Detailed description of the task (optional).
-   `status`: Current status of the task (`pending`, `completed`).
-   `priority`: Urgency level of the task (`High`, `Medium`, `Low`).
-   `tags`: Array of strings representing categories or labels for the task.
-   `dueDate`: Date when the task is due.
-   `dueTime`: Time when the task is due (optional, accompanies `dueDate`).
-   `isRecurring`: Boolean flag indicating if the task is recurring.
-   `recurrenceFrequency`: Frequency of recurrence if `isRecurring` is true (`daily`, `weekly`, `monthly`, `yearly`).
-   `parentTaskId`: Foreign Key referencing the `id` of the parent task for recurring task instances (optional).
-   `userId`: Foreign Key referencing the `userId` of the owner of the task.

### Conversation

Represents a continuous interaction session with the chatbot.

-   `id`: Unique identifier for the conversation (Primary Key).
-   `userId`: Foreign Key referencing the `userId` of the participant.
-   `startTime`: Timestamp when the conversation started.
-   `lastUpdateTime`: Timestamp of the last message in the conversation.

### Message

Represents a single message within a conversation.

-   `id`: Unique identifier for the message (Primary Key).
-   `conversationId`: Foreign Key referencing the `id` of the parent conversation.
-   `sender`: Role of the sender (`user`, `bot`).
-   `text`: Content of the message.
-   `timestamp`: Timestamp when the message was sent.

### Tag

Represents a categorization label for tasks.

-   (Implicitly handled as an array of strings within the `Task` entity for now. If more complex tag management is required in the future, it might become a separate entity with `tagId`, `name`, `userId`.)
