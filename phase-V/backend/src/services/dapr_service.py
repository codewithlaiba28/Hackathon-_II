from typing import Optional, Dict, Any
from datetime import datetime, timedelta, UTC
import httpx
import os
import json

# Constants for Dapr bindings
DAPR_JOB_BINDING_NAME = "dapr-job-binding" # This needs to be a configured Dapr binding for job scheduling

class DaprService:
    def __init__(self):
        self.dapr_http_port = os.getenv("DAPR_HTTP_PORT", "3500")
        self.base_url = f"http://localhost:{self.dapr_http_port}"

    async def schedule_reminder_job(self, task_id: int, user_id: str, remind_at: datetime, title: str = "Task Reminder") -> bool:
        """
        Schedules a reminder job using Dapr Jobs API.
        """
        print(f"DaprService: Scheduling reminder job for task {task_id} at {remind_at}")
        
        url = f"{self.base_url}/v1.0-alpha1/jobs/reminder-task-{task_id}"
        
        # Ensure remind_at is in UTC and formatted correctly for Dapr
        due_time = remind_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        payload = {
            "dueTime": due_time,
            "data": {
                "task_id": task_id,
                "user_id": user_id,
                "title": title,
                "event_type": "reminder.due"
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                if response.status_code in [200, 204]:
                    print(f"DaprService: Successfully scheduled job for task {task_id}")
                    return True
                else:
                    print(f"DaprService: Failed to schedule job. Status: {response.status_code}, Body: {response.text}")
                    return False
        except Exception as e:
            print(f"DaprService: Error calling Dapr Jobs API: {e}")
            return False

    async def cancel_reminder_job(self, task_id: int) -> bool:
        """
        Cancels a scheduled reminder job using Dapr Jobs API.
        """
        print(f"DaprService: Cancelling reminder job for task {task_id}")
        url = f"{self.base_url}/v1.0-alpha1/jobs/reminder-task-{task_id}"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(url)
                if response.status_code in [200, 204]:
                    print(f"DaprService: Successfully cancelled job for task {task_id}")
                    return True
                else:
                    print(f"DaprService: Failed to cancel job or job not found. Status: {response.status_code}")
                    return False
        except Exception as e:
            print(f"DaprService: Error cancelling Dapr Job: {e}")
            return False