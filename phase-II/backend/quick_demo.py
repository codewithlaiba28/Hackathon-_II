#!/usr/bin/env python3
"""
Quick demo script to showcase the new features of the enhanced Todo application.
"""

from src.services.repository import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.ui.cli import TodoCLI


def quick_demo():
    """Demonstrate the new features."""
    print("Quick Demo: Enhanced Todo Application")
    print("=" * 50)
    print()

    # Initialize the application components
    repository = InMemoryTaskRepository()
    task_service = TaskService(repository)
    cli = TodoCLI(task_service)

    print("Adding sample tasks...")
    task1 = task_service.add_task("Complete project proposal", "Write and review the project proposal")
    task2 = task_service.add_task("Schedule team meeting", "Set up meeting for project discussion")
    task3 = task_service.add_task("Prepare presentation", "Create slides for the demo")
    print(f"   Added {len(task_service.list_tasks())} tasks")
    print()

    print("Testing dashboard command...")
    cli._dashboard()
    print()

    print("Toggling a task to 'Complete' status...")
    task_service.toggle_task_status(task1.id)
    print()

    print("Testing dashboard after toggle...")
    cli._dashboard()
    print()

    print("Testing show command (alias for list)...")
    cli._list()
    print()

    print("New features successfully demonstrated!")
    print("   - dashboard command: Shows task statistics")
    print("   - show command: Alias for list (both work)")
    print("   - ASCII-based UI for compatibility")
    print("   - Enhanced statistics and progress tracking")
    print()
    print("Run 'python src/main.py' to use the full application!")


if __name__ == "__main__":
    quick_demo()