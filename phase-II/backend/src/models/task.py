from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a todo task with id, title, description, and status."""

    id: int
    title: str
    description: Optional[str] = ""
    status: str = "Pending"  # Either "Pending" or "Complete"

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title.strip():
            raise ValueError("Title cannot be empty")

        if self.status not in ["Pending", "Complete"]:
            raise ValueError("Status must be either 'Pending' or 'Complete'")

    @property
    def is_complete(self) -> bool:
        """Check if the task is complete."""
        return self.status == "Complete"

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.status = "Complete"

    def mark_pending(self) -> None:
        """Mark the task as pending."""
        self.status = "Pending"