"""SolarPlusIntelbrasEntity class."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN
from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator


class SolarPlusIntelbrasEntity(
    CoordinatorEntity[SolarPlusIntelbrasDataUpdateCoordinator]
):
    """SolarPlusIntelbrasEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: SolarPlusIntelbrasDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name="Solar Plus Intelbras",
            manufacturer="Intelbras",
            model="Solar Plus",
            sw_version="1.0.0",
        )


    