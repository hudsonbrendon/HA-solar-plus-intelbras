"""DataUpdateCoordinator for solar_plus_intelbras."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    SolarPlusIntelbrasApiClientAuthenticationError,
    SolarPlusIntelbrasApiClientError,
)
from .const import DOMAIN, LOGGER

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import SolarPlusIntelbrasConfigEntry


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class SolarPlusIntelbrasDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: SolarPlusIntelbrasConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        try:
            return await self.config_entry.runtime_data.client.async_get_data()
        except SolarPlusIntelbrasApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except SolarPlusIntelbrasApiClientError as exception:
            raise UpdateFailed(exception) from exception
