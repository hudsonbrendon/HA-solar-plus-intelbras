"""Tests for setup and service handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.solar_plus_intelbras.const import (
    CONF_EMAIL,
    CONF_PLANT_ID,
    CONF_PLUS,
    DOMAIN,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

_GET_DATA = "custom_components.solar_plus_intelbras.api.SolarPlusIntelbrasApiClient.async_get_data"
_IMPORT = "custom_components.solar_plus_intelbras.async_import_history"


@pytest.fixture(autouse=True)
def _enable_custom_integrations(enable_custom_integrations):  # noqa: ANN001, ANN202
    return


async def test_setup_registers_services(hass: HomeAssistant) -> None:
    """async_setup registers the integration services."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    assert hass.services.has_service(DOMAIN, "send_alert")
    assert hass.services.has_service(DOMAIN, "check_notifications")
    assert hass.services.has_service(DOMAIN, "import_history")


async def test_send_alert_service(hass: HomeAssistant) -> None:
    """The send_alert service creates a persistent notification."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    with patch("custom_components.solar_plus_intelbras.notify.create_notification") as create:
        await hass.services.async_call(DOMAIN, "send_alert", {"message": "hi"}, blocking=True)
    create.assert_called_once()


async def test_import_history_service_with_no_entries(hass: HomeAssistant) -> None:
    """import_history is a no-op when there are no loaded entries."""
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    with patch(_IMPORT, new=AsyncMock(return_value=0)) as imp:
        await hass.services.async_call(DOMAIN, "import_history", {}, blocking=True)
    imp.assert_not_called()


async def test_import_history_service_for_loaded_entry(hass: HomeAssistant) -> None:
    """import_history imports for each loaded plant."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="42",
        data={CONF_EMAIL: "e@mail.com", CONF_PLUS: "p", CONF_PLANT_ID: "42"},
    )
    entry.add_to_hass(hass)
    with (
        patch(_GET_DATA, new=AsyncMock(return_value={"rows": []})),
        patch(_IMPORT, new=AsyncMock(return_value=3)) as imp,
    ):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
        await hass.services.async_call(DOMAIN, "import_history", {"years": 1}, blocking=True)
    imp.assert_awaited_once()
