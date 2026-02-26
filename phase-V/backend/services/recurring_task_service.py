"""
Recurring Task Service for Advanced Todo Features

This module provides the service for handling recurring task logic,
including creation of new occurrences based on recurrence patterns.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlmodel import Session, select
from models import Task
from utils.cron_parser import calculate_next_occurrence, get_next_n_occurrences, is_recurrence_active
from utils.event_publisher import event_publisher, EventType
from utils.time_utils import utc_now
import logging
from enum import Enum


class RecurrenceValidationError(Exception):
    """Exception raised for recurrence validation errors."""
    pass


class RecurrenceAction(Enum):
    """Enum for different recurrence actions"""
    CREATE_NEXT_OCCURRENCE = "create_next_occurrence"
    UPDATE_EXISTING_SERIES = "update_existing_series"
    DELETE_SERIES = "delete_series"
    SKIP_OCCURRENCE = "skip_occurrence"


class RecurringTaskService:
    """Service for handling recurring task operations"""

    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.logger = logging.getLogger(__name__)

    def validate_recurrence_pattern(self, pattern: str) -> bool:
        """
        Validate a recurrence pattern.

        Args:
            pattern: Recurrence pattern string

        Returns:
            True if valid, False otherwise
        """
        from utils.cron_parser import parse_recurrence_pattern, validate_cron_expression

        parsed = parse_recurrence_pattern(pattern)
        if parsed:
            return True

        # If not a predefined pattern, check if it's a valid cron expression
        return validate_cron_expression(pattern)

    def create_recurring_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium",
        due_date: Optional[datetime] = None,
        reminder_offset_minutes: Optional[int] = None,
        recurrence_pattern: str = "daily",
        recurrence_end_date: Optional[datetime] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[Task]:
        """
        Create a new recurring task.

        Args:
            user_id: ID of the user creating the task
            title: Task title
            description: Task description
            priority: Task priority
            due_date: Due date for the task
            reminder_offset_minutes: Minutes before due date to send reminder
            recurrence_pattern: Pattern for recurrence
            recurrence_end_date: Date when recurrence should stop
            tags: List of tags for the task

        Returns:
            Created Task object or None if failed
        """
        # Validate recurrence pattern
        if not self.validate_recurrence_pattern(recurrence_pattern):
            raise RecurrenceValidationError(f"Invalid recurrence pattern: {recurrence_pattern}")

        # Create the initial recurring task
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            status="pending",
            priority=priority,
            due_date=due_date,
            reminder_offset_minutes=reminder_offset_minutes,
            is_recurring=True,
            recurrence_pattern=recurrence_pattern,
            recurrence_end_date=recurrence_end_date,
            parent_recurring_task_id=None  # This is the original recurring task
        )

        try:
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)

            # Publish event
            event_result = self.db_session.execute(
                select(Task).where(Task.id == task.id)
            ).scalar_one_or_none()

            if event_result:
                # Publish task created event
                # Since we can't await in this synchronous context, we'll just log it
                self.logger.info(f"Created recurring task {task.id} for user {user_id}")

            return task
        except Exception as e:
            self.db_session.rollback()
            self.logger.error(f"Error creating recurring task: {e}")
            return None

    def create_next_occurrence(self, original_task: Task) -> Optional[Task]:
        """
        Create the next occurrence of a recurring task.

        Args:
            original_task: The original recurring task

        Returns:
            New Task object representing the next occurrence or None if failed
        """
        # Check if recurrence is still active
        if not is_recurrence_active(
            original_task.recurrence_pattern,
            utc_now(),
            original_task.recurrence_end_date
        ):
            self.logger.info(f"Recurrence ended for task {original_task.id}")
            return None

        # Calculate next occurrence date
        if original_task.due_date:
            next_due_date = calculate_next_occurrence(
                original_task.recurrence_pattern,
                original_task.due_date
            )
        else:
            # If no due date, use current time as base
            next_due_date = calculate_next_occurrence(
                original_task.recurrence_pattern,
                utc_now()
            )

        if not next_due_date:
            self.logger.error(f"Could not calculate next occurrence for task {original_task.id}")
            return None

        # Create new task occurrence
        next_task = Task(
            user_id=original_task.user_id,
            title=original_task.title,
            description=original_task.description,
            status="pending",  # New occurrences start as pending
            priority=original_task.priority,
            due_date=next_due_date,
            reminder_offset_minutes=original_task.reminder_offset_minutes,
            is_recurring=True,
            recurrence_pattern=original_task.recurrence_pattern,
            recurrence_end_date=original_task.recurrence_end_date,
            parent_recurring_task_id=original_task.id  # Link to parent
        )

        try:
            self.db_session.add(next_task)
            self.db_session.commit()
            self.db_session.refresh(next_task)

            # Publish recurring task created event
            # In a real implementation, this would be awaited
            self.logger.info(f"Created next occurrence {next_task.id} for recurring task {original_task.id}")

            return next_task
        except Exception as e:
            self.db_session.rollback()
            self.logger.error(f"Error creating next occurrence for task {original_task.id}: {e}")
            return None

    def process_completed_recurring_task(self, task_id: int) -> bool:
        """
        Process a completed recurring task and create the next occurrence if needed.

        Args:
            task_id: ID of the completed task

        Returns:
            True if successful, False otherwise
        """
        # Get the completed task
        completed_task = self.db_session.get(Task, task_id)
        if not completed_task:
            self.logger.error(f"Task {task_id} not found")
            return False

        # Check if this is a recurring task
        if not completed_task.is_recurring:
            self.logger.info(f"Task {task_id} is not recurring, skipping recurrence processing")
            return True

        # If this is an occurrence (has a parent), get the original recurring task
        original_task_id = completed_task.parent_recurring_task_id or task_id
        original_task = self.db_session.get(Task, original_task_id)

        if not original_task or not original_task.is_recurring:
            self.logger.error(f"Original recurring task {original_task_id} not found or not recurring")
            return False

        # Create next occurrence
        next_occurrence = self.create_next_occurrence(original_task)
        if next_occurrence:
            self.logger.info(f"Created next occurrence {next_occurrence.id} for task {original_task_id}")
            return True
        else:
            self.logger.info(f"No next occurrence created for task {original_task_id} (recurrence may have ended)")
            return True

    def get_recurring_task_series(self, task_id: int) -> List[Task]:
        """
        Get all occurrences in a recurring task series.

        Args:
            task_id: ID of the original recurring task

        Returns:
            List of all tasks in the series
        """
        # First, check if this is the original recurring task or an occurrence
        task = self.db_session.get(Task, task_id)
        if not task:
            return []

        # If this is an occurrence, get the original task ID
        original_task_id = task.parent_recurring_task_id or task_id

        # Get all tasks that belong to this series (either the original or children)
        statement = select(Task).where(
            (Task.id == original_task_id) |
            (Task.parent_recurring_task_id == original_task_id)
        )
        series_tasks = self.db_session.exec(statement).all()

        return series_tasks

    def update_recurring_task_series(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[datetime] = None,
        reminder_offset_minutes: Optional[int] = None,
        recurrence_pattern: Optional[str] = None,
        recurrence_end_date: Optional[datetime] = None,
        update_future_occurrences: bool = True
    ) -> bool:
        """
        Update a recurring task series.

        Args:
            task_id: ID of the original recurring task or an occurrence
            title: New title
            description: New description
            priority: New priority
            due_date: New due date
            reminder_offset_minutes: New reminder offset
            recurrence_pattern: New recurrence pattern
            recurrence_end_date: New recurrence end date
            update_future_occurrences: Whether to update future occurrences

        Returns:
            True if successful, False otherwise
        """
        # Get the original recurring task
        task = self.db_session.get(Task, task_id)
        if not task:
            return False

        original_task_id = task.parent_recurring_task_id or task_id
        original_task = self.db_session.get(Task, original_task_id)

        if not original_task:
            self.logger.error(f"Original recurring task {original_task_id} not found")
            return False

        # Update the original task
        updates = {}
        if title is not None:
            updates['title'] = title
        if description is not None:
            updates['description'] = description
        if priority is not None:
            updates['priority'] = priority
        if due_date is not None:
            updates['due_date'] = due_date
        if reminder_offset_minutes is not None:
            updates['reminder_offset_minutes'] = reminder_offset_minutes
        if recurrence_pattern is not None:
            # Validate new pattern
            if not self.validate_recurrence_pattern(recurrence_pattern):
                raise RecurrenceValidationError(f"Invalid recurrence pattern: {recurrence_pattern}")
            updates['recurrence_pattern'] = recurrence_pattern
        if recurrence_end_date is not None:
            updates['recurrence_end_date'] = recurrence_end_date

        for field, value in updates.items():
            setattr(original_task, field, value)

        try:
            self.db_session.add(original_task)
            self.db_session.commit()

            # If updating future occurrences, we need to handle that logic
            # This is a simplified implementation - in a real app, you'd need to handle
            # updating upcoming occurrences based on the changes
            if update_future_occurrences:
                self.logger.info(f"Future occurrences will be affected by changes to task {original_task_id}")

            return True
        except Exception as e:
            self.db_session.rollback()
            self.logger.error(f"Error updating recurring task series: {e}")
            return False

    def delete_recurring_task_series(self, task_id: int, delete_all_occurrences: bool = True) -> bool:
        """
        Delete a recurring task series.

        Args:
            task_id: ID of the original recurring task or an occurrence
            delete_all_occurrences: Whether to delete all occurrences in the series

        Returns:
            True if successful, False otherwise
        """
        task = self.db_session.get(Task, task_id)
        if not task:
            return False

        original_task_id = task.parent_recurring_task_id or task_id

        if delete_all_occurrences:
            # Delete all occurrences in the series
            series_tasks = self.get_recurring_task_series(original_task_id)
            for series_task in series_tasks:
                self.db_session.delete(series_task)
        else:
            # Only delete the specific task
            self.db_session.delete(task)

        try:
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            self.logger.error(f"Error deleting recurring task series: {e}")
            return False

    def get_upcoming_recurring_tasks(self, user_id: str, days_ahead: int = 7) -> List[Task]:
        """
        Get recurring tasks that will have occurrences in the next N days.

        Args:
            user_id: ID of the user
            days_ahead: Number of days ahead to check

        Returns:
            List of recurring tasks that will generate occurrences
        """
        future_date = utc_now() + timedelta(days=days_ahead)

        # Get all recurring tasks for the user that are still active
        statement = select(Task).where(
            (Task.user_id == user_id) &
            (Task.is_recurring == True) &
            (Task.recurrence_end_date.is_(None) | (Task.recurrence_end_date >= utc_now()))
        )
        recurring_tasks = self.db_session.exec(statement).all()

        upcoming_tasks = []
        for task in recurring_tasks:
            # Check if this task will have occurrences in the next period
            if task.due_date:
                # If the task has a due date, calculate if it will recur soon
                next_occurrence = calculate_next_occurrence(
                    task.recurrence_pattern,
                    task.due_date
                )
                if next_occurrence and next_occurrence <= future_date:
                    upcoming_tasks.append(task)
            else:
                # If no due date, just check if recurrence is still active
                if is_recurrence_active(task.recurrence_pattern, utc_now(), task.recurrence_end_date):
                    upcoming_tasks.append(task)

        return upcoming_tasks

    def get_recurring_task_statistics(self, user_id: str) -> Dict[str, Any]:
        """
        Get statistics about recurring tasks for a user.

        Args:
            user_id: ID of the user

        Returns:
            Dictionary with recurring task statistics
        """
        statement = select(Task).where(
            (Task.user_id == user_id) &
            (Task.is_recurring == True)
        )
        all_recurring_tasks = self.db_session.exec(statement).all()

        stats = {
            "total_recurring_tasks": len(all_recurring_tasks),
            "patterns_used": {},
            "active_series": 0,
            "completed_occurrences": 0,
            "pending_occurrences": 0
        }

        for task in all_recurring_tasks:
            # Count patterns
            pattern = task.recurrence_pattern or "unknown"
            stats["patterns_used"][pattern] = stats["patterns_used"].get(pattern, 0) + 1

            # Check if series is still active
            if is_recurrence_active(task.recurrence_pattern, utc_now(), task.recurrence_end_date):
                stats["active_series"] += 1

        # Count occurrences (child tasks)
        child_statement = select(Task).where(
            (Task.user_id == user_id) &
            (Task.parent_recurring_task_id.is_not(None))
        )
        all_occurrences = self.db_session.exec(child_statement).all()

        for occurrence in all_occurrences:
            if occurrence.status == "completed":
                stats["completed_occurrences"] += 1
            else:
                stats["pending_occurrences"] += 1

        return stats


# Helper function to create the service with a session
def create_recurring_task_service(db_session: Session) -> RecurringTaskService:
    """
    Factory function to create a RecurringTaskService instance.

    Args:
        db_session: Database session to use

    Returns:
        RecurringTaskService instance
    """
    return RecurringTaskService(db_session)


if __name__ == "__main__":
    # Test the recurring task service
    print("Testing recurring task service...")

    # This would normally be tested with a real database session
    # For demonstration purposes, we'll just show the class structure

    print("RecurringTaskService class defined with methods:")
    print("- validate_recurrence_pattern()")
    print("- create_recurring_task()")
    print("- create_next_occurrence()")
    print("- process_completed_recurring_task()")
    print("- get_recurring_task_series()")
    print("- update_recurring_task_series()")
    print("- delete_recurring_task_series()")
    print("- get_upcoming_recurring_tasks()")
    print("- get_recurring_task_statistics()")

    print("Recurring task service test completed.")