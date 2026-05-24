"""Tests for the config flow."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant import config_entries, data_entry_flow
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.solar_plus_intelbras.api import (
    SolarPlusIntelbrasApiClientAuthenticationError,
    SolarPlusIntelbrasApiClientCommunicationError,
    SolarPlusIntelbrasApiClientError,
)
from custom_components.solar_plus_intelbras.const import (
    CONF_EMAIL,
    CONF_PLANT_ID,
    CONF_PLUS,
    CONF_SCAN_INTERVAL,
    DOMAIN,
)

_ENTRY_DATA = {CONF_EMAIL: "e@mail.com", CONF_PLUS: "old", CONF_PLANT_ID: "42"}

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


@pytest.mark.parametrize(
    ("exc", "expected"),
    [
        (SolarPlusIntelbrasApiClientCommunicationError, "connection"),
        (SolarPlusIntelbrasApiClientError, "unknown"),
    ],
)
async def test_user_step_error_mapping(hass: HomeAssistant, exc: type, expected: str) -> None:
    """Communication/unknown errors map to the right form error."""
    with patch(f"{_CLIENT}.async_get_plants", new=AsyncMock(side_effect=exc)):
        result = await _submit_user(hass)
    assert result["errors"] == {"base": expected}


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


async def test_reconfigure_updates_credentials(hass: HomeAssistant) -> None:
    """Reconfigure updates the email/plus while keeping the same plant (unique_id)."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id="42",
        data={CONF_EMAIL: "old@mail.com", CONF_PLUS: "old", CONF_PLANT_ID: "42"},
    )
    entry.add_to_hass(hass)
    with _patch_plants(PLANTS), _patch_setup_fetch():
        result = await entry.start_reconfigure_flow(hass)
        assert result["step_id"] == "reconfigure"
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_EMAIL: "new@mail.com", CONF_PLUS: "newtok"}
        )
        await hass.async_block_till_done()
    assert result2["type"] == data_entry_flow.FlowResultType.ABORT
    assert result2["reason"] == "reconfigure_successful"
    assert entry.data[CONF_EMAIL] == "new@mail.com"
    assert entry.data[CONF_PLUS] == "newtok"
    assert entry.data[CONF_PLANT_ID] == "42"


async def test_reauth_flow_updates_plus(hass: HomeAssistant) -> None:
    """Reauth accepts a new plus token and updates the entry."""
    entry = MockConfigEntry(domain=DOMAIN, unique_id="42", data=_ENTRY_DATA)
    entry.add_to_hass(hass)
    with _patch_plants(PLANTS), _patch_setup_fetch():
        result = await entry.start_reauth_flow(hass)
        assert result["step_id"] == "reauth_confirm"
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {CONF_PLUS: "newtok"})
        await hass.async_block_till_done()
    assert result2["type"] == data_entry_flow.FlowResultType.ABORT
    assert result2["reason"] == "reauth_successful"
    assert entry.data[CONF_PLUS] == "newtok"


async def test_reauth_invalid_shows_error(hass: HomeAssistant) -> None:
    """A bad token during reauth re-shows the form with an error."""
    entry = MockConfigEntry(domain=DOMAIN, unique_id="42", data=_ENTRY_DATA)
    entry.add_to_hass(hass)
    result = await entry.start_reauth_flow(hass)
    with patch(
        f"{_CLIENT}.async_get_plants",
        new=AsyncMock(side_effect=SolarPlusIntelbrasApiClientAuthenticationError),
    ):
        result2 = await hass.config_entries.flow.async_configure(result["flow_id"], {CONF_PLUS: "bad"})
    assert result2["step_id"] == "reauth_confirm"
    assert result2["errors"] == {"base": "auth"}


async def test_reconfigure_invalid_shows_error(hass: HomeAssistant) -> None:
    """A connection error during reconfigure re-shows the form with an error."""
    entry = MockConfigEntry(domain=DOMAIN, unique_id="42", data=_ENTRY_DATA)
    entry.add_to_hass(hass)
    result = await entry.start_reconfigure_flow(hass)
    with patch(
        f"{_CLIENT}.async_get_plants",
        new=AsyncMock(side_effect=SolarPlusIntelbrasApiClientCommunicationError),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], {CONF_EMAIL: "e@mail.com", CONF_PLUS: "bad"}
        )
    assert result2["step_id"] == "reconfigure"
    assert result2["errors"] == {"base": "connection"}


async def test_options_flow_sets_scan_interval(hass: HomeAssistant) -> None:
    """The options flow stores the chosen scan interval."""
    entry = MockConfigEntry(domain=DOMAIN, unique_id="42", data=_ENTRY_DATA)
    entry.add_to_hass(hass)
    with _patch_setup_fetch():
        result = await hass.config_entries.options.async_init(entry.entry_id)
        assert result["step_id"] == "init"
        result2 = await hass.config_entries.options.async_configure(result["flow_id"], {CONF_SCAN_INTERVAL: 10})
        await hass.async_block_till_done()
    assert result2["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert entry.options[CONF_SCAN_INTERVAL] == 10  # noqa: PLR2004


async def test_no_plants_left_aborts(hass: HomeAssistant) -> None:
    """When every plant is already configured, the second flow aborts."""
    single = {"rows": [{"id": 42, "name": "Casa"}]}
    with _patch_plants(single), _patch_setup_fetch():
        first = await _submit_user(hass)
        await hass.config_entries.flow.async_configure(first["flow_id"], {CONF_PLANT_ID: "42"})
        result = await _submit_user(hass)
    assert result["type"] == data_entry_flow.FlowResultType.ABORT
    assert result["reason"] == "no_plants"
