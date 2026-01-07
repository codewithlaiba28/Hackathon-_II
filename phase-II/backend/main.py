from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks
import auth
import os
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
allowed_origins = [
    "http://localhost:3000",
    "https://hackathon-ii-frontend.vercel.app",
    "https://hackahton-ii-phase-ii.vercel.app",
    "http://localhost:3001" # Added local development alternative
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth router for /me and /sync
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Include task router (now includes {user_id} in its paths)
app.include_router(tasks.router, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Phase II Todo API"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}