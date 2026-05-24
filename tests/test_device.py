"""Tests for device info builders."""

from __future__ import annotations

from custom_components.solar_plus_intelbras.const import DOMAIN
from custom_components.solar_plus_intelbras.device import (
    current_device_identifiers,
    datalogger_device_info,
    inverter_device_info,
    plant_device_info,
)


def test_plant_device_identifier_is_two_tuple() -> None:
    """Plant device uses a (domain, id) identifier and the given name."""
    info = plant_device_info("entry1", "My Plant")
    assert (DOMAIN, "entry1_plant") in info["identifiers"]
    assert info["name"] == "My Plant"


def test_inverter_device_carries_model_and_serial(inverters_response: dict) -> None:
    """Inverter device exposes manufacturer, model, and serial number."""
    row = inverters_response["rows"][0]
    info = inverter_device_info("entry1", row)
    assert (DOMAIN, "entry1_inverter_2113") in info["identifiers"]
    assert info["manufacturer"] == "Sungrow"
    assert info["model"] == "SG5.0RS-L"
    assert info["serial_number"] == "B1411309060"


def test_datalogger_device_is_child_of_inverter(inverters_response: dict) -> None:
    """Datalogger device is parented to its inverter via via_device."""
    row = inverters_response["rows"][0]
    info = datalogger_device_info("entry1", row)
    assert (DOMAIN, "entry1_datalogger_1139") in info["identifiers"]
    assert info["via_device"] == (DOMAIN, "entry1_inverter_2113")


def test_current_device_identifiers(inverters_response: dict) -> None:
    """The current identifiers cover plant + each inverter and datalogger."""
    ids = current_device_identifiers("entry1", {"inverters": inverters_response})
    assert ids == {
        (DOMAIN, "entry1_plant"),
        (DOMAIN, "entry1_inverter_2113"),
        (DOMAIN, "entry1_datalogger_1139"),
    }
