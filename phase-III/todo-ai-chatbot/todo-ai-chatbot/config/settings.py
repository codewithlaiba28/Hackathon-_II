"""
Settings for the Todo AI Chatbot
"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    app_name: str = "Todo AI Chatbot"
    app_version: str = "1.0.0"
    description: str = "AI-Powered Todo Chatbot with MCP Integration"
    allowed_origins: List[str] = ["*"]  # In production, specify actual origins
    openai_api_key: Optional[str] = None
    database_url: str = "postgresql+asyncpg://user:password@localhost/todo_chatbot"

    class Config:
        env_file = ".env"


settings = Settings()