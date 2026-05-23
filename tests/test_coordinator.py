"""Tests for the coordinator's data normalization helper."""

from __future__ import annotations

from custom_components.solar_plus_intelbras.coordinator import build_coordinator_data

SAMPLE_YEAR_ENERGY = 292.4


def test_build_coordinator_data_shape(inverters_response: dict) -> None:
    """build_coordinator_data returns a dict with the correct shape and values."""
    data = build_coordinator_data(inverters_response, year_energy=SAMPLE_YEAR_ENERGY, currency="BRL")
    assert data["inverters"] is inverters_response
    assert data["year_energy"] == SAMPLE_YEAR_ENERGY
    assert data["currency"] == "BRL"
