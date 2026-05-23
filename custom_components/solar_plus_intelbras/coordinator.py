"""DataUpdateCoordinator for solar_plus_intelbras."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    SolarPlusIntelbrasApiClientAuthenticationError,
    SolarPlusIntelbrasApiClientError,
)
from .const import (
    CONF_SCAN_INTERVAL,
    DEFAULT_CURRENCY,
    DEFAULT_SCAN_INTERVAL_MINUTES,
    DOMAIN,
    LOGGER,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import SolarPlusIntelbrasConfigEntry


def build_coordinator_data(
    inverters: dict,
    year_energy: float | None,
    currency: str,
) -> dict[str, Any]:
    """Build the normalized coordinator data dict (single source of truth)."""
    return {
        "inverters": inverters,
        "year_energy": year_energy,
        "currency": currency,
    }


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class SolarPlusIntelbrasDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: SolarPlusIntelbrasConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: SolarPlusIntelbrasConfigEntry,
    ) -> None:
        """Initialize."""
        minutes = config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL_MINUTES
        )
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            config_entry=config_entry,
            update_interval=timedelta(minutes=minutes),
        )

    async def _async_update_data(self) -> Any:
        """Update data via the API client."""
        client = self.config_entry.runtime_data.client
        try:
            inverters = await client.async_get_data()
            year = datetime.now(UTC).year
            try:
                year_energy = await client.async_get_year_energy(year)
            except SolarPlusIntelbrasApiClientError as exception:
                LOGGER.debug("Year energy unavailable: %s", exception)
                year_energy = None
            currency = client.currency or DEFAULT_CURRENCY
            return build_coordinator_data(inverters, year_energy, currency)
        except SolarPlusIntelbrasApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except SolarPlusIntelbrasApiClientError as exception:
            raise UpdateFailed(exception) from exception
