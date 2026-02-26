import sys
import os
sys.path.append('/app')
from db import engine
from sqlmodel import Session, text
import models
import schemas
import logging

logging.basicConfig(level=logging.INFO)

def test_delete():
    with Session(engine) as session:
        # Create a task
        task = models.Task(user_id="rXN5BqMPkWRMefrZYL1emZx3l4ScVWMy", title="Delete Test")
        session.add(task)
        session.commit()
        session.refresh(task)
        logging.info(f"Created task {task.id}")
        
        # Add a tag
        tag = models.TaskTag(task_id=task.id, tag="test-tag")
        session.add(tag)
        session.commit()
        logging.info(f"Created tag for task {task.id}")
        
        # Try to delete
        try:
            logging.info(f"Attempting to delete task {task.id}")
            session.delete(task)
            session.commit()
            logging.info("Delete successful")
        except Exception as e:
            logging.error(f"Delete failed as expected: {e}")
            session.rollback()

if __name__ == "__main__":
    test_delete()
