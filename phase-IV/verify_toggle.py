
import os
import sys
import asyncio
from sqlmodel import Session, select, create_engine
from dotenv import load_dotenv

# Add backend to path
backend_dir = r"c:\Code-journy\Quator-4\Hackathon-_II\phase-III\backend"
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

import models
from db import engine

async def test_toggle_persistence():
    load_dotenv(os.path.join(backend_dir, ".env"))
    
    user_id = "test_user_66" # From previous debug run
    
    with Session(engine) as session:
        # 1. Find a task
        query = select(models.Task).where(models.Task.user_id == user_id).limit(1)
        task = session.exec(query).first()
        
        if not task:
            print("No task found for test_user_66. Creating one...")
            task = models.Task(user_id=user_id, title="Test Persistence Task", status="pending")
            session.add(task)
            session.commit()
            session.refresh(task)
        
        task_id = task.id
        original_status = task.status
        print(f"Original status for task {task_id}: {original_status}")
        
        # 2. Toggle it
        new_status = "completed" if original_status == "pending" else "pending"
        print(f"Toggling to {new_status}...")
        
        task.status = new_status
        session.add(task)
        session.commit()
        print("Commit successful.")
        
    # 3. Verify in a NEW session
    print("Opening new session to verify...")
    with Session(engine) as session2:
        verified_task = session2.get(models.Task, task_id)
        if verified_task:
            print(f"Verified status in DB: {verified_task.status}")
            if verified_task.status == new_status:
                print("SUCCESS: Persistence confirmed.")
            else:
                print("FAILURE: Status reverted or didn't save.")
        else:
            print("FAILURE: Task not found in verification session.")

if __name__ == "__main__":
    asyncio.run(test_toggle_persistence())
