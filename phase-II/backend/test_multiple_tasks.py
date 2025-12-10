#!/usr/bin/env python3
"""Test script to verify multiple task functionality."""
from src.services.repository import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.ui.cli import TodoCLI

def test_multiple_task_addition():
    """Test that multiple tasks can be added via comma separation."""
    # Set up the service
    repository = InMemoryTaskRepository()
    task_service = TaskService(repository)
    cli = TodoCLI(task_service)

    # Simulate adding multiple tasks
    # We'll test the internal functionality by directly calling the method
    # that processes the comma-separated tasks

    # Add multiple tasks
    cli._add("Buy groceries, Finish Python assignment, Clean the room")

    # Check that all tasks were added
    tasks = task_service.list_tasks()

    print(f"Number of tasks created: {len(tasks)}")

    for task in tasks:
        print(f"Task ID: {task.id}, Title: '{task.title}', Status: {task.status}")

    # Verify we have 3 tasks
    assert len(tasks) == 3, f"Expected 3 tasks, but got {len(tasks)}"

    # Verify the task titles
    expected_titles = ["Buy groceries", "Finish Python assignment", "Clean the room"]
    actual_titles = [task.title for task in tasks]

    for expected in expected_titles:
        assert expected in actual_titles, f"Expected '{expected}' in tasks, but got {actual_titles}"

    print("[PASS] All tests passed! Multiple task addition works correctly.")

def test_single_task_addition():
    """Test that single task addition still works."""
    # Set up the service
    repository = InMemoryTaskRepository()
    task_service = TaskService(repository)
    cli = TodoCLI(task_service)

    # Add a single task - following the original format where first word is title, second is description
    cli._add("Single task")  # This will have "Single" as title and "task" as description

    # Check that the task was added
    tasks = task_service.list_tasks()

    assert len(tasks) == 1, f"Expected 1 task, but got {len(tasks)}"
    assert tasks[0].title == "Single", f"Expected 'Single', but got '{tasks[0].title}'"
    assert tasks[0].description == "task", f"Expected 'task', but got '{tasks[0].description}'"

    print("[PASS] Single task addition still works correctly.")

def test_single_task_with_quoted_title():
    """Test that single task with quoted title works."""
    # Set up the service
    repository = InMemoryTaskRepository()
    task_service = TaskService(repository)
    cli = TodoCLI(task_service)

    # Clear any existing tasks
    # We'll just create a fresh instance for this test
    repository = InMemoryTaskRepository()
    task_service = TaskService(repository)
    cli = TodoCLI(task_service)

    # Add a single task with quoted title to handle spaces
    cli._add('"Single task test"')

    # Check that the task was added
    tasks = task_service.list_tasks()

    assert len(tasks) == 1, f"Expected 1 task, but got {len(tasks)}"
    assert tasks[0].title == "Single task test", f"Expected 'Single task test', but got '{tasks[0].title}'"
    assert tasks[0].description == "", f"Expected empty description, but got '{tasks[0].description}'"

    print("[PASS] Single task with quoted title works correctly.")

if __name__ == "__main__":
    test_single_task_addition()
    test_single_task_with_quoted_title()
    test_multiple_task_addition()
    print("[PASS] All functionality tests passed!")