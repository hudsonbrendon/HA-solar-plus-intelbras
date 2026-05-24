"""
Historical energy statistics import for solar_plus_intelbras.

Backfills the Home Assistant long-term statistics (and therefore the Energy
Dashboard) with monthly generation history from the ``records/years`` endpoint,
exposed as an external statistic per plant.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from homeassistant.components.recorder.models import StatisticData, StatisticMetaData
from homeassistant.components.recorder.statistics import async_add_external_statistics
from homeassistant.const import UnitOfEnergy

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .api import SolarPlusIntelbrasApiClient


def statistic_id(plant_id: str) -> str:
    """Return the external statistic id for a plant's energy history."""
    return f"{DOMAIN}:plant_{plant_id}_energy"


def build_statistics(rows: list[dict]) -> list[StatisticData]:
    """
    Build cumulative monthly energy statistics from records/years rows.

    Each row is ``{"year": "2025", "month": "1", "total": <kWh>}``. Rows are
    sorted chronologically and turned into a monotonically increasing ``sum``.
    """
    points: list[tuple[datetime, float]] = []
    for row in rows:
        try:
            start = datetime(int(row["year"]), int(row["month"]), 1, tzinfo=UTC)
            total = float(row.get("total") or 0)
        except (KeyError, TypeError, ValueError):
            continue
        points.append((start, total))

    points.sort(key=lambda point: point[0])

    stats: list[StatisticData] = []
    running = 0.0
    for start, total in points:
        running += total
        stats.append(StatisticData(start=start, state=running, sum=running))
    return stats


async def async_import_history(
    hass: HomeAssistant,
    client: SolarPlusIntelbrasApiClient,
    plant_id: str,
    name: str,
    year_range: tuple[int, int],
) -> int:
    """
    Fetch monthly history and import it as an external statistic.

    ``year_range`` is an inclusive ``(start_year, end_year)`` pair. Returns the
    number of statistic points imported.
    """
    rows = await client.async_get_records_years(year_range[0], year_range[1])
    stats = build_statistics(rows)
    if not stats:
        return 0

    metadata = StatisticMetaData(
        has_mean=False,
        has_sum=True,
        name=f"{name} energy",
        source=DOMAIN,
        statistic_id=statistic_id(plant_id),
        unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
    )
    async_add_external_statistics(hass, metadata, stats)
    return len(stats)
