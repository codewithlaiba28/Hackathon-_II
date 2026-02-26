from fastapi import FastAPI, Depends, HTTPException, status
from dapr.clients import DaprClient
from dapr.ext.fastapi import DaprApp # For Dapr-specific FastAPI integration
from sqlmodel import Session

from .db import get_session
from .services.recurring_tasks_service import RecurringTaskService, DAPR_PUBSUB_NAME, TASK_EVENTS_TOPIC
from .services.dapr_service import DaprService
from .services.notification_service import NotificationService, REMINDERS_TOPIC # New import
from .api.routes import tasks # Import the tasks router
from .utils.logging import setup_logging, CorrelationIdMiddleware # New import

# Setup structured logging as early as possible
setup_logging()
import logging
logger = logging.getLogger(__name__)

app = FastAPI()
dapr_app = DaprApp(app) # Initialize DaprApp

# Add correlation ID middleware
app.add_middleware(CorrelationIdMiddleware)

# Initialize DaprClient (can be managed better with FastAPI lifecycle or dependency injection)
dapr_client = DaprClient()

@app.on_event("startup")
async def startup_event():
    logger.info("Main application startup event triggered.")
    # Example: Register a Dapr Pub/Sub subscription on startup
    # This might be more dynamically configured or handled via a Dapr YAML subscription.
    # For now, let's assume Dapr will auto-discover endpoints or this is a programmatic registration.
    pass

@app.get("/health/live")
async def health_live():
    """Liveness probe endpoint."""
    return {"status": "ok"}

@app.get("/health/ready")
async def health_ready():
    """Readiness probe endpoint."""
    return {"status": "ok"}

# Dependency for RecurringTaskService
def get_recurring_task_service(
    session: Session = Depends(get_session),
) -> RecurringTaskService:
    return RecurringTaskService(session=session, dapr_client=dapr_client)

# Dependency for DaprService
def get_dapr_service() -> DaprService:
    return DaprService(dapr_client=dapr_client)

# Dependency for NotificationService (new)
def get_notification_service(
    session: Session = Depends(get_session),
) -> NotificationService:
    return NotificationService(session=session, dapr_client=dapr_client)

# Dapr Pub/Sub topic subscription for task events
@dapr_app.subscribe(pubsub_name=DAPR_PUBSUB_NAME, topic=TASK_EVENTS_TOPIC)
async def task_event_handler(
    event_data: dict,
    recurring_task_service: RecurringTaskService = Depends(get_recurring_task_service)
):
    """
    Handles incoming task events from Dapr Pub/Sub.
    """
    logger.info(f"Received Dapr Pub/Sub event", extra={"event_data": event_data})
    event_type = event_data.get("event_type")
    task_id = event_data.get("task_id")

    if event_type == "task.completed" and task_id is not None:
        await recurring_task_service.handle_task_completed_event(task_id)
    else:
        logger.warning(f"Unknown or unhandled event type", extra={"event_type": event_type, "task_id": task_id})
    return {"status": "SUCCESS"} # Dapr expects a success status

# Dapr Pub/Sub topic subscription for reminders (new)
@dapr_app.subscribe(pubsub_name=DAPR_PUBSUB_NAME, topic=REMINDERS_TOPIC)
async def reminder_event_handler(
    event_data: dict,
    notification_service: NotificationService = Depends(get_notification_service)
):
    """
    Handles incoming reminder events from Dapr Pub/Sub.
    """
    logger.info(f"Received Dapr Pub/Sub reminder event", extra={"event_data": event_data})
    task_id = event_data.get("task_id") # Assuming event_data will contain task_id

    if task_id is not None:
        await notification_service.handle_reminder_due_event(task_id)
    else:
        logger.warning(f"Reminder event received without task_id", extra={"event_data": event_data})
    return {"status": "SUCCESS"}

# Include the tasks router
app.include_router(tasks.router)