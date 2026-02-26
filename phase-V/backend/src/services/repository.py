from typing import Dict, List, Optional
from src.models.task import Task


class InMemoryTaskRepository:
    """In-memory repository for managing tasks."""

    def __init__(self):
        """Initialize the repository with an empty task collection and ID counter."""
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add(self, task: Task) -> Task:
        """Add a new task to the repository with an auto-generated ID."""
        task_id = self._next_id
        self._next_id += 1
        task.id = task_id
        self._tasks[task_id] = task
        return task

    def get(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)

    def list(self) -> List[Task]:
        """Retrieve all tasks, sorted by ID in ascending order."""
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def update(self, task_id: int, updated_task: Task) -> Optional[Task]:
        """Update an existing task."""
        if task_id not in self._tasks:
            return None
        # Preserve the original ID
        updated_task.id = task_id
        self._tasks[task_id] = updated_task
        return updated_task

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID."""
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

    def toggle_status(self, task_id: int) -> Optional[Task]:
        """Toggle the completion status of a task."""
        task = self._tasks.get(task_id)
        if task is None:
            return None

        if task.status == "Pending":
            task.status = "Complete"
        else:
            task.status = "Pending"

        return task