import sys
import os

# Ensure we can import src
sys.path.append('/app')

print("Importing todo_agent...")
try:
    from src.custom_agents import todo_agent
except ImportError as e:
    print(f"ImportError: {e}")
    # Try alternate path if needed
    sys.path.append('/app/src')
    from custom_agents import todo_agent

import httpx
from httpx import AsyncHTTPTransport

print(f"AsyncHTTPTransport.__init__ is patched: {AsyncHTTPTransport.__init__ == todo_agent._patched_async_transport_init}")

import asyncio
from openai import AsyncOpenAI

async def main():
    # Create client WITHOUT configuring http_client manually. 
    # It should use the patched Transport by default.
    client = AsyncOpenAI(
        api_key=os.getenv("CEREBRAS_API_KEY"), 
        base_url=os.getenv("CEREBRAS_BASE_URL", "https://api.cerebras.ai/v1")
    )
    print("Attempting AI connection with default client (should be patched)...")
    try:
        response = await client.chat.completions.create(
            model=os.getenv("CEREBRAS_MODEL", "llama3.1-8b"), 
            messages=[{"role":"user","content":"hi"}]
        )
        print(f"Success! Response: {response.choices[0].message.content[:20]}...")
    except Exception as e:
        print(f"AsyncOpenAI Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
