import asyncio
import os
import sys
from dotenv import load_dotenv

# Ensure backend directory is in path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from src.custom_agents.todo_agent import TodoAgent

async def run_test():
    print("Initializing TodoAgent...")
    try:
        db_url = os.getenv("DATABASE_URL")
        user_id = "test_user_66"
        agent = TodoAgent(user_id=user_id, db_url=db_url)
        print(f"TodoAgent initialized for user {user_id}.")
        
        test_message = "Add a task to buy groceries"
        print(f"Running agent with input: '{test_message}'")
        
        response = await agent.run(test_message, history=[])
        print("Agent run successful!")
        print("Response:", response["response"])
        print("Tool Calls:", response["tool_calls"])
        
        # Verify in DB
        from sqlmodel import Session, create_engine, select
        from models import Task
        engine = create_engine(db_url)
        with Session(engine) as session:
            statement = select(Task).where(Task.user_id == user_id)
            tasks = session.exec(statement).all()
            print(f"Found {len(tasks)} tasks in DB for user {user_id}.")
            for t in tasks:
                print(f" - [{t.id}] {t.title} (Completed: {t.completed})")
                
    except Exception as e:
        import traceback
        print("\nCRITICAL FAILURE during agent execution:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())
