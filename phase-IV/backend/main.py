import sys
import os
import traceback

print("DEBUG: 1. main.py starting...", flush=True)

try:
    import asyncio
    print("DEBUG: 2. asyncio imported.", flush=True)
    import logging
    print("DEBUG: 3. logging imported.", flush=True)
    from fastapi import FastAPI
    print("DEBUG: 4. FastAPI imported.", flush=True)
    from fastapi.middleware.cors import CORSMiddleware
    print("DEBUG: 5. CORSMiddleware imported.", flush=True)
    from dotenv import load_dotenv
    print("DEBUG: 6. load_dotenv imported.", flush=True)

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

    app = FastAPI(
        title="Todo AI API",
        description="Stateless API with MCP for Todo Chatbot",
        version="3.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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

    @app.get("/api/health")
    async def health_check():
        db_status = "unknown"
        try:
            from sqlmodel import Session, text
            with Session(engine) as session:
                session.exec(text("SELECT 1"))
                db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
            
        return {
            "status": "ok", 
            "database": db_status,
            "env": os.getenv("APP_ENV", "unknown")
        }

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Phase IV Todo API"}

except Exception as e:
    print("CRITICAL ERROR during main.py startup:", flush=True)
    traceback.print_exc(file=sys.stdout)
    sys.exit(1)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
