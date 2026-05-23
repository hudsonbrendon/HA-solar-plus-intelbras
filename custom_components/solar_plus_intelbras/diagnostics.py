"""Diagnostics support for solar_plus_intelbras."""

from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any

from homeassistant.components.diagnostics import async_redact_data

from .const import CONF_EMAIL, CONF_PLANT_ID, CONF_PLUS

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import SolarPlusIntelbrasConfigEntry

TO_REDACT = {
    CONF_EMAIL,
    CONF_PLUS,
    CONF_PLANT_ID,
    "email",
    "latitude",
    "longitude",
    "zip",
    "serialNumber",
    "macAddress",
    "street",
    "userOwner",
    "accessJWT",
}


def redact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Recursively redact sensitive keys (pure, testable)."""
    return async_redact_data(copy.deepcopy(payload), TO_REDACT)


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: SolarPlusIntelbrasConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data.coordinator
    return redact_payload(
        {
            "entry": dict(entry.data),
            "options": dict(entry.options),
            "data": coordinator.data,
        }
    )
