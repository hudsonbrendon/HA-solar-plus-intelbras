"""Custom types for solar_plus_intelbras."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import SolarPlusIntelbrasApiClient
    from .coordinator import SolarPlusIntelbrasDataUpdateCoordinator


type SolarPlusIntelbrasConfigEntry = ConfigEntry[SolarPlusIntelbrasData]


@dataclass
class SolarPlusIntelbrasData:
    """Data for the Solar Plus Intelbras integration."""

    client: SolarPlusIntelbrasApiClient
    coordinator: SolarPlusIntelbrasDataUpdateCoordinator
    integration: Integration
