import sys
import os
sys.path.append('/app')
from db import engine
from sqlmodel import Session, text
import logging

logging.basicConfig(level=logging.INFO)

def migrate():
    with Session(engine) as session:
        try:
            logging.info("Applying CASCADE DELETE constraints...")
            
            # Step 1: Fix TaskTag foreign key
            session.execute(text("ALTER TABLE tasktag DROP CONSTRAINT IF EXISTS tasktag_task_id_fkey"))
            # Just in case it has a different name
            session.execute(text("""
                DO $$
                DECLARE
                    r record;
                BEGIN
                    FOR r IN 
                        SELECT constraint_name 
                        FROM information_schema.key_column_usage 
                        WHERE table_name = 'tasktag' AND column_name = 'task_id'
                    LOOP
                        EXECUTE 'ALTER TABLE tasktag DROP CONSTRAINT IF EXISTS ' || r.constraint_name;
                    END LOOP;
                END $$;
            """))
            session.execute(text("ALTER TABLE tasktag ADD CONSTRAINT tasktag_task_id_fkey FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE"))
            logging.info("TaskTag CASCADE constraint added.")

            # Step 2: Fix Task self-referencing foreign key (parent_recurring_task_id)
            session.execute(text("ALTER TABLE task DROP CONSTRAINT IF EXISTS task_parent_recurring_task_id_fkey"))
            session.execute(text("""
                DO $$
                DECLARE
                    r record;
                BEGIN
                    FOR r IN 
                        SELECT constraint_name 
                        FROM information_schema.key_column_usage 
                        WHERE table_name = 'task' AND column_name = 'parent_recurring_task_id'
                    LOOP
                        EXECUTE 'ALTER TABLE task DROP CONSTRAINT IF EXISTS ' || r.constraint_name;
                    END LOOP;
                END $$;
            """))
            session.execute(text("ALTER TABLE task ADD CONSTRAINT task_parent_recurring_task_id_fkey FOREIGN KEY (parent_recurring_task_id) REFERENCES task(id) ON DELETE CASCADE"))
            logging.info("Task self-ref CASCADE constraint added.")
            
            session.commit()
            logging.info("Migration successful.")
        except Exception as e:
            logging.error(f"Migration failed: {e}")
            session.rollback()

if __name__ == "__main__":
    migrate()
