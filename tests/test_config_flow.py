"""Tests for the config flow."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant import config_entries, data_entry_flow

from custom_components.solar_plus_intelbras.api import (
    SolarPlusIntelbrasApiClientAuthenticationError,
)
from custom_components.solar_plus_intelbras.const import (
    CONF_EMAIL,
    CONF_PLANT_ID,
    CONF_PLUS,
    DOMAIN,
)

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

_CLIENT = "custom_components.solar_plus_intelbras.config_flow.SolarPlusIntelbrasApiClient"
PLANTS = {"rows": [{"id": 42, "name": "Casa"}, {"id": 43, "name": "Sitio"}]}


@pytest.fixture(autouse=True)
def _enable_custom_integrations(enable_custom_integrations):  # noqa: ANN001, ANN202
    return


def _patch_plants(rows: dict) -> object:
    return patch(f"{_CLIENT}.async_get_plants", new=AsyncMock(return_value=rows))


def _patch_setup_fetch() -> object:
    # Entry setup runs async_get_data on first refresh; keep it from hitting the network.
    return patch(
        "custom_components.solar_plus_intelbras.api.SolarPlusIntelbrasApiClient.async_get_data",
        new=AsyncMock(return_value={"rows": []}),
    )


async def _submit_user(hass: HomeAssistant) -> data_entry_flow.FlowResult:
    """Run step 1 (email + plus) and return the resulting step."""
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"
    return await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_EMAIL: "e@mail.com", CONF_PLUS: "tok"}
    )


async def test_two_step_flow_creates_entry(hass: HomeAssistant) -> None:
    """Step 1 collects email+plus; step 2 selects a plant and creates the entry."""
    with _patch_plants(PLANTS), _patch_setup_fetch():
        plant_step = await _submit_user(hass)
        assert plant_step["type"] == data_entry_flow.FlowResultType.FORM
        assert plant_step["step_id"] == "plant"
        result = await hass.config_entries.flow.async_configure(plant_step["flow_id"], {CONF_PLANT_ID: "42"})
    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == "42"
    assert result["data"][CONF_PLANT_ID] == "42"
    assert result["data"][CONF_EMAIL] == "e@mail.com"


async def test_invalid_credentials_show_error(hass: HomeAssistant) -> None:
    """Auth failure on step 1 shows a form error and stays on the user step."""
    with patch(
        f"{_CLIENT}.async_get_plants",
        new=AsyncMock(side_effect=SolarPlusIntelbrasApiClientAuthenticationError),
    ):
        result = await _submit_user(hass)
    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {"base": "auth"}


async def test_configured_plant_is_filtered(hass: HomeAssistant) -> None:
    """An already-configured plant is not offered again; a different one can be added."""
    with _patch_plants(PLANTS), _patch_setup_fetch():
        first = await _submit_user(hass)
        await hass.config_entries.flow.async_configure(first["flow_id"], {CONF_PLANT_ID: "42"})

        second = await _submit_user(hass)
        assert second["step_id"] == "plant"
        result = await hass.config_entries.flow.async_configure(second["flow_id"], {CONF_PLANT_ID: "43"})
    assert result["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result["result"].unique_id == "43"


async def test_no_plants_left_aborts(hass: HomeAssistant) -> None:
    """When every plant is already configured, the second flow aborts."""
    single = {"rows": [{"id": 42, "name": "Casa"}]}
    with _patch_plants(single), _patch_setup_fetch():
        first = await _submit_user(hass)
        await hass.config_entries.flow.async_configure(first["flow_id"], {CONF_PLANT_ID: "42"})
        result = await _submit_user(hass)
    assert result["type"] == data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "no_plants"
