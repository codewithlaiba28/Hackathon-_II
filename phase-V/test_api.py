import requests
import json
import uuid

BASE_URL = "http://localhost:8000/api"

def test_flow():
    # 1. Sign up
    unique_id = str(uuid.uuid4())[:8]
    email = f"test_{unique_id}@example.com"
    password = "Password123!"
    
    print(f"Signing up with {email}...")
    resp = requests.post(f"{BASE_URL}/auth/sign-up", json={
        "email": email,
        "password": password,
        "name": f"Test User {unique_id}"
    })
    
    if resp.status_code != 200 and resp.status_code != 201:
        print(f"Sign up failed: {resp.status_code} - {resp.text}")
        return
        
    data = resp.json()
    user_id = data.get("user", {}).get("id") or data.get("id")
    token = data.get("token") or data.get("access_token")
    
    if not token:
        # Try login
        resp = requests.post(f"{BASE_URL}/auth/sign-in", json={
            "email": email,
            "password": password
        })
        data = resp.json()
        token = data.get("token") or data.get("access_token")
        user_id = data.get("user", {}).get("id") or data.get("id")
        
    print(f"Got user_id: {user_id}")
    
    if not user_id or not token:
        print("Failed to get token or user_id")
        return
        
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 2. Get tasks
    print("Getting tasks...")
    resp = requests.get(f"{BASE_URL}/{user_id}/tasks", headers=headers)
    print(f"GET tasks status: {resp.status_code}")
    
    # 3. Create task
    print("Creating task...")
    try:
        resp = requests.post(f"{BASE_URL}/{user_id}/tasks", headers=headers, json={
            "title": "My test task",
            "description": "Testing from script",
            "priority": "high",
            "status": "pending"
        })
        print(f"POST task status: {resp.status_code}")
        print(resp.text)
    except Exception as e:
        print(f"Exception during POST task: {e}")

if __name__ == "__main__":
    test_flow()
