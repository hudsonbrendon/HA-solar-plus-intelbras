"""Tests for the notifier."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.solar_plus_intelbras.const import (
    PRIORITY_CRITICAL,
    PRIORITY_NORMAL,
)
from custom_components.solar_plus_intelbras.notify import SolarPlusIntelbrasNotifier

CREATE = "custom_components.solar_plus_intelbras.notify.create_notification"


def _notifier() -> SolarPlusIntelbrasNotifier:
    hass = MagicMock()
    hass.services.async_call = AsyncMock()
    return SolarPlusIntelbrasNotifier(hass)


@pytest.mark.asyncio
async def test_critical_alert_awaits_notify_service() -> None:
    """A critical alert creates a persistent notification and calls notify.notify."""
    notifier = _notifier()
    with patch(CREATE) as create:
        await notifier.async_send_alert(message="Inverter down", title="Alert", priority=PRIORITY_CRITICAL)
        create.assert_called_once()
        notifier.hass.services.async_call.assert_awaited_once()


@pytest.mark.asyncio
async def test_normal_alert_does_not_call_notify_service() -> None:
    """A normal alert only creates a persistent notification."""
    notifier = _notifier()
    with patch(CREATE) as create:
        nid = await notifier.async_send_alert(message="hi", priority=PRIORITY_NORMAL)
        create.assert_called_once()
        notifier.hass.services.async_call.assert_not_called()
        assert nid.startswith("solar_plus_intelbras_")


@pytest.mark.asyncio
async def test_clear_notification_dismisses() -> None:
    """Clearing a notification calls the dismiss service."""
    notifier = _notifier()
    await notifier.async_clear_notification("abc")
    notifier.hass.services.async_call.assert_awaited_once()


@pytest.mark.asyncio
async def test_system_status_alert_maps_offline_to_critical() -> None:
    """An 'offline' status escalates to a critical alert."""
    notifier = _notifier()
    with patch(CREATE):
        await notifier.async_send_system_status_alert("offline", "no data")
        notifier.hass.services.async_call.assert_awaited_once()


@pytest.mark.asyncio
async def test_check_notifications_without_client_logs_and_returns() -> None:
    """With no API client registered, the check is a no-op."""
    notifier = _notifier()
    with patch(CREATE) as create:
        await notifier._async_check_notifications()  # noqa: SLF001
        create.assert_not_called()


@pytest.mark.asyncio
async def test_check_notifications_processes_and_dedups() -> None:
    """API notifications create alerts once per id (deduplicated)."""
    notifier = _notifier()
    client = AsyncMock()
    client.async_get_notifications = AsyncMock(return_value={"rows": [{"id": 1, "title": "T", "description": "D"}]})
    notifier.register_api_client(client)
    with patch(CREATE) as create:
        await notifier._async_check_notifications()  # noqa: SLF001
        await notifier._async_check_notifications()  # noqa: SLF001 (same id -> no second alert)
        create.assert_called_once()


@pytest.mark.asyncio
async def test_system_status_warning_maps_to_warning() -> None:
    """A 'degraded' status maps to a warning (no critical service call)."""
    notifier = _notifier()
    with patch(CREATE) as create:
        await notifier.async_send_system_status_alert("degraded")
        create.assert_called_once()
        notifier.hass.services.async_call.assert_not_called()


@pytest.mark.asyncio
async def test_check_notifications_service_runs() -> None:
    """The manual check service triggers a notification check."""
    notifier = _notifier()
    client = AsyncMock()
    client.async_get_notifications = AsyncMock(return_value={"rows": []})
    notifier.register_api_client(client)
    await notifier.async_check_notifications_service(MagicMock())
    client.async_get_notifications.assert_awaited_once()


@pytest.mark.asyncio
async def test_check_notifications_swallows_api_error() -> None:
    """An API error during the check is logged, not raised."""
    notifier = _notifier()
    client = AsyncMock()
    client.async_get_notifications = AsyncMock(side_effect=RuntimeError("boom"))
    notifier.register_api_client(client)
    await notifier._async_check_notifications()  # noqa: SLF001 (must not raise)


@pytest.mark.asyncio
async def test_setup_schedules_and_teardown_cancels() -> None:
    """async_setup schedules an interval and async_teardown cancels it."""
    notifier = _notifier()
    cancel = MagicMock()
    with patch(
        "custom_components.solar_plus_intelbras.notify.async_track_time_interval",
        return_value=cancel,
    ):
        await notifier.async_setup()
    notifier.async_teardown()
    cancel.assert_called_once()
