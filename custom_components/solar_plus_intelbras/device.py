"""Device info builders for solar_plus_intelbras."""

from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo

from .const import DOMAIN


def plant_device_info(entry_id: str, plant_name: str) -> DeviceInfo:
    """Return DeviceInfo for the plant (top-level device)."""
    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry_id}_plant")},
        name=plant_name or "Solar Plant",
        manufacturer="Intelbras",
        model="Solar Plus",
    )


def inverter_device_info(entry_id: str, row: dict) -> DeviceInfo:
    """Return DeviceInfo for a single inverter row."""
    model = row.get("inverterModel") or {}
    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry_id}_inverter_{row['id']}")},
        name=row.get("name") or "Inverter",
        manufacturer=model.get("manufacturer") or "Intelbras",
        model=model.get("pnManufacturer") or model.get("pnIntelbras") or "Inverter",
        serial_number=row.get("serialNumber"),
        via_device=(DOMAIN, f"{entry_id}_plant"),
    )


def datalogger_device_info(entry_id: str, row: dict) -> DeviceInfo:
    """Return DeviceInfo for the datalogger attached to an inverter row."""
    datalogger = row.get("datalogger") or {}
    return DeviceInfo(
        identifiers={(DOMAIN, f"{entry_id}_datalogger_{datalogger['id']}")},
        name="Datalogger",
        manufacturer="Intelbras",
        model="Datalogger",
        serial_number=datalogger.get("serialNumber"),
        sw_version=datalogger.get("firmwareVersion"),
        via_device=(DOMAIN, f"{entry_id}_inverter_{row['id']}"),
    )
