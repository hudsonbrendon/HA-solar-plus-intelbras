"""SolarPlusIntelbrasEntity base class."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator


class SolarPlusIntelbrasEntity(CoordinatorEntity[SolarPlusIntelbrasDataUpdateCoordinator]):
    """Base entity for Solar Plus Intelbras."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(self, coordinator: SolarPlusIntelbrasDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
