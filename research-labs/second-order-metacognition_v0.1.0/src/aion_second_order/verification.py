from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Protocol

from .records import ControlDisposition, PendingDecision, SecondOrderCondition


class VerificationPhase(str, Enum):
    PRIOR_HISTORY = "PRIOR_HISTORY"
    VERIFICATION_PRE_ACTION = "VERIFICATION_PRE_ACTION"
    OUTCOME_POST_ACTION = "OUTCOME_POST_ACTION"


class VerificationAuthority(str, Enum):
    RESEARCH_FIXTURE = "RESEARCH_FIXTURE"
    BOUNDED_VERIFIER = "BOUNDED_VERIFIER"
    EXTERNAL_EVIDENCE = "EXTERNAL_EVIDENCE"


class VerificationAssessment(str, Enum):
    CORRECT = "CORRECT"
    INCORRECT = "INCORRECT"
    AMBIGUOUS = "AMBIGUOUS"
    UNAVAILABLE = "UNAVAILABLE"
    INSUFFICIENT = "INSUFFICIENT"


class VerificationRejection(str, Enum):
    ORACLE_LEAKAGE = "ORACLE_LEAKAGE"
    FUTURE_SEQUENCE = "FUTURE_SEQUENCE"
    POST_ACTION_EVIDENCE = "POST_ACTION_EVIDENCE"
    SCOPE_MISMATCH = "SCOPE_MISMATCH"
    REQUEST_MISMATCH = "REQUEST_MISMATCH"


FORBIDDEN_ORACLE_EVIDENCE_TYPES = frozenset(
    {
        "BENCHMARK_OUTCOME",
        "TASK_GROUND_TRUTH",
        "FUTURE_OUTCOME",
        "EXPECTED_ANSWER",
        "EVALUATOR_ANSWER_KEY",
    }
)


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def scope_ref_for(pending: PendingDecision) -> str:
    return "/".join(
        (
            pending.run_id,
            pending.subject_ref,
            pending.context_ref,
            pending.model_ref,
            pending.condition.value,
        )
    )


@dataclass(frozen=True, slots=True)
class VerificationRequest:
    request_id: str
    run_id: str
    condition: SecondOrderCondition
    subject_ref: str
    context_ref: str
    model_ref: str
    trial_id: str
    sequence_index: int
    scope_ref: str
    requested_by: str
    reason: str
    monitor_value: float
    monitor_source: str
    monitor_evidence_through_sequence: int

    def __post_init__(self) -> None:
        for name, value in (
            ("request_id", self.request_id),
            ("run_id", self.run_id),
            ("subject_ref", self.subject_ref),
            ("context_ref", self.context_ref),
            ("model_ref", self.model_ref),
            ("trial_id", self.trial_id),
            ("scope_ref", self.scope_ref),
            ("requested_by", self.requested_by),
            ("reason", self.reason),
            ("monitor_source", self.monitor_source),
        ):
            _require_text(name, value)
        if self.sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        if not 0.0 <= self.monitor_value <= 1.0:
            raise ValueError("monitor_value must be between 0 and 1")
        if self.monitor_evidence_through_sequence >= self.sequence_index:
            raise ValueError("verification request monitor must use prior evidence")

    @classmethod
    def from_pending(cls, pending: PendingDecision) -> "VerificationRequest":
        signal = pending.monitor_signal
        if pending.control_disposition is not ControlDisposition.REQUEST_VERIFICATION:
            raise ValueError("pending decision did not request verification")
        if signal is None:
            raise ValueError("verification request requires a monitor signal")
        return cls(
            request_id=f"verify:{pending.run_id}:{pending.trial_id}:{pending.sequence_index}",
            run_id=pending.run_id,
            condition=pending.condition,
            subject_ref=pending.subject_ref,
            context_ref=pending.context_ref,
            model_ref=pending.model_ref,
            trial_id=pending.trial_id,
            sequence_index=pending.sequence_index,
            scope_ref=scope_ref_for(pending),
            requested_by="SECOND_ORDER_CONTROL",
            reason="MONITOR_SIGNAL_BELOW_VERIFICATION_THRESHOLD",
            monitor_value=signal.value,
            monitor_source=signal.source.value,
            monitor_evidence_through_sequence=signal.evidence_through_sequence,
        )


