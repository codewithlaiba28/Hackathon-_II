from better_auth import Auth, TokenProvider
from better_auth.models import User
from better_auth.oauth.github import GitHub
from sqlmodel import Session
from . import db
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Auth instance
auth = Auth(
    secret=os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-change-in-production"),
    # Database configuration
    database_url=os.getenv("DATABASE_URL", "sqlite:///./todo_app.db"),
    # Configure token provider
    token_provider=TokenProvider(
        secret=os.getenv("BETTER_AUTH_SECRET", "your-super-secret-key-change-in-production"),
        algorithm="HS256",
        access_token_ttl=3600,  # 1 hour
        refresh_token_ttl=7 * 24 * 3600,  # 7 days
    ),
    # Configure user model
    user_model=User,
    # Enable email/password authentication
    email_password=True,
    # Configure OAuth providers if needed
    oauth_providers={
        # "github": GitHub(
        #     client_id=os.getenv("GITHUB_CLIENT_ID"),
        #     client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        # ),
    },
)

# Get the FastAPI router for auth endpoints
auth_router = auth.router