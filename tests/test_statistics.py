"""Tests for historical statistics building."""

from __future__ import annotations

from datetime import UTC, datetime

from custom_components.solar_plus_intelbras.statistics import build_statistics, statistic_id


def test_build_statistics_is_sorted_and_cumulative() -> None:
    """Rows are sorted chronologically and turned into a cumulative sum."""
    rows = [
        {"year": "2025", "month": "2", "total": 10},
        {"year": "2025", "month": "1", "total": 30},
        {"year": "2024", "month": "12", "total": 5},
    ]
    stats = build_statistics(rows)
    assert [s["start"] for s in stats] == [
        datetime(2024, 12, 1, tzinfo=UTC),
        datetime(2025, 1, 1, tzinfo=UTC),
        datetime(2025, 2, 1, tzinfo=UTC),
    ]
    assert [s["sum"] for s in stats] == [5, 35, 45]
    assert [s["state"] for s in stats] == [5, 35, 45]


def test_build_statistics_skips_invalid_rows() -> None:
    """Rows with missing/invalid year, month or total are ignored."""
    rows = [
        {"year": "x", "month": "1", "total": 1},
        {"total": 5},
        {"year": "2025", "month": "3", "total": 7},
    ]
    stats = build_statistics(rows)
    assert len(stats) == 1
    assert stats[0]["sum"] == 7  # noqa: PLR2004


def test_statistic_id() -> None:
    """The external statistic id is namespaced by domain and plant."""
    assert statistic_id("42") == "solar_plus_intelbras:plant_42_energy"
