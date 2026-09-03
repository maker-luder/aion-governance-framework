# SPDX-License-Identifier: AGPL-3.0-only
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
import json

import pytest

from aion_swiss_ephemeris import chart as c

UTC = datetime(2000, 1, 1, 12, tzinfo=timezone.utc)


def output():
    return (Path(__file__).parent / "fixtures/taipei-2000-utc.txt").read_text(encoding="utf-8")


def test_native_utc_fixture_has_twelve_cusps_ten_planets_and_night_sect():
    r = c.parse_chart(output(), "", 0, UTC, 25.033, 121.5654)
    assert len(r["positions"]) == 10 and len(r["whole_sign_cusps"]) == 12
    assert r["ascendant_longitude"] == 137.119413
    assert r["is_day_chart"] is False
    assert r["jd_tt"] == pytest.approx(2451545 + 64.184/86400)


def test_small_jpl_observer_longitude_cross_check():
    ref = json.loads((Path(__file__).parent/"fixtures/jpl-2000-utc.json").read_text(encoding="utf-8"))
    result = c.parse_chart(output(), "", 0, UTC, 25.033, 121.5654)
    planets = {p["planet"]:p["longitude"] for p in result["positions"]}
    for row in ref["bodies"]:
        assert abs(planets[row["body"]]-row["longitude"]) <= ref["angular_tolerance_degrees"]


@pytest.mark.parametrize("value", ["2000-01-01", "2000-01-01T12:00:00", "2016-12-31T23:59:60Z", "2000-02-30T12:00:00Z", "2000-01-01T12:00:00+01:99", None])
def test_ambiguous_or_invalid_utc_input_rejected(value):
    with pytest.raises(ValueError):
        c.utc_input(value)


def test_civil_offset_matches_utc():
    assert c.utc_input("2000-01-01T20:00:00+08:00") == UTC


@pytest.mark.parametrize("value", ["1971-12-31T23:59:59Z", "2027-06-28T00:00:00Z"])
def test_epoch_outside_reviewed_leap_table_fails(value):
    with pytest.raises(ValueError):
        c.expected_tt(c.utc_input(value))


def test_leap_boundary_uses_two_seconds_between_adjacent_representable_instants():
    before = c.expected_tt(c.utc_input("2016-12-31T23:59:59Z"))
    after = c.expected_tt(c.utc_input("2017-01-01T00:00:00Z"))
    assert (after-before)*86400 == pytest.approx(2, abs=5e-5)


@pytest.mark.parametrize("mutate", [
    lambda t: t.replace("2.10.03", "2.10.02"),
    lambda t: t.replace("2451545.000742870", "2451545.000000000"),
    lambda t: t.replace("63.828915", "60.000000"),
    lambda t: t.replace("TT:", "MISSING:"),
    lambda t: t.replace("geo. long 121.565400", "geo. long nan"),
    lambda t: t.replace("lat 25.033000", "lat 20.033000"),
    lambda t: t.replace("Houses system W", "Houses system P"),
    lambda t: t.replace("280.3689229", "nan"),
    lambda t: t.replace("-36.2892833", "0.0000000"),
    lambda t: t.replace("120.0000000", "130.0000000"),
    lambda t: t.replace("Pluto", "Moon"),
    lambda t: t.replace("house 12", "house 13"),
    lambda t: t + "Sun,1,2,3\n",
    lambda t: t + "WARNING using Moshier\n",
    lambda t: t + "x"*65537,
])
def test_chart_parser_fails_closed(mutate):
    with pytest.raises(ValueError):
        c.parse_chart(mutate(output()), "", 0, UTC, 25.033, 121.5654)


@pytest.mark.parametrize("stderr,status", [("failure", 0), ("", 1)])
def test_chart_exit_and_stderr_rejected(stderr, status):
    with pytest.raises(ValueError):
        c.parse_chart(output(), stderr, status, UTC, 25.033, 121.5654)


@pytest.mark.parametrize("lat,lon", [(True, 1), (float("nan"), 1), (66, 1), (1, float("inf")), (1, 181)])
def test_coordinates_rejected_before_process(tmp_path, lat, lon):
    with pytest.raises(ValueError):
        c.calculate_chart(tmp_path, "2000-01-01T12:00:00Z", lat, lon)


def test_chart_process_and_classical_modern_bridge(monkeypatch, tmp_path):
    monkeypatch.setattr(c, "verify_cache", lambda _: [])
    monkeypatch.setattr(c.sys, "platform", "win32")
    seen = {}
    def run(argv, **kwargs):
        seen.update(argv=argv, **kwargs)
        return SimpleNamespace(stdout=output(), stderr="", returncode=0)
    monkeypatch.setattr(c.subprocess, "run", run)
    monkeypatch.setenv("SE_EPHE_PATH", "unreviewed")
    r = c.calculate_chart(tmp_path, "2000-01-01T20:00:00+08:00", 25.033, 121.5654)
    assert "SE_EPHE_PATH" not in seen["env"] and seen["timeout"] == 30
    assert "shell" not in seen and "-utc12:00:00" in seen["argv"]
    source = c.to_research_chart_input(r, input_id="SYNTHETIC_NATIVE_2000", location_label="SYNTHETIC_TAIPEI", synthetic_fixture=True)
    from aion_astra_classical_astrology import build_chart, integrated_classical_modern_profile
    built = build_chart(source, integrated_classical_modern_profile(), chart_id="SYNTHETIC_NATIVE_CHART_2000")
    assert len(built.planets) == 10 and built.sect == "NOCTURNAL"
    assert built.canonical_effect == "NONE" and built.deployment is False
    assert r["ut1_policy"] == "PINNED_SWISS_DELTA_T_MODEL_NOT_OBSERVED_IERS_UT1"
    json.dumps(r, allow_nan=False)


def test_explicit_nonresearch_input_is_not_relabelled():
    with pytest.raises(ValueError):
        c.to_research_chart_input({}, input_id="PERSON", location_label="HOME", synthetic_fixture=False)


def test_unreviewed_time_override_rejected(monkeypatch, tmp_path):
    monkeypatch.setattr(c, "verify_cache", lambda _: [])
    monkeypatch.setattr(c.sys, "platform", "win32")
    (tmp_path/"seleapsec.txt").write_text("20301231")
    with pytest.raises(ValueError, match="override"):
        c.calculate_chart(tmp_path, "2000-01-01T12:00:00Z", 25.033, 121.5654)


def test_unsupported_platform_and_cache_delimiter_fail(monkeypatch, tmp_path):
    monkeypatch.setattr(c, "verify_cache", lambda _: [])
    monkeypatch.setattr(c.sys, "platform", "linux")
    with pytest.raises(ValueError, match="Windows"):
        c.calculate_chart(tmp_path, "2000-01-01T12:00:00Z", 25.033, 121.5654)
    with pytest.raises(ValueError, match="delimiter"):
        c.calculate_chart(tmp_path/"bad,path", "2000-01-01T12:00:00Z", 25.033, 121.5654)


def test_tampered_leap_table_and_unrecognized_bridge_scope(monkeypatch):
    monkeypatch.setattr(c, "LEAP_SHA256", "0"*64)
    with pytest.raises(ValueError, match="leap-second"):
        c.expected_tt(UTC)
    with pytest.raises(ValueError, match="unsupported research"):
        c.to_research_chart_input({}, input_id="SYNTHETIC_1", location_label="SYNTHETIC_1", synthetic_fixture=True)
