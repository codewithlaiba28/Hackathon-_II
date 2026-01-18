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
        # Use a dummy user_id and the real DATABASE_URL
        db_url = os.getenv("DATABASE_URL")
        agent = TodoAgent(user_id="debug_user", db_url=db_url)
        print("TodoAgent initialized.")
        
        print("Running agent with input 'Hello'...")
        # Mock history as empty
        response = await agent.run("Hello", history=[])
        print("Agent run successful!")
        print("Response:", response)
        
    except Exception as e:
        import traceback
        print("\nCRITICAL FAILURE during agent execution:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())
