"""
Custom integration to integrate solar_plus_intelbras with Home Assistant.

For more details about this integration, please refer to
https://github.com/hudsonbrendon/HA-solar-plus-intelbras
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import SolarPlusIntelbrasApiClient
from .const import CONF_EMAIL, CONF_PLANT_ID, CONF_PLUS
from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator
from .data import SolarPlusIntelbrasData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import SolarPlusIntelbrasConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = SolarPlusIntelbrasDataUpdateCoordinator(
        hass=hass,
    )
    entry.runtime_data = SolarPlusIntelbrasData(
        client=SolarPlusIntelbrasApiClient(
            email=entry.data[CONF_EMAIL],
            plus=entry.data[CONF_PLUS],
            plant_id=entry.data[CONF_PLANT_ID],
            session=async_get_clientsession(hass),
        ),
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
