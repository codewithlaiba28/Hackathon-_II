import os
import logging
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO)
engine = create_engine(os.getenv('DATABASE_URL'))

def cleanup():
    with engine.connect() as conn:
        print("--- Recent Tasks ---")
        res = conn.execute(text("SELECT id, title, user_id, status FROM task ORDER BY created_at DESC LIMIT 10"))
        for row in res:
            print(row)
        
        print("\n--- Deleting 'Delete Test' tasks ---")
        # Use simple delete to test cascade
        # If this fails with 500 in the app, it's a metadata issue. 
        # Here we test if the DB itself cascades correctly.
        conn.execute(text("DELETE FROM task WHERE title = 'Delete Test'"))
        conn.commit()
        print("Cleanup successful.")

if __name__ == "__main__":
    cleanup()
