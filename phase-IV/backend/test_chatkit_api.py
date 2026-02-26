
import asyncio
import httpx
import jwt
import os
import json
from datetime import datetime

import sys
import os
# Add current directory to path so we can import auth
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from auth import SECRET_KEY, ALGORITHM

def create_test_token(user_id):
    payload = {
        "userId": user_id,
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": 9999999999 
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def test_chatkit_endpoint():
    user_id = "perfect_test_user"
    token = create_test_token(user_id)
    base_url = "http://localhost:8000"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Simulate ChatKit "create thread" or "send message" request
    # This payload is a guess based on standard ChatKit/Next.js integration
    # Ideally we'd capture the actual payload from the frontend.
    # But often ChatKit sends a simple POST.
    
    # If using @openai/chatkit-react with standard fetcher:
    # It might send a request to create a thread first, or append to one.
    
    # Let's try sending a message action
    # Note: The server expects a ChatKit action.
    # This part is tricky without knowing the exact library version protocol.
    # However, let's try a standard "messages.create" type payload if possible.
    
    # Actually, looking at OpenAIChatKitInterface.tsx, it creates a ChatKit instance.
    # The ChatKit library handles the protocol.
    
    # Let's try to just hit the endpoint and see if it authenticates, 
    # even with an invalid body it should pass auth.
    
    print(f"Testing /api/chatkit with user {user_id}...")
    
    payload = {
        "type": "threads.create",
        "params": {
            "input": {
                "value": "List my tasks",
                "content": [],
                "attachments": [],
                "inference_options": {}
            }
        },
        "message": {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": {
                        "value": "List my tasks"
                    }
                }
            ]
        }
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{base_url}/api/chatkit",
                headers=headers,
                json=payload
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_chatkit_endpoint())
