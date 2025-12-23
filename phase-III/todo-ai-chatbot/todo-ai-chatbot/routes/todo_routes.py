"""
Todo routes for the Todo AI Chatbot
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/todos")
async def get_todos():
    return {"message": "Get todos endpoint"}