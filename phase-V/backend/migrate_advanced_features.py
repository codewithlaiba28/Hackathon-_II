"""
Database Migration Script for Advanced Todo Features

This script adds new fields to the tasks table and creates the task_tags table
to support advanced features: priorities, due dates, reminders, recurring tasks, and tags.
"""

import asyncio
from sqlmodel import SQLModel, create_engine, Session, select
from sqlalchemy import text
from models import Task, TaskTag, User, Conversation, Message  # Import all models to register them
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - same as in db.py
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine - same settings as in db.py
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
elif DATABASE_URL.startswith("postgresql"):
    # Neon frequently requires SSL
    if "sslmode" not in DATABASE_URL:
        if "?" in DATABASE_URL:
            DATABASE_URL += "&sslmode=require"
        else:
            DATABASE_URL += "?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to True to see SQL statements
    connect_args=connect_args,
    pool_pre_ping=True if DATABASE_URL.startswith("postgresql") else False,
    pool_size=5 if DATABASE_URL.startswith("postgresql") else None,
    max_overflow=10 if DATABASE_URL.startswith("postgresql") else None
)


def migrate_database():
    """Execute database migration for advanced features"""
    print("Starting database migration for advanced features...")

    # Create all tables (this will create new tables and update existing ones if needed)
    SQLModel.metadata.create_all(engine)
    print("Tables created/updated successfully.")

    # Connect to database
    with Session(engine) as session:
        # Add new columns to tasks table
        try:
            # Check if we're using PostgreSQL
            if DATABASE_URL.startswith("postgresql"):
                print("Adding new columns to tasks table (PostgreSQL)...")

                # Add priority column
                try:
                    session.exec(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium';"))
                    print("+ Added priority column")
                except Exception as e:
                    print(f"? Priority column may already exist: {e}")

                # Add due_date column
                try:
                    session.exec(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;"))
                    print("+ Added due_date column")
                except Exception as e:
                    print(f"? Due date column may already exist: {e}")

                # Add reminder_offset_minutes column
                try:
                    session.exec(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_offset_minutes INTEGER;"))
                    print("+ Added reminder_offset_minutes column")
                except Exception as e:
                    print(f"? Reminder offset column may already exist: {e}")

                # Add is_recurring column
                try:
                    session.exec(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE;"))
                    print("+ Added is_recurring column")
                except Exception as e:
                    print(f"? Is recurring column may already exist: {e}")

                # Add recurrence_pattern column
                try:
                    session.exec(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(50);"))
                    print("+ Added recurrence_pattern column")
                except Exception as e:
                    print(f"? Recurrence pattern column may already exist: {e}")

                # Add recurrence_end_date column
                try:
                    session.exec(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_end_date TIMESTAMP WITH TIME ZONE;"))
                    print("+ Added recurrence_end_date column")
                except Exception as e:
                    print(f"? Recurrence end date column may already exist: {e}")

                # Add parent_recurring_task_id column
                try:
                    session.exec(text("ALTER TABLE task ADD COLUMN IF NOT EXISTS parent_recurring_task_id INTEGER REFERENCES task(id);"))
                    print("+ Added parent_recurring_task_id column")
                except Exception as e:
                    print(f"? Parent recurring task ID column may already exist: {e}")

                # Commit column changes immediately to prevent rollback if indexes fail
                session.commit()
                print("[OK] Column additions committed.")

            else:  # SQLite
                print("Adding new columns to tasks table (SQLite)...")

                # For SQLite, we need to recreate the table since ALTER COLUMN is limited
                # First, check if columns exist by querying pragma
                result = session.exec(text("PRAGMA table_info(task);"))
                columns = [row for row in result.fetchall()]
                column_names = [col[1] for col in columns]  # Second element is column name

                # Add priority column if it doesn't exist
                if 'priority' not in column_names:
                    session.exec(text("ALTER TABLE task ADD COLUMN priority TEXT DEFAULT 'medium';"))
                    print("[OK] Added priority column")
                else:
                    print("[INFO] Priority column already exists")

                # Add due_date column if it doesn't exist
                if 'due_date' not in column_names:
                    session.exec(text("ALTER TABLE task ADD COLUMN due_date TEXT;"))
                    print("[OK] Added due_date column")
                else:
                    print("[INFO] Due date column already exists")

                # Add reminder_offset_minutes column if it doesn't exist
                if 'reminder_offset_minutes' not in column_names:
                    session.exec(text("ALTER TABLE task ADD COLUMN reminder_offset_minutes INTEGER;"))
                    print("[OK] Added reminder_offset_minutes column")
                else:
                    print("[INFO] Reminder offset minutes column already exists")

                # Add is_recurring column if it doesn't exist
                if 'is_recurring' not in column_names:
                    session.exec(text("ALTER TABLE task ADD COLUMN is_recurring BOOLEAN DEFAULT 0;"))
                    print("[OK] Added is_recurring column")
                else:
                    print("[INFO] Is recurring column already exists")

                # Add recurrence_pattern column if it doesn't exist
                if 'recurrence_pattern' not in column_names:
                    session.exec(text("ALTER TABLE task ADD COLUMN recurrence_pattern TEXT;"))
                    print("[OK] Added recurrence_pattern column")
                else:
                    print("[INFO] Recurrence pattern column already exists")

                # Add recurrence_end_date column if it doesn't exist
                if 'recurrence_end_date' not in column_names:
                    session.exec(text("ALTER TABLE task ADD COLUMN recurrence_end_date TEXT;"))
                    print("[OK] Added recurrence_end_date column")
                else:
                    print("[INFO] Recurrence end date column already exists")

                # Add parent_recurring_task_id column if it doesn't exist
                if 'parent_recurring_task_id' not in column_names:
                    session.exec(text("ALTER TABLE task ADD COLUMN parent_recurring_task_id INTEGER;"))
                    print("[OK] Added parent_recurring_task_id column")
                else:
                    print("[INFO] Parent recurring task ID column already exists")

                # Commit SQLite changes
                session.commit()

            # Create indexes for performance
            print("Creating indexes for performance...")

            if DATABASE_URL.startswith("postgresql"):
                # PostgreSQL indexes
                try:
                    session.exec(text("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON task(due_date);"))
                    print("+ Created due_date index")
                except Exception as e:
                    print(f"? Due date index may already exist: {e}")

                try:
                    session.exec(text("CREATE INDEX IF NOT EXISTS idx_tasks_priority ON task(priority);"))
                    print("+ Created priority index")
                except Exception as e:
                    print(f"? Priority index may already exist: {e}")

                try:
                    session.exec(text("CREATE INDEX IF NOT EXISTS idx_task_tags_tag ON task_tag(tag);"))
                    print("+ Created tag index")
                except Exception as e:
                    print(f"? Tag index may already exist: {e}")

                try:
                    session.exec(text("CREATE INDEX IF NOT EXISTS idx_task_tags_task_id ON task_tag(task_id);"))
                    print("+ Created task_id index")
                except Exception as e:
                    print(f"? Task ID index may already exist: {e}")
            else:
                # SQLite indexes
                try:
                    session.exec(text("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON task(due_date);"))
                    print("+ Created due_date index")
                except Exception as e:
                    print(f"? Due date index may already exist: {e}")

                try:
                    session.exec(text("CREATE INDEX IF NOT EXISTS idx_tasks_priority ON task(priority);"))
                    print("+ Created priority index")
                except Exception as e:
                    print(f"? Priority index may already exist: {e}")

                try:
                    session.exec(text("CREATE INDEX IF NOT EXISTS idx_task_tags_tag ON task_tag(tag);"))
                    print("+ Created tag index")
                except Exception as e:
                    print(f"? Tag index may already exist: {e}")

                try:
                    session.exec(text("CREATE INDEX IF NOT EXISTS idx_task_tags_task_id ON task_tag(task_id);"))
                    print("+ Created task_id index")
                except Exception as e:
                    print(f"? Task ID index may already exist: {e}")

            # Commit all changes
            session.commit()
            print("\n+ Database migration completed successfully!")
            print(f"Database URL: {DATABASE_URL}")
            print("New features supported:")
            print("- Priority levels (low, medium, high, urgent)")
            print("- Due dates with timezone support")
            print("- Reminder notifications")
            print("- Recurring tasks with patterns")
            print("- Hierarchical tagging system")
            print("- Performance indexes for queries")

        except Exception as e:
            print(f"[ERROR] Error during migration: {e}")
            session.rollback()
            raise


if __name__ == "__main__":
    migrate_database()