from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from time import monotonic
from typing import Any, Mapping


class WholeSystemValidationError(ValueError):
    """Raised when the whole-system boundary receives invalid input."""


class WholeSystemStage(StrEnum):
    INPUT = "input"
    CONTEXT_INTAKE = "context_intake"
    IDENTITY_RESOLUTION = "identity_resolution"
    NAMESPACE_RESOLUTION = "namespace_resolution"
    MEMORY_RECALL = "memory_recall"
    PROVENANCE_VALIDATION = "provenance_validation"
    PLANNED = "planned"
    RISK_ASSESSED = "risk_assessed"
    TOOL_APPROVAL = "tool_approval"
    GENERATION = "generation"
    RESPONSE_BUILT = "response_built"
    WRITEBACK_DECIDED = "writeback_decided"
    MEMORY_INTENT = "memory_intent"
    MEMORY_UPDATED = "memory_updated"
    AUDIT = "audit"
    OUTPUT = "output"
    RECOVERY = "recovery"
    BLOCKED = "blocked"
    FAILED = "failed"


class WholeSystemStatus(StrEnum):
    COMPLETED = "COMPLETED"
    BLOCKED = "BLOCKED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    CANCELLED = "CANCELLED"
    RECOVERED = "RECOVERED"
    PENDING_RECONCILIATION = "PENDING_RECONCILIATION"


class ProvenanceStatus(StrEnum):
    CLAIMED = "CLAIMED_PROVENANCE"
    VERIFIED = "VERIFIED_PROVENANCE"
    UNVERIFIED = "UNVERIFIED_PROVENANCE"


@dataclass(slots=True)
class CancellationToken:
    cancelled: bool = False

    def cancel(self) -> None:
        self.cancelled = True


@dataclass(frozen=True, slots=True)
class TrustedApprovalRecord:
    """An externally registered approval; request fields never create this record."""

    approval_id: str
    requester: str
    approver: str
    authority: str
    tool_name: str
    namespace: str
    scopes: frozenset[str]
    issued_at: float
    expires_at: float
    revoked: bool = False

    def valid_for(self, invocation: "ToolInvocation", now: float | None = None) -> bool:
        current = monotonic() if now is None else now
        return (
            not self.revoked
            and self.approval_id == invocation.approval_id
            and self.requester == invocation.requester
            and self.tool_name == invocation.name
            and self.namespace == invocation.namespace
            and invocation.scopes.issubset(self.scopes)
            and invocation.approval_scope.issubset(self.scopes)
            and self.approver != invocation.requester
            and bool(self.authority.strip())
            and self.issued_at <= current < self.expires_at
        )


@dataclass(frozen=True, slots=True)
class TrustedProvenanceRecord:
    """Evidence registered independently of a requester's boolean claim."""

    record_id: str
    source_id: str
    source_kind: str
    source_locator: str
    source_digest: str | None
    branch_id: str
    authority: str
    valid: bool = True


