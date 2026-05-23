"""Sensor platform for solar_plus_intelbras."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity

from .device import (
    datalogger_device_info,
    inverter_device_info,
    plant_device_info,
)
from .entity import SolarPlusIntelbrasEntity
from .sensor_descriptions import (
    DATALOGGER_SENSORS,
    INVERTER_SENSORS,
    PLANT_SENSORS,
    SolarPlusSensorEntityDescription,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.typing import StateType

    from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator
    from .data import SolarPlusIntelbrasConfigEntry


def build_entities(
    coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
) -> list[SensorEntity]:
    """Create one set of plant sensors plus per-inverter/datalogger sensors."""
    plant = (
        (coordinator.data.get("inverters", {}).get("rows") or [{}])[0].get("plant")
        or {}
    )
    entities: list[SensorEntity] = [
        SolarPlusIntelbrasPlantSensor(coordinator, description, plant.get("name", ""))
        for description in PLANT_SENSORS
    ]

    rows = coordinator.data.get("inverters", {}).get("rows") or []
    for index, _row in enumerate(rows):
        entities.extend(
            SolarPlusIntelbrasInverterSensor(coordinator, description, index)
            for description in INVERTER_SENSORS
        )
        entities.extend(
            SolarPlusIntelbrasDataloggerSensor(coordinator, description, index)
            for description in DATALOGGER_SENSORS
        )
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(build_entities(entry.runtime_data.coordinator))


class _BaseSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Common behavior for description-driven sensors."""

    entity_description: SolarPlusSensorEntityDescription

    @property
    def native_unit_of_measurement(self) -> str | None:
        """Use the live account currency as the unit for monetary sensors."""
        if self.entity_description.device_class == SensorDeviceClass.MONETARY:
            return self.coordinator.data.get("currency", "BRL")
        return self.entity_description.native_unit_of_measurement


class SolarPlusIntelbrasPlantSensor(_BaseSensor):
    """A plant-level sensor (value_fn receives the full coordinator data)."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        description: SolarPlusSensorEntityDescription,
        plant_name: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.entity_description = description
        entry_id = coordinator.config_entry.entry_id
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_device_info = plant_device_info(entry_id, plant_name)

    @property
    def native_value(self) -> StateType:
        """Return the sensor value."""
        return self.entity_description.value_fn(self.coordinator.data)


class _RowSensor(_BaseSensor):
    """Base for sensors whose value_fn receives a single inverter row."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        description: SolarPlusSensorEntityDescription,
        row_index: int,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.entity_description = description
        self._row_index = row_index

    @property
    def _row(self) -> dict:
        rows = self.coordinator.data.get("inverters", {}).get("rows") or []
        return rows[self._row_index] if self._row_index < len(rows) else {}

    @property
    def available(self) -> bool:
        """Available only while the row still exists."""
        rows = self.coordinator.data.get("inverters", {}).get("rows") or []
        return super().available and self._row_index < len(rows)

    @property
    def native_value(self) -> StateType:
        """Return the sensor value for this row."""
        return self.entity_description.value_fn(self._row)


class SolarPlusIntelbrasInverterSensor(_RowSensor):
    """A per-inverter sensor."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        description: SolarPlusSensorEntityDescription,
        row_index: int,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, description, row_index)
        entry_id = coordinator.config_entry.entry_id
        row = self._row
        self._attr_unique_id = f"{entry_id}_inverter_{row.get('id')}_{description.key}"
        self._attr_device_info = inverter_device_info(entry_id, row)


class SolarPlusIntelbrasDataloggerSensor(_RowSensor):
    """A per-datalogger sensor."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        description: SolarPlusSensorEntityDescription,
        row_index: int,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, description, row_index)
        entry_id = coordinator.config_entry.entry_id
        row = self._row
        datalogger_id = (row.get("datalogger") or {}).get("id")
        self._attr_unique_id = (
            f"{entry_id}_datalogger_{datalogger_id}_{description.key}"
        )
        self._attr_device_info = datalogger_device_info(entry_id, row)
