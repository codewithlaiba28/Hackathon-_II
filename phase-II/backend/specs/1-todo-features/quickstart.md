# Quickstart Guide: Todo Application

## Prerequisites
- Python 3.13+
- pip package manager

## Setup
1. Clone the repository
2. Install dependencies: `pip install rich`
3. Run the application: `python src/main.py`

## Basic Usage
- Run `python src/main.py` to start the application
- Use the following commands:
  - `add "Task Title" "Optional Description"` - Add a new task
  - `list` - View all tasks in a formatted table
  - `update <id> "New Title" "Optional New Description"` - Update a task
  - `delete <id>` - Delete a task by ID
  - `toggle <id>` - Toggle task completion status
  - `export_html` - Generate HTML preview of tasks
  - `help` - Show available commands
  - `exit` - Exit the application

## Example Workflow
1. Start the app: `python src/main.py`
2. Add a task: `add "Buy groceries" "Milk, bread, eggs"`
3. View tasks: `list`
4. Mark as complete: `toggle 1`
5. Exit: `exit`

## Troubleshooting
- If you get import errors, ensure Rich library is installed: `pip install rich`
- If commands don't work, type `help` to see available commands