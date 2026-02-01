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
logging.basicConfig(level=logging.INFO if IS_VERCEL else logging.DEBUG)
logger = logging.getLogger(__name__)

from routers import tasks
from db import engine
from sqlmodel import SQLModel
import auth

# Create database tables (only if not on Vercel to save startup time, or run once)
# On Neon/PostgreSQL, tables should be pre-created by init_db.py
if not IS_VERCEL:
    SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="Todo AI API",
    description="Stateless API with MCP for Todo Chatbot",
    version="3.0.0"
)

# Add CORS middleware
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Specific production domains
    os.getenv("FRONTEND_URL"), 
    os.getenv("BETTER_AUTH_URL"),
    # Allow all Vercel preview/production/branch deployments
    "https://*.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if not IS_VERCEL else allowed_origins,
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
