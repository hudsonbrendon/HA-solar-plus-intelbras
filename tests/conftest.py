"""Shared fixtures for solar_plus_intelbras tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.fixture
def login_response() -> dict:
    """Return a sample /login response."""
    return _load("login.json")


@pytest.fixture
def inverters_response() -> dict:
    """Return a sample /inverters response."""
    return _load("inverters.json")


@pytest.fixture
def records_year_response() -> dict:
    """Return a sample /records/year response."""
    return _load("records_year.json")


@pytest.fixture
def coordinator_data(inverters_response: dict, records_year_response: dict) -> dict:
    """Return a normalized coordinator data dict (matches the locked contract)."""
    return {
        "inverters": inverters_response,
        "year_energy": records_year_response["data"]["total"],
        "currency": "BRL",
    }
