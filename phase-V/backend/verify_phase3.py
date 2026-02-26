import asyncio
import httpx
import sys
import os

async def test_chat_flow():
    # Setup: Create test user in DB to avoid foreign key errors
    from sqlmodel import Session, select, create_engine
    from models import User
    from db import DATABASE_URL
    
    engine = create_engine(DATABASE_URL)
    user_id = "test-user-123"
    
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            print(f"Creating test user {user_id}...")
            import random
            random_email = f"test_{random.randint(1000, 9999)}@example.com"
            user = User(id=user_id, email=random_email, name="Test User")
            session.add(user)
            session.commit()
    
    api_url = "http://localhost:8000"
    
    chat_payload = {
        "message": "Add a task to test Phase III implementation"
    }
    
    print(f"Testing chat endpoint for user: {user_id}")
    async with httpx.AsyncClient() as client:
        try:
            # First check health
            health = await client.get(f"{api_url}/api/health")
            print(f"Health check: {health.status_code}")
            
            # Test Chat
            response = await client.post(
                f"{api_url}/api/{user_id}/chat",
                json=chat_payload,
                timeout=120.0
            )
            print(f"Chat Response Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"AI Response: {data.get('response')}")
                print(f"Tool Calls: {data.get('tool_calls')}")
                
                # Now check if task exists in DB
                tasks_resp = await client.get(f"{api_url}/api/{user_id}/tasks")
                if tasks_resp.status_code == 200:
                    tasks = tasks_resp.json()
                    found = any("Phase III" in t.get('title', '') for t in tasks)
                    print(f"Task found in list: {found}")
                else:
                    print(f"Failed to fetch tasks: {tasks_resp.status_code}")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            import traceback
            traceback.print_exc()
            print("Make sure the backend is running on http://localhost:8000")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_chat_flow())
