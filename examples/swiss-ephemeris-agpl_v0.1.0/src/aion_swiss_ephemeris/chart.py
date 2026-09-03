# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026 AION Project Owner
"""Bounded civil-offset -> UTC -> TT/UT1 -> whole-sign chart acquisition."""
from datetime import datetime, timedelta, timezone
import hashlib
from importlib.resources import files
import math
import os
from pathlib import Path
import re
import subprocess
import sys

from .provider import BODIES, MAX_OUTPUT, UPSTREAM_COMMIT, VERSION, verify_cache

LEAP_SHA256 = "db5a895f16853b03bfc865e8d68f9fc8710ef1740e3400c701cd46a5bbbc3433"
ANGLES = ("Ascendant", "MC", "ARMC", "Vertex", "equat. Asc.", "co-Asc. W.Koch", "co-Asc Munkasey", "Polar Asc.")
ROWS = BODIES + tuple(f"house {i}" for i in range(1, 13)) + ANGLES


def utc_input(value: str) -> datetime:
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})", value
    ):
        raise ValueError("explicit ISO datetime with seconds and UTC offset required")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if not value.endswith("Z") and (int(value[-5:-3]) > 23 or int(value[-2:]) > 59):
        raise ValueError("invalid explicit UTC offset")
    return parsed.astimezone(timezone.utc)


def expected_tt(utc: datetime) -> float:
    payload = files(__package__).joinpath("leap-seconds.list").read_bytes()
    if hashlib.sha256(payload).hexdigest() != LEAP_SHA256:
        raise ValueError("pinned leap-second data mismatch")
    text = payload.decode("ascii")
    origin = datetime(1900, 1, 1, tzinfo=timezone.utc)
    expires = origin + timedelta(seconds=int(re.search(r"^#@\s+(\d+)", text, re.M)[1]))
    # Leap-second instants themselves are not representable by datetime and are
    # rejected at input. Future dates beyond the reviewed file validity fail.
    if not datetime(1972, 1, 1, tzinfo=timezone.utc) <= utc < expires:
        raise ValueError("UTC outside reviewed leap-table range [1972, expiry)")
    offset = None
    for ntp, tai in re.findall(r"^(\d+)\s+(\d+)\s+#", text, re.M):
        if origin + timedelta(seconds=int(ntp)) <= utc:
            offset = int(tai)
    jd_utc = 2451545.0 + (utc - datetime(2000, 1, 1, 12, tzinfo=timezone.utc)).total_seconds() / 86400
    return jd_utc + (offset + 32.184) / 86400


def coordinate(value, limit: float, name: str) -> float:
    if type(value) not in (int, float) or not -limit <= value <= limit:
        raise ValueError("invalid " + name)
    return float(value)


