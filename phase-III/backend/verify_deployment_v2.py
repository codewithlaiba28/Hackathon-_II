import asyncio
import os
import sys
from dotenv import load_dotenv

# Path fix
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

load_dotenv()

async def test_agent():
    print("Testing TodoAgent with Cerebras...")
    from src.custom_agents.todo_agent import TodoAgent
    from db import DATABASE_URL
    
    user_id = "test_user_ai"
    agent = TodoAgent(user_id=user_id, db_url=DATABASE_URL)
    
    # Test a simple message
    message = "Add 3 tasks: buy milk, call mom, and finish hackathon"
    print(f"User: {message}")
    
    try:
        result = await agent.run(message)
        print(f"Assistant: {result['response']}")
        print(f"Tool Calls: {result['tool_calls']}")
        
        # Test listing
        message = "What's on my list?"
        result = await agent.run(message)
        print(f"Assistant: {result['response']}")
        print(f"Tool Calls: {result['tool_calls']}")
        
    except Exception as e:
        print(f"Error during agent run: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if not os.getenv("CEREBRAS_API_KEY"):
        print("ERROR: CEREBRAS_API_KEY not set in .env")
        sys.exit(1)
    
    asyncio.run(test_agent())
