import os
from sqlalchemy import create_engine, text

# Connection string from neon-db-secret, available in the pod environment
# SQLModel uses postgresql+psycopg2 under the hood sometimes, but let SQLAlchemy decide based on the connection string
DATABASE_URL = os.environ.get("DATABASE_URL")

engine = create_engine(DATABASE_URL)

alter_statements = [
    "ALTER TABLE task ADD COLUMN IF NOT EXISTS due_date TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_sent BOOLEAN DEFAULT FALSE;",
    "ALTER TABLE task ADD COLUMN IF NOT EXISTS reminder_offset_minutes INTEGER DEFAULT 0;",
    "ALTER TABLE task ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE;",
    "ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR;",
    "ALTER TABLE task ADD COLUMN IF NOT EXISTS recurrence_end_date TIMESTAMP WITH TIME ZONE;",
    "ALTER TABLE task ADD COLUMN IF NOT EXISTS parent_recurring_task_id INTEGER;"
]

print("Starting database schema migration...")
try:
    with engine.begin() as conn:
        for stmt in alter_statements:
            print(f"Executing: {stmt}")
            conn.execute(text(stmt))
    print("Migration completed successfully!")
except Exception as e:
    print(f"Error during migration: {e}")
