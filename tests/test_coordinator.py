"""Tests for the coordinator."""

from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock

import pytest
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import UpdateFailed
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.solar_plus_intelbras.api import (
    SolarPlusIntelbrasApiClientAuthenticationError,
    SolarPlusIntelbrasApiClientError,
)
from custom_components.solar_plus_intelbras.const import DOMAIN
from custom_components.solar_plus_intelbras.coordinator import (
    SolarPlusIntelbrasDataUpdateCoordinator,
    build_coordinator_data,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

SAMPLE_YEAR_ENERGY = 292.4


@pytest.fixture(autouse=True)
def _enable_custom_integrations(enable_custom_integrations):  # noqa: ANN001, ANN202
    return


def test_build_coordinator_data_shape(inverters_response: dict) -> None:
    """build_coordinator_data returns a dict with the correct shape and values."""
    data = build_coordinator_data(inverters_response, year_energy=SAMPLE_YEAR_ENERGY, currency="BRL")
    assert data["inverters"] is inverters_response
    assert data["year_energy"] == SAMPLE_YEAR_ENERGY
    assert data["currency"] == "BRL"


def _make_coordinator(hass: HomeAssistant, client: object) -> SolarPlusIntelbrasDataUpdateCoordinator:
    entry = MockConfigEntry(domain=DOMAIN, unique_id="42")
    entry.add_to_hass(hass)
    coordinator = SolarPlusIntelbrasDataUpdateCoordinator(hass, entry)
    entry.runtime_data = SimpleNamespace(client=client)
    return coordinator


async def test_update_data_builds_contract(hass: HomeAssistant) -> None:
    """_async_update_data merges inverters, year energy and currency."""
    client = SimpleNamespace(
        async_get_data=AsyncMock(return_value={"rows": [{"id": 1}]}),
        async_get_year_energy=AsyncMock(return_value=SAMPLE_YEAR_ENERGY),
        currency="BRL",
    )
    coordinator = _make_coordinator(hass, client)
    data = await coordinator._async_update_data()  # noqa: SLF001
    assert data["inverters"]["rows"][0]["id"] == 1
    assert data["year_energy"] == SAMPLE_YEAR_ENERGY
    assert data["currency"] == "BRL"


async def test_update_data_tolerates_year_energy_error(hass: HomeAssistant) -> None:
    """A failure fetching year energy leaves year_energy=None but still returns data."""
    client = SimpleNamespace(
        async_get_data=AsyncMock(return_value={"rows": []}),
        async_get_year_energy=AsyncMock(side_effect=SolarPlusIntelbrasApiClientError("boom")),
        currency="BRL",
    )
    coordinator = _make_coordinator(hass, client)
    data = await coordinator._async_update_data()  # noqa: SLF001
    assert data["year_energy"] is None
    assert data["currency"] == "BRL"


async def test_update_data_auth_error_raises_reauth(hass: HomeAssistant) -> None:
    """An authentication error surfaces as ConfigEntryAuthFailed (drives reauth)."""
    client = SimpleNamespace(
        async_get_data=AsyncMock(side_effect=SolarPlusIntelbrasApiClientAuthenticationError),
    )
    coordinator = _make_coordinator(hass, client)
    with pytest.raises(ConfigEntryAuthFailed):
        await coordinator._async_update_data()  # noqa: SLF001


async def test_update_data_api_error_raises_update_failed(hass: HomeAssistant) -> None:
    """A generic API error surfaces as UpdateFailed."""
    client = SimpleNamespace(
        async_get_data=AsyncMock(side_effect=SolarPlusIntelbrasApiClientError("boom")),
    )
    coordinator = _make_coordinator(hass, client)
    with pytest.raises(UpdateFailed):
        await coordinator._async_update_data()  # noqa: SLF001
