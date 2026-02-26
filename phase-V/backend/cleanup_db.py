import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from db import engine
from sqlmodel import Session, text
import logging

logging.basicConfig(level=logging.INFO)

def cleanup():
    with Session(engine) as session:
        try:
            logging.info("Checking columns...")
            # Drop completed column if it exists
            session.execute(text("ALTER TABLE task DROP COLUMN IF EXISTS completed"))
            session.commit()
            logging.info("Cleaned up 'completed' column.")
            
            # Verify columns
            res = session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'task'"))
            cols = [r[0] for r in res]
            logging.info(f"Final columns: {cols}")
        except Exception as e:
            logging.error(f"Cleanup failed: {e}")

if __name__ == "__main__":
    cleanup()
