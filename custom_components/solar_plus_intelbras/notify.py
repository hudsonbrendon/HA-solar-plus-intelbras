"""Notification handling for Solar Plus Intelbras integration."""

import time
from datetime import date
from typing import Any

from homeassistant.components.persistent_notification import create as create_notification
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.event import async_track_time_interval

from .api import SolarPlusIntelbrasApiClient
from .const import (
    DEFAULT_NOTIFICATION_CHECK_INTERVAL,
    LOGGER,
    NOTIFICATION_ID_FORMAT,
    NOTIFICATION_TITLE_DEFAULT,
    PRIORITY_CRITICAL,
    PRIORITY_INFO,
    PRIORITY_NORMAL,
    PRIORITY_WARNING,
)


class SolarPlusIntelbrasNotifier:
    """Class to handle notifications for Solar Plus Intelbras."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the notifier."""
        self.hass = hass
        self._unprocessed_notifications = set()
        self._check_interval = None
        self._api_client = None

    def register_api_client(self, api_client: SolarPlusIntelbrasApiClient) -> None:
        """Register the API client for notification checks."""
        self._api_client = api_client

    async def async_setup(self) -> None:
        """Set up the notifier with a scheduled check."""
        if self._check_interval is not None:
            self._check_interval()

        # Schedule periodic checks for notifications
        self._check_interval = async_track_time_interval(
            self.hass,
            self._async_check_notifications,
            DEFAULT_NOTIFICATION_CHECK_INTERVAL,
        )

    async def _async_check_notifications(self, *_) -> None:  # noqa: ANN002
        """Check for new notifications from the API."""
        if self._api_client is None:
            LOGGER.warning("Cannot check notifications: API client not registered")
            return

        try:
            today = date.today()  # noqa: DTZ011
            notifications = await self._api_client.async_get_notifications(start_date=today, end_date=today)

            if notifications.get("rows"):
                await self._process_api_notifications(notifications["rows"])
            else:
                LOGGER.debug("No new notifications found for today")

        except Exception as ex:  # noqa: BLE001
            LOGGER.error("Error checking for notifications: %s", str(ex))

    async def _process_api_notifications(self, notifications: list[dict[str, Any]]) -> None:
        """Process notifications from the API response."""
        for notif in notifications:
            notif_id = str(notif.get("id", ""))

            if notif_id in self._unprocessed_notifications:
                continue

            self._unprocessed_notifications.add(notif_id)

            title = notif.get("title", "Intelbras Solar Plus")
            description = notif.get("description", "")

            notification_id = f"{NOTIFICATION_ID_FORMAT}_api_{notif_id}"
            self.send_alert(message=description, title=title, notification_id=notification_id, priority=PRIORITY_INFO)

            LOGGER.info("Created notification from API: %s", title)

    def send_alert(
        self,
        message: str,
        title: str = NOTIFICATION_TITLE_DEFAULT,
        notification_id: str | None = None,
        priority: str = PRIORITY_NORMAL,
    ) -> str:
        """Send an alert notification."""
        if notification_id is None:
            notification_id = f"{NOTIFICATION_ID_FORMAT}_{int(time.time())}"

        if priority != PRIORITY_NORMAL:
            message = f"[{priority.upper()}] {message}"

        create_notification(self.hass, message=message, title=title, notification_id=notification_id)

        if priority == PRIORITY_CRITICAL:
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

    async def async_check_notifications_service(self, call: ServiceCall) -> None:  # noqa: ARG002
        """Service handler for manually checking notifications."""
        await self._async_check_notifications()
