from sqlmodel import create_engine, text, SQLModel
from models import Task  # Import definitions
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

with engine.connect() as conn:
    print("Dropping incorrect 'task' table...")
    conn.execute(text("DROP TABLE IF EXISTS task CASCADE;"))
    conn.commit()
    print("Task table dropped.")

print("Recreating tables with correct schema...")
# Re-import models to ensure registry is populated
import models
SQLModel.metadata.create_all(engine)
print("Tables recreated.")

# Verify
with engine.connect() as conn:
    print("Inspecting 'task' table columns after fix:")
    query = text("""
        SELECT column_name, data_type, column_default 
        FROM information_schema.columns 
        WHERE table_name = 'task';
    """)
    result = conn.execute(query)
    for row in result:
        print(f"Column: {row.column_name}, Type: {row.data_type}, Default: {row.column_default}")
