from sqlmodel import create_engine, Session
from .models import User, Task  # Import models to register them
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - using SQLite for simplicity, can be changed to PostgreSQL in production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine with async support
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session