"""
Event Publishing Utilities for Advanced Todo Features

This module provides utilities for publishing events to Kafka via Dapr
for the event-driven architecture implementation.
"""

import asyncio
import os
import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import logging
from enum import Enum


class EventType(Enum):
    """Enumeration of event types for the todo application"""
    TASK_CREATED = "task.created"
    TASK_UPDATED = "task.updated"
    TASK_COMPLETED = "task.completed"
    TASK_DELETED = "task.deleted"
    TASK_REMINDER_SCHEDULED = "task.reminder.scheduled"
    TASK_REMINDER_SENT = "task.reminder.sent"
    TASK_RECURRING_CREATED = "task.recurring.created"
    TASK_RECURRING_PROCESSED = "task.recurring.processed"
    TASK_SEARCH_INDEXED = "task.search.indexed"


class EventPublisher:
    """Utility class for publishing events via Dapr"""

    def __init__(self, dapr_http_port: int = 3500, dapr_grpc_port: int = 50001):
        self.dapr_http_port = dapr_http_port
        self.dapr_grpc_port = dapr_grpc_port
        self.base_url = f"http://localhost:{dapr_http_port}"
        # Make pubsub component name configurable (default to 'kafka-pubsub' as per existing code, or 'pubsub' for K8s/Redis)
        # Use 'pubsub' as default for K8s deployment
        self.pubsub_name = os.getenv("DAPR_PUBSUB_NAME", "pubsub")
        self.logger = logging.getLogger(__name__)


    async def publish_event(
        self,
        topic_name: str,
        event_type: EventType,
        data: Dict[str, Any],
        correlation_id: Optional[str] = None
    ) -> bool:
        """
        Publish an event to a Kafka topic via Dapr.

        Args:
            topic_name: Name of the Kafka topic to publish to
            event_type: Type of event being published
            data: Event data payload
            correlation_id: Optional correlation ID for tracking

        Returns:
            True if published successfully, False otherwise
        """
        try:
            # Construct the event envelope
            event_payload = {
                "id": correlation_id or f"event_{datetime.utcnow().isoformat()}_{hash(str(data))}",
                "type": event_type.value,
                "source": "todo-app.backend",
                "data": data,
                "datacontenttype": "application/json",
                "time": datetime.utcnow().isoformat() + "Z",
                "correlation_id": correlation_id or ""
            }

            # Publish via Dapr pubsub
            url = f"{self.base_url}/v1.0/publish/{self.pubsub_name}/{topic_name}"


            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    url,
                    json=event_payload,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code in [200, 204]:
                    self.logger.info(f"Event published successfully to topic '{topic_name}': {event_type.value}")
                    return True
                else:
                    self.logger.error(f"Failed to publish event to topic '{topic_name}': {response.status_code} - {response.text}")
                    return False

        except httpx.RequestError as e:
            self.logger.error(f"Request error when publishing event: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error when publishing event: {e}")
            return False

    async def publish_task_event(
        self,
        user_id: str,
        task_id: int,
        event_type: EventType,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Publish a task-related event.

        Args:
            user_id: ID of the user associated with the task
            task_id: ID of the task
            event_type: Type of task event
            additional_data: Additional event data

        Returns:
            True if published successfully, False otherwise
        """
        data = {
            "user_id": user_id,
            "task_id": task_id,
            "timestamp": datetime.utcnow().isoformat()
        }

        if additional_data:
            data.update(additional_data)

        topic_map = {
            EventType.TASK_CREATED: "task-events",
            EventType.TASK_UPDATED: "task-events",
            EventType.TASK_COMPLETED: "task-events",
            EventType.TASK_DELETED: "task-events",
            EventType.TASK_REMINDER_SCHEDULED: "reminders",
            EventType.TASK_REMINDER_SENT: "reminders",
            EventType.TASK_RECURRING_CREATED: "task-events",
            EventType.TASK_RECURRING_PROCESSED: "task-events",
            EventType.TASK_SEARCH_INDEXED: "task-search-index"
        }

        topic_name = topic_map.get(event_type, "task-events")
        return await self.publish_event(topic_name, event_type, data)

    async def batch_publish_events(
        self,
        events: List[Dict[str, Any]]
    ) -> List[bool]:
        """
        Publish multiple events in a batch.

        Args:
            events: List of event dictionaries with keys: topic_name, event_type, data, correlation_id

        Returns:
            List of boolean results indicating success/failure for each event
        """
        results = []
        for event in events:
            result = await self.publish_event(
                event["topic_name"],
                event["event_type"],
                event["data"],
                event.get("correlation_id")
            )
            results.append(result)

        return results

    async def publish_task_created_event(
        self,
        user_id: str,
        task_id: int,
        task_title: str,
        priority: str = "medium"
    ) -> bool:
        """Publish a task created event."""
        return await self.publish_task_event(
            user_id, task_id, EventType.TASK_CREATED,
            {
                "title": task_title,
                "priority": priority
            }
        )

    async def publish_task_updated_event(
        self,
        user_id: str,
        task_id: int,
        changes: Dict[str, Any]
    ) -> bool:
        """Publish a task updated event."""
        return await self.publish_task_event(
            user_id, task_id, EventType.TASK_UPDATED,
            {"changes": changes}
        )

    async def publish_task_completed_event(
        self,
        user_id: str,
        task_id: int,
        is_recurring: bool = False,
        recurrence_pattern: Optional[str] = None
    ) -> bool:
        """Publish a task completed event."""
        return await self.publish_task_event(
            user_id, task_id, EventType.TASK_COMPLETED,
            {
                "event_type": "task.completed", # Explicitly add for older consumers
                "is_recurring": is_recurring,
                "recurrence_pattern": recurrence_pattern
            }
        )

    async def publish_task_deleted_event(
        self,
        user_id: str,
        task_id: int
    ) -> bool:
        """Publish a task deleted event."""
        return await self.publish_task_event(
            user_id, task_id, EventType.TASK_DELETED
        )

    async def publish_reminder_scheduled_event(
        self,
        user_id: str,
        task_id: int,
        reminder_time: datetime,
        notification_type: str = "email"
    ) -> bool:
        """Publish a reminder scheduled event."""
        return await self.publish_task_event(
            user_id, task_id, EventType.TASK_REMINDER_SCHEDULED,
            {
                "reminder_time": reminder_time.isoformat(),
                "notification_type": notification_type
            }
        )

    async def publish_reminder_sent_event(
        self,
        user_id: str,
        task_id: int,
        notification_id: str,
        success: bool = True
    ) -> bool:
        """Publish a reminder sent event."""
        return await self.publish_task_event(
            user_id, task_id, EventType.TASK_REMINDER_SENT,
            {
                "notification_id": notification_id,
                "success": success
            }
        )

    async def publish_recurring_task_created_event(
        self,
        user_id: str,
        original_task_id: int,
        new_task_id: int,
        recurrence_pattern: str
    ) -> bool:
        """Publish a recurring task created event."""
        return await self.publish_task_event(
            user_id, new_task_id, EventType.TASK_RECURRING_CREATED,
            {
                "original_task_id": original_task_id,
                "recurrence_pattern": recurrence_pattern
            }
        )

    async def publish_search_indexed_event(
        self,
        user_id: str,
        task_id: int,
        indexed_fields: List[str]
    ) -> bool:
        """Publish a search indexed event."""
        return await self.publish_task_event(
            user_id, task_id, EventType.TASK_SEARCH_INDEXED,
            {"indexed_fields": indexed_fields}
        )


class MockEventPublisher(EventPublisher):
    """Mock event publisher for development/testing when Dapr is not available"""

    def __init__(self):
        super().__init__()
        self.published_events = []
        self.logger = logging.getLogger(__name__)

    async def publish_event(
        self,
        topic_name: str,
        event_type: EventType,
        data: Dict[str, Any],
        correlation_id: Optional[str] = None
    ) -> bool:
        """
        Mock publish event - stores in memory instead of sending to Dapr/Kafka.
        """
        try:
            event_payload = {
                "id": correlation_id or f"mock_event_{datetime.utcnow().isoformat()}_{hash(str(data))}",
                "type": event_type.value,
                "source": "todo-app.backend.mock",
                "data": data,
                "datacontenttype": "application/json",
                "time": datetime.utcnow().isoformat() + "Z",
                "correlation_id": correlation_id or "",
                "topic": topic_name
            }

            self.published_events.append(event_payload)
            self.logger.info(f"[MOCK] Event published to topic '{topic_name}': {event_type.value}")
            print(f"[MOCK EVENT] Topic: {topic_name}")
            print(f"[MOCK EVENT] Type: {event_type.value}")
            print(f"[MOCK EVENT] Data: {json.dumps(data, indent=2, default=str)}")

            return True
        except Exception as e:
            self.logger.error(f"Mock event publishing failed: {e}")
            return False

    def get_published_events(self) -> List[Dict[str, Any]]:
        """Get list of published events for testing purposes."""
        return self.published_events.copy()

    def clear_events(self):
        """Clear the list of published events."""
        self.published_events.clear()


def get_event_publisher(use_mock: bool = False) -> EventPublisher:
    """
    Get the appropriate event publisher instance.

    Args:
        use_mock: If True, return a mock publisher instead of the real one

    Returns:
        An EventPublisher instance
    """
    if use_mock:
        return MockEventPublisher()
    else:
        # Check if Dapr is enabled via environment variable
        import os
        enable_dapr = os.getenv("ENABLE_DAPR", "false").lower() == "true"
        
        if not enable_dapr:
            return MockEventPublisher()

        # Check if Dapr configuration is available
        try:
            dapr_http_port = int(os.getenv("DAPR_HTTP_PORT", 3500))
            dapr_grpc_port = int(os.getenv("DAPR_GRPC_PORT", 50001))
            return EventPublisher(dapr_http_port, dapr_grpc_port)
        except (ImportError, ValueError):
            # Fallback to mock
            return MockEventPublisher()


# Global instance for convenience
event_publisher = get_event_publisher()


if __name__ == "__main__":
    # Test the event publisher
    async def test_event_publisher():
        print("Testing event publisher...")

        # Test with mock publisher
        mock_publisher = MockEventPublisher()

        # Test basic event publishing
        result = await mock_publisher.publish_event(
            "test-topic",
            EventType.TASK_CREATED,
            {"test": "data", "value": 42}
        )
        print(f"Basic event published: {result}")

        # Test task event publishing
        result = await mock_publisher.publish_task_created_event(
            "user123",
            1,
            "Test Task",
            "high"
        )
        print(f"Task created event published: {result}")

        # Test reminder scheduled event
        result = await mock_publisher.publish_reminder_scheduled_event(
            "user123",
            1,
            datetime.utcnow()
        )
        print(f"Reminder scheduled event published: {result}")

        # Test recurring task event
        result = await mock_publisher.publish_recurring_task_created_event(
            "user123",
            1,
            2,
            "daily"
        )
        print(f"Recurring task created event published: {result}")

        # Show all published events
        print(f"\nTotal published events: {len(mock_publisher.get_published_events())}")
        for i, event in enumerate(mock_publisher.get_published_events()):
            print(f"Event {i+1}: {event['type']} on topic {event['topic']}")

        print("Event publisher test completed.")

    # Run the test
    asyncio.run(test_event_publisher())