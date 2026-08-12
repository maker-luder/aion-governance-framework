from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

NONE: Final[str] = "NONE"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_refs(name: str, values: tuple[str, ...]) -> None:
    if not values or any(not value.strip() for value in values):
        raise ValueError(f"{name} must contain non-empty references")


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


class AuthorizationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    REVOKED = "REVOKED"


class GateDecision(str, Enum):
    PROCEED = "PROCEED"
    QUARANTINE = "QUARANTINE"
    REJECT = "REJECT"


class HandoffPhase(str, Enum):
    REQUESTED = "REQUESTED"
    AUTHORIZED = "AUTHORIZED"
    PREPARED = "PREPARED"
    TRANSFERRED = "TRANSFERRED"
    VERIFIED = "VERIFIED"
    COMMITTED = "COMMITTED"
    QUARANTINED = "QUARANTINED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"


TERMINAL_PHASES: Final[frozenset[HandoffPhase]] = frozenset(
    {
        HandoffPhase.COMMITTED,
        HandoffPhase.QUARANTINED,
        HandoffPhase.REJECTED,
        HandoffPhase.FAILED,
        HandoffPhase.ROLLED_BACK,
    }
)


@dataclass(frozen=True, slots=True)
class HandoffRequest:
    request_id: str
    requesting_actor: str
    actual_actor: str
    authorizing_party: str
    agent_id: str
    source_embodiment_id: str
    target_embodiment_id: str
    authorization_status: AuthorizationStatus
    authorization_evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    reason: str
    canonical_effect: str = NONE
    identity_change_claim: str = NOT_ESTABLISHED
    continuity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in (
            "request_id",
            "requesting_actor",
            "actual_actor",
            "authorizing_party",
            "agent_id",
            "source_embodiment_id",
            "target_embodiment_id",
            "reason",
        ):
            _require_text(name, getattr(self, name))
        _require_refs("provenance_refs", self.provenance_refs)
        if self.authorization_status is AuthorizationStatus.VERIFIED:
            _require_refs("authorization_evidence_refs", self.authorization_evidence_refs)
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")
        if self.identity_change_claim != NOT_ESTABLISHED:
            raise ValueError("identity change must remain NOT_ESTABLISHED")
        if self.continuity_claim != NOT_ESTABLISHED:
            raise ValueError("continuity must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class CompatibilityMeasurement:
    measurement_id: str
    metric_name: str
    score: float
    threshold: float
    method_ref: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        for name in ("measurement_id", "metric_name", "method_ref"):
            _require_text(name, getattr(self, name))
        _require_unit_interval("score", self.score)
        _require_unit_interval("threshold", self.threshold)
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")

    @property
    def passed(self) -> bool:
        return self.score >= self.threshold


@dataclass(frozen=True, slots=True)
class TransferArtifact:
    artifact_id: str
    artifact_kind: str
    source_ref: str
    target_ref: str
    integrity_ref: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        for name in ("artifact_id", "artifact_kind", "source_ref", "target_ref", "integrity_ref"):
            _require_text(name, getattr(self, name))
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")


@dataclass(frozen=True, slots=True)
class VerificationResult:
    verification_id: str
    check_name: str
    passed: bool
    method_ref: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE
    identity_continuity_claim: str = NOT_ESTABLISHED
    subjectivity_preservation_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("verification_id", "check_name", "method_ref"):
            _require_text(name, getattr(self, name))
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")
        if self.identity_continuity_claim != NOT_ESTABLISHED:
            raise ValueError("identity continuity must remain NOT_ESTABLISHED")
        if self.subjectivity_preservation_claim != NOT_ESTABLISHED:
            raise ValueError("subjectivity preservation must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class HandoffTransition:
    transition_id: str
    from_phase: HandoffPhase
    to_phase: HandoffPhase
    timestamp: str
    reason: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        for name in ("transition_id", "timestamp", "reason"):
            _require_text(name, getattr(self, name))
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")


@dataclass(frozen=True, slots=True)
class HandoffRecord:
    record_id: str
    request: HandoffRequest
    current_phase: HandoffPhase
    compatibility_measurements: tuple[CompatibilityMeasurement, ...] = field(default_factory=tuple)
    transfer_artifacts: tuple[TransferArtifact, ...] = field(default_factory=tuple)
    verification_results: tuple[VerificationResult, ...] = field(default_factory=tuple)
    transitions: tuple[HandoffTransition, ...] = field(default_factory=tuple)
    rollback_target_ref: str | None = None
    canonical_effect: str = NONE
    identity_continuity_claim: str = NOT_ESTABLISHED
    personal_identity_claim: str = NOT_ESTABLISHED
    subjectivity_preservation_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        _require_text("record_id", self.record_id)
        for name, items, attr in (
            ("compatibility_measurement", self.compatibility_measurements, "measurement_id"),
            ("transfer_artifact", self.transfer_artifacts, "artifact_id"),
            ("verification_result", self.verification_results, "verification_id"),
            ("transition", self.transitions, "transition_id"),
        ):
            ids = [getattr(item, attr) for item in items]
            if len(ids) != len(set(ids)):
                raise ValueError(f"{name} ids must be unique")
        if self.rollback_target_ref is not None:
            _require_text("rollback_target_ref", self.rollback_target_ref)
        if self.canonical_effect != NONE:
            raise ValueError("canonical_effect must remain NONE")
        if self.identity_continuity_claim != NOT_ESTABLISHED:
            raise ValueError("identity continuity must remain NOT_ESTABLISHED")
        if self.personal_identity_claim != NOT_ESTABLISHED:
            raise ValueError("personal identity must remain NOT_ESTABLISHED")
        if self.subjectivity_preservation_claim != NOT_ESTABLISHED:
            raise ValueError("subjectivity preservation must remain NOT_ESTABLISHED")

    @property
    def is_terminal(self) -> bool:
        return self.current_phase in TERMINAL_PHASES

    @property
    def compatibility_passed(self) -> bool:
        return bool(self.compatibility_measurements) and all(
            measurement.passed for measurement in self.compatibility_measurements
        )

    @property
    def verification_passed(self) -> bool:
        return bool(self.verification_results) and all(
            result.passed for result in self.verification_results
        )
