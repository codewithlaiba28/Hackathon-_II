"""
Chat schemas for the Todo AI Chatbot
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str


class ToolCall(BaseModel):
    id: str
    type: str
    function: dict


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    timestamp: datetime
    tool_calls: List[ToolCall] = []