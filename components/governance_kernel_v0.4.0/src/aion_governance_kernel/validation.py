
from __future__ import annotations

import json, re
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping, TypeVar
from uuid import uuid4

from .errors import InputValidationError
from .models import ActionType, AuthorizationState, Environment, OperationRequest, SourceType

MAX_SERIALIZED_BYTES = 16_384
MAX_DESCRIPTION_LENGTH = 4_096
MAX_TARGET_LENGTH = 1_024
MAX_METADATA_ITEMS = 20
MAX_METADATA_VALUE_LENGTH = 1_024
MAX_DEPTH = 4
REQUEST_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
ALLOWED_FIELDS = {
    "request_id", "source_type", "action", "target", "environment",
    "authorization", "destructive", "network_access", "description",
    "metadata", "risk_level", "risk_hint",
}
ACTION_ALIASES = {
    "ANALYSE_DOCUMENT": ActionType.ANALYZE_DOCUMENT,
    "ANALYZE": ActionType.ANALYZE_DOCUMENT,
    "READ": ActionType.READ_FILE,
    "WRITE": ActionType.WRITE_FILE,
    "MODIFY": ActionType.MODIFY_PROJECT,
    "TEST": ActionType.RUN_TESTS,
}
EnumT = TypeVar("EnumT", bound=Enum)

def _depth(value: Any, current: int = 0) -> int:
    if current > MAX_DEPTH:
        return current
    if isinstance(value, Mapping):
        return max([current] + [_depth(v, current + 1) for v in value.values()])
    if isinstance(value, (list, tuple)):
        return max([current] + [_depth(v, current + 1) for v in value])
    return current

def _enum(enum_cls: type[EnumT], raw: Any, field: str) -> EnumT:
    if not isinstance(raw, str):
        raise InputValidationError(f"{field} must be a string")
    key = raw.strip().upper().replace("-", "_").replace(" ", "_")
    try:
        return enum_cls(key)
    except ValueError as exc:
        raise InputValidationError(f"unsupported {field}") from exc

def _action(raw: Any) -> ActionType:
    if not isinstance(raw, str) or not raw.strip():
        raise InputValidationError("action must be a non-empty string")
    key = raw.strip().upper().replace("-", "_").replace(" ", "_")
    if key in ACTION_ALIASES:
        return ACTION_ALIASES[key]
    try:
        return ActionType(key)
    except ValueError:
        return ActionType.UNKNOWN

def _bool(raw: Any, field: str) -> bool:
    if type(raw) is not bool:
        raise InputValidationError(f"{field} must be boolean")
    return raw

def validate_operation_request(raw: Mapping[str, Any]) -> OperationRequest:
    if not isinstance(raw, Mapping):
        raise InputValidationError("request must be a mapping")
    unknown = set(raw) - ALLOWED_FIELDS
    if unknown:
        raise InputValidationError("unknown fields are not allowed")
    try:
        encoded = json.dumps(raw, ensure_ascii=False, default=str).encode("utf-8")
    except Exception as exc:
        raise InputValidationError("request is not JSON-serializable") from exc
    if len(encoded) > MAX_SERIALIZED_BYTES:
        raise InputValidationError("request exceeds size limit")
    if _depth(raw) > MAX_DEPTH:
        raise InputValidationError("request exceeds nesting limit")

    request_id = raw.get("request_id") or str(uuid4())
    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id):
        raise InputValidationError("invalid request_id")
    description = raw.get("description", "")
    target = raw.get("target", "")
    if not isinstance(description, str) or len(description) > MAX_DESCRIPTION_LENGTH:
        raise InputValidationError("invalid description")
    if not isinstance(target, str) or len(target) > MAX_TARGET_LENGTH:
        raise InputValidationError("invalid target")

    metadata_raw = raw.get("metadata", {})
    if not isinstance(metadata_raw, Mapping) or len(metadata_raw) > MAX_METADATA_ITEMS:
        raise InputValidationError("invalid metadata")
    metadata: dict[str, str] = {}
    for key, value in metadata_raw.items():
        if not isinstance(key, str) or not isinstance(value, (str, int, float, bool)):
            raise InputValidationError("metadata must contain scalar values")
        value_text = str(value)
        if len(key) > 128 or len(value_text) > MAX_METADATA_VALUE_LENGTH:
            raise InputValidationError("metadata item exceeds limit")
        metadata[key] = value_text
    if "risk_hint" in raw:
        metadata["untrusted_risk_hint"] = str(raw["risk_hint"])[:MAX_METADATA_VALUE_LENGTH]
    # risk_level is intentionally ignored; callers cannot self-assign it.

    return OperationRequest(
        request_id=request_id,
        source_type=_enum(SourceType, raw.get("source_type", "USER"), "source_type"),
        action=_action(raw.get("action")),
        target=target,
        environment=_enum(Environment, raw.get("environment", "SANDBOX"), "environment"),
        authorization=_enum(AuthorizationState, raw.get("authorization", "NONE"), "authorization"),
        destructive=_bool(raw.get("destructive", False), "destructive"),
        network_access=_bool(raw.get("network_access", False), "network_access"),
        description=description,
        metadata=OperationRequest.freeze_metadata(metadata),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
