# Task API Contracts

## Task Creation Contract

**Endpoint**: CLI command `add`
**Input**: title (string, required), description (string, optional)
**Output**: Task object with id, title, description, status
**Success Response**:
- Status: Created task with unique ID
- Format: Task object with all fields populated
**Error Response**:
- Invalid input: Error message prompting for valid input

## Task Listing Contract

**Endpoint**: CLI command `list`
**Input**: None
**Output**: Array of Task objects
**Success Response**:
- Status: List of all tasks in formatted table
- Format: Table with ID, Title, Description, Status columns

## Task Update Contract

**Endpoint**: CLI command `update <id>`
**Input**: task ID (int, required), new title (string, optional), new description (string, optional)
**Output**: Updated Task object
**Success Response**:
- Status: Updated task object with changes applied
- Format: Task object with updated fields

## Task Deletion Contract

**Endpoint**: CLI command `delete <id>`
**Input**: task ID (int, required)
**Output**: Deletion confirmation
**Success Response**:
- Status: Confirmation that task was deleted
- Format: Success message with task ID

## Task Toggle Contract

**Endpoint**: CLI command `toggle <id>`
**Input**: task ID (int, required)
**Output**: Task object with toggled status
**Success Response**:
- Status: Task with completion status flipped
- Format: Task object with updated status