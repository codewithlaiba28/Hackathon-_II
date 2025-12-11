import requests
from jose import jwt
import datetime
import sys

SECRET = "better_auth_secret_hackathon_phase2_secure_key"
ALGORITHM = "HS256"
BASE_URL = "http://localhost:8000"

def generate_test_token():
    # Simulate a Better Auth token (or at least a valid JWT signed with the secret)
    payload = {
        "sub": "test_user_manual_verification",
        "name": "Test User",
        "email": "test@example.com",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return token

def verify_backend():
    token = generate_test_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"Testing Backend with token: {token[:20]}...")
    
    try:
        # Try to fetch tasks. If auth works, it should return 200 (even if empty list)
        # Assuming the backend auto-creates user if not found? 
        # Wait, backend/auth.py checks `user = session.get(models.User, token_data.user_id)`
        # If user doesn't exist, it returns 401 User not found.
        # So we expect 401 "User not found" BUT NOT "Could not validate credentials".
        
        response = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)
        
        if response.status_code == 200:
            print("Success! Backend accepted token.")
            return True
        elif response.status_code == 401:
            print(f"Got 401: {response.text}")
            if "User not found" in response.text:
                 print("Success! Token signature verified (User just doesn't exist in DB yet).")
                 return True
            else:
                 print("Failed: Token validation error.")
                 return False
        else:
            print(f"Unexpected status: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Connection error: {e}")
        return False

if __name__ == "__main__":
    if verify_backend():
        print("Backend Verification PASSED")
        sys.exit(0)
    else:
        print("Backend Verification FAILED")
        sys.exit(1)