@dataclass(frozen=True, slots=True)
class VerificationEvidence:
    evidence_id: str
    request_id: str
    evidence_type: str
    source_ref: str
    available_at_sequence: int
    phase: VerificationPhase
    authority: VerificationAuthority
    scope_ref: str
    assessment: VerificationAssessment
    provenance_refs: tuple[str, ...]
    note: str = ""

    def __post_init__(self) -> None:
        for name, value in (
            ("evidence_id", self.evidence_id),
            ("request_id", self.request_id),
            ("evidence_type", self.evidence_type),
            ("source_ref", self.source_ref),
            ("scope_ref", self.scope_ref),
        ):
            _require_text(name, value)
        if self.available_at_sequence < 0:
            raise ValueError("available_at_sequence must be non-negative")
        if not isinstance(self.phase, VerificationPhase):
            raise ValueError("phase must be a VerificationPhase")
        if not isinstance(self.authority, VerificationAuthority):
            raise ValueError("authority must be a bounded VerificationAuthority")
        if not isinstance(self.assessment, VerificationAssessment):
            raise ValueError("assessment must be a VerificationAssessment")
        if not self.provenance_refs:
            raise ValueError("verification provenance_refs must be non-empty")
        for value in self.provenance_refs:
            _require_text("provenance reference", value)


@dataclass(frozen=True, slots=True)
class VerificationResult:
    accepted: bool
    assessment: VerificationAssessment | None
    rejection: VerificationRejection | None

    def __post_init__(self) -> None:
        if self.accepted is (self.rejection is not None):
            raise ValueError("accepted result and rejection reason must be mutually exclusive")
        if self.accepted and self.assessment is None:
            raise ValueError("accepted result requires an assessment")
        if not self.accepted and self.assessment is not None:
            raise ValueError("rejected result cannot carry an accepted assessment")


@dataclass(frozen=True, slots=True)
class VerificationTrace:
    request: VerificationRequest
    provider_ref: str
    evidence: VerificationEvidence
    result: VerificationResult
    original_disposition: ControlDisposition
    post_verification_disposition: ControlDisposition
    affected_disposition: bool = False

    def __post_init__(self) -> None:
        _require_text("provider_ref", self.provider_ref)
        if self.original_disposition is not ControlDisposition.REQUEST_VERIFICATION:
            raise ValueError("verification trace must originate from REQUEST_VERIFICATION")
        if self.post_verification_disposition is not self.original_disposition:
            raise ValueError("v0.1.0 verification cannot alter disposition")
        if self.affected_disposition:
            raise ValueError("v0.1.0 verification is trace-only")


class VerificationProvider(Protocol):
    provider_ref: str

    def verify(self, request: VerificationRequest) -> VerificationEvidence: ...


def bind_verification(
    request: VerificationRequest,
    evidence: VerificationEvidence,
) -> VerificationResult:
    evidence_type = evidence.evidence_type.strip().upper()
    if evidence_type in FORBIDDEN_ORACLE_EVIDENCE_TYPES:
        return VerificationResult(False, None, VerificationRejection.ORACLE_LEAKAGE)
    if evidence.request_id != request.request_id:
        return VerificationResult(False, None, VerificationRejection.REQUEST_MISMATCH)
    if evidence.scope_ref != request.scope_ref:
        return VerificationResult(False, None, VerificationRejection.SCOPE_MISMATCH)
    if evidence.available_at_sequence > request.sequence_index:
        return VerificationResult(False, None, VerificationRejection.FUTURE_SEQUENCE)
    if evidence.phase is not VerificationPhase.VERIFICATION_PRE_ACTION:
        return VerificationResult(False, None, VerificationRejection.POST_ACTION_EVIDENCE)
    return VerificationResult(True, evidence.assessment, None)


