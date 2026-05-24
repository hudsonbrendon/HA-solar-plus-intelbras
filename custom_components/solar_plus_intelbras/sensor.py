"""Sensor platform for solar_plus_intelbras."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import callback

from .device import datalogger_device_info, inverter_device_info, plant_device_info
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

# Entities are read-only and served from a single coordinator poll.
PARALLEL_UPDATES = 0


def _rows(data: dict) -> list[dict]:
    return data.get("inverters", {}).get("rows") or []


def row_ids(data: dict) -> list:
    """Return the inverter row ids present in the coordinator data."""
    return [row["id"] for row in _rows(data) if "id" in row]


def build_plant_entities(coordinator: SolarPlusIntelbrasDataUpdateCoordinator) -> list[SensorEntity]:
    """Return the (static) plant-level sensors."""
    plant = (_rows(coordinator.data) or [{}])[0].get("plant") or {}
    name = plant.get("name", "")
    return [SolarPlusIntelbrasPlantSensor(coordinator, description, name) for description in PLANT_SENSORS]


def build_row_entities(
    coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
    row_id: object,
) -> list[SensorEntity]:
    """Return the inverter and datalogger sensors for a single inverter id."""
    entities: list[SensorEntity] = [
        SolarPlusIntelbrasInverterSensor(coordinator, description, row_id) for description in INVERTER_SENSORS
    ]
    entities.extend(
        SolarPlusIntelbrasDataloggerSensor(coordinator, description, row_id) for description in DATALOGGER_SENSORS
    )
    return entities


def build_entities(coordinator: SolarPlusIntelbrasDataUpdateCoordinator) -> list[SensorEntity]:
    """Return all current entities (plant + per-inverter/datalogger)."""
    entities = build_plant_entities(coordinator)
    for row_id in row_ids(coordinator.data):
        entities.extend(build_row_entities(coordinator, row_id))
    return entities


def new_row_entities(
    coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
    known: set,
) -> list[SensorEntity]:
    """Return entities for inverter ids not yet in ``known`` and record them."""
    new: list[SensorEntity] = []
    for row_id in row_ids(coordinator.data):
        if row_id in known:
            continue
        known.add(row_id)
        new.extend(build_row_entities(coordinator, row_id))
    return new


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform with dynamic per-inverter discovery."""
    coordinator = entry.runtime_data.coordinator
    async_add_entities(build_plant_entities(coordinator))

    known: set = set()

    @callback
    def _add_new_inverters() -> None:
        entities = new_row_entities(coordinator, known)
        if entities:
            async_add_entities(entities)

    _add_new_inverters()
    entry.async_on_unload(coordinator.async_add_listener(_add_new_inverters))


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
    """Base for sensors bound to a single inverter row (looked up by id)."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        description: SolarPlusSensorEntityDescription,
        row_id: object,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self.entity_description = description
        self._row_id = row_id

    @property
    def _row(self) -> dict:
        for row in _rows(self.coordinator.data):
            if row.get("id") == self._row_id:
                return row
        return {}

    @property
    def available(self) -> bool:
        """Available only while the inverter row still exists."""
        return super().available and any(row.get("id") == self._row_id for row in _rows(self.coordinator.data))

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
        row_id: object,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, description, row_id)
        entry_id = coordinator.config_entry.entry_id
        self._attr_unique_id = f"{entry_id}_inverter_{row_id}_{description.key}"
        self._attr_device_info = inverter_device_info(entry_id, self._row)


class SolarPlusIntelbrasDataloggerSensor(_RowSensor):
    """A per-datalogger sensor."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        description: SolarPlusSensorEntityDescription,
        row_id: object,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator, description, row_id)
        entry_id = coordinator.config_entry.entry_id
        datalogger_id = (self._row.get("datalogger") or {}).get("id")
        self._attr_unique_id = f"{entry_id}_datalogger_{datalogger_id}_{description.key}"
        self._attr_device_info = datalogger_device_info(entry_id, self._row)
