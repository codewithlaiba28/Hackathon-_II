import urllib.request
import json
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY") # This is actualy Gemini key
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"

print(f"Querying: {url.replace(key, 'HIDDEN')}")

try:
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())
        print("Available models:")
        for m in data.get('models', []):
            if "generateContent" in m.get("supportedGenerationMethods", []):
                print(f" - {m['name']}")
except Exception as e:
    print(f"Error: {e}")
