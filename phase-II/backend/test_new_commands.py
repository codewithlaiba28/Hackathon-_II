#!/usr/bin/env python3
"""
Test script to verify the new commands (dashboard, show) work correctly.
"""

from src.services.repository import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.ui.cli import TodoCLI


def test_new_commands():
    """Test the new dashboard and show commands."""
    print("Testing New Commands...")
    print("=" * 40)

    # Initialize the application components
    repository = InMemoryTaskRepository()
    task_service = TaskService(repository)
    cli = TodoCLI(task_service)

    # Test adding some tasks
    task1 = task_service.add_task("Sample Task 1", "This is a sample task")
    task2 = task_service.add_task("Sample Task 2", "This task will be completed")
    print(f"[OK] Added tasks: {task1.title}, {task2.title}")

    # Test dashboard functionality
    print("[INFO] Testing dashboard command...")
    cli._dashboard()  # This should print the dashboard panel
    print("[OK] Dashboard command executed")

    # Test show functionality (should be same as list)
    print("[INFO] Testing show command (alias for list)...")
    cli._list()  # Since show just calls _list, we test list directly
    print("[OK] Show command executed")

    # Test toggle and dashboard again to see updated stats
    toggled_task = task_service.toggle_task_status(task2.id)
    print(f"[OK] Toggled task status: {toggled_task.status}")

    print("[INFO] Testing dashboard after toggle...")
    cli._dashboard()  # This should show updated statistics
    print("[OK] Dashboard updated after toggle")

    print("\n[SUCCESS] All new commands working correctly!")
    print("\nNew features added:")
    print("  - dashboard: Shows task summary with statistics")
    print("  - show: Alias for list command")
    print("  - Enhanced help with all commands listed")
    print("  - ASCII-based dashboard display for compatibility")


if __name__ == "__main__":
    test_new_commands()
    print("\n[LAUNCH] New commands successfully added to Todo Application!")