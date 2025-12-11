import requests
import json
import sys
import random

BASE_URL = "http://localhost:8000"

def test_complete_auth_flow():
    print("Testing complete authentication flow...")

    # Step 1: Signup
    email = f"testuser_{random.randint(1000, 9999)}@example.com"
    password = "password123"
    name = "Test User"

    print(f"1. Testing Signup for {email}...")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/signup", json={
            "email": email,
            "password": password,
            "name": name
        })

        if response.status_code == 200:
            print("   Signup Successful!")
            data = response.json()
            token = data['token']
            user = data['user']
            print(f"   Token received: {token[:20]}...")
            print(f"   User created: {user['email']}")
        else:
            print(f"   Signup Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   Error during signup: {e}")
        return False

    # Step 2: Test protected endpoint with token
    print(f"2. Testing protected endpoint with token...")
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)

        if response.status_code == 200:
            print("   Protected endpoint access successful!")
            tasks = response.json()
            print(f"   Retrieved {len(tasks)} tasks for user")
        else:
            print(f"   Protected endpoint access failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   Error accessing protected endpoint: {e}")
        return False

    # Step 3: Create a task
    print(f"3. Testing task creation...")
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        task_data = {
            "title": "Test Task",
            "description": "This is a test task"
        }

        response = requests.post(f"{BASE_URL}/api/tasks/", json=task_data, headers=headers)

        if response.status_code == 200:
            print("   Task creation successful!")
            task = response.json()
            print(f"   Created task ID: {task['id']}")
            task_id = task['id']
        else:
            print(f"   Task creation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   Error creating task: {e}")
        return False

    # Step 4: Test task access (should only see own tasks)
    print(f"4. Testing task access...")
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)

        if response.status_code == 200:
            tasks = response.json()
            print(f"   Retrieved {len(tasks)} tasks for user (should be 1)")
            if len(tasks) == 1 and tasks[0]['id'] == task_id:
                print("   User can only access their own tasks - CORRECT!")
            else:
                print("   ERROR: User can access tasks that don't belong to them!")
                return False
        else:
            print(f"   Task access failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   Error accessing tasks: {e}")
        return False

    print("\nAll tests passed! Authentication flow is working correctly.")
    return True

if __name__ == "__main__":
    if test_complete_auth_flow():
        print("\nVerification Passed: Complete Auth Flow is working.")
        sys.exit(0)
    else:
        print("\nVerification Failed.")
        sys.exit(1)