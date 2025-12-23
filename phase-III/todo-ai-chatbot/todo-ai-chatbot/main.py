import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database.database import engine
from config.settings import settings
from models.conversation import Conversation
from models.message import Message
from models.task import Task
from sqlmodel import SQLModel
from routes.chat_routes import router as chat_router
from routes.todo_routes import router as todo_router
from routes.auth_routes import router as auth_router
from routes.nlp_routes import router as nlp_router

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    # Add cleanup code here if needed

async def init_db():
    """Initialize the database"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.description,
        lifespan=lifespan
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(chat_router, prefix="", tags=["chat"])
    app.include_router(todo_router, prefix="/api/v1", tags=["todos"])
    app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
    app.include_router(nlp_router, prefix="/api/v1", tags=["nlp"])

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "version": settings.app_version}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )