"""Tests for diagnostics redaction."""

from __future__ import annotations

from custom_components.solar_plus_intelbras.diagnostics import redact_payload


def test_redacts_credentials_and_location() -> None:
    """Credentials and location fields are redacted; non-sensitive fields survive."""
    payload = {
        "entry": {"email": "secret@mail.com", "plus": "tok", "plant_id": "42"},
        "data": {
            "inverters": {
                "rows": [
                    {
                        "id": 1,
                        "serialNumber": "B1411309060",
                        "plant": {"latitude": -5.1, "longitude": -35.1, "zip": "59155-810"},
                    }
                ]
            }
        },
    }
    out = redact_payload(payload)
    assert out["entry"]["email"] == "**REDACTED**"
    assert out["entry"]["plus"] == "**REDACTED**"
    row = out["data"]["inverters"]["rows"][0]
    assert row["plant"]["latitude"] == "**REDACTED**"
    assert row["plant"]["zip"] == "**REDACTED**"
    assert row["id"] == 1
