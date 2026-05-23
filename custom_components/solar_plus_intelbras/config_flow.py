"""Adds config flow for Solar Plus Intelbras."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries, data_entry_flow
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    SolarPlusIntelbrasApiClient,
    SolarPlusIntelbrasApiClientAuthenticationError,
    SolarPlusIntelbrasApiClientCommunicationError,
    SolarPlusIntelbrasApiClientError,
)
from .const import (
    CONF_EMAIL,
    CONF_PLANT_ID,
    CONF_PLUS,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL_MINUTES,
    DOMAIN,
    LOGGER,
    MAX_SCAN_INTERVAL_MINUTES,
    MIN_SCAN_INTERVAL_MINUTES,
)


class SolarPlusIntelbrasFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Solar Plus Intelbras."""

    VERSION = 1

    async def _validate(self, email: str, plus: str, plant_id: str) -> None:
        """Validate credentials by performing a data fetch."""
        client = SolarPlusIntelbrasApiClient(
            email=email,
            plus=plus,
            plant_id=plant_id,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_data()

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors: dict[str, str] = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_PLANT_ID])
            self._abort_if_unique_id_configured()
            try:
                await self._validate(
                    email=user_input[CONF_EMAIL],
                    plus=user_input[CONF_PLUS],
                    plant_id=user_input[CONF_PLANT_ID],
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
                        selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT),
                    ),
                    vol.Required(CONF_PLUS): selector.TextSelector(
                        selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD),
                    ),
                    vol.Required(
                        CONF_PLANT_ID,
                        default=(user_input or {}).get(CONF_PLANT_ID, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT),
                    ),
                },
            ),
            errors=_errors,
        )

    async def async_step_reauth(
        self, _entry_data: dict[str, Any]
    ) -> data_entry_flow.FlowResult:
        """Handle re-authentication when the plus token rotates."""
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict | None = None
    ) -> data_entry_flow.FlowResult:
        """Confirm reauth by accepting a new plus token."""
        _errors: dict[str, str] = {}
        entry = self._get_reauth_entry()
        if user_input is not None:
            try:
                await self._validate(
                    email=entry.data[CONF_EMAIL],
                    plus=user_input[CONF_PLUS],
                    plant_id=entry.data[CONF_PLANT_ID],
                )
            except SolarPlusIntelbrasApiClientAuthenticationError:
                _errors["base"] = "auth"
            except SolarPlusIntelbrasApiClientCommunicationError:
                _errors["base"] = "connection"
            except SolarPlusIntelbrasApiClientError:
                _errors["base"] = "unknown"
            else:
                self.hass.config_entries.async_update_entry(
                    entry, data={**entry.data, CONF_PLUS: user_input[CONF_PLUS]}
                )
                await self.hass.config_entries.async_reload(entry.entry_id)
                return self.async_abort(reason="reauth_successful")

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PLUS): selector.TextSelector(
                        selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD),
                    ),
                }
            ),
            errors=_errors,
        )

    @staticmethod
    @config_entries.callback
    def async_get_options_flow(
        _config_entry: config_entries.ConfigEntry,
    ) -> SolarPlusIntelbrasOptionsFlow:
        """Return the options flow handler."""
        return SolarPlusIntelbrasOptionsFlow()


class SolarPlusIntelbrasOptionsFlow(config_entries.OptionsFlow):
    """Options flow to change the polling interval."""

    async def async_step_init(
        self, user_input: dict | None = None
    ) -> data_entry_flow.FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = self.config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL_MINUTES
        )
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_SCAN_INTERVAL, default=current
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=MIN_SCAN_INTERVAL_MINUTES,
                            max=MAX_SCAN_INTERVAL_MINUTES,
                            mode=selector.NumberSelectorMode.BOX,
                            unit_of_measurement="min",
                        )
                    ),
                }
            ),
        )
