"""Adapter for existing repository-native AION/Astra runtime audit events."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from .models import EventFamily, NormalizedEvent, RuntimeBinding, SubstrateError, sha256_json

NATIVE_PROFILE_ID = "AION_ASTRA_BOUNDED_RUNTIME_NATIVE_V0.1.0"

_ADMITTED_ACTIONS = frozenset(
    {
        "runtime.started",
        "planner.decision",
        "tool.completed",
        "runtime.hold",
        "task.started",
        "task.completed",
        "runtime.stopped",
        "runtime.recovered",
        "memory.written",
        "memory.recalled",
    }
)


def normalize_event(
    raw: Mapping[str, Any],
    *,
    binding: RuntimeBinding,
    sequence: int,
) -> NormalizedEvent:
    action = str(raw.get("action") or raw.get("event_type") or "").strip()
    if action not in _ADMITTED_ACTIONS:
        raise SubstrateError(f"native runtime event is unsupported: {action}")
    details = raw.get("details", {})
    if not isinstance(details, Mapping):
        raise SubstrateError("native runtime event details must be an object")
    return NormalizedEvent(
        sequence=sequence,
        source=NATIVE_PROFILE_ID,
        source_event_type=action,
        family=EventFamily.NATIVE_RUNTIME,
        session_id=binding.session_id,
        payload_sha256=sha256_json(details),
        payload_keys=tuple(sorted(str(key) for key in details)),
    )


def normalize_trajectory(
    events: Iterable[Mapping[str, Any]],
    *,
    binding: RuntimeBinding,
) -> tuple[NormalizedEvent, ...]:
    normalized = tuple(
        normalize_event(raw, binding=binding, sequence=index)
        for index, raw in enumerate(events, start=1)
    )
    if not normalized:
        raise SubstrateError("trajectory requires at least one native runtime event")
    return normalized
