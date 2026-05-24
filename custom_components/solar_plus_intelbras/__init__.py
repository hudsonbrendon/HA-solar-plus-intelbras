"""
Custom integration to integrate solar_plus_intelbras with Home Assistant.

For more details about this integration, please refer to
https://github.com/hudsonbrendon/HA-solar-plus-intelbras
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import ConfigEntryState
from homeassistant.const import Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.loader import async_get_loaded_integration

from .api import SolarPlusIntelbrasApiClient
from .const import (
    ATTR_MESSAGE,
    ATTR_NOTIFICATION_ID,
    ATTR_PRIORITY,
    ATTR_TITLE,
    CONF_EMAIL,
    CONF_PLANT_ID,
    CONF_PLUS,
    CONF_YEARS,
    DEFAULT_IMPORT_YEARS,
    DOMAIN,
    LOGGER,
    MAX_IMPORT_YEARS,
    NOTIFICATION_TITLE_DEFAULT,
    PRIORITY_CRITICAL,
    PRIORITY_INFO,
    PRIORITY_NORMAL,
    PRIORITY_WARNING,
)
from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator
from .data import SolarPlusIntelbrasData
from .notify import SolarPlusIntelbrasNotifier
from .statistics import async_import_history

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import SolarPlusIntelbrasConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
]

# This integration is configured via the UI and accepts no YAML config keys.
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = SolarPlusIntelbrasDataUpdateCoordinator(
        hass=hass,
        config_entry=entry,
    )

    client = SolarPlusIntelbrasApiClient(
        email=entry.data[CONF_EMAIL],
        plus=entry.data[CONF_PLUS],
        plant_id=entry.data[CONF_PLANT_ID],
        session=async_get_clientsession(hass),
    )

    entry.runtime_data = SolarPlusIntelbrasData(
        client=client,
        integration=async_get_loaded_integration(hass, entry.domain),
        coordinator=coordinator,
    )

    # Register the API client with the notifier for notifications
    if DOMAIN in hass.data and "notifier" in hass.data[DOMAIN]:
        notifier = hass.data[DOMAIN]["notifier"]
        notifier.register_api_client(client)
        await notifier.async_setup()

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
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded and DOMAIN in hass.data and "notifier" in hass.data[DOMAIN]:
        hass.data[DOMAIN]["notifier"].async_teardown()
    return unloaded


async def async_reload_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Solar Plus Intelbras component."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    notifier = SolarPlusIntelbrasNotifier(hass)
    hass.data[DOMAIN]["notifier"] = notifier

    async def handle_send_alert(call: vol.Schema) -> dict:
        """Handle the service call."""
        message = call.data.get(ATTR_MESSAGE, "")
        title = call.data.get(ATTR_TITLE, NOTIFICATION_TITLE_DEFAULT)
        notification_id = call.data.get(ATTR_NOTIFICATION_ID)
        priority = call.data.get(ATTR_PRIORITY, PRIORITY_NORMAL)

        notification_id = await notifier.async_send_alert(
            message=message, title=title, notification_id=notification_id, priority=priority
        )
        LOGGER.info("Created notification: %s", title)

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

    hass.services.async_register(
        DOMAIN,
        "check_notifications",
        notifier.async_check_notifications_service,
        schema=vol.Schema({}),
    )

    async def handle_import_history(call: vol.Schema) -> None:
        """Backfill long-term statistics with monthly generation history."""
        years = call.data.get(CONF_YEARS, DEFAULT_IMPORT_YEARS)
        end_year = datetime.now(UTC).year
        start_year = end_year - years + 1
        for entry in hass.config_entries.async_entries(DOMAIN):
            if entry.state is not ConfigEntryState.LOADED:
                continue
            count = await async_import_history(
                hass,
                entry.runtime_data.client,
                plant_id=entry.data[CONF_PLANT_ID],
                name=entry.title,
                year_range=(start_year, end_year),
            )
            LOGGER.info("Imported %s history points for plant %s", count, entry.data[CONF_PLANT_ID])

    hass.services.async_register(
        DOMAIN,
        "import_history",
        handle_import_history,
        schema=vol.Schema(
            {
                vol.Optional(CONF_YEARS, default=DEFAULT_IMPORT_YEARS): vol.All(
                    int, vol.Range(min=1, max=MAX_IMPORT_YEARS)
                )
            }
        ),
    )
    return True
