"""Tests for the binary sensor platform."""

from __future__ import annotations

from custom_components.solar_plus_intelbras.binary_sensor import build_binary_entities


class _FakeCoordinator:
    def __init__(self, data: dict) -> None:
        self.data = data
        self.config_entry = type("E", (), {"entry_id": "entry1"})()
        self.last_update_success = True


def test_one_online_sensor_per_inverter(coordinator_data: dict) -> None:
    """Exactly one connectivity sensor is created per inverter row."""
    coordinator = _FakeCoordinator(coordinator_data)
    entities = build_binary_entities(coordinator)
    assert len(entities) == 1
    assert entities[0].unique_id == "entry1_inverter_2113_online"


def test_online_reads_row_value(coordinator_data: dict) -> None:
    """is_on reflects the inverter row's online flag."""
    coordinator = _FakeCoordinator(coordinator_data)
    entity = build_binary_entities(coordinator)[0]
    assert entity.is_on is False
