from sqlmodel import Session, select
from dapr.clients import DaprClient
from ..models.task import Task # Assuming Task model is defined
from ..schemas import TaskCreate
from typing import List, Optional
from datetime import datetime, timedelta, UTC
import uuid

# Constants for Dapr PubSub
DAPR_PUBSUB_NAME = "kafka-pubsub" # As defined in dapr/components/kafka-pubsub.yaml
TASK_EVENTS_TOPIC = "task-events"

class RecurringTaskService:
    def __init__(self, session: Session, dapr_client: DaprClient):
        self.session = session
        self.dapr_client = dapr_client

    async def handle_task_completed_event(self, task_id: int):
        """
        Handles a task completed event, checks if it's a recurring task,
        and schedules the next occurrence.
        """
        # Placeholder for event handling logic
        print(f"RecurringTaskService: Handling completed task {task_id}")
        task = self.session.exec(select(Task).where(Task.id == task_id)).first()

        if task and task.is_recurring and task.recurrence_pattern:
            print(f"Task {task_id} is recurring. Scheduling next occurrence.")
            # Logic to calculate next due date
            next_due_date = self._calculate_next_due_date(task)
            
            if next_due_date:
                new_task_create = TaskCreate(
                    title=f"{task.title} (Next)",
                    description=task.description,
                    status="pending",
                    priority=task.priority,
                    tags=task.tags,
                    due_date=next_due_date,
                    is_recurring=True,
                    recurrence_pattern=task.recurrence_pattern,
                    parent_recurring_task_id=task.id, # Link to the original recurring task
                )
                await self._create_next_recurring_task(new_task_create, task.user_id)
        else:
            print(f"Task {task_id} is not recurring or frequency is not set.")

    def _calculate_next_due_date(self, task: Task) -> Optional[datetime]:
        """
        Calculates the next due date based on the recurrence pattern.
        """
        if not task.due_date:
            return None # Cannot calculate next due date without an initial one

        if task.recurrence_pattern == "daily":
            return task.due_date + timedelta(days=1)
        elif task.recurrence_pattern == "weekly":
            return task.due_date + timedelta(weeks=1)
        elif task.recurrence_pattern == "monthly":
            # Simple monthly increment for now, could be more complex (e.g., end of month)
            return task.due_date + timedelta(days=30) # Approx
        elif task.recurrence_pattern == "yearly":
            return task.due_date + timedelta(days=365) # Approx
        else:
            return None

    async def _create_next_recurring_task(self, task_create: TaskCreate, user_id: str):
        """
        Creates the next recurring task and publishes a task.created event.
        """
        from ..services.task_service import TaskService # Avoid circular import

        task_service = TaskService(self.session) # Create a new instance for this operation
        new_task = task_service.create_task(task_create, user_id)
        print(f"Created next recurring task: {new_task.title} (ID: {new_task.id})")

        # Publish task.created event via Dapr Pub/Sub
        await self.dapr_client.publish_event(
            pubsub_name=DAPR_PUBSUB_NAME,
            topic_name=TASK_EVENTS_TOPIC,
            data={"task_id": new_task.id, "user_id": str(new_task.user_id), "event_type": "task.created", "timestamp": datetime.now(UTC).isoformat()},
            data_content_type='application/json'
        )
        print(f"Published task.created event for task {new_task.id}")

# Other methods for recurring tasks will be added here
