"""Sensor platform for solar_plus_intelbras."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.device_registry import DeviceInfo

from .entity import SolarPlusIntelbrasEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator
    from .data import SolarPlusIntelbrasConfigEntry

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="solar_plus_intelbras_energy_today",
        name="Energy Today",
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


async def async_setup_entry(  # noqa:  PLR0912
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
                SolarPlusIntelbrasInverterEnergyTodaySensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_today_economy":
            sensors.append(
                SolarPlusIntelbrasInverterTodayEconomySensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_energy_total":
            sensors.append(
                SolarPlusIntelbrasInverterEnergyTotalSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_total_economy":
            sensors.append(
                SolarPlusIntelbrasInverterTotalEconomySensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_current_power":
            sensors.append(
                SolarPlusIntelbrasInverterCurrentPowerSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_economy_of_last_30":
            sensors.append(
                SolarPlusIntelbrasInverterEconomyOfLast30Sensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_year_economy":
            sensors.append(
                SolarPlusIntelbrasInverterYearEconomySensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_energy_of_last_30":
            sensors.append(
                SolarPlusIntelbrasInverterEnergyOfLast30Sensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_saved_co2":
            sensors.append(
                SolarPlusIntelbrasInverterSavedCo2Sensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_saved_trees":
            sensors.append(
                SolarPlusIntelbrasInverterSavedTreesSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_saved_coal":
            sensors.append(
                SolarPlusIntelbrasInverterSavedCoalSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_inverters":
            sensors.append(
                SolarPlusIntelbrasInverterInvertersSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_dataloggers":
            sensors.append(
                SolarPlusIntelbrasInverterDataloggersSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_alerts":
            sensors.append(
                SolarPlusIntelbrasInverterAlertsSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_today_alerts":
            sensors.append(
                SolarPlusIntelbrasInverterTodayAlertsSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_price":
            sensors.append(
                SolarPlusIntelbrasInverterPriceSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_capacity_installed":
            sensors.append(
                SolarPlusIntelbrasInverterCapacityInstalledSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_modules_amount":
            sensors.append(
                SolarPlusIntelbrasInverterModulesAmountSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_status":
            sensors.append(
                SolarPlusIntelbrasInverterStatusSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_offgrid":
            sensors.append(
                SolarPlusIntelbrasInverterOffgridSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )
        elif entity_description.key == "solar_plus_intelbras_last_record":
            sensors.append(
                SolarPlusIntelbrasInverterLastRecordSensor(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )

    async_add_entities(sensors)


class SolarPlusIntelbrasInverterEnergyTodaySensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Energy Today Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["energyToday"]

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["energyToday"]


class SolarPlusIntelbrasInverterTodayEconomySensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Today Economy Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["todayEconomy"], 2
        )

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["todayEconomy"], 2
        )


class SolarPlusIntelbrasInverterEnergyTotalSensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Energy Total Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["energyTotal"]

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["energyTotal"]


class SolarPlusIntelbrasInverterTotalEconomySensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Total Economy Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["totalEconomy"], 2
        )

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["totalEconomy"], 2
        )


class SolarPlusIntelbrasInverterCurrentPowerSensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Current Power Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["currentPower"]

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["currentPower"]


class SolarPlusIntelbrasInverterEconomyOfLast30Sensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Economy Of Last 30 Days Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["todayEconomy"], 2
        )

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["economyOfLast30"], 2
        )


class SolarPlusIntelbrasInverterYearEconomySensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Year Economy Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["yearEconomy"], 2
        )

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["yearEconomy"], 2
        )


class SolarPlusIntelbrasInverterEnergyOfLast30Sensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Energy Of Last 30 Days Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["energyOfLast30"]

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["energyOfLast30"]


class SolarPlusIntelbrasInverterSavedCo2Sensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Inverter Saved Co2 Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["savedCo2"], 2
        )

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["savedCo2"], 2
        )


class SolarPlusIntelbrasInverterSavedTreesSensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Saved Trees Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["savedTrees"], 2
        )

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["savedTrees"], 2
        )


class SolarPlusIntelbrasInverterSavedCoalSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Inverter Saved Coal Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["savedCoal"],
            2,
        )

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(
            self.coordinator.data["rows"][0]["plant"]["metrics"]["savedCoal"],
            2,
        )


class SolarPlusIntelbrasInverterInvertersSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Inverter Inverters Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["components"]["inverters"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["components"]["inverters"]


class SolarPlusIntelbrasInverterDataloggersSensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Dataloggers Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["components"]["dataloggers"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["components"]["dataloggers"]


class SolarPlusIntelbrasInverterAlertsSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Inverter Alerts Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["components"]["alerts"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["components"]["alerts"]


class SolarPlusIntelbrasInverterTodayAlertsSensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Today Alerts Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["components"]["todayAlerts"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["components"]["todayAlerts"]


class SolarPlusIntelbrasInverterPriceSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Inverter Price Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return round(self.coordinator.data["rows"][0]["plant"]["price"], 2)

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
    def state(self) -> str:
        """Return the state of the sensor."""
        return round(self.coordinator.data["rows"][0]["plant"]["price"], 2)


class SolarPlusIntelbrasInverterCapacityInstalledSensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Capacity Installed Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["capacityInstalled"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["capacityInstalled"]


class SolarPlusIntelbrasInverterModulesAmountSensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Modules Amount Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["modulesAmount"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["modulesAmount"]


class SolarPlusIntelbrasInverterStatusSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Inverter Status Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["status"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["status"]


class SolarPlusIntelbrasInverterOffgridSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Inverter Offgrid Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["offgrid"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["offgrid"]


class SolarPlusIntelbrasInverterLastRecordSensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Inverter Last Record Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Inverter",
            manufacturer="Intelbras",
            model="Inverter",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["last_record"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["last_record"]


class SolarPlusIntelbrasDataloggerTemperatureSensor(
    SolarPlusIntelbrasEntity, SensorEntity
):
    """Solar Plus Intelbras Datalogger Temperature Sensor class."""

    def __init__(
        self,
        coordinator: SolarPlusIntelbrasDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = entity_description.key
        self._attr_name = entity_description.name
        self.entity_id = f"sensor.{entity_description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(coordinator.config_entry.entry_id,)},
            name="Datalogger",
            manufacturer="Intelbras",
            model="Datalogger",
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["temperature"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["temperature"]
