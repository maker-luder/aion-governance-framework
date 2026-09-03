from datetime import timezone, timedelta
from dataclasses import replace
from pathlib import Path
import json

import pytest

from aion_astra_bazi_core import timezone_data as tz
from aion_astra_bazi_core.calendar_engine import calendar_context, normalize_source_time
from aion_astra_bazi_core.errors import ValidationError
from aion_astra_bazi_core.rule_profiles import standard_lichun_profile


def test_host_timezone_search_is_not_used(monkeypatch, source_factory):
    import zoneinfo
    monkeypatch.setattr(zoneinfo, "TZPATH", ("/untrusted-host-data",))
    context, _, _ = calendar_context(source_factory(), standard_lichun_profile())
    assert context.timezone_data_version == "tzdata-2026.3/IANA-2026c"
    assert len(context.timezone_data_sha256) == 64
    assert context.utc_datetime == "1986-05-28T16:00:00+00:00"


@pytest.mark.parametrize("offset,expected", [("-04:00", "05:30"), ("-05:00", "06:30")])
def test_fold_resolved_by_recorded_offset(source_factory, offset, expected):
    source = source_factory(local_datetime="2021-11-07T01:30:00", timezone_id="America/New_York", offset=offset)
    civil, _ = normalize_source_time(source, standard_lichun_profile())
    assert civil.astimezone(timezone.utc).isoformat() == f"2021-11-07T{expected}:00+00:00"


@pytest.mark.parametrize("value,offset", [
    ("2021-03-14T02:30:00", "-05:00"),
    ("2021-03-14T02:30:00", "-04:00"),
    ("2021-03-14T02:30:00-05:00", "-04:00"),
    ("2021-11-07T01:30:00", "-06:00"),
])
def test_nonexistent_or_inconsistent_local_time_fails(source_factory, value, offset):
    source = source_factory(local_datetime=value, timezone_id="America/New_York", offset=offset)
    with pytest.raises(ValidationError):
        normalize_source_time(source, standard_lichun_profile())


def test_explicit_offset_fold_and_naive_fold_agree(source_factory):
    source = source_factory(local_datetime="2021-11-07T01:30:00-05:00", timezone_id="America/New_York", offset="-05:00")
    explicit = normalize_source_time(source, standard_lichun_profile())[0]
    naive = normalize_source_time(replace(source, local_datetime="2021-11-07T01:30:00"), standard_lichun_profile())[0]
    assert explicit.astimezone(timezone.utc) == naive.astimezone(timezone.utc)


@pytest.mark.parametrize("key", ["../UTC", "/UTC", "Asia//Taipei", "Unknown/Zone", "Asia", "", None])
def test_invalid_zone(key):
    with pytest.raises(ValidationError):
        tz.pinned_zone(key)


def test_wrong_package_version_fails(monkeypatch):
    monkeypatch.setattr(tz.tzdata, "__version__", "unexpected")
    with pytest.raises(ValidationError, match="version mismatch"):
        tz.pinned_zone("UTC")


def test_invalid_local_datetime_and_broken_tzif_fail(monkeypatch):
    with pytest.raises(ValidationError):
        tz.resolve_civil("not-a-datetime", "UTC", "+00:00")
    monkeypatch.setattr(tz, "timezone_bytes", lambda _: b"broken")
    with pytest.raises(ValidationError, match="TZif"):
        tz.pinned_zone("UTC")


def test_historical_offset_seconds_are_not_truncated():
    assert tz.offset_text(timedelta(hours=7, minutes=36, seconds=42)) == "+07:36:42"
    with pytest.raises(ValidationError):
        tz.offset_text(None)


def test_hko_2033_month_boundaries_are_external_facts():
    from lunar_python import Solar
    path = Path(__file__).parents[1] / "docs/HKO_2033_BOUNDARY_VECTORS.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["source_sha256"] == "416a9c2c0cb7788fa79127e0bb7f574f08dbaca78ef056c42b4ef38e05fca009"
    for row in data["vectors"]:
        y, m, d = map(int, row["gregorian_date"].split("-"))
        lunar = Solar.fromYmdHms(y, m, d, 12, 0, 0).getLunar()
        assert (lunar.getYear(), lunar.getMonth(), lunar.getDay()) == tuple(row["lunar_ymd"])
