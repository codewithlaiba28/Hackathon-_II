"""Basic tests for the todo application components."""
from src.models.task import Task
from src.services.repository import InMemoryTaskRepository
from src.services.task_service import TaskService


def test_task_creation():
    """Test that tasks can be created with proper attributes."""
    task = Task(id=1, title="Test Task", description="Test Description", status="Pending")

    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "Pending"
    assert not task.is_complete


def test_task_validation():
    """Test that tasks validate their attributes."""
    # Test empty title validation
    try:
        Task(id=1, title="", description="Test Description", status="Pending")
        assert False, "Should have raised ValueError for empty title"
    except ValueError:
        pass

    # Test invalid status validation
    try:
        Task(id=1, title="Test Task", description="Test Description", status="Invalid")
        assert False, "Should have raised ValueError for invalid status"
    except ValueError:
        pass


def test_repository_operations():
    """Test basic repository operations."""
    repo = InMemoryTaskRepository()

    # Test adding a task
    task = Task(id=0, title="Test Task", description="Test Description", status="Pending")
    added_task = repo.add(task)

    assert added_task.id == 1  # First task should get ID 1
    assert added_task.title == "Test Task"

    # Test getting a task
    retrieved_task = repo.get(1)
    assert retrieved_task is not None
    assert retrieved_task.id == 1
    assert retrieved_task.title == "Test Task"

    # Test listing tasks
    tasks = repo.list()
    assert len(tasks) == 1
    assert tasks[0].id == 1


def test_task_service_operations():
    """Test basic task service operations."""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    # Test adding a task
    task = service.add_task("Test Title", "Test Description")
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.status == "Pending"

    # Test listing tasks
    tasks = service.list_tasks()
    assert len(tasks) == 1

    # Test toggling status
    toggled_task = service.toggle_task_status(1)
    assert toggled_task is not None
    assert toggled_task.status == "Complete"

    # Toggle back to pending
    toggled_task = service.toggle_task_status(1)
    assert toggled_task is not None
    assert toggled_task.status == "Pending"

    # Test updating a task
    updated_task = service.update_task(1, "New Title", "New Description")
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"

    # Test deleting a task
    result = service.delete_task(1)
    assert result is True

    # Verify task is gone
    tasks = service.list_tasks()
    assert len(tasks) == 0


if __name__ == "__main__":
    test_task_creation()
    test_task_validation()
    test_repository_operations()
    test_task_service_operations()
    print("All tests passed!")