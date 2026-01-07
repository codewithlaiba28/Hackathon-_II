from sqlmodel import SQLModel, create_engine
from models import User, Task, Session
from db import DATABASE_URL, engine

def init_db():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("✅ Tables created successfully.")

if __name__ == "__main__":
    init_db()
