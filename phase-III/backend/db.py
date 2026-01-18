from sqlmodel import create_engine, Session
from models import User, Task
import os
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required!")

# Handle postgres:// vs postgresql:// (Neon sometimes uses postgres://)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Ensure SSL is enabled for Neon
if DATABASE_URL.startswith("postgresql") and "sslmode" not in DATABASE_URL:
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,  # Recycle connections after 5 minutes (good for Neon)
)

def get_session():
    with Session(engine) as session:
        yield session