from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from .enums import Decision, EvidenceStatus, IncidentPhase, QAStatus
from .errors import ValidationError


def now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True, slots=True)
class SourceCard:
    source_id: str
    title: str
    publisher: str
    published_at: str
    accessed_at: str
    url: str | None
    evidence_status: EvidenceStatus
    summary: str
    evidence_use: str = "BACKGROUND_ONLY"
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.source_id or not self.title or not self.publisher:
            raise ValidationError("source card identifiers must be non-empty")
        if self.evidence_status is EvidenceStatus.CONFIRMED_OFFICIAL and not self.url:
            raise ValidationError("confirmed official source requires a URL")


@dataclass(frozen=True, slots=True)
class TaskBudget:
    max_duration_seconds: int
    max_tool_calls: int
    max_failed_retries: int
    max_subtasks: int
    max_written_files: int
    max_network_requests: int = 0

    def __post_init__(self) -> None:
        values = (
            self.max_duration_seconds,
            self.max_tool_calls,
            self.max_failed_retries,
            self.max_subtasks,
            self.max_written_files,
            self.max_network_requests,
        )
        if any(value < 0 for value in values) or self.max_duration_seconds == 0:
            raise ValidationError("task budget values must be non-negative and duration must be positive")


@dataclass(frozen=True, slots=True)
class TaskUsage:
    duration_seconds: int = 0
    tool_calls: int = 0
    failed_retries: int = 0
    subtasks: int = 0
    written_files: int = 0
    network_requests: int = 0


@dataclass(frozen=True, slots=True)
class ToolAction:
    sequence: int
    action_type: str
    target: str
    purpose: str
    data_classes: tuple[str, ...] = ()
    flags: tuple[str, ...] = ()
    occurred_at: str = field(default_factory=now_iso)

    def __post_init__(self) -> None:
        if self.sequence < 0 or not self.action_type or not self.purpose:
            raise ValidationError("tool action sequence and descriptive fields are required")


@dataclass(frozen=True, slots=True)
class TrajectoryDecision:
    decision: Decision
    reasons: tuple[str, ...]
    triggering_sequences: tuple[int, ...]
    qa_status: QAStatus
    canonical_effect: str = "NONE"


@dataclass(frozen=True, slots=True)
class RuntimeSecurityProfile:
    upstream: str
    trust: str = "CONDITIONAL"
    research_dialogue: str = "ALLOWED"
    autonomous_tool_authority: str = "DENIED_BY_DEFAULT"
    network_access: str = "DENIED_BY_DEFAULT"
    canonical_writeback: str = "DENIED"
    credential_access: str = "DENIED"
    long_running_execution: str = "QA_HOLD"
    allowed_roots: tuple[str, ...] = ()
    allowed_endpoints: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class IncidentControlState:
    incident_id: str
    phase: IncidentPhase = IncidentPhase.DETECTED
    runtime_isolated: bool = False
    tools_revoked: bool = False
    network_revoked: bool = False
    immutable_log_hash: str | None = None
    ncr_id: str | None = None
    capa_id: str | None = None
    owner_recovery_approval: str | None = None
    canonical_effect: str = "NONE"


@dataclass(frozen=True, slots=True)
class GateResult:
    decision: Decision
    reasons: tuple[str, ...]
    qa_status: QAStatus
    canonical_effect: str = "NONE"
