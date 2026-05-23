"""Binary sensor platform for solar_plus_intelbras."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.entity import EntityCategory

from .device import inverter_device_info
from .entity import SolarPlusIntelbrasEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator
    from .data import SolarPlusIntelbrasConfigEntry

ONLINE_DESCRIPTION = BinarySensorEntityDescription(
    key="online",
    translation_key="online",
    device_class=BinarySensorDeviceClass.CONNECTIVITY,
    entity_category=EntityCategory.DIAGNOSTIC,
)


def build_binary_entities(
    coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
) -> list[BinarySensorEntity]:
    """One connectivity binary sensor per inverter row."""
    rows = coordinator.data.get("inverters", {}).get("rows") or []
    return [
        SolarPlusIntelbrasOnlineBinarySensor(coordinator, index)
        for index in range(len(rows))
    ]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    async_add_entities(build_binary_entities(entry.runtime_data.coordinator))


class SolarPlusIntelbrasOnlineBinarySensor(SolarPlusIntelbrasEntity, BinarySensorEntity):
    """Inverter connectivity binary sensor."""

    entity_description = ONLINE_DESCRIPTION

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        row_index: int,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._row_index = row_index
        entry_id = coordinator.config_entry.entry_id
        row = self._row
        self._attr_unique_id = f"{entry_id}_inverter_{row.get('id')}_online"
        self._attr_device_info = inverter_device_info(entry_id, row)

    @property
    def _row(self) -> dict:
        rows = self.coordinator.data.get("inverters", {}).get("rows") or []
        return rows[self._row_index] if self._row_index < len(rows) else {}

    @property
    def is_on(self) -> bool | None:
        """Return true if the inverter reports online."""
        return self._row.get("online")
