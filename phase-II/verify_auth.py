import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_signup():
    email = "testuser_unique_123@example.com"
    password = "password123"
    name = "Test User"
    
    print(f"Testing Signup for {email}...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": email,
            "password": password,
            "name": name
        })
        
        if response.status_code == 200:
            print("Signup Successful!")
            data = response.json()
            if "token" in data and "user" in data:
                print(f"Token received: {data['token'][:20]}...")
                print(f"User created: {data['user']['email']}")
                return True
            else:
                print("Response missing token or user data")
        else:
            print(f"Signup Failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        print("Ensure backend is running on localhost:8000")
        
    return False

if __name__ == "__main__":
    if test_signup():
        print("\nVerification Passed: Auth Endpoint is working.")
        sys.exit(0)
    else:
        print("\nVerification Failed.")
        sys.exit(1)
