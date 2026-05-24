"""Tests for setup and service handlers."""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.helpers import device_registry as dr
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.solar_plus_intelbras.const import (
    CONF_EMAIL,
    CONF_PLANT_ID,
    CONF_PLUS,
    DOMAIN,
)
from custom_components.solar_plus_intelbras.coordinator import build_coordinator_data

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


def _entry_ids(hass: HomeAssistant, entry_id: str) -> set[tuple[str, str]]:
    registry = dr.async_get(hass)
    ids: set[tuple[str, str]] = set()
    for device in dr.async_entries_for_config_entry(registry, entry_id):
        ids |= device.identifiers
    return ids


async def test_dynamic_and_stale_devices(hass: HomeAssistant, inverters_response: dict) -> None:
    """New inverters are added at runtime and removed ones are pruned."""
    row1 = inverters_response["rows"][0]
    row2 = copy.deepcopy(row1)
    row2["id"] = 9999
    row2["datalogger"] = copy.deepcopy(row1["datalogger"])
    row2["datalogger"]["id"] = 8888

    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="42",
        data={CONF_EMAIL: "e@mail.com", CONF_PLUS: "p", CONF_PLANT_ID: "42"},
    )
    entry.add_to_hass(hass)

    with patch(_GET_DATA, new=AsyncMock(return_value={"rows": [row1]})):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    eid = entry.entry_id
    assert (DOMAIN, f"{eid}_inverter_2113") in _entry_ids(hass, eid)

    coordinator = entry.runtime_data.coordinator

    # A second inverter appears -> its device is added dynamically.
    coordinator.async_set_updated_data(build_coordinator_data({"rows": [row1, row2]}, None, "BRL"))
    await hass.async_block_till_done()
    assert (DOMAIN, f"{eid}_inverter_9999") in _entry_ids(hass, eid)

    # The first inverter disappears -> its device is pruned.
    coordinator.async_set_updated_data(build_coordinator_data({"rows": [row2]}, None, "BRL"))
    await hass.async_block_till_done()
    ids = _entry_ids(hass, eid)
    assert (DOMAIN, f"{eid}_inverter_2113") not in ids
    assert (DOMAIN, f"{eid}_inverter_9999") in ids
