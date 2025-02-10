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
        name="Today Generation",
        icon="mdi:solar-panel",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_today_economy",
        name="Today Economy",
        icon="mdi:currency-usd",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_energy_total",
        name="Total",
        icon="mdi:solar-panel",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_total_economy",
        name="Total Economy",
        icon="mdi:currency-usd",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_current_power",
        name="Current Power",
        icon="mdi:solar-panel-large",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_economy_of_last_30",
        name="Economy of Last 30 Days",
        icon="mdi:currency-usd",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_year_economy",
        name="Year Economy",
        icon="mdi:currency-usd",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_energy_of_last_30",
        name="Energy of Last 30 Days",
        icon="mdi:solar-panel",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_saved_co2",
        name="Saved Co2",
        icon="mdi:molecule-co2",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_saved_trees",
        name="Saved Trees",
        icon="mdi:tree",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_saved_coal",
        name="Saved Coal",
        icon="mdi:grill",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_inverters",
        name="Inverters",
        icon="mdi:server-minus",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_dataloggers",
        name="Dataloggers",
        icon="mdi:server",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_alerts",
        name="Alerts",
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_today_alerts",
        name="Today Alerts",
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_price",
        name="Price",
        icon="mdi:currency-usd",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_capacity_installed",
        name="Capacity Installed",
        icon="mdi:solar-panel-large",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_modules_amount",
        name="Modules Amount",
        icon="mdi:solar-panel-large",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_status",
        name="Status",
        icon="mdi:check-circle",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_offgrid",
        name="Offgrid",
        icon="mdi:solar-panel",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_last_record",
        name="Last Record",
        icon="mdi:clock-time-three",
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
        elif entity_description.key == "solar_plus_intelbras_energy_total":
            sensors.append(
                SolarPlusIntelbrasEnergyTotalSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_total_economy":
            sensors.append(
                SolarPlusIntelbrasTotalEconomySensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_current_power":
            sensors.append(
                SolarPlusIntelbrasCurrentPowerSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_economy_of_last_30":
            sensors.append(
                SolarPlusIntelbrasEconomyOfLast30Sensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_year_economy":
            sensors.append(
                SolarPlusIntelbrasYearEconomySensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_energy_of_last_30":
            sensors.append(
                SolarPlusIntelbrasEnergyOfLast30Sensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_saved_co2":
            sensors.append(
                SolarPlusIntelbrasSavedCo2Sensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_saved_trees":
            sensors.append(
                SolarPlusIntelbrasSavedTreesSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_saved_coal":
            sensors.append(
                SolarPlusIntelbrasSavedCoalSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_inverters":
            sensors.append(
                SolarPlusIntelbrasInvertersSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_dataloggers":
            sensors.append(
                SolarPlusIntelbrasDataloggersSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_alerts":
            sensors.append(
                SolarPlusIntelbrasAlertsSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_today_alerts":
            sensors.append(
                SolarPlusIntelbrasTodayAlertsSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_price":
            sensors.append(
                SolarPlusIntelbrasPriceSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_capacity_installed":
            sensors.append(
                SolarPlusIntelbrasCapacityInstalledSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_modules_amount":
            sensors.append(
                SolarPlusIntelbrasModulesAmountSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_status":
            sensors.append(
                SolarPlusIntelbrasStatusSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_offgrid":
            sensors.append(
                SolarPlusIntelbrasOffgridSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_last_record":
            sensors.append(
                SolarPlusIntelbrasLastRecordSensor(
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
        return "total_increasing"

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
        return round(self.coordinator.data["rows"][0]["metrics"]["todayEconomy"], 2)

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "$"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

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


class SolarPlusIntelbrasEnergyTotalSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Energy Total Sensor class."""

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
        return self.coordinator.data["rows"][0]["metrics"]["energyTotal"]

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "kWh"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

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
        return "solar_plus_intelbras_energy_total"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Energy Total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["metrics"]["energyTotal"]


class SolarPlusIntelbrasTotalEconomySensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Total Economy Sensor class."""

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
        return round(self.coordinator.data["rows"][0]["metrics"]["totalEconomy"], 2)

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "$"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

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
        return "solar_plus_intelbras_total_economy"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Total Economy"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(self.coordinator.data["rows"][0]["metrics"]["totalEconomy"], 2)


class SolarPlusIntelbrasCurrentPowerSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Current Power Sensor class."""

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
        return self.coordinator.data["rows"][0]["metrics"]["currentPower"]

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
        return "solar_plus_intelbras_current_power"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Current Power"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["metrics"]["currentPower"]


class SolarPlusIntelbrasEconomyOfLast30Sensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Economy Of Last 30 Days Sensor class."""

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
        return round(self.coordinator.data["rows"][0]["metrics"]["todayEconomy"], 2)

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "$"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

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
        return "solar_plus_intelbras_economy_of_last_30"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Economy Of Last 30 Days"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(self.coordinator.data["rows"][0]["metrics"]["economyOfLast30"], 2)


class SolarPlusIntelbrasYearEconomySensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Year Economy Sensor class."""

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
        return round(self.coordinator.data["rows"][0]["metrics"]["yearEconomy"], 2)

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "$"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

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
        return "solar_plus_intelbras_year_economy"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Year Economy"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(self.coordinator.data["rows"][0]["metrics"]["yearEconomy"], 2)


class SolarPlusIntelbrasEnergyOfLast30Sensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Energy Of Last 30 Days Sensor class."""

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
        return self.coordinator.data["rows"][0]["metrics"]["energyOfLast30"]

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
        return "solar_plus_intelbras_energy_of_last_30"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Energy Of Last 30 Days"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["metrics"]["energyOfLast30"]


class SolarPlusIntelbrasSavedCo2Sensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Saved Co2 Sensor class."""

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
        return round(self.coordinator.data["rows"][0]["metrics"]["savedCo2"], 2)

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "Co2"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "measurement"

    @property
    def device_class(self) -> str:
        """Return the device class of the sensor."""
        return "CO2"

    @property
    def unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        return "Co2"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_saved_co2"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Saved Co2"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(self.coordinator.data["rows"][0]["metrics"]["savedCo2"], 2)


class SolarPlusIntelbrasEnergyOfLast30Sensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Energy Of Last 30 Days Sensor class."""

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
        return self.coordinator.data["rows"][0]["metrics"]["energyOfLast30"]

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "kWh"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

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
        return "solar_plus_intelbras_energy_of_last_30"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Energy Of Last 30 Days"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["metrics"]["energyOfLast30"]


class SolarPlusIntelbrasSavedTreesSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Saved Trees Sensor class."""

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
        return round(self.coordinator.data["rows"][0]["metrics"]["savedTrees"], 2)

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_saved_trees"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Saved Trees"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(self.coordinator.data["rows"][0]["metrics"]["savedTrees"], 2)


class SolarPlusIntelbrasSavedCoalSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Saved Coal Sensor class."""

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
        return round(self.coordinator.data["rows"][0]["metrics"]["savedCoal"], 2)

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_saved_coal"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Saved Coal"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(self.coordinator.data["rows"][0]["metrics"]["savedCoal"], 2)


class SolarPlusIntelbrasInvertersSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Inverters Sensor class."""

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
        return self.coordinator.data["rows"][0]["components"]["inverters"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_inverters"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Inverters"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["components"]["inverters"]


class SolarPlusIntelbrasDataloggersSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Dataloggers Sensor class."""

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
        return self.coordinator.data["rows"][0]["components"]["dataloggers"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_dataloggers"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Dataloggers"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["components"]["dataloggers"]


class SolarPlusIntelbrasAlertsSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Alerts Sensor class."""

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
        return self.coordinator.data["rows"][0]["components"]["alerts"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_alerts"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Alerts"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["components"]["alerts"]


class SolarPlusIntelbrasTodayAlertsSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Today Alerts Sensor class."""

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
        return self.coordinator.data["rows"][0]["components"]["todayAlerts"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_today_alerts"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Today Alerts"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["components"]["todayAlerts"]


class SolarPlusIntelbrasPriceSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Price Sensor class."""

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
        return round(self.coordinator.data["rows"][0]["price"], 2)

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of this entity, if any."""
        return "$"

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

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
        return "solar_plus_intelbras_price"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Price"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(self.coordinator.data["rows"][0]["price"], 2)


class SolarPlusIntelbrasCapacityInstalledSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Capacity Installed Sensor class."""

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
        return self.coordinator.data["rows"][0]["capacityInstalled"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_capacity_installed"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Capacity Installed"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["capacityInstalled"]


class SolarPlusIntelbrasModulesAmountSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Modules Amount Sensor class."""

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
        return self.coordinator.data["rows"][0]["modulesAmount"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_modules_amount"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Modules Amount"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["modulesAmount"]


class SolarPlusIntelbrasStatusSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Status Sensor class."""

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
        return self.coordinator.data["rows"][0]["status"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_status"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Status"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["status"]


class SolarPlusIntelbrasOffgridSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Offgrid Sensor class."""

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
        return self.coordinator.data["rows"][0]["offgrid"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_offgrid"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Offgrid"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["offgrid"]


class SolarPlusIntelbrasLastRecordSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Last Record Sensor class."""

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
        return self.coordinator.data["rows"][0]["last_record"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "solar_plus_intelbras_last_record"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return "Last Record"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["last_record"]
