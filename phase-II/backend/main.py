from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from routers import tasks
import auth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Better Auth
try:
    from better_auth_config import auth_app
    better_auth_available = True
except ImportError:
    better_auth_available = False
    print("Better Auth not available, using legacy auth")

app = FastAPI(
    title="Todo API",
    description="API for the Todo application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Better Auth endpoints if available
if better_auth_available:
    app.mount("/api/better-auth", auth_app)
    print("Better Auth endpoints mounted at /api/better-auth")

    # We'll use Better Auth for login/signup but keep our custom auth router for API authentication
    # Better Auth handles the session management, but we still need our auth middleware for API calls
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
else:
    # Include legacy auth router for login/signup endpoints
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# Include task router - it will use the auth validation from the auth module
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}