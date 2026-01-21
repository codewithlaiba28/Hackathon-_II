import sys
import os
import asyncio
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Path fix for Vercel/Serverless
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Load environment variables FIRST
load_dotenv()

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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from routers import tasks
from db import engine
from sqlmodel import SQLModel
import auth

# Create database tables
SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Todo API",
    description="API for the Todo application",
    version="2.0.0"
)

# Add CORS middleware
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.103:3000", # User's current network IP
    "https://todo-chat.vercel.app"
]

# In development, it's often safer to allow all for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Temporarily allow all for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth router for /me and /sync
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Include chat router
from routers import chat
app.include_router(chat.router, prefix="/api", tags=["chat"])

# Include chatkit router
from routers import chatkit
app.include_router(chatkit.router, prefix="/api", tags=["chatkit"])

# Include task router
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Phase II Todo API"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
