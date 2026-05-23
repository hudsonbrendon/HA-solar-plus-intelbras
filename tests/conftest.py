"""Shared fixtures for solar_plus_intelbras tests."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pycares
import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session", autouse=True)
def _prespawn_aiodns_thread() -> Iterator[None]:
    """
    Pre-spawn the pycares/aiodns daemon DNS thread.

    aiohttp's default resolver (aiodns/pycares) lazily starts a daemon thread
    named ``_run_safe_shutdown_loop`` the first time a ClientSession is created.
    When that happens inside a test body, pytest-homeassistant-custom-component's
    ``verify_cleanup`` fixture sees a thread that was absent from its pre-test
    snapshot and fails the test at teardown. Spawning (and holding) the channel
    once at session scope keeps the thread present in every test's snapshot.
    """
    channel = pycares.Channel()
    yield
    del channel


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
