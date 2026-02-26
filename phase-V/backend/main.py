import sys
import os
import traceback

print("DEBUG: 1. main.py starting...", flush=True)

try:
    import asyncio
    print("DEBUG: 2. asyncio imported.", flush=True)
    import logging
    print("DEBUG: 3. logging imported.", flush=True)
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    print("DEBUG: 4. FastAPI imported.", flush=True)
    from fastapi.middleware.cors import CORSMiddleware
    print("DEBUG: 5. CORSMiddleware imported.", flush=True)
    from dotenv import load_dotenv
    print("DEBUG: 6. load_dotenv imported.", flush=True)
    import httpx
    print("DEBUG: 6b. httpx imported.", flush=True)

    # Path fix for Vercel/Serverless
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)

    # Load environment variables FIRST
    load_dotenv()
    print("DEBUG: 7. Environment variables loaded.", flush=True)

    # Fix for Windows asyncio loop with httpx/ssl
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # Force UTF-8 encoding for Windows console to handle emojis
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')

    # Set up logging
    IS_VERCEL = os.getenv("VERCEL_REGION") is not None
    logging.basicConfig(level=logging.INFO if IS_VERCEL else logging.DEBUG)
    logger = logging.getLogger(__name__)
    print("DEBUG: Startup initialization...", flush=True)

    # Dapr configuration
    DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
    DAPR_BASE_URL = f"http://localhost:{DAPR_HTTP_PORT}"
    PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")
    ENABLE_DAPR = os.getenv("ENABLE_DAPR", "false").lower() == "true"
    print(f"DEBUG: Dapr config - enabled={ENABLE_DAPR}, port={DAPR_HTTP_PORT}", flush=True)

    app = FastAPI(
        title="Todo AI API",
        description="Phase V Cloud-Native API with Full Dapr Integration",
        version="5.0.0"
    )

    # Add CORS middleware - K8s internal calls + localhost dev
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # Add Request Logging Middleware
    @app.middleware("http")
    async def log_requests(request, call_next):
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.debug(f"Headers: {request.headers}")
        try:
            response = await call_next(request)
            logger.info(f"Response status: {response.status_code}")
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise e

    # Database and Models
    from db import engine
    from sqlmodel import SQLModel
    import models
    SQLModel.metadata.create_all(engine)
    print("DEBUG: Database initialized.", flush=True)

    # Include routers
    import auth
    from routers import tasks, chat, chatkit
    app.include_router(auth.router, prefix="/api/identity/auth", tags=["auth"])
    app.include_router(chat.router, prefix="/api", tags=["chat"])
    app.include_router(chatkit.router, prefix="/api", tags=["chatkit"])
    app.include_router(tasks.router, prefix="/api", tags=["tasks"])
    print("DEBUG: Application ready.", flush=True)

    # ── Dapr Pub/Sub Subscription Endpoint ──
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
        logger.info(f"Dapr subscription request: returning {len(subscriptions)} subscriptions")
        return JSONResponse(content=subscriptions)

    @app.post("/api/events/task-events")
    async def handle_task_events(request: Request):
        """Handle task events from Dapr Pub/Sub."""
        try:
            event_data = await request.json()
            logger.info(f"Received task event: {event_data.get('data', {}).get('event_type', 'unknown')}")

            data = event_data.get("data", {})
            event_type = data.get("event_type", "")

            if event_type == "task.completed":
                # Microservices (recurring-task-service) handle this now.
                # We just log it here for monitoring.
                logger.info(f"Task completion received: {data.get('task_id')}. Microservice will handle recurrence.")

            return JSONResponse(content={"status": "SUCCESS"}, status_code=200)
        except Exception as e:
            logger.error(f"Error handling task event: {e}")
            return JSONResponse(content={"status": "RETRY"}, status_code=500)

    # ── Dapr Cron Binding Handler ──
    @app.post("/todo-cron")
    async def handle_cron_binding(request: Request):
        """Handle Dapr cron binding trigger — checks for due reminders."""
        logger.info("[CRON] Dapr cron binding triggered — checking for due reminders")
        try:
            from sqlmodel import Session, select
            from datetime import datetime, timezone
            with Session(engine) as session:
                now = datetime.now(timezone.utc)
                statement = select(models.Task).where(
                    models.Task.due_date <= now,
                    models.Task.status != "completed",
                    models.Task.reminder_sent == False
                )
                due_tasks = session.exec(statement).all()
                logger.info(f"[CRON] Found {len(due_tasks)} tasks with due reminders")

                for task in due_tasks:
                    # Publish reminder event via Dapr Pub/Sub
                    if ENABLE_DAPR:
                        try:
                            async with httpx.AsyncClient() as client:
                                await client.post(
                                    f"{DAPR_BASE_URL}/v1.0/publish/{PUBSUB_NAME}/reminders",
                                    json={
                                        "event_type": "reminder.due",
                                        "task_id": task.id,
                                        "user_id": task.user_id,
                                        "title": task.title,
                                        "due_date": task.due_date.isoformat() if task.due_date else None
                                    },
                                    headers={"Content-Type": "application/json"}
                                )
                            logger.info(f"[CRON] Published reminder for task {task.id}")
                        except Exception as e:
                            logger.error(f"[CRON] Failed to publish reminder for task {task.id}: {e}")
                    else:
                        logger.info(f"[CRON] (Dapr disabled) Would remind for task {task.id}: {task.title}")

            return JSONResponse(content={"status": "ok", "checked": len(due_tasks)}, status_code=200)
        except Exception as e:
            logger.error(f"[CRON] Error checking reminders: {e}")
            return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

    # ── Dapr Secrets Access Demo ──
    @app.get("/api/dapr/secrets/{secret_name}")
    async def get_dapr_secret(secret_name: str):
        """Access a Kubernetes secret via Dapr Secrets API."""
        if not ENABLE_DAPR:
            return JSONResponse(
                content={"error": "Dapr is not enabled"},
                status_code=503
            )
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{DAPR_BASE_URL}/v1.0/secrets/kubernetes-secrets/{secret_name}"
                )
                if resp.status_code == 200:
                    # Return only the key names, never the values
                    secret_keys = list(resp.json().keys())
                    return {"secret_name": secret_name, "available_keys": secret_keys}
                else:
                    return JSONResponse(
                        content={"error": f"Secret not found: {resp.status_code}"},
                        status_code=resp.status_code
                    )
        except Exception as e:
            logger.error(f"Failed to access Dapr secret: {e}")
            return JSONResponse(content={"error": str(e)}, status_code=500)

    # ── Health Check Endpoints (K8s Probes) ──
    @app.get("/api/health")
    @app.get("/health/live")
    async def health_check():
        """Liveness probe — app is running."""
        return {"status": "ok", "env": os.getenv("APP_ENV", "unknown")}

    @app.get("/health/ready")
    async def readiness_check():
        """Readiness probe — app + DB + Dapr sidecar are ready."""
        db_status = "unknown"
        dapr_status = "disabled"
        try:
            from sqlmodel import Session, text
            with Session(engine) as session:
                session.exec(text("SELECT 1"))
                db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"

        if ENABLE_DAPR:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(f"{DAPR_BASE_URL}/v1.0/healthz", timeout=2.0)
                    dapr_status = "ready" if resp.status_code == 204 or resp.status_code == 200 else f"not ready ({resp.status_code})"
            except Exception:
                dapr_status = "unreachable"

        return {
            "status": "ok" if db_status == "connected" else "degraded",
            "database": db_status,
            "dapr": dapr_status,
            "env": os.getenv("APP_ENV", "unknown")
        }

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Phase V Todo API — Cloud-Native with Dapr"}

except Exception as e:
    print("CRITICAL ERROR during main.py startup:", flush=True)
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
