from sqlmodel import create_engine, Session
from models import User, Task  # Import models to register them
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - prioritizes environment variable (e.g., from Neon)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Use In-memory SQLite for Vercel if no DATABASE_URL is provided to avoid read-only FS errors
    DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(DATABASE_URL, echo=True)
else:
    # Clean the DATABASE_URL (remove quotes, psql prefix if accidentally added)
    DATABASE_URL = DATABASE_URL.strip().strip("'").strip('"')
    if DATABASE_URL.startswith("psql "):
        DATABASE_URL = DATABASE_URL.replace("psql ", "", 1)
    
    # Handle PostgreSQL for Neon, ensuring SSL if needed
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # create_engine for PostgreSQL - for Neon, sslmode is usually required in the URL
    engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def get_session():
    if not engine:
        return
    with Session(engine) as session:
        yield session
