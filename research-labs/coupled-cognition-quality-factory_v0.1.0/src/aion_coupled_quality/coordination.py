from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import StrEnum

from .models import QualityError


def _text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise QualityError(f"{name} must be non-empty text")


class CoordinationRole(StrEnum):
    PRODUCER = "PRODUCER"
    REVIEWER = "REVIEWER"
    MONITOR = "MONITOR"
    ORCHESTRATOR = "ORCHESTRATOR"


class EventKind(StrEnum):
    TURN = "TURN"
    TURN_REQUEST = "TURN_REQUEST"
    TOPIC_SWITCH_REQUEST = "TOPIC_SWITCH_REQUEST"
    REQUEST_RESOLVED = "REQUEST_RESOLVED"
    STOP = "STOP"
    HANDOFF = "HANDOFF"


class SpeakerPolicy(StrEnum):
    ROUND_ROBIN = "ROUND_ROBIN"
    ADAPTIVE = "ADAPTIVE"
    DECENTRALIZED = "DECENTRALIZED"


class ContextPolicy(StrEnum):
    FULL_SHARED = "FULL_SHARED"
    SCOPED = "SCOPED"


class MonitorPolicy(StrEnum):
    PER_AGENT = "PER_AGENT"
    SYSTEM_LEVEL = "SYSTEM_LEVEL"


@dataclass(frozen=True, slots=True)
class CoordinationCondition:
    speaker_policy: SpeakerPolicy
    context_policy: ContextPolicy
    monitor_policy: MonitorPolicy
    condition_payload_sha256: str

    def __post_init__(self) -> None:
        for name, expected in (
            ("speaker_policy", SpeakerPolicy),
            ("context_policy", ContextPolicy),
            ("monitor_policy", MonitorPolicy),
        ):
            if type(getattr(self, name)) is not expected:
                raise QualityError(f"{name} must be an exact {expected.__name__}")
        _text("condition_payload_sha256", self.condition_payload_sha256)
        if len(self.condition_payload_sha256) != 64 or any(
            char not in "0123456789abcdef" for char in self.condition_payload_sha256
        ):
            raise QualityError("condition_payload_sha256 must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class CoordinationEvent:
    sequence: int
    actor_id: str
    role: CoordinationRole
    kind: EventKind
    topic_id: str
    content_sha256: str
    request_id: str = ""

    def __post_init__(self) -> None:
        if type(self.sequence) is not int or self.sequence < 0:
            raise QualityError("sequence must be a non-negative exact int")
        _text("actor_id", self.actor_id)
        _text("topic_id", self.topic_id)
        if type(self.role) is not CoordinationRole or type(self.kind) is not EventKind:
            raise QualityError("role and kind must use exact enums")
        if len(self.content_sha256) != 64 or any(
            char not in "0123456789abcdef" for char in self.content_sha256
        ):
            raise QualityError("content_sha256 must be a lowercase SHA-256 digest")
        if self.kind in {
            EventKind.TURN_REQUEST,
            EventKind.TOPIC_SWITCH_REQUEST,
            EventKind.REQUEST_RESOLVED,
        }:
            _text("request_id", self.request_id)
        elif self.request_id:
            raise QualityError("request_id is valid only for request or resolution events")


@dataclass(frozen=True, slots=True)
class CoordinationRequirement:
    required_roles: frozenset[CoordinationRole]
    maximum_request_latency: int
    require_termination: bool = True

    def __post_init__(self) -> None:
        if type(self.required_roles) is not frozenset or not self.required_roles:
            raise QualityError("required_roles must be a non-empty frozenset")
        if any(type(role) is not CoordinationRole for role in self.required_roles):
            raise QualityError("required_roles must contain exact CoordinationRole values")
        if type(self.maximum_request_latency) is not int or self.maximum_request_latency < 0:
            raise QualityError("maximum_request_latency must be a non-negative exact int")
        if type(self.require_termination) is not bool:
            raise QualityError("require_termination must be an exact bool")


@dataclass(frozen=True, slots=True)
class CoordinationAudit:
    turn_concentration: float
    role_coverage: float
    topic_switch_latencies: tuple[int, ...]
    unresolved_request_ids: tuple[str, ...]
    repeated_turn_content: int
    termination_quality: str
    ncr_reasons: tuple[str, ...]
    scientific_disposition: str = "HOLD"
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_coordination(
    events: tuple[CoordinationEvent, ...],
    requirement: CoordinationRequirement,
) -> CoordinationAudit:
    if not events:
        raise QualityError("coordination audit requires events")
    sequences = [event.sequence for event in events]
    if sequences != sorted(sequences) or len(sequences) != len(set(sequences)):
        raise QualityError("event sequence must be strictly ordered and unique")

    turns = [event for event in events if event.kind is EventKind.TURN]
    if not turns:
        raise QualityError("coordination audit requires at least one TURN")
    counts = Counter(event.actor_id for event in turns)
    total = len(turns)
    concentration = sum((count / total) ** 2 for count in counts.values())
    observed_roles = {event.role for event in turns}
    role_coverage = len(observed_roles & requirement.required_roles) / len(requirement.required_roles)

    opened: dict[str, CoordinationEvent] = {}
    latencies: list[int] = []
    ncrs: list[str] = []
    for event in events:
        if event.kind in {EventKind.TURN_REQUEST, EventKind.TOPIC_SWITCH_REQUEST}:
            if event.request_id in opened:
                raise QualityError(f"duplicate open request_id: {event.request_id}")
            opened[event.request_id] = event
        elif event.kind is EventKind.REQUEST_RESOLVED:
            if event.request_id not in opened:
                raise QualityError(f"resolution for unknown request_id: {event.request_id}")
            latency = event.sequence - opened.pop(event.request_id).sequence
            latencies.append(latency)
            if latency > requirement.maximum_request_latency:
                ncrs.append(f"REQUEST_LATENCY_EXCEEDED:{event.request_id}")

    missing_roles = sorted(role.value for role in requirement.required_roles - observed_roles)
    if missing_roles:
        ncrs.append("REQUIRED_ROLE_NO_TURN:" + ",".join(missing_roles))
    unresolved = tuple(sorted(opened))
    ncrs.extend(f"UNRESOLVED_REQUEST:{request_id}" for request_id in unresolved)
    terminated = events[-1].kind in {EventKind.STOP, EventKind.HANDOFF}
    if requirement.require_termination and not terminated:
        ncrs.append("TERMINATION_OR_HANDOFF_MISSING")
    duplicates = sum(count - 1 for count in Counter(event.content_sha256 for event in turns).values())
    return CoordinationAudit(
        turn_concentration=concentration,
        role_coverage=role_coverage,
        topic_switch_latencies=tuple(latencies),
        unresolved_request_ids=unresolved,
        repeated_turn_content=duplicates,
        termination_quality="EXPLICIT" if terminated else "MISSING",
        ncr_reasons=tuple(ncrs),
    )
