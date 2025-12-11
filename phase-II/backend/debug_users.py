"""
Debug script to list all users in the database
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import engine
from models import User, Task
from sqlmodel import Session, select

def list_users():
    """List all users in the database."""
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        print(f"\n{'='*50}")
        print(f"Total users in database: {len(users)}")
        print(f"{'='*50}\n")
        
        for user in users:
            print(f"User ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Name: {user.name}")
            print(f"Created: {user.created_at}")
            print(f"Last Login: {user.last_login_at}")
            
            # Count tasks for this user
            tasks = session.exec(select(Task).where(Task.user_id == user.id)).all()
            print(f"Tasks: {len(tasks)}")
            print("-" * 50)

if __name__ == "__main__":
    list_users()
