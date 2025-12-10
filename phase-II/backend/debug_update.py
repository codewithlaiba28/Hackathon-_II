#!/usr/bin/env python3
"""
Debug script to understand the update command parsing.
"""

from src.services.repository import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.ui.cli import TodoCLI


def debug_update_command():
    """Debug the update command parsing."""
    print("Debugging Update Command...")
    print("=" * 40)

    # Initialize the application components
    repository = InMemoryTaskRepository()
    task_service = TaskService(repository)
    cli = TodoCLI(task_service)

    # Add a sample task
    task = task_service.add_task("Original Task", "Original description")
    print(f"Added task with ID: {task.id}")

    # Test the _parse_args method directly
    print(f"\nTesting _parse_args method:")
    result1 = cli._parse_args(f"{task.id} Updated Title")
    print(f"_parse_args('{task.id} Updated Title') = {result1}")

    result2 = cli._parse_args(f"tasks {task.id} Updated Title")
    print(f"_parse_args('tasks {task.id} Updated Title') = {result2}")

    # Test the internal logic of the update command
    print(f"\nTesting the fix logic:")
    args_with_tasks = f"tasks {task.id} Updated Title"
    print(f"args_with_tasks = '{args_with_tasks}'")

    if args_with_tasks.startswith('tasks '):
        subcommand_args = args_with_tasks[6:].strip()  # Remove 'tasks ' part
        print(f"After removing 'tasks ': '{subcommand_args}'")

        # Parse these args
        parts = cli._parse_args(subcommand_args)
        print(f"Parsed parts: {parts}")

        if parts:
            print(f"First part (potential ID): '{parts[0]}'")
            try:
                task_id = int(parts[0])
                print(f"Successfully converted to int: {task_id}")
            except ValueError:
                print(f"Failed to convert '{parts[0]}' to int - this is the problem!")


if __name__ == "__main__":
    debug_update_command()