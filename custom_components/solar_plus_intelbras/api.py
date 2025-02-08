"""Sample API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout
from .const import SOLAR_PLUS_INTELBRAS_API_URL


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
        username: str,
        password: str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._session = session

    async def async_login(self) -> Any:
        """Login to the API."""
        return await self._api_wrapper(
            method="post",
            url=f"{SOLAR_PLUS_INTELBRAS_API_URL}/login",
            data={"email": self._username},
            headers={"plus": self._password},
        )

    async def async_get_token(self) -> str:
        """Get token from the API."""
        response = await self.async_login()
        return response["accessToken"]["accessJWT"]

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="get",
            url=f"{SOLAR_PLUS_INTELBRAS_API_URL}/plants",
            headers={
                "Authorization": f"Bearer {await self.async_get_token()}",
                "plus": self._password,
            },
        )

    async def async_set_title(self, value: str) -> Any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Timeout error fetching information - {exception}"
            raise SolarPlusIntelbrasApiClientCommunicationError(
                msg,
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Error fetching information - {exception}"
            raise SolarPlusIntelbrasApiClientCommunicationError(
                msg,
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Something really wrong happened! - {exception}"
            raise SolarPlusIntelbrasApiClientError(
                msg,
            ) from exception
