"""
Custom integration to integrate solar_plus_intelbras with Home Assistant.

For more details about this integration, please refer to
https://github.com/hudsonbrendon/HA-solar-plus-intelbras
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import SolarPlusIntelbrasApiClient
from .const import CONF_EMAIL, CONF_PLANT_ID, CONF_PLUS, DOMAIN
from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator
from .data import SolarPlusIntelbrasData
from .notify import (
    ATTR_MESSAGE,
    ATTR_NOTIFICATION_ID,
    ATTR_PRIORITY,
    ATTR_TITLE,
    NOTIFICATION_TITLE_DEFAULT,
    PRIORITY_CRITICAL,
    PRIORITY_INFO,
    PRIORITY_NORMAL,
    PRIORITY_WARNING,
    SolarPlusIntelbrasNotifier,
)

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


async def async_setup(hass, config):
    """Set up the Solar Plus Intelbras component."""
    # Initialize the dictionary for the domain if it doesn't exist
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    # Initialize the notifier
    hass.data[DOMAIN]["notifier"] = SolarPlusIntelbrasNotifier(hass)

    # Register service to send custom alerts
    async def handle_send_alert(call):
        """Handle the service call."""
        message = call.data.get(ATTR_MESSAGE, "")
        title = call.data.get(ATTR_TITLE, NOTIFICATION_TITLE_DEFAULT)
        notification_id = call.data.get(ATTR_NOTIFICATION_ID)
        priority = call.data.get(ATTR_PRIORITY, PRIORITY_NORMAL)

        notifier = hass.data[DOMAIN]["notifier"]
        notification_id = notifier.send_alert(
            message=message, title=title, notification_id=notification_id, priority=priority
        )

        return {"notification_id": notification_id}

    hass.services.async_register(
        DOMAIN,
        "send_alert",
        handle_send_alert,
        schema=vol.Schema(
            {
                vol.Required(ATTR_MESSAGE): cv.string,
                vol.Optional(ATTR_TITLE): cv.string,
                vol.Optional(ATTR_NOTIFICATION_ID): cv.string,
                vol.Optional(ATTR_PRIORITY): vol.In(
                    [PRIORITY_NORMAL, PRIORITY_WARNING, PRIORITY_CRITICAL, PRIORITY_INFO]
                ),
            }
        ),
    )

    # Return True to indicate successful setup
    return True
