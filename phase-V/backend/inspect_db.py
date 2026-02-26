
from sqlmodel import Session, select, create_engine
import os
import sys

# Add current dir to path to import models and db
sys.path.append(os.getcwd())

try:
    from db import engine, DATABASE_URL
    import models
    
    with open("db_inspection_utf8.txt", "w", encoding="utf-8") as f:
        f.write(f"DEBUG: Using Database URL: {DATABASE_URL}\n")
        
        with Session(engine) as session:
            statement = select(models.Task)
            tasks = session.exec(statement).all()
            
            f.write("\n--- ALL TASKS IN DB ---\n")
            if not tasks:
                f.write("No tasks found.\n")
            for t in tasks:
                f.write(f"ID: {t.id} | Title: {t.title} | UserID: {t.user_id} | Status: {t.status} | CreatedAt: {t.created_at}\n")
            f.write("-----------------------\n\n")
            
            # Also check users to see if IDs match
            statement_users = select(models.User)
            users = session.exec(statement_users).all()
            f.write("--- ALL USERS IN DB ---\n")
            for u in users:
                f.write(f"ID: {u.id} | Email: {u.email}\n")
            f.write("-----------------------\n\n")
    print("Inspection complete. See db_inspection_utf8.txt")

except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
