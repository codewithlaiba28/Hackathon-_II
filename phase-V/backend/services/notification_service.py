"""
Notification Service for Advanced Todo Features

This module provides the interface and implementation for sending
notifications for reminders, recurring tasks, and other events.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import logging
from dataclasses import dataclass


@dataclass
class Notification:
    """Data class for notification information"""
    recipient_id: str
    title: str
    message: str
    notification_type: str  # 'reminder', 'recurring_task', 'task_update', etc.
    task_id: Optional[int] = None
    scheduled_time: Optional[datetime] = None
    priority: str = "normal"  # 'low', 'normal', 'high', 'urgent'


class NotificationServiceInterface(ABC):
    """Abstract interface for notification services"""

    @abstractmethod
    async def send_notification(self, notification: Notification) -> bool:
        """
        Send a notification to the recipient.

        Args:
            notification: Notification object containing details

        Returns:
            True if sent successfully, False otherwise
        """
        pass

    @abstractmethod
    async def schedule_notification(self, notification: Notification) -> str:
        """
        Schedule a notification to be sent at a later time.

        Args:
            notification: Notification object containing details

        Returns:
            Scheduled notification ID
        """
        pass

    @abstractmethod
    async def cancel_scheduled_notification(self, notification_id: str) -> bool:
        """
        Cancel a scheduled notification.

        Args:
            notification_id: ID of the scheduled notification to cancel

        Returns:
            True if canceled successfully, False otherwise
        """
        pass


class MockNotificationService(NotificationServiceInterface):
    """Mock notification service for development/testing"""

    def __init__(self):
        self.notifications_sent = []
        self.scheduled_notifications = {}
        self._notification_counter = 0
        self.logger = logging.getLogger(__name__)

    async def send_notification(self, notification: Notification) -> bool:
        """Send a notification to the recipient."""
        try:
            self.logger.info(f"Sending notification to {notification.recipient_id}: {notification.title}")
            self.notifications_sent.append({
                "recipient_id": notification.recipient_id,
                "title": notification.title,
                "message": notification.message,
                "type": notification.notification_type,
                "task_id": notification.task_id,
                "sent_at": datetime.now(),
                "priority": notification.priority
            })
            print(f"[MOCK NOTIFICATION] To: {notification.recipient_id}")
            print(f"[MOCK NOTIFICATION] Title: {notification.title}")
            print(f"[MOCK NOTIFICATION] Message: {notification.message}")
            print(f"[MOCK NOTIFICATION] Type: {notification.notification_type}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
            return False

    async def schedule_notification(self, notification: Notification) -> str:
        """Schedule a notification to be sent at a later time."""
        try:
            self._notification_counter += 1
            notification_id = f"scheduled_{self._notification_counter}_{notification.recipient_id}"
            self.scheduled_notifications[notification_id] = {
                "notification": notification,
                "scheduled_at": datetime.now(),
                "status": "scheduled"
            }
            self.logger.info(f"Scheduled notification {notification_id} for {notification.recipient_id}")
            return notification_id
        except Exception as e:
            self.logger.error(f"Failed to schedule notification: {e}")
            return ""

    async def cancel_scheduled_notification(self, notification_id: str) -> bool:
        """Cancel a scheduled notification."""
        try:
            if notification_id in self.scheduled_notifications:
                self.scheduled_notifications[notification_id]["status"] = "cancelled"
                self.logger.info(f"Cancelled scheduled notification {notification_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to cancel scheduled notification: {e}")
            return False

    def get_sent_notifications(self) -> list:
        """Get list of sent notifications for testing purposes."""
        return self.notifications_sent.copy()

    def get_scheduled_notifications(self) -> dict:
        """Get dictionary of scheduled notifications for testing purposes."""
        return self.scheduled_notifications.copy()


class WebSocketNotificationService(NotificationServiceInterface):
    """WebSocket-based notification service for real-time delivery"""

    def __init__(self, websocket_manager=None):
        self.websocket_manager = websocket_manager
        self.logger = logging.getLogger(__name__)
        self.active_connections = {}

    async def send_notification(self, notification: Notification) -> bool:
        """Send a notification via WebSocket."""
        try:
            # In a real implementation, this would send the notification via WebSocket
            # to the connected client for the recipient_id
            self.logger.info(f"Sending WebSocket notification to {notification.recipient_id}")

            # For now, we'll simulate WebSocket sending
            if self.websocket_manager:
                # This would broadcast to all connections for the user
                await self.websocket_manager.broadcast_to_user(
                    notification.recipient_id,
                    {
                        "type": "notification",
                        "title": notification.title,
                        "message": notification.message,
                        "task_id": notification.task_id,
                        "notification_type": notification.notification_type,
                        "timestamp": datetime.now().isoformat()
                    }
                )
            else:
                # Simulate WebSocket sending without actual manager
                print(f"[WS NOTIFICATION] To: {notification.recipient_id}")
                print(f"[WS NOTIFICATION] Title: {notification.title}")
                print(f"[WS NOTIFICATION] Message: {notification.message}")
                print(f"[WS NOTIFICATION] Type: {notification.notification_type}")

            return True
        except Exception as e:
            self.logger.error(f"Failed to send WebSocket notification: {e}")
            return False

    async def schedule_notification(self, notification: Notification) -> str:
        """Schedule a notification - for WebSocket, this would use a background service."""
        # For WebSocket notifications, scheduling would be handled by a separate
        # service that triggers the WebSocket notification at the right time
        self.logger.info(f"Scheduling WebSocket notification via external service for {notification.recipient_id}")
        # Return a mock ID
        return f"ws_scheduled_{hash(notification.recipient_id + str(notification.scheduled_time))}"

    async def cancel_scheduled_notification(self, notification_id: str) -> bool:
        """Cancel a scheduled WebSocket notification."""
        # Implementation would depend on how scheduling is handled
        self.logger.info(f"Attempting to cancel scheduled WebSocket notification {notification_id}")
        return True  # Simplified for mock


class EmailNotificationService(NotificationServiceInterface):
    """Email-based notification service"""

    def __init__(self, smtp_config: Optional[Dict[str, Any]] = None):
        self.smtp_config = smtp_config or {}
        self.logger = logging.getLogger(__name__)

    async def send_notification(self, notification: Notification) -> bool:
        """Send a notification via email."""
        try:
            self.logger.info(f"Sending email notification to {notification.recipient_id}")
            # In a real implementation, this would send an email
            print(f"[EMAIL NOTIFICATION] To: {notification.recipient_id}")
            print(f"[EMAIL NOTIFICATION] Subject: {notification.title}")
            print(f"[EMAIL NOTIFICATION] Body: {notification.message}")
            print(f"[EMAIL NOTIFICATION] Type: {notification.notification_type}")

            # Simulate email sending delay
            await asyncio.sleep(0.1)
            return True
        except Exception as e:
            self.logger.error(f"Failed to send email notification: {e}")
            return False

    async def schedule_notification(self, notification: Notification) -> str:
        """Schedule an email notification."""
        self.logger.info(f"Scheduling email notification for {notification.recipient_id}")
        # Return a mock ID
        return f"email_scheduled_{hash(notification.recipient_id + str(notification.scheduled_time))}"

    async def cancel_scheduled_notification(self, notification_id: str) -> bool:
        """Cancel a scheduled email notification."""
        self.logger.info(f"Attempting to cancel scheduled email notification {notification_id}")
        return True


class SMSNotificationService(NotificationServiceInterface):
    """SMS-based notification service"""

    def __init__(self, sms_config: Optional[Dict[str, Any]] = None):
        self.sms_config = sms_config or {}
        self.logger = logging.getLogger(__name__)

    async def send_notification(self, notification: Notification) -> bool:
        """Send a notification via SMS."""
        try:
            self.logger.info(f"Sending SMS notification to {notification.recipient_id}")
            # In a real implementation, this would send an SMS
            print(f"[SMS NOTIFICATION] To: {notification.recipient_id}")
            print(f"[SMS NOTIFICATION] Message: {notification.message}")
            print(f"[SMS NOTIFICATION] Type: {notification.notification_type}")

            # Simulate SMS sending delay
            await asyncio.sleep(0.1)
            return True
        except Exception as e:
            self.logger.error(f"Failed to send SMS notification: {e}")
            return False

    async def schedule_notification(self, notification: Notification) -> str:
        """Schedule an SMS notification."""
        self.logger.info(f"Scheduling SMS notification for {notification.recipient_id}")
        # Return a mock ID
        return f"sms_scheduled_{hash(notification.recipient_id + str(notification.scheduled_time))}"

    async def cancel_scheduled_notification(self, notification_id: str) -> bool:
        """Cancel a scheduled SMS notification."""
        self.logger.info(f"Attempting to cancel scheduled SMS notification {notification_id}")
        return True


class CompositeNotificationService(NotificationServiceInterface):
    """Composite notification service that combines multiple services"""

    def __init__(self, services: Optional[list] = None):
        self.services = services or []
        self.logger = logging.getLogger(__name__)

    def add_service(self, service: NotificationServiceInterface):
        """Add a notification service to the composite."""
        self.services.append(service)

    async def send_notification(self, notification: Notification) -> bool:
        """Send notification using all registered services."""
        results = []
        for service in self.services:
            try:
                result = await service.send_notification(notification)
                results.append(result)
                if result:
                    self.logger.debug(f"Notification sent successfully via {type(service).__name__}")
                else:
                    self.logger.warning(f"Failed to send notification via {type(service).__name__}")
            except Exception as e:
                self.logger.error(f"Error sending notification via {type(service).__name__}: {e}")
                results.append(False)

        # Return True if at least one service succeeded
        return any(results)

    async def schedule_notification(self, notification: Notification) -> str:
        """Schedule notification using all registered services."""
        # In a real implementation, you might want to schedule differently for each service
        # For now, we'll return a mock ID
        self.logger.info(f"Scheduling notification across {len(self.services)} services")
        return f"composite_{hash(notification.recipient_id + str(notification.scheduled_time))}"

    async def cancel_scheduled_notification(self, notification_id: str) -> bool:
        """Cancel scheduled notification across all services."""
        results = []
        for service in self.services:
            try:
                result = await service.cancel_scheduled_notification(notification_id)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error cancelling notification via {type(service).__name__}: {e}")
                results.append(False)

        return any(results)


# Default notification service instance
def get_default_notification_service() -> NotificationServiceInterface:
    """
    Get the default notification service instance.
    In a real application, this would be configured based on environment settings.
    """
    # For development, use mock service
    return MockNotificationService()


if __name__ == "__main__":
    # Test the notification services
    async def test_notifications():
        print("Testing notification services...")

        # Test mock notification service
        mock_service = MockNotificationService()
        notification = Notification(
            recipient_id="user123",
            title="Task Reminder",
            message="Your task 'Complete project' is due soon!",
            notification_type="reminder",
            task_id=1,
            priority="high"
        )

        result = await mock_service.send_notification(notification)
        print(f"Mock notification sent: {result}")

        # Test WebSocket notification service
        ws_service = WebSocketNotificationService()
        result = await ws_service.send_notification(notification)
        print(f"WebSocket notification sent: {result}")

        # Test composite service
        composite = CompositeNotificationService([
            MockNotificationService(),
            EmailNotificationService()
        ])
        result = await composite.send_notification(notification)
        print(f"Composite notification sent: {result}")

        print("Notification services test completed.")

    # Run the test
    asyncio.run(test_notifications())