import asyncio
import os
import sys
import httpx
from dotenv import load_dotenv
from openai import AsyncOpenAI

# Force Selector loop on Windows to avoid Proactor issues
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

async def test_models():
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai/")
    
    print(f"Testing with Base URL: {base_url}")
    print(f"API Key present: {bool(api_key)}")
    
    # Disable SSL verification for testing
    http_client = httpx.AsyncClient(verify=False)
    client = AsyncOpenAI(
        api_key=api_key, 
        base_url=base_url,
        http_client=http_client
    )
    
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "gemini-1.5-flash-latest",
        "models/gemini-1.5-flash",
        "gemini-2.0-flash-exp",
        "gemini-1.5-pro"
    ]
    
    for model in models_to_test:
        print(f"\n--- Testing model: {model} ---")
        try:
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            print(f"SUCCESS! Model '{model}' works.")
            print(f"Response: {response.choices[0].message.content}")
            return # Stop after first success
        except Exception as e:
            print(f"FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_models())
