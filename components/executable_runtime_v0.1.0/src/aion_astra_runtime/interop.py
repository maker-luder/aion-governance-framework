"""Versioned language-neutral interoperability primitives for the reference runtime.

This module is intentionally a reference implementation, not the definition of
AION semantics by Python. The profile is strict for security-sensitive contract
inputs: ambiguous JSON, non-NFC strings, non-finite numbers, unsupported
versions, and non-UTC timestamps fail closed.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any, Mapping


SERIALIZATION_PROFILE = "AION-JCS-COMPATIBLE-0.1.0"
INTEROP_VERSION = "0.1.0"
MAX_SAFE_INTEGER = 2**53 - 1


class InteropError(ValueError):
    """Stable reference error for malformed or unsupported interop values."""

    def __init__(self, error_code: str, message: str) -> None:
        super().__init__(message)
        self.error_code = error_code


class ErrorCategory(StrEnum):
    MALFORMED_INPUT = "MALFORMED_INPUT"
    UNKNOWN_FIELD = "UNKNOWN_FIELD"
    UNSUPPORTED_VERSION = "UNSUPPORTED_VERSION"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    AUTHORITY_DENIED = "AUTHORITY_DENIED"
    INVALID_TRANSITION = "INVALID_TRANSITION"
    CONFLICT = "CONFLICT"
    PERSISTENCE_FAILURE = "PERSISTENCE_FAILURE"
    INTEGRITY_FAILURE = "INTEGRITY_FAILURE"


@dataclass(frozen=True, slots=True)
class ErrorEnvelope:
    """Language-neutral admission result; native exceptions stay internal."""

    error_code: str
    category: ErrorCategory
    retryable: bool
    state_mutated: bool
    message: str
    details: dict[str, Any] = field(default_factory=dict)
    schema_version: str = INTEROP_VERSION
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        validate_version(self.schema_version)
        validate_identifier(self.error_code, field_name="error_code")
        validate_identifier(self.message, field_name="message")
        if type(self.retryable) is not bool or type(self.state_mutated) is not bool:
            raise InteropError("MALFORMED_INPUT", "error envelope flags must be booleans")
        if self.canonical_effect != "NONE":
            raise InteropError("AUTHORITY_DENIED", "canonical effects are not admitted")
        validate_json_value(self.details, path="details")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "error_code": self.error_code,
            "category": self.category.value,
            "retryable": self.retryable,
            "state_mutated": self.state_mutated,
            "canonical_effect": self.canonical_effect,
            "message": self.message,
            "details": dict(self.details),
        }

    @classmethod
    def from_dict(cls, raw: Mapping[str, Any]) -> "ErrorEnvelope":
        if not isinstance(raw, Mapping):
            raise InteropError("MALFORMED_INPUT", "error envelope must be an object")
        required = {
            "schema_version",
            "error_code",
            "category",
            "retryable",
            "state_mutated",
            "canonical_effect",
            "message",
            "details",
        }
        unknown = set(raw) - required
        missing = required - set(raw)
        if unknown:
            raise InteropError("UNKNOWN_FIELD", "error envelope contains unknown fields")
        if missing:
            raise InteropError("MALFORMED_INPUT", "error envelope is missing fields")
        try:
            category = ErrorCategory(raw["category"])
        except (KeyError, ValueError, TypeError) as exc:
            raise InteropError("MALFORMED_INPUT", "error envelope category is unsupported") from exc
        details = raw["details"]
        if not isinstance(details, dict):
            raise InteropError("MALFORMED_INPUT", "error envelope details must be an object")
        return cls(
            schema_version=raw["schema_version"],
            error_code=raw["error_code"],
            category=category,
            retryable=raw["retryable"],
            state_mutated=raw["state_mutated"],
            canonical_effect=raw["canonical_effect"],
            message=raw["message"],
            details=details,
        )


def validate_identifier(value: object, *, field_name: str = "identifier") -> str:
    """Validate an opaque security-sensitive identifier without silent coercion."""

    if not isinstance(value, str):
        raise InteropError("MALFORMED_INPUT", f"{field_name} must be a string")
    if not value or value.strip() != value or not value.strip():
        raise InteropError("MALFORMED_INPUT", f"{field_name} must be non-empty and untrimmed")
    if unicodedata.normalize("NFC", value) != value:
        raise InteropError("MALFORMED_INPUT", f"{field_name} must already be NFC-normalized")
    if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
        raise InteropError("MALFORMED_INPUT", f"{field_name} contains an unpaired surrogate")
    if len(value) > 256:
        raise InteropError("MALFORMED_INPUT", f"{field_name} exceeds the maximum length")
    return value


def validate_version(value: object) -> str:
    if value != INTEROP_VERSION:
        raise InteropError("UNSUPPORTED_VERSION", f"unsupported interop version: {value!r}")
    return INTEROP_VERSION


_TIMESTAMP_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})T(?P<time>\d{2}:\d{2}:\d{2})\.(?P<fraction>\d{6})Z$"
)


def validate_timestamp(value: object) -> str:
    """Validate the v0.1.0 UTC timestamp profile at six fractional digits."""

    if not isinstance(value, str):
        raise InteropError("MALFORMED_INPUT", "timestamp must be a string")
    match = _TIMESTAMP_RE.fullmatch(value)
    if match is None:
        raise InteropError("MALFORMED_INPUT", "timestamp must be RFC3339 UTC with six fractional digits")
    try:
        datetime.fromisoformat(f"{match.group('date')}T{match.group('time')}.{match.group('fraction')}+00:00")
    except ValueError as exc:
        raise InteropError("MALFORMED_INPUT", "timestamp is not a valid UTC instant") from exc
    return value


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InteropError("MALFORMED_INPUT", "duplicate JSON object member")
        result[key] = value
    return result


def _reject_non_finite(value: str) -> Any:
    raise InteropError("MALFORMED_INPUT", f"non-finite JSON number is not allowed: {value}")


def parse_strict_json(raw: str) -> Any:
    if not isinstance(raw, str):
        raise InteropError("MALFORMED_INPUT", "JSON input must be text")
    try:
        value = json.loads(
            raw,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_non_finite,
        )
    except InteropError:
        raise
    except (TypeError, json.JSONDecodeError) as exc:
        raise InteropError("MALFORMED_INPUT", "invalid JSON text") from exc
    validate_json_value(value)
    return value


def validate_json_value(value: object, *, path: str = "$", require_nfc: bool = True) -> None:
    """Validate the restricted JSON subset used by security-sensitive contracts."""

    if value is None or isinstance(value, bool):
        return
    if isinstance(value, int):
        if abs(value) > MAX_SAFE_INTEGER:
            raise InteropError("MALFORMED_INPUT", f"integer outside safe range at {path}")
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise InteropError("MALFORMED_INPUT", f"non-finite number at {path}")
        raise InteropError("MALFORMED_INPUT", f"floating-point numbers are not admitted at {path}")
    if isinstance(value, str):
        if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
            raise InteropError("MALFORMED_INPUT", f"unpaired surrogate at {path}")
        if require_nfc and unicodedata.normalize("NFC", value) != value:
            raise InteropError("MALFORMED_INPUT", f"string is not NFC-normalized at {path}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            validate_json_value(item, path=f"{path}[{index}]", require_nfc=require_nfc)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise InteropError("MALFORMED_INPUT", f"object key is not a string at {path}")
            if require_nfc and unicodedata.normalize("NFC", key) != key:
                raise InteropError("MALFORMED_INPUT", f"object key is not NFC-normalized at {path}")
            validate_json_value(item, path=f"{path}.{key}", require_nfc=require_nfc)
        return
    raise InteropError("MALFORMED_INPUT", f"unsupported JSON value at {path}")


def _utf16_sort_key(value: str) -> bytes:
    return value.encode("utf-16-be", errors="strict")


def _canonical_value(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: _canonical_value(value[key])
            for key in sorted(value, key=_utf16_sort_key)
        }
    if isinstance(value, list):
        return [_canonical_value(item) for item in value]
    return value


def canonical_json_text(value: object) -> str:
    """Return deterministic, whitespace-free JSON for the AION v0.1.0 subset."""

    validate_json_value(value)
    return json.dumps(
        _canonical_value(value),
        ensure_ascii=False,
        sort_keys=False,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_json_bytes(value: object) -> bytes:
    return canonical_json_text(value).encode("utf-8")


def sha256_canonical(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()
