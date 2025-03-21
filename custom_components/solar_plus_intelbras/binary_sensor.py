"""Binary sensor platform for solar_plus_intelbras."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory

from .entity import SolarPlusIntelbrasEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator
    from .data import SolarPlusIntelbrasConfigEntry

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="solar_plus_intelbras_online_inverter",
        name="Inverter",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(
        SolarPlusIntelbrasBinarySensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class SolarPlusIntelbrasBinarySensor(SolarPlusIntelbrasEntity, BinarySensorEntity):
    """solar_plus_intelbras binary_sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"binary_sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def is_on(self) -> bool:
        """Return true if the binary_sensor is on."""
        return self.coordinator.data["rows"][0]["online"]
