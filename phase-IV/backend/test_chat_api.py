import httpx
import asyncio
import json

async def test_chat_api():
    base_url = "http://localhost:8000"
    user_id = "test_user_phase_3"
    
    payload = {
        "message": "List my tasks please",
        "conversation_id": None
    }
    
    print(f"Sending message to /api/{user_id}/chat...")
    async with httpx.AsyncClient(timeout=150.0) as client:
        try:
            response = await client.post(
                f"{base_url}/api/{user_id}/chat",
                json=payload
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print("Response JSON:")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_chat_api())
