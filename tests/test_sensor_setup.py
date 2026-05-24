"""Tests for sensor entity setup and per-entity behavior."""

from __future__ import annotations

import copy

from custom_components.solar_plus_intelbras.sensor import (
    SolarPlusIntelbrasInverterSensor,
    build_entities,
    new_row_entities,
)
from custom_components.solar_plus_intelbras.sensor_descriptions import (
    DATALOGGER_SENSORS,
    INVERTER_SENSORS,
    PLANT_SENSORS,
)


class _FakeCoordinator:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.config_entry = type("E", (), {"entry_id": "entry1"})()
        self.last_update_success = True


def test_build_entities_counts(coordinator_data: dict) -> None:
    """One set of plant sensors + inverter/datalogger sensors per row."""
    coordinator = _FakeCoordinator(coordinator_data)
    entities = build_entities(coordinator)
    expected = len(PLANT_SENSORS) + len(INVERTER_SENSORS) + len(DATALOGGER_SENSORS)
    assert len(entities) == expected


def test_row_sensor_unavailable_when_row_disappears(coordinator_data: dict) -> None:
    """A per-row sensor becomes unavailable (value None) if its inverter is gone."""
    coordinator = _FakeCoordinator(coordinator_data)
    sensor = SolarPlusIntelbrasInverterSensor(coordinator, INVERTER_SENSORS[0], 2113)
    coordinator.data = {"inverters": {"rows": []}, "year_energy": None, "currency": "BRL"}
    assert sensor.available is False
    assert sensor.native_value is None


def test_new_row_entities_only_returns_unseen_inverters(coordinator_data: dict) -> None:
    """Dynamic discovery adds entities only for inverter ids not yet seen."""
    coordinator = _FakeCoordinator(coordinator_data)
    known: set = set()
    first = new_row_entities(coordinator, known)
    assert len(first) == len(INVERTER_SENSORS) + len(DATALOGGER_SENSORS)
    # Same data again -> nothing new.
    assert new_row_entities(coordinator, known) == []
    # A second inverter appears -> only its entities are created.
    data = copy.deepcopy(coordinator_data)
    second_row = copy.deepcopy(data["inverters"]["rows"][0])
    second_row["id"] = 9999
    second_row["datalogger"]["id"] = 8888
    data["inverters"]["rows"].append(second_row)
    coordinator.data = data
    added = new_row_entities(coordinator, known)
    assert len(added) == len(INVERTER_SENSORS) + len(DATALOGGER_SENSORS)
    assert all("_9999_" in e.unique_id or "_8888_" in e.unique_id for e in added)


def test_unique_ids_are_distinct(coordinator_data: dict) -> None:
    """Every entity has a distinct unique_id prefixed with the entry id."""
    coordinator = _FakeCoordinator(coordinator_data)
    ids = [e.unique_id for e in build_entities(coordinator)]
    assert len(ids) == len(set(ids))
    assert all(uid.startswith("entry1_") for uid in ids)


def test_monetary_unit_follows_currency(coordinator_data: dict) -> None:
    """Monetary sensors use the account currency as their unit."""
    coordinator = _FakeCoordinator(coordinator_data)
    price = next(e for e in build_entities(coordinator) if e.unique_id == "entry1_price")
    assert price.native_unit_of_measurement == "BRL"
