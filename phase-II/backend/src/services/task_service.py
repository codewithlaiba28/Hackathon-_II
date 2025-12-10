from typing import List, Optional
from src.models.task import Task
from src.services.repository import InMemoryTaskRepository


class TaskService:
    """Business logic layer for task management."""

    def __init__(self, repository: InMemoryTaskRepository):
        """Initialize the service with a repository.

        Args:
            repository: The task repository to use for data operations.
        """
        self.repository = repository

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Create a new task with the provided title and optional description.

        Args:
            title: The title of the task (required).
            description: The description of the task (optional).

        Returns:
            The created Task object with a unique ID and "Pending" status.

        Raises:
            ValueError: If the title is empty or None.
        """
        # Validate input
        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty")

        # Create task with initial status "Pending"
        task = Task(id=0, title=title.strip(), description=description or "", status="Pending")
        return self.repository.add(task)

    def list_tasks(self) -> List[Task]:
        """Retrieve all tasks, sorted by ID in ascending order.

        Returns:
            A list of all Task objects, sorted by ID.
        """
        return self.repository.list()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a specific task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The Task object if found, None otherwise.
        """
        return self.repository.get(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]:
        """Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: The new title for the task (optional).
            description: The new description for the task (optional).

        Returns:
            The updated Task object.

        Raises:
            ValueError: If the task doesn't exist or if the new title is empty.
        """
        # Check if task exists
        existing_task = self.repository.get(task_id)
        if existing_task is None:
            raise ValueError(f"Task with ID {task_id} does not exist")

        # Prepare updated task
        updated_title = title if title is not None else existing_task.title
        updated_description = description if description is not None else existing_task.description

        # Validate title if it's being updated
        if title is not None and (not title or not title.strip()):
            raise ValueError("Title cannot be empty")

        updated_task = Task(
            id=task_id,
            title=updated_title.strip() if updated_title else updated_title,
            description=updated_description,
            status=existing_task.status
        )

        return self.repository.update(task_id, updated_task)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was successfully deleted, False otherwise.

        Raises:
            ValueError: If the task doesn't exist.
        """
        if self.repository.get(task_id) is None:
            raise ValueError(f"Task with ID {task_id} does not exist")
        return self.repository.delete(task_id)

    def toggle_task_status(self, task_id: int) -> Optional[Task]:
        """Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated Task object with toggled status.

        Raises:
            ValueError: If the task doesn't exist.
        """
        task = self.repository.get(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} does not exist")
        return self.repository.toggle_status(task_id)