def parse_chart(stdout: str, stderr: str, code: int, utc: datetime, latitude: float, longitude: float) -> dict:
    if code != 0 or stderr.strip() or len(stdout.encode("utf-8")) > MAX_OUTPUT:
        raise ValueError("native chart execution failed")
    if re.search(r"warning|error|moshier|not found", stdout, re.I):
        raise ValueError("native warning or fallback rejected")
    if re.findall(r"\bversion\s+(\S+)", stdout) != [VERSION]:
        raise ValueError("unexpected native version")
    tt = re.findall(r"^TT:\s+([0-9.]+)\s*$", stdout, re.M)
    ut = re.findall(r"^UT:\s+([0-9.]+)\s+delta t:\s+([0-9.]+) sec\s*$", stdout, re.M)
    if len(tt) != 1 or len(ut) != 1:
        raise ValueError("missing or duplicate time-scale headers")
    tt, (ut1, delta) = float(tt[0]), tuple(map(float, ut[0]))
    if abs(tt - expected_tt(utc)) > 2e-9 or abs((tt-ut1)*86400-delta) > 0.0002:
        raise ValueError("UTC/TT/UT1 binding mismatch; UTC-as-UT fallback rejected")
    geo = re.findall(r"^geo\. long ([^,]+), lat ([^,]+), alt (\S+)\s*$", stdout, re.M)
    if (len(geo) != 1 or not all(math.isfinite(float(v)) for v in geo[0])
            or abs(float(geo[0][0])-longitude) > 5e-7
            or abs(float(geo[0][1])-latitude) > 5e-7 or float(geo[0][2]) != 0):
        raise ValueError("geographic header mismatch")
    if len(re.findall(r"^Houses system W \(equal/ whole sign\) for", stdout, re.M)) != 1:
        raise ValueError("whole-sign house header required")
    rows = []
    started = False
    for line in stdout.splitlines():
        parts = [p.strip() for p in line.split(",")]
        label = " ".join(parts[0].split())
        if label in ROWS:
            started = True
        if not started or not line.strip():
            continue
        if len(parts) != 4 or label not in ROWS:
            raise ValueError("unknown or malformed chart record")
        values = tuple(map(float, parts[1:]))
        if not all(math.isfinite(x) for x in values) or not 0 <= values[0] < 360 or not -90 <= values[2] <= 90:
            raise ValueError("chart values outside finite bounds")
        rows.append((label, values))
    if tuple(k for k, v in rows) != ROWS:
        raise ValueError("chart rows missing, duplicated or out of order")
    data = dict(rows)
    asc, mc = data["Ascendant"][0], data["MC"][0]
    cusps = [data[f"house {i}"][0] for i in range(1, 13)]
    if any(abs(cusp - ((int(asc // 30) + i) % 12) * 30) > 1e-6 for i, cusp in enumerate(cusps)):
        raise ValueError("whole-sign cusp sequence disagrees with ascendant")
    altitude = data["Sun"][2]
    if abs(altitude) <= 0.1:
        raise ValueError("solar centre near horizon; sect requires a separate reviewed convention")
    return {"jd_tt": tt, "jd_ut1": ut1, "delta_t_seconds": delta,
            "ascendant_longitude": asc, "midheaven_longitude": mc,
            "whole_sign_cusps": cusps, "is_day_chart": altitude > 0,
            "sun_geometric_altitude_degrees": altitude,
            "positions": [{"planet":name.upper(), "longitude":data[name][0],
                           "speed_longitude":data[name][1]} for name in BODIES]}


def calculate_chart(cache: Path, event_datetime: str, latitude: float, longitude: float) -> dict:
    utc = utc_input(event_datetime)
    expected_tt(utc)  # Fail before native execution for unsupported epochs.
    latitude = coordinate(latitude, 65, "latitude (reviewed range +/-65 degrees)")
    longitude = coordinate(longitude, 180, "longitude")
    cache = Path(cache).resolve()
    if any(c in str(cache) for c in (";", ",", "\n", "\r")):
        raise ValueError("cache path has an ephemeris delimiter")
    entries = verify_cache(cache)
    if sys.platform != "win32":
        raise ValueError("pinned native chart profile requires Windows x64")
    for directory in (cache, cache / "ephe"):
        for name in ("seleapsec.txt", "swe_deltat.txt", "sedeltat.txt"):
            if (directory / name).exists():
                raise ValueError("unreviewed native time override present")
    argv = [str(cache / "windows/programs/swetest64.exe"), f"-b{utc.day}.{utc.month}.{utc.year}",
            "-utc"+utc.strftime("%H:%M:%S"), "-p0123456789", "-eswe", "-edir"+str(cache/"ephe"),
            "-fPlsh", "-g,", f"-house{longitude:.8f},{latitude:.8f},W",
            f"-geopos{longitude:.8f},{latitude:.8f},0"]
    env = {k:v for k,v in os.environ.items() if k.upper() != "SE_EPHE_PATH"}
    proc = subprocess.run(argv, cwd=cache/"ephe", capture_output=True, text=True,
                          encoding="utf-8", errors="strict", env=env, timeout=30, check=False)
    result = parse_chart(proc.stdout, proc.stderr, proc.returncode, utc, latitude, longitude)
    verify_cache(cache)
    result.update(event_datetime_utc=utc.isoformat().replace("+00:00", "Z"),
                  latitude=latitude, longitude=longitude, engine_version=VERSION,
                  upstream_commit=UPSTREAM_COMMIT, provider="SWISS_EPHEMERIS_AGPL_PINNED_WINDOWS_CHART_V1",
                  coordinate_frame="GEOCENTRIC_TROPICAL_ECLIPTIC_OF_DATE",
                  chart_scope="TEN_PLANET_TROPICAL_WHOLE_SIGN_V1",
                  sect_rule="GEOCENTRIC_SOLAR_CENTRE_GEOMETRIC_ALTITUDE_NO_REFRACTION_0.1_DEGREE_HOLD",
                  ut1_policy="PINNED_SWISS_DELTA_T_MODEL_NOT_OBSERVED_IERS_UT1",
                  leap_seconds_sha256=LEAP_SHA256, precision_scope="NOT_INDEPENDENTLY_CERTIFIED",
                  file_hashes={e["path"]:e["sha256"] for e in entries},
                  execution={"argv":argv, "exit_status":proc.returncode, "stdout":proc.stdout, "stderr":proc.stderr},
                  network_during_calculation=False, complete_chart=True,
                  adapter_license="AGPL-3.0-only", subjectivity="NOT_ESTABLISHED",
                  canonical_effect="NONE", deployment=False, action_authority="NONE")
    return result


def to_research_chart_input(result: dict, *, input_id: str, location_label: str, synthetic_fixture: bool):
    """Bridge only explicitly declared synthetic research inputs; no personal binding."""
    if synthetic_fixture is not True or not input_id.startswith("SYNTHETIC_") or not location_label.startswith("SYNTHETIC_"):
        raise ValueError("classical engine bridge requires explicit synthetic research labels")
    if result.get("chart_scope") != "TEN_PLANET_TROPICAL_WHOLE_SIGN_V1" or result.get("canonical_effect") != "NONE":
        raise ValueError("unsupported research chart result")
    from aion_astra_classical_astrology import ChartInput, PlanetPosition
    return ChartInput(input_id=input_id, event_datetime_utc=result["event_datetime_utc"],
                      location_label=location_label, latitude=result["latitude"], longitude=result["longitude"],
                      ascendant_longitude=result["ascendant_longitude"], midheaven_longitude=result["midheaven_longitude"],
                      is_day_chart=result["is_day_chart"], positions=tuple(PlanetPosition(**p) for p in result["positions"]),
                      ephemeris_source=result["provider"], ephemeris_version=result["engine_version"],
                      coordinate_frame=result["coordinate_frame"], synthetic_fixture=True)
