from db import engine
from sqlmodel import text, Session

def fix_jwks():
    try:
        with Session(engine) as session:
            print("Checking for JWKS table...")
            # Delete all entries in the jwks table
            # Better Auth will regenerate them automatically on next start
            session.exec(text("DELETE FROM jwks"))
            session.commit()
            print("✅ SUCCESS: Old JWKS keys deleted.")
            print("Restart your backend and frontend to generate new keys.")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    fix_jwks()
