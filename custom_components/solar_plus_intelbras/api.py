"""Sample API Client."""

from __future__ import annotations

import asyncio
import socket
import time
from datetime import date
from typing import Any

import aiohttp
import async_timeout

from .const import DEFAULT_CURRENCY, LOGGER, SOLAR_PLUS_INTELBRAS_API_URL


class SolarPlusIntelbrasApiClientError(Exception):
    """Exception to indicate a general API error."""


class SolarPlusIntelbrasApiClientCommunicationError(
    SolarPlusIntelbrasApiClientError,
):
    """Exception to indicate a communication error."""


class SolarPlusIntelbrasApiClientAuthenticationError(
    SolarPlusIntelbrasApiClientError,
):
    """Exception to indicate an authentication error."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise SolarPlusIntelbrasApiClientAuthenticationError(
            msg,
        )
    response.raise_for_status()


class SolarPlusIntelbrasApiClient:
    """Sample API Client."""

    def __init__(
        self,
        email: str,
        plus: str,
        plant_id: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._email = email
        self._plus = plus
        self._plant_id = plant_id
        self._session = session
        self._access_token: str | None = None
        self._token_expires_at: float = 0.0
        self._currency: str = DEFAULT_CURRENCY

    @property
    def currency(self) -> str:
        """Return the account currency reported at login."""
        return self._currency

    async def async_login(self) -> Any:
        """Login to the API."""
        return await self._api_wrapper(
            method="post",
            url=f"{SOLAR_PLUS_INTELBRAS_API_URL}/login",
            data={"email": self._email},
            headers={"plus": self._plus},
        )

    async def async_get_token(self) -> None:
        """Get token from the API and cache it with its expiry."""
        response = await self.async_login()
        access = response["accessToken"]
        self._access_token = access["accessJWT"]
        # Refresh 60s before the server-reported expiry; fall back to 5 min.
        exp = access.get("exp")
        self._token_expires_at = (exp - 60) if exp else (time.time() + 300)
        try:
            self._currency = response["user"]["preferences"]["currency"] or DEFAULT_CURRENCY
        except (KeyError, TypeError):
            self._currency = DEFAULT_CURRENCY

    async def async_ensure_token(self) -> None:
        """Ensure that we have a valid, unexpired access token."""
        if self._access_token is None or time.time() >= self._token_expires_at:
            await self.async_get_token()

    @staticmethod
    def _extract_rows(response: Any, label: str) -> list:
        """Return the rows of an endpoint response, or [] if it failed."""
        if isinstance(response, BaseException):
            LOGGER.debug("Skipping %s endpoint: %s", label, response)
            return []
        return (response or {}).get("rows", []) or []

    async def async_get_data(self) -> Any:
        """
        Return inverter and microinverter rows merged into one response.

        Plants with microinverters return no rows from ``/inverters``, so both
        endpoints are queried in parallel and their rows merged. A failure of
        one endpoint (e.g. a plant that has no microinverters) is tolerated as
        long as the other succeeds; if both fail, the inverters error is raised
        so the update is reported as failed.
        """
        await self.async_ensure_token()
        headers = {
            "Authorization": f"Bearer {self._access_token}",
            "plus": self._plus,
        }
        inverters, microinverters = await asyncio.gather(
            self._api_wrapper(
                method="get",
                url=f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/{self._plant_id}/inverters?limit=20&page=1",
                headers=headers,
            ),
            self._api_wrapper(
                method="get",
                url=f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/{self._plant_id}/microinverters?limit=20&page=1",
                headers=headers,
            ),
            return_exceptions=True,
        )

        if isinstance(inverters, BaseException) and isinstance(microinverters, BaseException):
            raise inverters

        base = inverters if isinstance(inverters, dict) else microinverters
        merged = dict(base) if isinstance(base, dict) else {}
        merged["rows"] = self._extract_rows(inverters, "inverters") + self._extract_rows(
            microinverters, "microinverters"
        )
        return merged

    async def async_get_plants(self) -> Any:
        """Return the list of plants for the account (does not need a plant id)."""
        await self.async_ensure_token()
        return await self._api_wrapper(
            method="get",
            url=f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants",
            headers={
                "Authorization": f"Bearer {self._access_token}",
                "plus": self._plus,
            },
        )

    async def async_get_year_energy(self, year: int) -> float | None:
        """Return total energy (kWh) generated in the given year."""
        await self.async_ensure_token()
        url = (
            f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/{self._plant_id}/records/year"
            f"?period=year&year={year}&key=energy_today"
        )
        response = await self._api_wrapper(
            method="get",
            url=url,
            headers={"Authorization": f"Bearer {self._access_token}", "plus": self._plus},
        )
        if not response:
            return None
        return response.get("data", {}).get("total")

    async def async_get_plant_detail(self) -> Any:
        """Return the plant detail document."""
        await self.async_ensure_token()
        return await self._api_wrapper(
            method="get",
            url=f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/{self._plant_id}",
            headers={"Authorization": f"Bearer {self._access_token}", "plus": self._plus},
        )

    async def async_get_notifications(self, start_date: None | date = None, end_date: None | date = None) -> dict:
        """Get notifications from the API."""
        await self.async_ensure_token()

        if start_date is None:
            start_date = date.today()  # noqa: DTZ011
        if end_date is None:
            end_date = start_date

        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")

        url = f"{SOLAR_PLUS_INTELBRAS_API_URL}/user/notifications?page=1&start_date={start_date_str}&end_date={end_date_str}&pendings=true"  # noqa: E501

        return await self._api_wrapper(
            method="get",
            url=url,
            headers={"Authorization": f"Bearer {self._access_token}", "plus": self._plus},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
        retry_count: int = 2,
    ) -> Any:
        """Get information from the API."""
        for attempt in range(retry_count + 1):
            try:
                # Aumentado o timeout de 10 para 30 segundos para evitar erros de timeout
                async with async_timeout.timeout(30):
                    response = await self._session.request(
                        method=method,
                        url=url,
                        headers=headers,
                        json=data,
                    )
                    _verify_response_or_raise(response)
                    return await response.json()

            except TimeoutError as exception:
                if attempt < retry_count:
                    wait_time = 2 * (attempt + 1)  # Backoff exponencial
                    LOGGER.warning(
                        "Timeout error on attempt %s of %s, retrying in %s seconds: %s",
                        attempt + 1,
                        retry_count + 1,
                        wait_time,
                        str(exception),
                    )
                    await asyncio.sleep(wait_time)
                else:
                    msg = f"Timeout error fetching information after {retry_count + 1} attempts - {exception}"
                    raise SolarPlusIntelbrasApiClientCommunicationError(msg) from exception

            except (aiohttp.ClientError, socket.gaierror) as exception:
                if attempt < retry_count:
                    wait_time = 2 * (attempt + 1)  # Backoff exponencial
                    LOGGER.warning(
                        "Connection error on attempt %s of %s, retrying in %s seconds: %s",
                        attempt + 1,
                        retry_count + 1,
                        wait_time,
                        str(exception),
                    )
                    await asyncio.sleep(wait_time)
                else:
                    msg = f"Error fetching information after {retry_count + 1} attempts - {exception}"
                    raise SolarPlusIntelbrasApiClientCommunicationError(msg) from exception

            except Exception as exception:  # pylint: disable=broad-except
                msg = f"Something really wrong happened! - {exception}"
                raise SolarPlusIntelbrasApiClientError(
                    msg,
                ) from exception

        # Add explicit return statement at the end to satisfy the linter
        return None
