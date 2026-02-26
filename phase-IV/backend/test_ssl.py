import httpx
import sys

print("Testing httpx get...")
try:
    with httpx.Client() as client:
        resp = client.get("https://google.com")
        print(f"Response: {resp.status_code}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("Testing httpx with verify=False...")
try:
    with httpx.Client(verify=False) as client:
        resp = client.get("https://google.com")
        print(f"Response (verify=False): {resp.status_code}")
except Exception as e:
    print(f"Error (verify=False): {e}")