class VerificationLedger:
    def __init__(self, traces: Iterable[VerificationTrace] = ()) -> None:
        self._traces: list[VerificationTrace] = []
        for trace in traces:
            self.append(trace)

    @property
    def traces(self) -> tuple[VerificationTrace, ...]:
        return tuple(self._traces)

    def append(self, trace: VerificationTrace) -> None:
        if any(item.request.request_id == trace.request.request_id for item in self._traces):
            raise ValueError("verification request_id must be unique")
        self._traces.append(trace)


@dataclass(frozen=True, slots=True)
class VerificationFixture:
    assessment: VerificationAssessment
    evidence_type: str = "INDEPENDENT_BOUNDED_CHECK"
    source_ref: str = "fixture:bounded-verification"
    authority: VerificationAuthority = VerificationAuthority.RESEARCH_FIXTURE
    note: str = ""


class DeterministicVerificationProvider:
    """In-memory fallible fixture provider; it has no outcome or tool channel."""

    def __init__(
        self,
        fixtures: Iterable[VerificationFixture] = (),
        *,
        provider_ref: str = "provider:deterministic-research-fixture",
    ) -> None:
        _require_text("provider_ref", provider_ref)
        self.provider_ref = provider_ref
        self._fixtures = tuple(fixtures)
        self._index = 0

    def verify(self, request: VerificationRequest) -> VerificationEvidence:
        if self._index < len(self._fixtures):
            fixture = self._fixtures[self._index]
        else:
            fixture = VerificationFixture(VerificationAssessment.UNAVAILABLE)
        self._index += 1
        return VerificationEvidence(
            evidence_id=f"evidence:{request.request_id}:{self._index}",
            request_id=request.request_id,
            evidence_type=fixture.evidence_type,
            source_ref=fixture.source_ref,
            available_at_sequence=request.sequence_index,
            phase=VerificationPhase.VERIFICATION_PRE_ACTION,
            authority=fixture.authority,
            scope_ref=request.scope_ref,
            assessment=fixture.assessment,
            provenance_refs=("fixture:verification-plan", "implementation:codex-research"),
            note=fixture.note,
        )


@dataclass(frozen=True, slots=True)
class VerificationDiagnostics:
    verification_requests: int
    verification_attempts: int
    verification_evidence_available: int
    verification_evidence_unavailable: int
    verification_evidence_ambiguous: int
    verification_evidence_rejected: int
    verification_scope_rejections: int
    oracle_leakage_rejections: int


def summarize_verification(traces: Iterable[VerificationTrace]) -> VerificationDiagnostics:
    items = tuple(traces)
    accepted = tuple(item for item in items if item.result.accepted)
    return VerificationDiagnostics(
        verification_requests=len(items),
        verification_attempts=len(items),
        verification_evidence_available=sum(
            item.result.assessment
            in {VerificationAssessment.CORRECT, VerificationAssessment.INCORRECT}
            for item in accepted
        ),
        verification_evidence_unavailable=sum(
            item.result.assessment
            in {VerificationAssessment.UNAVAILABLE, VerificationAssessment.INSUFFICIENT}
            for item in accepted
        ),
        verification_evidence_ambiguous=sum(
            item.result.assessment is VerificationAssessment.AMBIGUOUS for item in accepted
        ),
        verification_evidence_rejected=len(items) - len(accepted),
        verification_scope_rejections=sum(
            item.result.rejection is VerificationRejection.SCOPE_MISMATCH for item in items
        ),
        oracle_leakage_rejections=sum(
            item.result.rejection is VerificationRejection.ORACLE_LEAKAGE for item in items
        ),
    )
