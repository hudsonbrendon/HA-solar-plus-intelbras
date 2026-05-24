"""Binary sensor platform for solar_plus_intelbras."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.core import callback
from homeassistant.helpers.entity import EntityCategory

from .device import inverter_device_info
from .entity import SolarPlusIntelbrasEntity
from .sensor import row_ids

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator
    from .data import SolarPlusIntelbrasConfigEntry

# Entities are read-only and served from a single coordinator poll.
PARALLEL_UPDATES = 0

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
    return [SolarPlusIntelbrasOnlineBinarySensor(coordinator, row_id) for row_id in row_ids(coordinator.data)]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform with dynamic per-inverter discovery."""
    coordinator = entry.runtime_data.coordinator
    known: set = set()

    @callback
    def _add_new_inverters() -> None:
        new = []
        for row_id in row_ids(coordinator.data):
            if row_id in known:
                continue
            known.add(row_id)
            new.append(SolarPlusIntelbrasOnlineBinarySensor(coordinator, row_id))
        if new:
            async_add_entities(new)

    _add_new_inverters()
    entry.async_on_unload(coordinator.async_add_listener(_add_new_inverters))


class SolarPlusIntelbrasOnlineBinarySensor(SolarPlusIntelbrasEntity, BinarySensorEntity):
    """Inverter connectivity binary sensor."""

    entity_description = ONLINE_DESCRIPTION

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        row_id: object,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._row_id = row_id
        entry_id = coordinator.config_entry.entry_id
        self._attr_unique_id = f"{entry_id}_inverter_{row_id}_online"
        self._attr_device_info = inverter_device_info(entry_id, self._row)

    @property
    def _row(self) -> dict:
        rows = self.coordinator.data.get("inverters", {}).get("rows") or []
        for row in rows:
            if row.get("id") == self._row_id:
                return row
        return {}

    @property
    def available(self) -> bool:
        """Available only while the inverter row still exists."""
        rows = self.coordinator.data.get("inverters", {}).get("rows") or []
        return super().available and any(row.get("id") == self._row_id for row in rows)

    @property
    def is_on(self) -> bool | None:
        """Return true if the inverter reports online."""
        return self._row.get("online")
