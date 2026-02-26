from sqlmodel import SQLModel, create_engine
from models import User, Task, Conversation, Message
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Error: DATABASE_URL not set in environment")
    exit(1)

# Handle SSL for Neon
if DATABASE_URL.startswith("postgresql") and "sslmode" not in DATABASE_URL:
    if "?" in DATABASE_URL:
        DATABASE_URL += "&sslmode=require"
    else:
        DATABASE_URL += "?sslmode=require"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    print(f"Initializing database at {DATABASE_URL}")
    SQLModel.metadata.drop_all(engine) # Drop existing to ensure schema sync
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_db()
