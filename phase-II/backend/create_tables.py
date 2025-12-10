import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import engine
from models import User, Task
from sqlmodel import SQLModel

def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables()