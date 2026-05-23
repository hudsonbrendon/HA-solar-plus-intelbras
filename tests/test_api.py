"""Tests for the Solar Plus Intelbras API client."""

from __future__ import annotations

import time
from unittest.mock import AsyncMock, patch

import aiohttp
import pytest
from aioresponses import aioresponses

from custom_components.solar_plus_intelbras.api import SolarPlusIntelbrasApiClient
from custom_components.solar_plus_intelbras.const import SOLAR_PLUS_INTELBRAS_API_URL

INVERTERS_URL = f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/1/inverters?limit=20&page=1"
MICROINVERTERS_URL = f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/1/microinverters?limit=20&page=1"
LOGIN_URL = f"{SOLAR_PLUS_INTELBRAS_API_URL}/login"


@pytest.mark.asyncio
async def test_token_is_reused_until_expiry(login_response: dict) -> None:
    """A second data call must not trigger a second /login request."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    async with aiohttp.ClientSession() as session:
        client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
        with aioresponses() as mocked:
            mocked.post(LOGIN_URL, payload=login_response)
            mocked.get(INVERTERS_URL, payload={"rows": []}, repeat=True)
            mocked.get(MICROINVERTERS_URL, payload={"rows": []}, repeat=True)
            await client.async_get_data()
            await client.async_get_data()
            login_calls = [key for key in mocked.requests if key[0] == "post"]
            assert len(login_calls) == 1


@pytest.mark.asyncio
async def test_currency_captured_from_login(login_response: dict) -> None:
    """The client exposes the currency from the login preferences."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    async with aiohttp.ClientSession() as session:
        client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
        with aioresponses() as mocked:
            mocked.post(LOGIN_URL, payload=login_response)
            mocked.get(INVERTERS_URL, payload={"rows": []})
            mocked.get(MICROINVERTERS_URL, payload={"rows": []})
            await client.async_get_data()
            assert client.currency == "BRL"


@pytest.mark.asyncio
async def test_inverter_and_microinverter_rows_merged(login_response: dict) -> None:
    """Rows from both /inverters and /microinverters are merged into one response."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    async with aiohttp.ClientSession() as session:
        client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
        with aioresponses() as mocked:
            mocked.post(LOGIN_URL, payload=login_response)
            mocked.get(INVERTERS_URL, payload={"rows": [{"id": 1}]})
            mocked.get(MICROINVERTERS_URL, payload={"rows": [{"id": 2}]})
            data = await client.async_get_data()
            assert [row["id"] for row in data["rows"]] == [1, 2]


@pytest.mark.asyncio
async def test_microinverters_failure_is_tolerated(login_response: dict) -> None:
    """A failing /microinverters endpoint must not break inverter-only plants."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    async with aiohttp.ClientSession() as session:
        client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
        with (
            aioresponses() as mocked,
            patch("custom_components.solar_plus_intelbras.api.asyncio.sleep", new=AsyncMock()),
        ):
            mocked.post(LOGIN_URL, payload=login_response)
            mocked.get(INVERTERS_URL, payload={"rows": [{"id": 1}]})
            mocked.get(MICROINVERTERS_URL, status=500, repeat=True)
            data = await client.async_get_data()
            assert [row["id"] for row in data["rows"]] == [1]


@pytest.mark.asyncio
async def test_year_energy_returns_total(login_response: dict, records_year_response: dict) -> None:
    """async_get_year_energy returns data.total from records/year."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    async with aiohttp.ClientSession() as session:
        client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
        with aioresponses() as mocked:
            mocked.post(LOGIN_URL, payload=login_response)
            mocked.get(
                f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/1/records/year?period=year&year=2025&key=energy_today",
                payload=records_year_response,
            )
            total = await client.async_get_year_energy(2025)
            assert total == records_year_response["data"]["total"]


@pytest.mark.asyncio
async def test_get_plants_returns_rows(login_response: dict) -> None:
    """async_get_plants returns the account's plant list."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    async with aiohttp.ClientSession() as session:
        client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "", session)
        with aioresponses() as mocked:
            mocked.post(LOGIN_URL, payload=login_response)
            mocked.get(
                f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants",
                payload={"rows": [{"id": 42, "name": "Casa"}]},
            )
            response = await client.async_get_plants()
            assert response["rows"][0]["id"] == 42  # noqa: PLR2004
