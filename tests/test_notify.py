"""Tests for the notifier's critical-alert dispatch."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from custom_components.solar_plus_intelbras.const import PRIORITY_CRITICAL
from custom_components.solar_plus_intelbras.notify import SolarPlusIntelbrasNotifier


@pytest.mark.asyncio
async def test_critical_alert_awaits_notify_service() -> None:
    """A critical alert creates a persistent notification and calls notify.notify."""
    hass = MagicMock()
    hass.services.async_call = AsyncMock()
    notifier = SolarPlusIntelbrasNotifier(hass)
    with patch(
        "custom_components.solar_plus_intelbras.notify.create_notification"
    ) as create:
        await notifier.async_send_alert(
            message="Inverter down",
            title="Alert",
            priority=PRIORITY_CRITICAL,
        )
        create.assert_called_once()
        hass.services.async_call.assert_awaited_once()
