import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# Path fix for Vercel/Serverless
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from routers import tasks
import auth

# Fix for Windows asyncio loop with httpx/ssl
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Todo API",
    description="API for the Todo application",
    version="2.0.0"
)

# Add CORS middleware
allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
from routers import tasks
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
