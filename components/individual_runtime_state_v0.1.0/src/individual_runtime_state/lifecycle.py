from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .store import RuntimeEvent, RuntimeStateError


_LIFECYCLE_REQUEST_FIELDS = ("event_type", "canonical_effect")
_ALLOWED_EVENT_TYPES = ("runtime.started", "runtime.stopped")


@dataclass(frozen=True, slots=True)
class LifecycleTransitionRequest:
    """Strict caller request; persisted and implementation-derived fields are excluded."""

    event_type: str
    canonical_effect: str = "NONE"

    @classmethod
    def from_dict(cls, raw: object) -> "LifecycleTransitionRequest":
        if not isinstance(raw, dict):
            raise RuntimeStateError("lifecycle transition request must be an object")
        missing = [field for field in _LIFECYCLE_REQUEST_FIELDS if field not in raw]
        unknown = sorted(
            (str(field) for field in raw if field not in _LIFECYCLE_REQUEST_FIELDS),
            key=str,
        )
        non_strings = [
            field
            for field in _LIFECYCLE_REQUEST_FIELDS
            if field in raw and not isinstance(raw[field], str)
        ]
        if missing:
            raise RuntimeStateError(
                f"lifecycle transition request is missing fields: {', '.join(missing)}"
            )
        if unknown:
            raise RuntimeStateError(
                f"lifecycle transition request contains unknown fields: {', '.join(unknown)}"
            )
        if non_strings:
            raise RuntimeStateError(
                "lifecycle transition request fields must be strings: "
                + ", ".join(non_strings)
            )
        event_type = raw["event_type"]
        canonical_effect = raw["canonical_effect"]
        if event_type not in _ALLOWED_EVENT_TYPES:
            raise RuntimeStateError(f"unsupported runtime lifecycle event: {event_type}")
        if canonical_effect != "NONE":
            raise RuntimeStateError("lifecycle transition canonical_effect must be NONE")
        return cls(event_type=event_type, canonical_effect=canonical_effect)

    def to_dict(self) -> dict[str, str]:
        return {
            "event_type": self.event_type,
            "canonical_effect": self.canonical_effect,
        }


@dataclass(frozen=True, slots=True)
class LifecycleTransitionOutcome:
    """Derived result after the state layer reads, validates, and appends a request."""

    request: LifecycleTransitionRequest
    from_state: str
    to_state: str
    event: RuntimeEvent

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": self.request.to_dict(),
            "from_state": self.from_state,
            "to_state": self.to_state,
            "event_sequence": self.event.sequence,
            "event_hash": self.event.event_hash,
        }
