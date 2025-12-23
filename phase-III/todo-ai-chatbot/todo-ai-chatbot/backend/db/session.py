from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Default to sqlite for development if no URL is set
    DATABASE_URL = "sqlite+aiosqlite:///./todo_chatbot.db"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get async database session"""
    async with AsyncSession(engine) as session:
        yield session