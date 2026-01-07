from sqlmodel import create_engine, Session
from models import User, Task  # Import models to register them
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - using SQLite for simplicity, can be changed to PostgreSQL in production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine settings based on database type
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
elif DATABASE_URL.startswith("postgresql"):
    # Neon frequently requires SSL
    if "sslmode" not in DATABASE_URL:
        if "?" in DATABASE_URL:
            DATABASE_URL += "&sslmode=require"
        else:
            DATABASE_URL += "?sslmode=require"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args=connect_args,
    # Add pooling for PostgreSQL
    pool_pre_ping=True if DATABASE_URL.startswith("postgresql") else False
)

def get_session():
    with Session(engine) as session:
        yield session