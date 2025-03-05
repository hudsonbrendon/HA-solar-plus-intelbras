"""Notification handling for Solar Plus Intelbras integration."""

import logging
import time

from homeassistant.components.persistent_notification import create as create_notification
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

NOTIFICATION_ID_FORMAT = "solar_plus_intelbras"
NOTIFICATION_TITLE_DEFAULT = "Solar Plus Intelbras Alert"

ATTR_MESSAGE = "message"
ATTR_TITLE = "title"
ATTR_NOTIFICATION_ID = "notification_id"
ATTR_PRIORITY = "priority"

PRIORITY_NORMAL = "normal"
PRIORITY_CRITICAL = "critical"
PRIORITY_WARNING = "warning"
PRIORITY_INFO = "info"


class SolarPlusIntelbrasNotifier:
    """Class to handle notifications for Solar Plus Intelbras."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the notifier."""
        self.hass = hass

    def send_alert(
        self,
        message: str,
        title: str = NOTIFICATION_TITLE_DEFAULT,
        notification_id: str | None = None,
        priority: str = PRIORITY_NORMAL,
    ) -> str:
        """Send an alert notification."""
        if notification_id is None:
            # Create a unique ID using timestamp
            notification_id = f"{NOTIFICATION_ID_FORMAT}_{int(time.time())}"

        # Create the notification
        _LOGGER.debug("Sending notification: %s - %s", title, message)

        # Add priority to message if not normal
        if priority != PRIORITY_NORMAL:
            message = f"[{priority.upper()}] {message}"

        # Create a persistent notification
        create_notification(self.hass, message=message, title=title, notification_id=notification_id)

        # You can also send to other notification methods based on priority
        if priority == PRIORITY_CRITICAL:
            # Could send to multiple services like mobile app, etc.
            service_data = {"message": f"{title}: {message}", "title": "CRITICAL ALERT"}
            self.hass.services.call("notify", "notify", service_data)

        return notification_id

    def send_system_status_alert(self, status: str, details: str | None = None) -> str:
        """Send a system status notification."""
        message = f"System Status: {status}"
        if details:
            message += f"\nDetails: {details}"

        priority = PRIORITY_NORMAL
        if status.lower() in ["error", "failure", "offline"]:
            priority = PRIORITY_CRITICAL
        elif status.lower() in ["warning", "degraded"]:
            priority = PRIORITY_WARNING

        return self.send_alert(
            message=message,
            title="Solar Plus Intelbras System Status",
            notification_id=f"{NOTIFICATION_ID_FORMAT}_system_status",
            priority=priority,
        )

    def clear_notification(self, notification_id: str) -> None:
        """Clear a specific notification."""
        service_data = {"notification_id": notification_id}
        self.hass.services.call("persistent_notification", "dismiss", service_data)
        _LOGGER.debug("Cleared notification: %s", notification_id)
