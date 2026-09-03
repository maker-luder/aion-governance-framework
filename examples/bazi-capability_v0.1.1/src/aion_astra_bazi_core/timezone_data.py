"""Read pinned package TZif bytes, never host TZPATH or a global ZoneInfo cache."""
from datetime import datetime, timedelta, timezone
import hashlib
from importlib.resources import files
import io
import re
from zoneinfo import ZoneInfo

import tzdata

from .errors import ValidationError

TZDATA_VERSION = "2026.3"
IANA_VERSION = "2026c"


def offset_text(value: timedelta | None) -> str:
    if value is None:
        raise ValidationError("timezone offset is unavailable")
    total = int(value.total_seconds())
    sign = "+" if total >= 0 else "-"
    total = abs(total)
    result = f"{sign}{total // 3600:02d}:{(total % 3600) // 60:02d}"
    return result + (f":{total % 60:02d}" if total % 60 else "")


def timezone_bytes(key: str) -> bytes:
    if (not isinstance(key, str) or not re.fullmatch(r"[A-Za-z0-9_+/-]+", key)
            or any(part in ("", ".", "..") for part in key.split("/"))):
        raise ValidationError("invalid IANA timezone identifier")
    if tzdata.__version__ != TZDATA_VERSION or tzdata.IANA_VERSION != IANA_VERSION:
        raise ValidationError("pinned tzdata version mismatch")
    try:
        return files("tzdata.zoneinfo").joinpath(*key.split("/")).read_bytes()
    except (FileNotFoundError, IsADirectoryError, OSError) as exc:
        raise ValidationError("unknown IANA timezone: " + key) from exc


def timezone_provenance(key: str) -> dict[str, str]:
    payload = timezone_bytes(key)
    return {"provider": "TZDATA_PACKAGE_ONLY", "package_version": TZDATA_VERSION,
            "iana_version": IANA_VERSION, "timezone_id": key,
            "tzif_sha256": hashlib.sha256(payload).hexdigest()}


def pinned_zone(key: str) -> ZoneInfo:
    try:
        return ZoneInfo.from_file(io.BytesIO(timezone_bytes(key)), key=key)
    except ValueError as exc:
        raise ValidationError("invalid pinned TZif data") from exc


def resolve_civil(value: str, key: str, recorded_offset: str) -> datetime:
    """Reject gaps; resolve a fold only with its already-required recorded offset."""
    zone = pinned_zone(key)
    try:
        parsed = datetime.fromisoformat(value)
    except (ValueError, TypeError) as exc:
        raise ValidationError("invalid ISO local datetime") from exc

    if parsed.tzinfo is not None:
        # An explicit offset is a statement about this local wall time, not a
        # request to silently translate an inconsistent local input to this zone.
        local = parsed.astimezone(zone)
        if (local.replace(tzinfo=None) != parsed.replace(tzinfo=None)
                or local.utcoffset() != parsed.utcoffset()
                or offset_text(local.utcoffset()) != recorded_offset):
            raise ValidationError("explicit datetime offset disagrees with IANA wall time")
        return local
    candidates = {}
    for fold in (0, 1):
        candidate = parsed.replace(tzinfo=zone, fold=fold)
        utc = candidate.astimezone(timezone.utc)
        back = utc.astimezone(zone)
        if (back.replace(tzinfo=None) == parsed and back.utcoffset() == candidate.utcoffset()
                and offset_text(candidate.utcoffset()) == recorded_offset):
            candidates[utc.isoformat()] = candidate
    if len(candidates) != 1:
        raise ValidationError("nonexistent local time or recorded offset does not resolve it")
    return next(iter(candidates.values()))
