"""Sample API Client."""

from __future__ import annotations

import asyncio
import socket
from datetime import date
from typing import Any

import aiohttp
import async_timeout

from .const import LOGGER, SOLAR_PLUS_INTELBRAS_API_URL


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
        self._access_token = None

    async def async_login(self) -> Any:
        """Login to the API."""
        return await self._api_wrapper(
            method="post",
            url=f"{SOLAR_PLUS_INTELBRAS_API_URL}/login",
            data={"email": self._email},
            headers={"plus": self._plus},
        )

    async def async_get_token(self) -> None:
        """Get token from the API."""
        response = await self.async_login()
        self._access_token = response["accessToken"]["accessJWT"]

    async def async_ensure_token(self) -> None:
        """Ensure that we have a valid access token."""
        # if self._access_token is None:
        await self.async_get_token()

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        await self.async_ensure_token()
        return await self._api_wrapper(
            method="get",
            url=f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants/{self._plant_id}/inverters?limit=20&page=1",
            headers={
                "Authorization": f"Bearer {self._access_token}",
                "plus": self._plus,
            },
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
