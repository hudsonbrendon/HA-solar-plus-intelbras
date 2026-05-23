"""Tests for the config flow."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant import config_entries, data_entry_flow

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

from custom_components.solar_plus_intelbras.const import (
    CONF_EMAIL,
    CONF_PLANT_ID,
    CONF_PLUS,
    DOMAIN,
)


@pytest.fixture(autouse=True)
def _enable_custom_integrations(enable_custom_integrations):  # noqa: ANN001, ANN202
    return


async def test_user_flow_creates_entry(hass: HomeAssistant) -> None:
    """A valid user submission creates an entry with unique_id = plant_id."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == data_entry_flow.FlowResultType.FORM

    with patch(
        "custom_components.solar_plus_intelbras.config_flow.SolarPlusIntelbrasApiClient.async_get_data",
        new=AsyncMock(return_value={"rows": []}),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {CONF_EMAIL: "e@mail.com", CONF_PLUS: "tok", CONF_PLANT_ID: "42"},
        )
    assert result2["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result2["result"].unique_id == "42"


async def test_duplicate_plant_id_aborts(hass: HomeAssistant) -> None:
    """Adding the same plant_id twice aborts the second flow."""
    first = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    with patch(
        "custom_components.solar_plus_intelbras.config_flow.SolarPlusIntelbrasApiClient.async_get_data",
        new=AsyncMock(return_value={"rows": []}),
    ):
        await hass.config_entries.flow.async_configure(
            first["flow_id"],
            {CONF_EMAIL: "e@mail.com", CONF_PLUS: "tok", CONF_PLANT_ID: "42"},
        )
        second = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        result = await hass.config_entries.flow.async_configure(
            second["flow_id"],
            {CONF_EMAIL: "e@mail.com", CONF_PLUS: "tok", CONF_PLANT_ID: "42"},
        )
    assert result["type"] == data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "already_configured"
