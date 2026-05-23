"""Tests for sensor entity setup and per-entity behavior."""

from __future__ import annotations

from custom_components.solar_plus_intelbras.sensor import build_entities
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
