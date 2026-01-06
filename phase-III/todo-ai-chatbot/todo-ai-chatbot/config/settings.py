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
    openai_base_url: str = "https://api.groq.com/openai/v1"
    openai_model: str = "openai/gpt-oss-120b"
    database_url: str = "postgresql+asyncpg://user:password@localhost/todo_chatbot"
    jwt_secret_key: str = "your-secret-key"
    jwt_algorithm: str = "HS256"
    debug: bool = False
    mcp_server_host: str = "localhost"
    mcp_server_port: int = 8001

    class Config:
        env_file = ".env"


settings = Settings()