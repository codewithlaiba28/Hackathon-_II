from sqlmodel import create_engine, Session
from models import User, Task  # Import models to register them
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - prioritizes environment variable (e.g., from Neon)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Use SQLite for local development if no DATABASE_URL is provided
    DATABASE_URL = "sqlite:///./todo_app.db"
    engine = create_engine(DATABASE_URL, echo=True)
else:
    # Handle PostgreSQL for Neon, ensuring SSL if needed
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # create_engine for PostgreSQL - for Neon, sslmode is usually required in the URL
    engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def get_session():
    with Session(engine) as session:
        yield session
