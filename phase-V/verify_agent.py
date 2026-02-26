import asyncio
import json
import sys
import os

# Set up paths
sys.path.append("/app/src")

async def test_agent():
    try:
        from custom_agents.todo_agent import TodoAgent
        from db import engine, DATABASE_URL
        
        print(f"DEBUG: Using DATABASE_URL: {DATABASE_URL}")
        
        # Test Case 1: Greeting
        print("\n--- Test 1: Greeting ---")
        agent = TodoAgent(user_id="verification_user", db_url=DATABASE_URL)
        result1 = await agent.run("Hello, who are you?", [])
        print(f"AGENT_RESPONSE: {result1.get('response')}")
        print(f"TOOL_CALLS: {result1.get('tool_calls')}")
        
        # Test Case 2: Add Task (The fix verification)
        print("\n--- Test 2: Add Task ---")
        msg = "Add a task called internal_verification_success with priority high and tag verification"
        result2 = await agent.run(msg, [])
        print(f"AGENT_RESPONSE: {result2.get('response')}")
        print(f"TOOL_CALLS: {result2.get('tool_calls')}")
        
        # Verify if JSON leaked
        leaked = "{" in result2.get('response', '') or "}" in result2.get('response', '')
        print(f"JSON_LEAK_DETECTED: {leaked}")
        
        # Check DB
        from sqlmodel import Session, select
        from models import Task
        with Session(engine) as session:
            task = session.exec(select(Task).where(Task.title == "internal_verification_success")).first()
            if task:
                print(f"VERIFICATION: Task found in database! ID={task.id}, Priority={task.priority}")
            else:
                print("VERIFICATION: Task NOT found in database.")

    except Exception as e:
        print(f"ERROR during verification: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agent())
