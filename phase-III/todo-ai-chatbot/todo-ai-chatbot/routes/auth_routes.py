"""
Auth routes for the Todo AI Chatbot
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/auth")
async def get_auth():
    return {"message": "Auth endpoint"}