"""Sensor platform for solar_plus_intelbras."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory

from .device import DataloggerDevice  # Import DataloggerDevice
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
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_today_economy",
        name="Today Economy",
        icon="mdi:currency-usd",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_energy_total",
        name="Total",
        icon="mdi:solar-panel",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_total_economy",
        name="Total Economy",
        icon="mdi:currency-usd",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_current_power",
        name="Current Power",
        icon="mdi:solar-panel-large",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_economy_of_last_30",
        name="Economy of Last 30 Days",
        icon="mdi:currency-usd",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_year_economy",
        name="Year Economy",
        icon="mdi:currency-usd",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_energy_of_last_30",
        name="Energy of Last 30 Days",
        icon="mdi:solar-panel",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_saved_co2",
        name="Saved Co2",
        icon="mdi:molecule-co2",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_saved_trees",
        name="Saved Trees",
        icon="mdi:tree",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_saved_coal",
        name="Saved Coal",
        icon="mdi:grill",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_inverters",
        name="Inverters",
        icon="mdi:server-minus",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_dataloggers",
        name="Dataloggers",
        icon="mdi:server",
        entity_category=EntityCategory.DIAGNOSTIC,
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
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_price",
        name="Price",
        icon="mdi:currency-usd",
        suggested_display_precision=2,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_capacity_installed",
        name="Capacity Installed",
        icon="mdi:solar-panel-large",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_modules_amount",
        name="Modules Amount",
        icon="mdi:solar-panel-large",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_status",
        name="Status",
        icon="mdi:check-circle",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_offgrid",
        name="Offgrid",
        icon="mdi:solar-panel",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_last_record",
        name="Last Record",
        icon="mdi:clock-time-three",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_datalogger_model_id",
        name="Model ID",
        icon="mdi:server",
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_datalogger_firmware_version",
        name="Firmware Version",
        icon="mdi:select-inverse",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_datalogger_last_record",
        name="Last Record",
        icon="mdi:clock-time-three",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_datalogger_mac_address",
        name="MAC Address",
        icon="mdi:network",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    SensorEntityDescription(
        key="solar_plus_intelbras_datalogger_rssi",
        name="RSSI",
        icon="mdi:wifi",
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    sensors = []

    sensor_classes = {
        "solar_plus_intelbras_energy_today": SolarPlusIntelbrasInverterEnergyTodaySensor,
        "solar_plus_intelbras_today_economy": SolarPlusIntelbrasInverterTodayEconomySensor,
        "solar_plus_intelbras_energy_total": SolarPlusIntelbrasInverterEnergyTotalSensor,
        "solar_plus_intelbras_total_economy": SolarPlusIntelbrasInverterTotalEconomySensor,
        "solar_plus_intelbras_current_power": SolarPlusIntelbrasInverterCurrentPowerSensor,
        "solar_plus_intelbras_economy_of_last_30": SolarPlusIntelbrasInverterEconomyOfLast30Sensor,
        "solar_plus_intelbras_year_economy": SolarPlusIntelbrasInverterYearEconomySensor,
        "solar_plus_intelbras_energy_of_last_30": SolarPlusIntelbrasInverterEnergyOfLast30Sensor,
        "solar_plus_intelbras_saved_co2": SolarPlusIntelbrasInverterSavedCo2Sensor,
        "solar_plus_intelbras_saved_trees": SolarPlusIntelbrasInverterSavedTreesSensor,
        "solar_plus_intelbras_saved_coal": SolarPlusIntelbrasInverterSavedCoalSensor,
        "solar_plus_intelbras_inverters": SolarPlusIntelbrasInverterInvertersSensor,
        "solar_plus_intelbras_dataloggers": SolarPlusIntelbrasInverterDataloggersSensor,
        "solar_plus_intelbras_alerts": SolarPlusIntelbrasInverterAlertsSensor,
        "solar_plus_intelbras_today_alerts": SolarPlusIntelbrasInverterTodayAlertsSensor,
        "solar_plus_intelbras_price": SolarPlusIntelbrasInverterPriceSensor,
        "solar_plus_intelbras_capacity_installed": SolarPlusIntelbrasInverterCapacityInstalledSensor,
        "solar_plus_intelbras_modules_amount": SolarPlusIntelbrasInverterModulesAmountSensor,
        "solar_plus_intelbras_status": SolarPlusIntelbrasInverterStatusSensor,
        "solar_plus_intelbras_offgrid": SolarPlusIntelbrasInverterOffgridSensor,
        "solar_plus_intelbras_last_record": SolarPlusIntelbrasInverterLastRecordSensor,
        "solar_plus_intelbras_datalogger_model_id": SolarPlusIntelbrasDataloggerModelIDSensor,
        "solar_plus_intelbras_datalogger_firmware_version": SolarPlusIntelbrasDataloggerFirmwareVersionSensor,
        "solar_plus_intelbras_datalogger_last_record": SolarPlusIntelbrasDataloggerLastRecordSensor,
        "solar_plus_intelbras_datalogger_mac_address": SolarPlusIntelbrasDataloggerMacAddressSensor,
        "solar_plus_intelbras_datalogger_rssi": SolarPlusIntelbrasDataloggerRssiSensor,
    }

    for entity_description in ENTITY_DESCRIPTIONS:
        sensor_class = sensor_classes.get(entity_description.key)
        if sensor_class:
            sensors.append(
                sensor_class(
                    coordinator=entry.runtime_data.coordinator,
                    entity_description=entity_description,
                )
            )

    async_add_entities(sensors)


class SolarPlusIntelbrasInverterEnergyTodaySensor(SolarPlusIntelbrasEntity, SensorEntity):
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


class SolarPlusIntelbrasInverterTodayEconomySensor(SolarPlusIntelbrasEntity, SensorEntity):
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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["todayEconomy"]

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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["todayEconomy"]


class SolarPlusIntelbrasInverterEnergyTotalSensor(SolarPlusIntelbrasEntity, SensorEntity):
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


class SolarPlusIntelbrasInverterTotalEconomySensor(SolarPlusIntelbrasEntity, SensorEntity):
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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["totalEconomy"]

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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["totalEconomy"]


class SolarPlusIntelbrasInverterCurrentPowerSensor(SolarPlusIntelbrasEntity, SensorEntity):
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


class SolarPlusIntelbrasInverterEconomyOfLast30Sensor(SolarPlusIntelbrasEntity, SensorEntity):
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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["todayEconomy"]

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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["economyOfLast30"]


class SolarPlusIntelbrasInverterYearEconomySensor(SolarPlusIntelbrasEntity, SensorEntity):
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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["yearEconomy"]

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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["yearEconomy"]


class SolarPlusIntelbrasInverterEnergyOfLast30Sensor(SolarPlusIntelbrasEntity, SensorEntity):
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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["savedCo2"]

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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["savedCo2"]


class SolarPlusIntelbrasInverterSavedTreesSensor(SolarPlusIntelbrasEntity, SensorEntity):
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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["savedTrees"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["savedTrees"]


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
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["savedCoal"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["plant"]["metrics"]["savedCoal"]


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


class SolarPlusIntelbrasInverterDataloggersSensor(SolarPlusIntelbrasEntity, SensorEntity):
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


class SolarPlusIntelbrasInverterTodayAlertsSensor(SolarPlusIntelbrasEntity, SensorEntity):
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
        return self.coordinator.data["rows"][0]["plant"]["price"]

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
        return self.coordinator.data["rows"][0]["plant"]["price"]


class SolarPlusIntelbrasInverterCapacityInstalledSensor(SolarPlusIntelbrasEntity, SensorEntity):
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


class SolarPlusIntelbrasInverterModulesAmountSensor(SolarPlusIntelbrasEntity, SensorEntity):
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


class SolarPlusIntelbrasInverterLastRecordSensor(SolarPlusIntelbrasEntity, SensorEntity):
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


class SolarPlusIntelbrasDataloggerModelIDSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Datalogger Model ID Sensor class."""

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
        self._datalogger_device = DataloggerDevice(
            identifier=f"{coordinator.config_entry.entry_id}_datalogger",
            name="Datalogger",
        )
        self._attr_device_info = self._datalogger_device.device_info

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["dataloggerModelID"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["dataloggerModelID"]


class SolarPlusIntelbrasDataloggerFirmwareVersionSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Datalogger Firmware Version Sensor class."""

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
        self._datalogger_device = DataloggerDevice(
            identifier=f"{coordinator.config_entry.entry_id}_datalogger",
            name="Datalogger",
        )
        self._attr_device_info = self._datalogger_device.device_info

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["firmwareVersion"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["firmwareVersion"]


class SolarPlusIntelbrasDataloggerLastRecordSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Datalogger Last Record Sensor class."""

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
        self._datalogger_device = DataloggerDevice(
            identifier=f"{coordinator.config_entry.entry_id}_datalogger",
            name="Datalogger",
        )
        self._attr_device_info = self._datalogger_device.device_info

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["last_record"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total_increasing"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["last_record"]


class SolarPlusIntelbrasDataloggerMacAddressSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Datalogger MAC Address Sensor class."""

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
        self._datalogger_device = DataloggerDevice(
            identifier=f"{coordinator.config_entry.entry_id}_datalogger",
            name="Datalogger",
        )
        self._attr_device_info = self._datalogger_device.device_info

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["macAddress"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["macAddress"]


class SolarPlusIntelbrasDataloggerRssiSensor(SolarPlusIntelbrasEntity, SensorEntity):
    """Solar Plus Intelbras Datalogger RSSI Sensor class."""

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
        self._datalogger_device = DataloggerDevice(
            identifier=f"{coordinator.config_entry.entry_id}_datalogger",
            name="Datalogger",
        )
        self._attr_device_info = self._datalogger_device.device_info

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["rssi"]

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return "total"

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data["rows"][0]["datalogger"]["rssi"]
