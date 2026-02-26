"""
Notification Service — Dapr-aware FastAPI Microservice

Subscribes to the 'reminders' topic via Dapr Pub/Sub and processes
reminder events (due dates, recurring task spawns, etc.).
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
logger = logging.getLogger("notification-service")

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")

app = FastAPI(
    title="Notification Service",
    description="Dapr-aware service that handles reminder notifications",
    version="1.0.0"
)


# ── Dapr Pub/Sub Subscription ──
@app.get("/dapr/subscribe")
async def dapr_subscribe():
    """Tell Dapr which topics this service subscribes to."""
    subscriptions = [
        {
            "pubsubname": PUBSUB_NAME,
            "topic": "reminders",
            "route": "/api/events/reminders"
        }
    ]
    logger.info(f"Dapr subscription: {subscriptions}")
    return JSONResponse(content=subscriptions)


@app.post("/api/events/reminders")
async def handle_reminder_event(request: Request):
    """Handle reminder events from Dapr Pub/Sub."""
    try:
        event_data = await request.json()
        data = event_data.get("data", {})
        event_type = data.get("event_type", "unknown")

        logger.info(f"[NOTIFICATION] Received event: {event_type}")
        logger.info(f"[NOTIFICATION] Data: {data}")

        if event_type == "reminder.due":
            task_id = data.get("task_id")
            user_id = data.get("user_id")
            title = data.get("title", "Untitled Task")
            due_date = data.get("due_date")

            logger.info(
                f"[NOTIFICATION] 🔔 REMINDER: Task '{title}' (ID: {task_id}) "
                f"is due for user {user_id} at {due_date}"
            )

            # In production, this would send email/push/SMS
            # For now, we log and optionally save state via Dapr
            try:
                import httpx
                async with httpx.AsyncClient() as client:
                    await client.post(
                        f"{DAPR_BASE_URL}/v1.0/state/statestore",
                        json=[{
                            "key": f"notification-{task_id}-{user_id}",
                            "value": {
                                "task_id": task_id,
                                "user_id": user_id,
                                "title": title,
                                "sent_at": datetime.now(timezone.utc).isoformat(),
                                "channel": "log"
                            }
                        }]
                    )
                    logger.info(f"[NOTIFICATION] Saved notification state for task {task_id}")
            except Exception as e:
                logger.warning(f"[NOTIFICATION] Could not save state: {e}")

        elif event_type == "recurring.spawn_next":
            task_id = data.get("task_id")
            user_id = data.get("user_id")
            pattern = data.get("recurrence_pattern", "daily")
            logger.info(
                f"[NOTIFICATION] 🔄 Recurring task {task_id} completed by {user_id}. "
                f"Pattern: {pattern}. Next occurrence should be created."
            )

        else:
            logger.info(f"[NOTIFICATION] Unhandled event type: {event_type}")

        return JSONResponse(content={"status": "SUCCESS"}, status_code=200)

    except Exception as e:
        logger.error(f"[NOTIFICATION] Error processing event: {e}")
        return JSONResponse(content={"status": "RETRY"}, status_code=500)


# ── Health Probes ──
@app.get("/health/live")
async def liveness():
    """Liveness probe."""
    return {"status": "ok", "service": "notification-service"}


@app.get("/health/ready")
async def readiness():
    """Readiness probe — checks Dapr sidecar availability."""
    dapr_status = "unknown"
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{DAPR_BASE_URL}/v1.0/healthz", timeout=2.0)
            dapr_status = "ready" if resp.status_code in (200, 204) else f"not ready ({resp.status_code})"
    except Exception:
        dapr_status = "unreachable"

    return {
        "status": "ok",
        "service": "notification-service",
        "dapr": dapr_status
    }


@app.get("/")
def root():
    return {"service": "notification-service", "version": "1.0.0"}
