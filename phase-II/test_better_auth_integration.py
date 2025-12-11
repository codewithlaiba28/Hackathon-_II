import requests
import json
import sys
import random

BASE_URL = "http://localhost:8000"

def test_better_auth_integration():
    print("Testing Better Auth integration with FastAPI backend...")

    # Step 1: Test the new sync endpoint
    email = f"testuser_{random.randint(1000, 9999)}@example.com"
    name = "Test User"

    print(f"1. Testing Better Auth sync endpoint for {email}...")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/sync-better-auth-user", json={
            "email": email,
            "name": name
        })

        if response.status_code == 200:
            print("   Better Auth sync successful!")
            data = response.json()
            token = data['token']
            user = data['user']
            print(f"   JWT token received: {token[:20]}...")
            print(f"   User created: {user['email']}")
        else:
            print(f"   Better Auth sync failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   Error during Better Auth sync: {e}")
        return False

    # Step 2: Test that we can use the JWT token to access protected endpoints
    print(f"2. Testing protected endpoint access with JWT token...")
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

    # Step 3: Test creating a task with the JWT token
    print(f"3. Testing task creation with JWT token...")
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        task_data = {
            "title": "Test Task from Better Auth",
            "description": "Task created via Better Auth integration"
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

    # Step 4: Test retrieving the created task
    print(f"4. Testing task retrieval...")
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.get(f"{BASE_URL}/api/tasks/", headers=headers)

        if response.status_code == 200:
            tasks = response.json()
            print(f"   Retrieved {len(tasks)} tasks for user")
            if len(tasks) == 1 and tasks[0]['id'] == task_id:
                print("   User can only access their own tasks - CORRECT!")
            else:
                print("   ERROR: Unexpected task access behavior!")
                return False
        else:
            print(f"   Task retrieval failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   Error retrieving tasks: {e}")
        return False

    print("\nAll Better Auth integration tests passed!")
    return True

if __name__ == "__main__":
    if test_better_auth_integration():
        print("\nVerification Passed: Better Auth integration with FastAPI backend is working.")
        sys.exit(0)
    else:
        print("\nVerification Failed.")
        sys.exit(1)