from db import engine
from sqlmodel import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_schema():
    with engine.connect() as conn:
        # Check task table columns
        res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'task'"))
        columns = [r[0] for r in res]
        print(f"Task table columns: {columns}")
        
        # Check if status exists
        if 'status' not in columns:
            print("CRITICAL: 'status' column is MISSING from task table")
        else:
            print("'status' column exists")

if __name__ == "__main__":
    check_schema()
