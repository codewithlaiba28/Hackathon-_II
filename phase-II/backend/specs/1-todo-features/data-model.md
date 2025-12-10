# Data Model: Todo Application

## Task Entity

**Entity Name**: Task

**Fields**:
- `id` (int): Unique identifier, auto-incremented, required
- `title` (str): Task title, required, non-empty
- `description` (str): Task description, optional, can be empty string
- `status` (str): Task completion status, required, values: "Pending" or "Complete"

**Validation Rules**:
- ID must be unique within the system
- Title must be provided and not empty
- Status must be one of the allowed values
- ID must be positive integer

**State Transitions**:
- Initial state: "Pending" when task is created
- Transition: "Pending" ↔ "Complete" when toggled

## Task List Collection

**Entity Name**: TaskList

**Description**: Collection of Task entities managed by the repository

**Operations**:
- Add: Insert new Task with auto-generated unique ID
- Get All: Retrieve all tasks
- Get by ID: Retrieve specific task by ID
- Update: Modify existing task properties
- Delete: Remove task by ID
- Toggle Status: Switch between "Pending" and "Complete"