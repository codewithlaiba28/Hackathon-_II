import os
import sys
import logging

# Path fix for K8s environment to find local modules
sys.path.append("/app")

from sqlmodel import Session, text
from db import engine
import models

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate():
    logger.info("Starting database migration to Phase 5...")
    
    with Session(engine) as session:
        try:
            # 1. Add missing columns to task table
            logger.info("Adding missing columns to 'task' table...")
            
            # Check if columns already exist to avoid errors
            res = session.exec(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'task'"))
            existing_columns = [r[0] for r in res]
            
            columns_to_add = {
                "status": "VARCHAR(50) DEFAULT 'pending'",
                "priority": "VARCHAR(20) DEFAULT 'medium'",
                "due_date": "TIMESTAMP",
                "reminder_sent": "BOOLEAN DEFAULT FALSE",
                "reminder_offset_minutes": "INTEGER DEFAULT 0",
                "is_recurring": "BOOLEAN DEFAULT FALSE",
                "recurrence_pattern": "VARCHAR(50)",
                "recurrence_end_date": "TIMESTAMP",
                "parent_recurring_task_id": "INTEGER REFERENCES task(id)"
            }
            
            for col, col_type in columns_to_add.items():
                if col not in existing_columns:
                    logger.info(f"Adding column '{col}'...")
                    session.exec(text(f"ALTER TABLE task ADD COLUMN {col} {col_type}"))
                else:
                    logger.info(f"Column '{col}' already exists.")
            
            # 2. Migrate data from 'completed' to 'status' if 'completed' exists
            if 'completed' in existing_columns:
                logger.info("Migrating data from 'completed' to 'status'...")
                session.exec(text("UPDATE task SET status = 'completed' WHERE completed = TRUE"))
                session.exec(text("UPDATE task SET status = 'pending' WHERE completed = FALSE"))
                
                # Optional: Drop 'completed' column after migration
                # logger.info("Dropping 'completed' column...")
                # session.exec(text("ALTER TABLE task DROP COLUMN completed"))
            
            session.commit()
            logger.info("Task table migration completed.")
            
            # 3. Create new Phase 5 tables
            logger.info("Creating new Phase 5 tables (if not existing)...")
            from sqlmodel import SQLModel
            # Ensure all models are registered
            import models
            SQLModel.metadata.create_all(engine)
            
            logger.info("Database migration completed successfully!")
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            session.rollback()
            raise e

if __name__ == "__main__":
    migrate()
