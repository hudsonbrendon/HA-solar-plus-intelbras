"""Tests for the Solar Plus Intelbras API client."""

from __future__ import annotations

import asyncio
import time
from datetime import date
from unittest.mock import AsyncMock, patch

import pytest
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker

from custom_components.solar_plus_intelbras.api import (
    SolarPlusIntelbrasApiClient,
    SolarPlusIntelbrasApiClientAuthenticationError,
    SolarPlusIntelbrasApiClientCommunicationError,
    SolarPlusIntelbrasApiClientError,
)
from custom_components.solar_plus_intelbras.const import SOLAR_PLUS_INTELBRAS_API_URL

INVERTERS_URL = f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/1/inverters?limit=20&page=1"
MICROINVERTERS_URL = f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/1/microinverters?limit=20&page=1"
LOGIN_URL = f"{SOLAR_PLUS_INTELBRAS_API_URL}/login"


@pytest.fixture
def mocked() -> AiohttpClientMocker:
    return AiohttpClientMocker()


@pytest.fixture
async def session(mocked: AiohttpClientMocker):
    s = mocked.create_session(asyncio.get_running_loop())
    yield s
    await s.close()


@pytest.mark.asyncio
async def test_token_is_reused_until_expiry(mocked, session, login_response: dict) -> None:
    """A second data call must not trigger a second /login request."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(INVERTERS_URL, json={"rows": []})
    mocked.get(MICROINVERTERS_URL, json={"rows": []})
    await client.async_get_data()
    await client.async_get_data()
    login_calls = [key for key in mocked.mock_calls if key[0] == "post"]
    assert len(login_calls) == 1


@pytest.mark.asyncio
async def test_currency_captured_from_login(mocked, session, login_response: dict) -> None:
    """The client exposes the currency from the login preferences."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(INVERTERS_URL, json={"rows": []})
    mocked.get(MICROINVERTERS_URL, json={"rows": []})
    await client.async_get_data()
    assert client.currency == "BRL"


@pytest.mark.asyncio
async def test_inverter_and_microinverter_rows_merged(mocked, session, login_response: dict) -> None:
    """Rows from both /inverters and /microinverters are merged into one response."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(INVERTERS_URL, json={"rows": [{"id": 1}]})
    mocked.get(MICROINVERTERS_URL, json={"rows": [{"id": 2}]})
    data = await client.async_get_data()
    assert [row["id"] for row in data["rows"]] == [1, 2]


@pytest.mark.asyncio
async def test_microinverters_failure_is_tolerated(mocked, session, login_response: dict) -> None:
    """A failing /microinverters endpoint must not break inverter-only plants."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    with patch("custom_components.solar_plus_intelbras.api.asyncio.sleep", new=AsyncMock()):
        mocked.post(LOGIN_URL, json=login_response)
        mocked.get(INVERTERS_URL, json={"rows": [{"id": 1}]})
        mocked.get(MICROINVERTERS_URL, status=500)
        data = await client.async_get_data()
        assert [row["id"] for row in data["rows"]] == [1]


@pytest.mark.asyncio
async def test_year_energy_returns_total(mocked, session, login_response: dict, records_year_response: dict) -> None:
    """async_get_year_energy returns data.total from records/year."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(
        f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/1/records/year?period=year&year=2025&key=energy_today",
        json=records_year_response,
    )
    total = await client.async_get_year_energy(2025)
    assert total == records_year_response["data"]["total"]


@pytest.mark.asyncio
async def test_timeout_is_retried_then_raises(mocked, session, login_response: dict) -> None:
    """A persistent timeout is retried and then surfaces as a communication error."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    with patch("custom_components.solar_plus_intelbras.api.asyncio.sleep", new=AsyncMock()):
        mocked.post(LOGIN_URL, json=login_response)
        mocked.get(f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants", exc=TimeoutError())
        with pytest.raises(SolarPlusIntelbrasApiClientCommunicationError):
            await client.async_get_plants()


@pytest.mark.asyncio
async def test_unexpected_error_becomes_client_error(mocked, session, login_response: dict) -> None:
    """An unexpected error is wrapped as a generic client error."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants", exc=ValueError("boom"))
    with pytest.raises(SolarPlusIntelbrasApiClientError):
        await client.async_get_plants()


@pytest.mark.asyncio
async def test_get_plants_returns_rows(mocked, session, login_response: dict) -> None:
    """async_get_plants returns the account's plant list."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(
        f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants",
        json={"rows": [{"id": 42, "name": "Casa"}]},
    )
    response = await client.async_get_plants()
    assert response["rows"][0]["id"] == 42  # noqa: PLR2004


@pytest.mark.asyncio
async def test_get_records_years_returns_rows(mocked, session, login_response: dict) -> None:
    """async_get_records_years returns the monthly rows from data.rows."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(
        f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/1/records/years?start_year=2024&end_year=2025&key=energy_today",
        json={"data": {"rows": [{"year": "2025", "month": "1", "total": 5}], "total": 5}},
    )
    rows = await client.async_get_records_years(2024, 2025)
    assert rows[0]["total"] == 5  # noqa: PLR2004


@pytest.mark.asyncio
async def test_get_notifications_returns_payload(mocked, session, login_response: dict) -> None:
    """async_get_notifications fetches the notifications for a date range."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(
        f"{SOLAR_PLUS_INTELBRAS_API_URL}/user/notifications"
        "?page=1&start_date=2025-01-01&end_date=2025-01-01&pendings=true",
        json={"rows": [{"id": 1}]},
    )
    resp = await client.async_get_notifications(start_date=date(2025, 1, 1), end_date=date(2025, 1, 1))
    assert resp["rows"][0]["id"] == 1


@pytest.mark.asyncio
async def test_auth_error_keeps_its_type(mocked, session, login_response: dict) -> None:
    """A 401 surfaces as an authentication error (not a generic one) so reauth works."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants", status=401)
    with pytest.raises(SolarPlusIntelbrasApiClientAuthenticationError):
        await client.async_get_plants()


@pytest.mark.asyncio
async def test_client_error_is_not_retried(mocked, session, login_response: dict) -> None:
    """A 404 fails fast without burning the retry budget (single request)."""
    login_response["accessToken"]["exp"] = int(time.time()) + 3600
    client = SolarPlusIntelbrasApiClient("e@mail.com", "plus", "1", session)
    mocked.post(LOGIN_URL, json=login_response)
    mocked.get(f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants", status=404)
    with pytest.raises(SolarPlusIntelbrasApiClientCommunicationError):
        await client.async_get_plants()
    plant_calls = [k for k in mocked.mock_calls if k[0] == "get"]
    assert len(plant_calls) == 1
