"""
Database configuration for the Todo AI Chatbot
"""
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
import os

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/todo_chatbot")

# Create async engine
engine = create_async_engine(DATABASE_URL)

async def create_db_and_tables():
    """Create database tables"""
    async with engine.begin() as conn:
        # Import all models that should be created in the database
        from ..models.conversation import Conversation
        from ..models.message import Message
        from ..models.task import Task
        # This will create all tables
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency for getting async database session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session