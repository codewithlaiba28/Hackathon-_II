import sys
sys.path.append('/app')
from db import engine
from sqlmodel import text

def check():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'task'"))
        cols = [r[0] for r in res]
        print(f"COLUMNS: {cols}")

if __name__ == "__main__":
    check()