@dataclass(frozen=True, slots=True)
class MemoryContext:
    """A bounded, authorized representation passed to Language Core."""

    memory_id: str
    content: str
    namespace: str
    authority: str
    confidence: float
    revision: int
    timestamp: str
    provenance_source: str
    provenance_status: ProvenanceStatus
    supersession_status: str

    def __post_init__(self) -> None:
        if not self.memory_id.strip() or not self.namespace.strip():
            raise WholeSystemValidationError("memory context identity is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise WholeSystemValidationError("memory context confidence must be in [0, 1]")
        if self.revision < 1:
            raise WholeSystemValidationError("memory context revision must be positive")


@dataclass(frozen=True, slots=True)
class ToolInvocation:
    call_id: str
    name: str
    arguments: Mapping[str, Any]
    requester: str
    namespace: str
    scopes: frozenset[str] = frozenset()
    # Retained only as an untrusted claim for regression tests. Runtime ignores it.
    approved: bool = False
    approval_id: str = ""
    approval_scope: frozenset[str] = frozenset()
    timeout_ms: int = 5_000

    def __post_init__(self) -> None:
        required = {
            "call_id": self.call_id,
            "name": self.name,
            "requester": self.requester,
            "namespace": self.namespace,
        }
        blank = [key for key, value in required.items() if not value.strip()]
        if blank:
            raise WholeSystemValidationError(f"blank tool invocation fields: {', '.join(blank)}")
        if self.timeout_ms < 1:
            raise WholeSystemValidationError("tool timeout_ms must be positive")


@dataclass(frozen=True, slots=True)
class WholeSystemRequest:
    run_id: str
    user_id: str
    agent_id: str
    namespace: str
    prompt: str
    requester_scopes: frozenset[str] = frozenset()
    entity_cues: frozenset[str] = frozenset()
    topic_cues: frozenset[str] = frozenset()
    source_id: str = "whole-system-input"
    source_kind: str = "runtime_request"
    source_locator: str = "in-process"
    source_digest: str | None = None
    # These booleans are claims, not proof. Trusted registries are authoritative.
    provenance_verified: bool = False
    owner_approved: bool = False
    requests_writeback: bool = False
    writeback_memory_id: str | None = None
    writeback_authority: str = "CANDIDATE"
    writeback_confidence: float = 0.8
    tool_calls: tuple[ToolInvocation, ...] = ()
    timeout_ms: int = 5_000
    cancellation: CancellationToken | None = None

    def __post_init__(self) -> None:
        required = {
            "run_id": self.run_id,
            "user_id": self.user_id,
            "agent_id": self.agent_id,
            "namespace": self.namespace,
            "prompt": self.prompt,
            "source_id": self.source_id,
            "source_kind": self.source_kind,
            "source_locator": self.source_locator,
        }
        blank = [key for key, value in required.items() if not value.strip()]
        if blank:
            raise WholeSystemValidationError(f"blank request fields: {', '.join(blank)}")
        if self.timeout_ms < 1:
            raise WholeSystemValidationError("timeout_ms must be positive")
        if not 0.0 <= self.writeback_confidence <= 1.0:
            raise WholeSystemValidationError("writeback_confidence must be in [0, 1]")
        if self.requests_writeback and not self.writeback_memory_id:
            raise WholeSystemValidationError("writeback_memory_id is required when writeback is requested")

    def deadline(self) -> float:
        return monotonic() + (self.timeout_ms / 1000.0)


@dataclass(frozen=True, slots=True)
class WholeSystemEvent:
    event_id: str
    run_id: str
    sequence: int
    stage: WholeSystemStage
    status: WholeSystemStatus | str
    payload: Mapping[str, Any] = field(default_factory=dict)
    occurred_at: str = ""
    canonical_effect: str = "NONE"
    event_hash: str = ""

    def __post_init__(self) -> None:
        if not self.event_id.strip() or not self.run_id.strip():
            raise WholeSystemValidationError("event_id and run_id must be non-empty")
        if self.sequence < 1:
            raise WholeSystemValidationError("event sequence must be positive")
        if self.canonical_effect != "NONE":
            raise WholeSystemValidationError("whole-system events cannot create canonical effect")


@dataclass(frozen=True, slots=True)
class WholeSystemResponse:
    run_id: str
    status: WholeSystemStatus
    text: str = ""
    error_code: str | None = None
    error_detail: str | None = None
    recalled_memory_ids: tuple[str, ...] = ()
    authorized_memory_contexts: tuple[MemoryContext, ...] = ()
    writeback_allowed: bool = False
    writeback_memory_id: str | None = None
    pending_transaction_id: str | None = None
    events: tuple[WholeSystemEvent, ...] = ()
    provenance_record_id: str | None = None
    provenance_status: ProvenanceStatus = ProvenanceStatus.UNVERIFIED
    state_checkpoint_id: str | None = None
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.run_id.strip():
            raise WholeSystemValidationError("response run_id must be non-empty")
        if self.canonical_effect != "NONE" or self.deployment:
            raise WholeSystemValidationError("whole-system response cannot promote or deploy")


@dataclass(frozen=True, slots=True)
class RecoveryRecord:
    run_id: str
    last_sequence: int
    checkpoint_id: str | None
    state: Mapping[str, Any]
    chain_valid: bool
    events: tuple[WholeSystemEvent, ...]
