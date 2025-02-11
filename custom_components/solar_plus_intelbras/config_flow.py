"""Adds config flow for Solar Plus Intelbras."""

from __future__ import annotations

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    SolarPlusIntelbrasApiClient,
    SolarPlusIntelbrasApiClientAuthenticationError,
    SolarPlusIntelbrasApiClientCommunicationError,
    SolarPlusIntelbrasApiClientError,
)
from .const import CONF_EMAIL, CONF_PLUS, DOMAIN, LOGGER

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PLUS): cv.string,
    }
)


class SolarPlusIntelbrasFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Solar Plus Intelbras."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    email=user_input[CONF_EMAIL],
                    plus=user_input[CONF_PLUS],
                )
            except SolarPlusIntelbrasApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except SolarPlusIntelbrasApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except SolarPlusIntelbrasApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_EMAIL],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_EMAIL,
                        default=(user_input or {}).get(CONF_EMAIL, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(CONF_PLUS): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def _test_credentials(self, email: str, plus: str) -> None:
        """Validate credentials."""
        client = SolarPlusIntelbrasApiClient(
            email=email,
            plus=plus,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()
