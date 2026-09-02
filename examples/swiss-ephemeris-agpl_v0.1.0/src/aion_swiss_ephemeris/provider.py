# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026 AION Project Owner
from __future__ import annotations

import hashlib
from importlib.resources import files
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

UPSTREAM_COMMIT = "3fd0f956d73898b91cc4f67cf18b21af656d1342"
VERSION = "2.10.03"
BODIES = ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto")
MAX_OUTPUT = 65536


def manifest() -> dict:
    result = json.loads(files(__package__).joinpath("lock.json").read_text(encoding="utf-8"))
    if result["commit"] != UPSTREAM_COMMIT:
        raise ValueError("unexpected upstream revision")
    return result


def cache_path(cache: Path, relative: str) -> Path:
    root = Path(cache).resolve()
    path = root / relative
    if path.is_symlink() or root not in path.resolve().parents:
        raise ValueError("cache entry escapes the cache root")
    return path


def verify_bytes(payload: bytes, entry: dict) -> None:
    if len(payload) != entry["bytes"] or hashlib.sha256(payload).hexdigest() != entry["sha256"]:
        raise ValueError("pinned file size or SHA-256 mismatch: " + entry["path"])


def verify_cache(cache: Path) -> list[dict]:
    entries = manifest()["files"]
    for entry in entries:
        path = cache_path(cache, entry["path"])
        with path.open("rb") as stream:
            payload = stream.read(entry["bytes"] + 1)
        verify_bytes(payload, entry)
    return entries


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(cache: Path) -> dict:
    """Explicit acquisition only, with immutable public URLs and no credentials."""
    entries = manifest()["files"]
    opener = urllib.request.build_opener(NoRedirect)
    for entry in entries:
        path = cache_path(cache, entry["path"])
        if path.exists():
            with path.open("rb") as stream:
                verify_bytes(stream.read(entry["bytes"] + 1), entry)
            continue
        url = "https://raw.githubusercontent.com/aloistr/swisseph/" + UPSTREAM_COMMIT + "/" + entry["path"]
        with opener.open(url, timeout=60) as response:
            payload = response.read(entry["bytes"] + 1)
        verify_bytes(payload, entry)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Never overwrite an existing file, including a concurrent download.
        with path.open("xb") as stream:
            stream.write(payload)
    verify_cache(cache)
    return {"status": "PASS", "files": len(entries), "upstream_commit": UPSTREAM_COMMIT,
            "license_route": "AGPL-3.0", "purchase": False}


def validate_jd(jd_tt: float) -> float:
    # Deliberately narrow engineering envelope, not the full upstream date range.
    if type(jd_tt) not in (int, float) or not 2400000.0 <= jd_tt <= 2500000.0:
        raise ValueError("JD TT must be finite numeric in [2400000, 2500000]")
    return float(jd_tt)


def parse_output(stdout: str, stderr: str, exit_status: int, jd_tt: float) -> list[dict]:
    jd_tt = validate_jd(jd_tt)
    if exit_status != 0 or stderr.strip() or len(stdout.encode("utf-8")) > MAX_OUTPUT:
        raise ValueError("ephemeris process failed or output contract exceeded")
    if re.search(r"warning|error|moshier|not found", stdout, re.IGNORECASE):
        raise ValueError("ephemeris warning or backend fallback rejected")
    versions = re.findall(r"\bversion\s+(\S+)", stdout)
    times = re.findall(r"^TT:\s+([0-9.]+)\s*$", stdout, re.MULTILINE)
    if versions != [VERSION] or len(times) != 1 or abs(float(times[0]) - jd_tt) > 1e-8:
        raise ValueError("engine version or TT epoch differs from the request")
    positions = []
    for line in stdout.splitlines():
        parts = [p.strip() for p in line.split(",")]
        if parts[0] not in BODIES:
            continue
        if len(parts) != 3:
            raise ValueError("malformed planet output")
        longitude, speed = map(float, parts[1:])
        if not (math.isfinite(longitude) and 0 <= longitude < 360 and math.isfinite(speed)):
            raise ValueError("non-finite or out-of-range planet output")
        positions.append({"body": parts[0].upper(), "longitude_degrees": longitude,
                          "speed_degrees_per_day": speed})
    if [p["body"] for p in positions] != [name.upper() for name in BODIES]:
        raise ValueError("expected exactly ten ordered unique planets")
    return positions


def calculate(cache: Path, jd_tt: float) -> dict:
    jd_tt = validate_jd(jd_tt)
    entries = verify_cache(cache)  # Detect missing/tampered data BEFORE execution.
    if sys.platform != "win32":
        raise ValueError("this pinned native executable profile requires Windows x64")
    cache = Path(cache).resolve()
    if any(c in str(cache) for c in (";", ",", "\n", "\r")):
        raise ValueError("cache path contains an ephemeris path-list delimiter")
    argv = [str(cache / "windows/programs/swetest64.exe"), f"-bj{jd_tt:.9f}",
            "-p0123456789", "-eswe", "-edir" + str(cache / "ephe"), "-fPls", "-g,"]
    proc = subprocess.run(argv, cwd=cache, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=30, check=False)
    positions = parse_output(proc.stdout, proc.stderr, proc.returncode, jd_tt)
    return {
        "provider": "SWISS_EPHEMERIS_AGPL_PINNED_WINDOWS_V1", "engine_version": VERSION,
        "upstream_commit": UPSTREAM_COMMIT, "jd_tt": jd_tt, "time_scale": "TT",
        "coordinate_frame": "GEOCENTRIC_TROPICAL_ECLIPTIC_OF_DATE",
        "backend": "REQUESTED_SWISS_DATA_NO_REPORTED_FALLBACK",
        "precision_scope": "7_DECIMAL_DEGREE_CLI_OUTPUT_NOT_INDEPENDENT_CERTIFICATION",
        "positions": positions, "file_hashes": {e["path"]: e["sha256"] for e in entries},
        "execution": {"argv": argv, "exit_status": proc.returncode,
                      "stdout": proc.stdout, "stderr": proc.stderr},
        "adapter_license": "AGPL-3.0-only", "network_during_calculation": False,
        "complete_chart": False, "subjectivity": "NOT_ESTABLISHED",
        "canonical_effect": "NONE", "deployment": False, "action_authority": "NONE",
    }
