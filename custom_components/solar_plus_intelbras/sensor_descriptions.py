"""Typed sensor descriptions and value accessors for solar_plus_intelbras."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
)
from homeassistant.helpers.entity import EntityCategory
from homeassistant.util import dt as dt_util

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime

    from homeassistant.helpers.typing import StateType


@dataclass(frozen=True, kw_only=True)
class SolarPlusSensorEntityDescription(SensorEntityDescription):
    """
    Sensor description carrying a value function.

    For PLANT_SENSORS, ``value_fn`` receives the full coordinator data dict.
    For INVERTER_SENSORS / DATALOGGER_SENSORS, ``value_fn`` receives one
    inverter row (``coordinator.data["inverters"]["rows"][i]``).
    """

    value_fn: Callable[[Any], StateType]


def _parse_dt(value: str | None) -> datetime | None:
    """Parse an ISO8601 timestamp to an aware datetime, or None."""
    if not value:
        return None
    return dt_util.parse_datetime(value)


# --- plant-level accessors -------------------------------------------------
def _first_row(data: dict) -> dict:
    rows = data.get("inverters", {}).get("rows") or []
    return rows[0] if rows else {}


def _plant(data: dict) -> dict:
    return _first_row(data).get("plant") or {}


def _metric(data: dict, key: str) -> StateType:
    return (_plant(data).get("metrics") or {}).get(key)


def _component(data: dict, key: str) -> StateType:
    return (_plant(data).get("components") or {}).get(key)


def _plant_field(data: dict, key: str) -> StateType:
    return _plant(data).get(key)


def _weather(data: dict) -> dict:
    return (_plant(data).get("weather") or {}).get("current") or {}


# --- inverter / datalogger accessors (value_fn receives one row) -----------
def _datalogger(row: dict) -> dict:
    return row.get("datalogger") or {}


PLANT_SENSORS: tuple[SolarPlusSensorEntityDescription, ...] = (
    SolarPlusSensorEntityDescription(
        key="energy_today",
        translation_key="energy_today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "energyToday"),
    ),
    SolarPlusSensorEntityDescription(
        key="energy_total",
        translation_key="energy_total",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "energyTotal"),
    ),
    SolarPlusSensorEntityDescription(
        key="energy_of_last_30",
        translation_key="energy_of_last_30",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "energyOfLast30"),
    ),
    SolarPlusSensorEntityDescription(
        key="year_energy",
        translation_key="year_energy",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda d: d.get("year_energy"),
    ),
    SolarPlusSensorEntityDescription(
        key="current_power",
        translation_key="current_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=0,
        value_fn=lambda d: _metric(d, "currentPower"),
    ),
    SolarPlusSensorEntityDescription(
        key="today_economy",
        translation_key="today_economy",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "todayEconomy"),
    ),
    SolarPlusSensorEntityDescription(
        key="total_economy",
        translation_key="total_economy",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "totalEconomy"),
    ),
    SolarPlusSensorEntityDescription(
        key="economy_of_last_30",
        translation_key="economy_of_last_30",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "economyOfLast30"),
    ),
    SolarPlusSensorEntityDescription(
        key="year_economy",
        translation_key="year_economy",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "yearEconomy"),
    ),
    SolarPlusSensorEntityDescription(
        key="saved_co2",
        translation_key="saved_co2",
        native_unit_of_measurement="kg",
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "savedCo2"),
    ),
    SolarPlusSensorEntityDescription(
        key="saved_trees",
        translation_key="saved_trees",
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "savedTrees"),
    ),
    SolarPlusSensorEntityDescription(
        key="saved_coal",
        translation_key="saved_coal",
        native_unit_of_measurement="kg",
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda d: _metric(d, "savedCoal"),
    ),
    SolarPlusSensorEntityDescription(
        key="price",
        translation_key="price",
        device_class=SensorDeviceClass.MONETARY,
        suggested_display_precision=2,
        value_fn=lambda d: _plant_field(d, "price"),
    ),
    SolarPlusSensorEntityDescription(
        key="capacity_installed",
        translation_key="capacity_installed",
        native_unit_of_measurement="kWp",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: _plant_field(d, "capacityInstalled"),
    ),
    SolarPlusSensorEntityDescription(
        key="modules_amount",
        translation_key="modules_amount",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: _plant_field(d, "modulesAmount"),
    ),
    SolarPlusSensorEntityDescription(
        key="plant_status",
        translation_key="plant_status",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: _plant_field(d, "status"),
    ),
    SolarPlusSensorEntityDescription(
        key="alerts",
        translation_key="alerts",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: _component(d, "alerts"),
    ),
    SolarPlusSensorEntityDescription(
        key="today_alerts",
        translation_key="today_alerts",
        entity_category=EntityCategory.DIAGNOSTIC,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: _component(d, "todayAlerts"),
    ),
    SolarPlusSensorEntityDescription(
        key="weather_temperature",
        translation_key="weather_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: _weather(d).get("temp_c"),
    ),
    SolarPlusSensorEntityDescription(
        key="weather_humidity",
        translation_key="weather_humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        native_unit_of_measurement=PERCENTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: _weather(d).get("humidity"),
    ),
    SolarPlusSensorEntityDescription(
        key="weather_condition",
        translation_key="weather_condition",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda d: (_weather(d).get("condition") or {}).get("text"),
    ),
)


INVERTER_SENSORS: tuple[SolarPlusSensorEntityDescription, ...] = (
    SolarPlusSensorEntityDescription(
        key="inverter_temperature",
        translation_key="inverter_temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda row: row.get("temperature"),
    ),
    SolarPlusSensorEntityDescription(
        key="inverter_current_power",
        translation_key="inverter_current_power",
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda row: row.get("currentPower"),
    ),
    SolarPlusSensorEntityDescription(
        key="inverter_energy_today",
        translation_key="inverter_energy_today",
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        suggested_display_precision=2,
        value_fn=lambda row: row.get("energyToday"),
    ),
    SolarPlusSensorEntityDescription(
        key="inverter_status",
        translation_key="inverter_status",
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda row: row.get("status"),
    ),
    SolarPlusSensorEntityDescription(
        key="inverter_serial_number",
        translation_key="inverter_serial_number",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda row: row.get("serialNumber"),
    ),
    SolarPlusSensorEntityDescription(
        key="inverter_last_record",
        translation_key="inverter_last_record",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda row: _parse_dt(row.get("last_record")),
    ),
)


DATALOGGER_SENSORS: tuple[SolarPlusSensorEntityDescription, ...] = (
    SolarPlusSensorEntityDescription(
        key="datalogger_firmware_version",
        translation_key="datalogger_firmware_version",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda row: _datalogger(row).get("firmwareVersion"),
    ),
    SolarPlusSensorEntityDescription(
        key="datalogger_mac_address",
        translation_key="datalogger_mac_address",
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda row: _datalogger(row).get("macAddress"),
    ),
    SolarPlusSensorEntityDescription(
        key="datalogger_rssi",
        translation_key="datalogger_rssi",
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        value_fn=lambda row: _datalogger(row).get("rssi"),
    ),
    SolarPlusSensorEntityDescription(
        key="datalogger_last_record",
        translation_key="datalogger_last_record",
        device_class=SensorDeviceClass.TIMESTAMP,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
        value_fn=lambda row: _parse_dt(_datalogger(row).get("last_record")),
    ),
)
