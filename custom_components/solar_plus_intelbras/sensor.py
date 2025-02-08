"""Sensor platform for solar_plus_intelbras."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .entity import SolarPlusIntelbrasEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator
    from .data import SolarPlusIntelbrasConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="solar_plus_intelbras_energy_today",
        name="Generation",  # TODO: Add translation # noqa
        icon="mdi:solar-panel",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_today_economy",
        name="Economy",  # TODO: Add translation # noqa
        icon="mdi:currency-usd",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: SolarPlusIntelbrasConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    sensors = []

    # Create one instance of each sensor type with its corresponding entity description
    for entity_description in ENTITY_DESCRIPTIONS:
        if entity_description.key == "solar_plus_intelbras_energy_today":
            sensors.append(
                SolarPlusIntelbrasEnergyTodaySensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_today_economy":
            sensors.append(
                SolarPlusIntelbrasTodayEconomySensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )

    async_add_entities(sensors)


class SolarPlusIntelbrasEnergyTodaySensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Energy Today Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["metrics"]["energyToday"]

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "kWh"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "measurement"

    @property
    def device_class(self) -> str:
        """Return the device class of the sensor."""
        return "energy"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        return "kWh"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_energy_today"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Energy Today"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["metrics"]["energyToday"]


class SolarPlusIntelbrasTodayEconomySensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Today Economy Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["metrics"]["todayEconomy"]

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "$"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "measurement"

    @property
    def device_class(self) -> str:
        """Return the device class of the sensor."""
        return "monetary"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        return "$"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_today_economy"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Today Economy"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(self.coordinator.data["rows"][0]["metrics"]["todayEconomy"], 2)
