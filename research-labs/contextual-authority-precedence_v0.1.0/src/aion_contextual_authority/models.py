from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class SourceType(StrEnum):
    HUMAN_OWNER = "HUMAN_OWNER"
    TEACHER = "TEACHER"
    COLLABORATOR = "COLLABORATOR"
    REPOSITORY_DOCUMENT = "REPOSITORY_DOCUMENT"
    TOOL_OUTPUT = "TOOL_OUTPUT"
    UNTRUSTED_EXTERNAL_TEXT = "UNTRUSTED_EXTERNAL_TEXT"
    SYNTHETIC_FIXTURE = "SYNTHETIC_FIXTURE"


class DecisionClass(StrEnum):
    EXECUTE = "EXECUTE"
    ASK = "ASK"
    HOLD = "HOLD"
    DENY = "DENY"


@dataclass(frozen=True, slots=True)
class AuthorityContext:
    source_type: SourceType
    source_id: str
    scope: frozenset[str]
    priority: int
    issued_at: datetime
    expires_at: datetime | None = None
    revoked: bool = False
    non_overridable: bool = False
    explicit_authorization: bool = False
    allowed_actions: frozenset[str] = frozenset()
    blocked_actions: frozenset[str] = frozenset()
    text: str = ""

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id must be non-empty")
        if not self.scope or any(not item.strip() for item in self.scope):
            raise ValueError("scope must contain non-empty values")
        if not 0 <= self.priority <= 100:
            raise ValueError("priority must be between 0 and 100")
        if self.issued_at.tzinfo is None or self.issued_at.utcoffset() is None:
            raise ValueError("issued_at must be timezone-aware")
        if self.expires_at is not None:
            if self.expires_at.tzinfo is None or self.expires_at.utcoffset() is None:
                raise ValueError("expires_at must be timezone-aware")
            if self.expires_at < self.issued_at:
                raise ValueError("expires_at cannot precede issued_at")
        if self.non_overridable and not self.blocked_actions:
            raise ValueError("non_overridable context requires blocked_actions")


@dataclass(frozen=True, slots=True)
class ActionRequest:
    action_id: str
    requested_action: str
    target_scope: frozenset[str]
    requested_at: datetime

    def __post_init__(self) -> None:
        if not self.action_id.strip() or not self.requested_action.strip():
            raise ValueError("action_id and requested_action must be non-empty")
        if not self.target_scope or any(not item.strip() for item in self.target_scope):
            raise ValueError("target_scope must contain non-empty values")
        if self.requested_at.tzinfo is None or self.requested_at.utcoffset() is None:
            raise ValueError("requested_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class AuthorityDecision:
    decision: DecisionClass
    reason: str
    action_id: str
    source_type: SourceType | None
    source_id: str | None
    considered_sources: tuple[str, ...]
    higher_priority_conflict: bool = False
    canonical_effect: str = "NONE"
    deployment: bool = False
    live_runtime_effect: str = "NONE"

    def __post_init__(self) -> None:
        if self.canonical_effect != "NONE":
            raise ValueError("research decision must keep canonical_effect=NONE")
        if self.deployment:
            raise ValueError("research decision cannot enable deployment")
        if self.live_runtime_effect != "NONE":
            raise ValueError("research decision cannot create live runtime effect")

    def as_dict(self) -> dict[str, object]:
        return {
            "decision": self.decision.value,
            "reason": self.reason,
            "action_id": self.action_id,
            "source_type": self.source_type.value if self.source_type else None,
            "source_id": self.source_id,
            "considered_sources": list(self.considered_sources),
            "higher_priority_conflict": self.higher_priority_conflict,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
            "live_runtime_effect": self.live_runtime_effect,
        }
