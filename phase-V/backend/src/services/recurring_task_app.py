"""
Recurring Task Service — Dapr-aware FastAPI Microservice

Subscribes to the 'task-events' topic via Dapr Pub/Sub and processes
task completion events to spawn next occurrences for recurring tasks.
"""

import os
import sys
import logging
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Path fix so we can import from parent
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(os.path.dirname(current_dir))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("recurring-task-service")

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")

app = FastAPI(
    title="Recurring Task Service",
    description="Dapr-aware service that handles recurring task logic",
    version="1.0.0"
)


# ── Dapr Pub/Sub Subscription ──
@app.get("/dapr/subscribe")
async def dapr_subscribe():
    """Tell Dapr which topics this service subscribes to."""
    subscriptions = [
        {
            "pubsubname": PUBSUB_NAME,
            "topic": "task-events",
            "route": "/api/events/task-events"
        }
    ]
    logger.info(f"Dapr subscription: {subscriptions}")
    return JSONResponse(content=subscriptions)


@app.post("/api/events/task-events")
async def handle_task_event(request: Request):
    """Handle task events — create next occurrence for recurring tasks."""
    try:
        event_data = await request.json()
        data = event_data.get("data", {})
        event_type = data.get("event_type", "unknown")

        logger.info(f"[RECURRING] Received event: {event_type}")

        if event_type == "task.completed":
            task_id = data.get("task_id")
            user_id = data.get("user_id")
            is_recurring = data.get("is_recurring", False)
            recurrence_pattern = data.get("recurrence_pattern")

            if is_recurring and recurrence_pattern:
                logger.info(
                    f"[RECURRING] 🔄 Task {task_id} completed by {user_id}. "
                    f"Pattern: {recurrence_pattern}. Creating next occurrence..."
                )

                try:
                    from db import engine
                    from sqlmodel import Session
                    from services.recurring_task_service import RecurringTaskService
                    import models

                    with Session(engine) as session:
                        service = RecurringTaskService(session)
                        result = service.process_completed_recurring_task(task_id)
                        if result:
                            logger.info(f"[RECURRING] ✅ Next occurrence created for task {task_id}")
                        else:
                            logger.warning(f"[RECURRING] ⚠ Could not create next occurrence for task {task_id}")
                except Exception as e:
                    logger.error(f"[RECURRING] Failed to process recurring task {task_id}: {e}")

                # Save processing state via Dapr
                try:
                    import httpx
                    async with httpx.AsyncClient() as client:
                        await client.post(
                            f"{DAPR_BASE_URL}/v1.0/state/statestore",
                            json=[{
                                "key": f"recurring-processed-{task_id}",
                                "value": {
                                    "task_id": task_id,
                                    "user_id": user_id,
                                    "pattern": recurrence_pattern,
                                    "processed_at": datetime.now(timezone.utc).isoformat()
                                }
                            }]
                        )
                except Exception as e:
                    logger.warning(f"[RECURRING] Could not save state: {e}")
            else:
                logger.info(f"[RECURRING] Task {task_id} is not recurring, skipping")

        elif event_type == "task.created":
            logger.info(f"[RECURRING] New task created: {data.get('task_id')}")

        elif event_type == "task.deleted":
            logger.info(f"[RECURRING] Task deleted: {data.get('task_id')}")

        else:
            logger.info(f"[RECURRING] Unhandled event type: {event_type}")

        return JSONResponse(content={"status": "SUCCESS"}, status_code=200)

    except Exception as e:
        logger.error(f"[RECURRING] Error processing event: {e}")
        return JSONResponse(content={"status": "RETRY"}, status_code=500)


# ── Health Probes ──
@app.get("/health/live")
async def liveness():
    """Liveness probe."""
    return {"status": "ok", "service": "recurring-task-service"}


@app.get("/health/ready")
async def readiness():
    """Readiness probe — checks DB and Dapr sidecar."""
    db_status = "unknown"
    dapr_status = "unknown"

    try:
        from db import engine
        from sqlmodel import Session, text
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    try:
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{DAPR_BASE_URL}/v1.0/healthz", timeout=2.0)
            dapr_status = "ready" if resp.status_code in (200, 204) else f"not ready ({resp.status_code})"
    except Exception:
        dapr_status = "unreachable"

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "service": "recurring-task-service",
        "database": db_status,
        "dapr": dapr_status
    }


@app.get("/")
def root():
    return {"service": "recurring-task-service", "version": "1.0.0"}