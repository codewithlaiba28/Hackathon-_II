"""
NLP routes for the Todo AI Chatbot
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/nlp")
async def get_nlp():
    return {"message": "NLP endpoint"}