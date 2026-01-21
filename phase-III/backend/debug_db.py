from sqlmodel import Session, select, create_engine, SQLModel
from models import Session as SessionModel
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Connecting to: {db_url}")

if not db_url:
    print("ERROR: No DATABASE_URL found")
    exit(1)

engine = create_engine(db_url)

from models import User

with Session(engine) as session:
    try:
        print("\n--- Checking User Table ---")
        users = session.exec(select(User).where(User.id == "test_user_66")).all()
        print(f"Found {len(users)} users with id 'test_user_66'")
        for u in users:
            print(f"User: {u.id}, Email: {u.email}")
            
    except Exception as e:
        print(f"Error querying users: {e}")
        # Try raw sql as fallback
        from sqlalchemy import text
        print("\n--- Raw SQL Fallback ---")
        result = session.exec(text("SELECT * FROM session")).all()
        for row in result:
            print(row)
