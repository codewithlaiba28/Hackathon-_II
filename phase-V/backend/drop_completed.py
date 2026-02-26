import sys
sys.path.append('/app')
from db import engine
from sqlmodel import text
import logging

logging.basicConfig(level=logging.INFO)

def run():
    with engine.connect() as conn:
        try:
            logging.info("Checking for 'completed' column...")
            res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'task' AND column_name = 'completed'"))
            if res.fetchone():
                logging.info("Column 'completed' found. Dropping it...")
                conn.execute(text("ALTER TABLE task DROP COLUMN completed"))
                conn.commit()
                logging.info("Column 'completed' dropped successfully.")
            else:
                logging.info("Column 'completed' not found.")
        except Exception as e:
            logging.error(f"Error: {e}")

if __name__ == "__main__":
    run()
