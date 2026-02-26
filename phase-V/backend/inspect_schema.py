from sqlmodel import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

with engine.connect() as conn:
    print("Inspecting 'task' table columns:")
    # Postgres specific query to check default value
    query = text("""
        SELECT column_name, data_type, column_default, is_nullable
        FROM information_schema.columns 
        WHERE table_name = 'task';
    """)
    result = conn.execute(query)
    for row in result:
        print(f"Column: {row.column_name}, Type: {row.data_type}, Default: {row.column_default}, Nullable: {row.is_nullable}")
