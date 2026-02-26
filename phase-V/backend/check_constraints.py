import os
import logging
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO)
engine = create_engine(os.getenv('DATABASE_URL'))

def check():
    with engine.connect() as conn:
        print("--- Table: tasktag ---")
        res = conn.execute(text("""
            SELECT 
                conname AS constraint_name, 
                pg_get_constraintdef(oid) AS constraint_def
            FROM pg_constraint 
            WHERE conrelid = 'tasktag'::regclass
        """))
        for row in res:
            print(f"Name: {row.constraint_name}")
            print(f"Def:  {row.constraint_def}")

        print("\n--- Table: task ---")
        res = conn.execute(text("""
            SELECT 
                conname AS constraint_name, 
                pg_get_constraintdef(oid) AS constraint_def
            FROM pg_constraint 
            WHERE conrelid = 'task'::regclass
        """))
        for row in res:
            if 'parent_recurring_task_id' in row.constraint_def:
                print(f"Name: {row.constraint_name}")
                print(f"Def:  {row.constraint_def}")

if __name__ == "__main__":
    check()
