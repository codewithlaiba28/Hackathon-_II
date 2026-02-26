import asyncio
import os
import httpx
import socket
from openai import AsyncOpenAI
from httpx import AsyncHTTPTransport

async def main():
    print("Testing connection...")
    try:
        transport = AsyncHTTPTransport(local_address='0.0.0.0', retries=3)
        client = AsyncOpenAI(
            api_key=os.getenv('CEREBRAS_API_KEY'),
            base_url=os.getenv('CEREBRAS_BASE_URL', 'https://api.cerebras.ai/v1'),
            http_client=httpx.AsyncClient(transport=transport, timeout=10.0)
        )
        print(f"Connecting to {client.base_url} with local_address=0.0.0.0")
        response = await client.chat.completions.create(
            model=os.getenv('CEREBRAS_MODEL', 'llama3.1-8b'),
            messages=[{'role':'user','content':'hi'}]
        )
        print(f"Success! Response: {response.choices[0].message.content[:20]}...")
    except Exception as e:
        print(f"AsyncOpenAI Failed: {e}")

    print("Testing raw socket bind...")
    try:
        s = socket.create_connection(('api.cerebras.ai', 443), timeout=5, source_address=('0.0.0.0', 0))
        print(f"Socket connected! Bound to {s.getsockname()}")
        s.close()
    except Exception as e:
        print(f"Socket failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
