from __future__ import annotations

import json
import math
from dataclasses import dataclass
from enum import Enum
from hashlib import sha256
from typing import Any, Iterable, Protocol

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


class VerificationTargetKind(str, Enum):
    FIRST_ORDER_PREDICTION = "FIRST_ORDER_PREDICTION"


class VerificationEvidenceType(str, Enum):
    INDEPENDENT_BOUNDED_CHECK = "INDEPENDENT_BOUNDED_CHECK"
    SYNTHETIC_RESEARCH_CHECK = "SYNTHETIC_RESEARCH_CHECK"


class VerificationRejection(str, Enum):
    ORACLE_LEAKAGE = "ORACLE_LEAKAGE"
    UNRECOGNIZED_EVIDENCE_TYPE = "UNRECOGNIZED_EVIDENCE_TYPE"
    FUTURE_SEQUENCE = "FUTURE_SEQUENCE"
    POST_ACTION_EVIDENCE = "POST_ACTION_EVIDENCE"
    SCOPE_MISMATCH = "SCOPE_MISMATCH"
    REQUEST_MISMATCH = "REQUEST_MISMATCH"
    TARGET_MISMATCH = "TARGET_MISMATCH"
    TRIAL_MISMATCH = "TRIAL_MISMATCH"


class VerificationInterventionCondition(str, Enum):
    TRACE_ONLY = "VERIFICATION_TRACE_ONLY"
    APPLIED = "VERIFICATION_APPLIED"
    ABLATED = "VERIFICATION_ABLATED"
    RANDOMIZED = "VERIFICATION_RANDOMIZED"


class InterventionPolicyKind(str, Enum):
    CONSERVATIVE_DEFER = "CONSERVATIVE_DEFER"
    TRACE_ONLY = "TRACE_ONLY"
    ACCEPT_UNLESS_NEGATIVE = "ACCEPT_UNLESS_NEGATIVE"


@dataclass(frozen=True, slots=True)
class InterventionPolicy:
    kind: InterventionPolicyKind
    policy_ref: str
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_text("policy_ref", self.policy_ref)
        if not self.provenance_refs or any(not item.strip() for item in self.provenance_refs):
            raise ValueError("policy provenance_refs must be non-empty")

    def disposition(
        self,
        result: "VerificationResult",
        original: ControlDisposition,
    ) -> ControlDisposition:
        if self.kind is InterventionPolicyKind.TRACE_ONLY:
            return original
        if self.kind is InterventionPolicyKind.CONSERVATIVE_DEFER:
            return (
                ControlDisposition.ACCEPT_FIRST_ORDER
                if result.accepted and result.assessment is VerificationAssessment.CORRECT
                else ControlDisposition.DEFER
            )
        if not result.accepted or result.assessment is VerificationAssessment.INCORRECT:
            return ControlDisposition.DEFER
        if result.assessment is VerificationAssessment.CORRECT:
            return ControlDisposition.ACCEPT_FIRST_ORDER
        return original


def default_intervention_policy(
    kind: InterventionPolicyKind = InterventionPolicyKind.CONSERVATIVE_DEFER,
) -> InterventionPolicy:
    return InterventionPolicy(
        kind=kind,
        policy_ref=f"policy:research:{kind.value.lower()}:v0.1.x",
        provenance_refs=(
            "research:chatgpt-intervention-policy-matrix",
            "implementation:codex-research",
        ),
    )


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
class VerificationTarget:
    kind: VerificationTargetKind
    target_ref: str
    trial_id: str
    target_snapshot: bool

    def __post_init__(self) -> None:
        if self.kind is not VerificationTargetKind.FIRST_ORDER_PREDICTION:
            raise ValueError("v0.1.x only supports FIRST_ORDER_PREDICTION")
        _require_text("target_ref", self.target_ref)
        _require_text("trial_id", self.trial_id)
        if not isinstance(self.target_snapshot, bool):
            raise ValueError("target_snapshot must preserve the boolean first-order prediction")

    @classmethod
    def from_pending(cls, pending: PendingDecision) -> "VerificationTarget":
        return cls(
            kind=VerificationTargetKind.FIRST_ORDER_PREDICTION,
            target_ref=f"first-order-prediction:{pending.run_id}:{pending.trial_id}",
            trial_id=pending.trial_id,
            target_snapshot=pending.first_order_prediction,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "target_ref": self.target_ref,
            "trial_id": self.trial_id,
            "target_snapshot": self.target_snapshot,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VerificationTarget":
        return cls(
            kind=VerificationTargetKind(data["kind"]),
            target_ref=str(data["target_ref"]),
            trial_id=str(data["trial_id"]),
            target_snapshot=data["target_snapshot"],
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
    target: VerificationTarget
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
        if self.target.trial_id != self.trial_id:
            raise ValueError("verification target trial_id must match request trial_id")
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
            target=VerificationTarget.from_pending(pending),
            requested_by="SECOND_ORDER_CONTROL",
            reason="MONITOR_SIGNAL_BELOW_VERIFICATION_THRESHOLD",
            monitor_value=signal.value,
            monitor_source=signal.source.value,
            monitor_evidence_through_sequence=signal.evidence_through_sequence,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "run_id": self.run_id,
            "condition": self.condition.value,
            "subject_ref": self.subject_ref,
            "context_ref": self.context_ref,
            "model_ref": self.model_ref,
            "trial_id": self.trial_id,
            "sequence_index": self.sequence_index,
            "scope_ref": self.scope_ref,
            "target": self.target.to_dict(),
            "requested_by": self.requested_by,
            "reason": self.reason,
            "monitor_value": self.monitor_value,
            "monitor_source": self.monitor_source,
            "monitor_evidence_through_sequence": self.monitor_evidence_through_sequence,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VerificationRequest":
        return cls(
            request_id=str(data["request_id"]),
            run_id=str(data["run_id"]),
            condition=SecondOrderCondition(data["condition"]),
            subject_ref=str(data["subject_ref"]),
            context_ref=str(data["context_ref"]),
            model_ref=str(data["model_ref"]),
            trial_id=str(data["trial_id"]),
            sequence_index=int(data["sequence_index"]),
            scope_ref=str(data["scope_ref"]),
            target=VerificationTarget.from_dict(data["target"]),
            requested_by=str(data["requested_by"]),
            reason=str(data["reason"]),
            monitor_value=float(data["monitor_value"]),
            monitor_source=str(data["monitor_source"]),
            monitor_evidence_through_sequence=int(data["monitor_evidence_through_sequence"]),
        )


@dataclass(frozen=True, slots=True)
class VerificationEvidence:
    evidence_id: str
    request_id: str
    evidence_type: VerificationEvidenceType | str
    source_ref: str
    available_at_sequence: int
    phase: VerificationPhase
    authority: VerificationAuthority
    scope_ref: str
    target: VerificationTarget
    assessment: VerificationAssessment
    provenance_refs: tuple[str, ...]
    note: str = ""

    def __post_init__(self) -> None:
        for name, value in (
            ("evidence_id", self.evidence_id),
            ("request_id", self.request_id),
            ("source_ref", self.source_ref),
            ("scope_ref", self.scope_ref),
        ):
            _require_text(name, value)
        if isinstance(self.evidence_type, str) and not isinstance(
            self.evidence_type, VerificationEvidenceType
        ):
            _require_text("evidence_type", self.evidence_type)
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

    def to_dict(self) -> dict[str, Any]:
        typed = isinstance(self.evidence_type, VerificationEvidenceType)
        return {
            "evidence_id": self.evidence_id,
            "request_id": self.request_id,
            "evidence_type": self.evidence_type.value if typed else self.evidence_type,
            "evidence_type_typed": typed,
            "source_ref": self.source_ref,
            "available_at_sequence": self.available_at_sequence,
            "phase": self.phase.value,
            "authority": self.authority.value,
            "scope_ref": self.scope_ref,
            "target": self.target.to_dict(),
            "assessment": self.assessment.value,
            "provenance_refs": list(self.provenance_refs),
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VerificationEvidence":
        evidence_type: VerificationEvidenceType | str = str(data["evidence_type"])
        if data["evidence_type_typed"]:
            evidence_type = VerificationEvidenceType(evidence_type)
        return cls(
            evidence_id=str(data["evidence_id"]),
            request_id=str(data["request_id"]),
            evidence_type=evidence_type,
            source_ref=str(data["source_ref"]),
            available_at_sequence=int(data["available_at_sequence"]),
            phase=VerificationPhase(data["phase"]),
            authority=VerificationAuthority(data["authority"]),
            scope_ref=str(data["scope_ref"]),
            target=VerificationTarget.from_dict(data["target"]),
            assessment=VerificationAssessment(data["assessment"]),
            provenance_refs=tuple(data["provenance_refs"]),
            note=str(data["note"]),
        )


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

    def to_dict(self) -> dict[str, Any]:
        return {
            "accepted": self.accepted,
            "assessment": None if self.assessment is None else self.assessment.value,
            "rejection": None if self.rejection is None else self.rejection.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "VerificationResult":
        return cls(
            accepted=bool(data["accepted"]),
            assessment=None
            if data["assessment"] is None
            else VerificationAssessment(data["assessment"]),
            rejection=None
            if data["rejection"] is None
            else VerificationRejection(data["rejection"]),
        )


@dataclass(frozen=True, slots=True)
class VerificationTrace:
    request: VerificationRequest
    provider_ref: str
    evidence: VerificationEvidence
    result: VerificationResult
    original_disposition: ControlDisposition
    post_verification_disposit×Ýù¶‰žËkºwµçI¥™¥…Ñ¥½¹}‘¥ÍÁ½Í¥Ñ¥½¸è½¹ÑÉ½±¥ÍÁ½Í¥Ñ¥½¸(€€€…™™•Ñ•‘}‘¥ÍÁ½Í¥Ñ¥½¸è‰½½°(€€€Á½±¥å}É•˜èÍÑÈ(€€€É•…Í½¸èÍÑÈ(€€€ÁÉ½Ù•¹…¹•}É•™ÌèÑÕÁ±•mÍÑÈ°€¸¸¹t(€€€É…¹‘½µ}Í••è¥¹Ðð9½¹”€ô9½¹”(€€€É…¹‘½µ¥é•‘}Í½ÕÉ”èÍÑÈð9½¹”€ô9½¹”(€€€ÉÕ¹}É•˜èÍÑÈ€ô€ˆˆ(€€€ÑÉ¥…±}É•˜èÍÑÈ€ô€ˆˆ(€€€Á½±¥å}­¥¹è%¹Ñ•ÉÙ•¹Ñ¥½¹A½±¥å-¥¹€ô%¹Ñ•ÉÙ•¹Ñ¥½¹A½±¥å-¥¹¹=9MIYQ%Y}H(€€€…¹½¹¥…±}•™™•ÐèÍÑÈ€ô€‰9=9ˆ(€€€ÉÕ¹Ñ¥µ•}•™™•ÐèÍÑÈ€ô€‰9=9ˆ((€€€‘•˜}}Á½ÍÑ}¥¹¥Ñ}|¡Í•±˜¤€´ø9½¹”è(€€€€€€€™½È¹…µ”°Ù…±Õ”¥¸€ (€€€€€€€€€€€€ ‰¥¹Ñ•ÉÙ•¹Ñ¥½¹}¥ˆ°Í•±˜¹¥¹Ñ•ÉÙ•¹Ñ¥½¹}¥¤°(€€€€€€€€€€€€ ‰É•ÅÕ•ÍÑ}¥ˆ°Í•±˜¹É•ÅÕ•ÍÑ}¥¤°(€€€€€€€€€€€€ ‰Á½±¥å}É•˜ˆ°Í•±˜¹Á½±¥å}É•˜¤°(€€€€€€€€€€€€ ‰É•…Í½¸ˆ°Í•±˜¹É•…Í½¸¤°(€€€€€€€€€€€€ ‰ÉÕ¹}É•˜ˆ°Í•±˜¹ÉÕ¹}É•˜¤°(€€€€€€€€€€€€ ‰ÑÉ¥…±}É•˜ˆ°Í•±˜¹ÑÉ¥…±}É•˜¤°(€€€€€€€€¤è(€€€€€€€€€€€}É•ÅÕ¥É•}Ñ•áÐ¡¹…µ”°Ù…±Õ”¤(€€€€€€€¥˜Í•±˜¹Ñ…É•Ð¹ÑÉ¥…±}¥€„ôÍ•±˜¹ÑÉ¥…±}É•˜è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰¥¹Ñ•ÉÙ•¹Ñ¥½¸Ñ…É•ÐÑÉ¥…±}¥µÕÍÐµ…Ñ ÑÉ¥…±}É•˜ˆ¤(€€€€€€€¥˜Í•±˜¹½É¥¥¹…±}‘¥ÍÁ½Í¥Ñ¥½¸¥Ì¹½Ð½¹ÑÉ½±¥ÍÁ½Í¥Ñ¥½¸¹IEUMQ}YI%%Q%=8è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰¥¹Ñ•ÉÙ•¹Ñ¥½¸µÕÍÐÁÉ•Í•ÉÙ”IEUMQ}YI%%Q%=8…Ì½É¥¥¸ˆ¤(€€€€€€€¥˜Í•±˜¹…™™•Ñ•‘}‘¥ÍÁ½Í¥Ñ¥½¸¥Ì€ (€€€€€€€€€€€Í•±˜¹Á½ÍÑ}Ù•É¥™¥…Ñ¥½¹}‘¥ÍÁ½Í¥Ñ¥½¸¥ÌÍ•±˜¹½É¥¥¹…±}‘¥ÍÁ½Í¥Ñ¥½¸(€€€€€€€€¤è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰…™™•Ñ•‘}‘¥ÍÁ½Í¥Ñ¥½¸µÕÍÐµ…Ñ ‘¥ÍÁ½Í¥Ñ¥½¸‘¥™™•É•¹”ˆ¤(€€€€€€€¥˜Í•±˜¹½¹‘¥Ñ¥½¸¥ÌY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹½¹‘¥Ñ¥½¸¹I9=5%iè(€€€€€€€€€€€¥˜Í•±˜¹É…¹‘½µ}Í••¥Ì9½¹”½È¹½ÐÍ•±˜¹É…¹‘½µ¥é•‘}Í½ÕÉ”è(€€€€€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰É…¹‘½µ¥é•¥¹Ñ•ÉÙ•¹Ñ¥½¸É•ÅÕ¥É•ÌÍ••…¹Í½ÕÉ”ˆ¤(€€€€€€€•±¥˜Í•±˜¹É…¹‘½µ}Í••¥Ì¹½Ð9½¹”½ÈÍ•±˜¹É…¹‘½µ¥é•‘}Í½ÕÉ”¥Ì¹½Ð9½¹”è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰½¹±äÉ…¹‘½µ¥é•¥¹Ñ•ÉÙ•¹Ñ¥½¸µ…ä…ÉÉäÉ…¹‘½µ¥é…Ñ¥½¸µ•Ñ…‘…Ñ„ˆ¤(€€€€€€€¥˜¹½ÐÍ•±˜¹ÁÉ½Ù•¹…¹•}É•™Ì½È…¹ä¡¹½Ð¥Ñ•´¹ÍÑÉ¥À ¤™½È¥Ñ•´¥¸Í•±˜¹ÁÉ½Ù•¹…¹•}É•™Ì¤è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰¥¹Ñ•ÉÙ•¹Ñ¥½¸ÁÉ½Ù•¹…¹•}É•™ÌµÕÍÐ‰”¹½¸µ•µÁÑäˆ¤(€€€€€€€¥˜Í•±˜¹…¹½¹¥…±}•™™•Ð€„ô€‰9=9ˆ½ÈÍ•±˜¹ÉÕ¹Ñ¥µ•}•™™•Ð€„ô€‰9=9ˆè(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰É•Í•…É ¥¹Ñ•ÉÙ•¹Ñ¥½¸•™™•ÑÌµÕÍÐÉ•µ…¥¸9=9ˆ¤((€€€‘•˜Ñ½}‘¥Ð¡Í•±˜¤€´ø‘¥ÑmÍÑÈ°¹åtè(€€€€€€€É•ÑÕÉ¸ì(€€€€€€€€€€€€‰¥¹Ñ•ÉÙ•¹Ñ¥½¹}¥ˆèÍ•±˜¹¥¹Ñ•ÉÙ•¹Ñ¥½¹}¥°(€€€€€€€€€€€€‰½¹‘¥Ñ¥½¸ˆèÍ•±˜¹½¹‘¥Ñ¥½¸¹Ù…±Õ”°(€€€€€€€€€€€€‰É•ÅÕ•ÍÑ}¥ˆèÍ•±˜¹É•ÅÕ•ÍÑ}¥°(€€€€€€€€€€€€‰Ñ…É•ÐˆèÍ•±˜¹Ñ…É•Ð¹Ñ½}‘¥Ð ¤°(€€€€€€€€€€€€‰½É¥¥¹…±}‘¥ÍÁ½Í¥Ñ¥½¸ˆèÍ•±˜¹½É¥¥¹…±}‘¥ÍÁ½Í¥Ñ¥½¸¹Ù…±Õ”°(€€€€€€€€€€€€‰Á½ÍÑ}Ù•É¥™¥…Ñ¥½¹}‘¥ÍÁ½Í¥Ñ¥½¸ˆèÍ•±˜¹Á½ÍÑ}Ù•É¥™¥…Ñ¥½¹}‘¥ÍÁ½Í¥Ñ¥½¸¹Ù…±Õ”°(€€€€€€€€€€€€‰…™™•Ñ•‘}‘¥ÍÁ½Í¥Ñ¥½¸ˆèÍ•±˜¹…™™•Ñ•‘}‘¥ÍÁ½Í¥Ñ¥½¸°(€€€€€€€€€€€€‰Á½±¥å}É•˜ˆèÍ•±˜¹Á½±¥å}É•˜°(€€€€€€€€€€€€‰Á½±¥å}­¥¹ˆèÍ•±˜¹Á½±¥å}­¥¹¹Ù…±Õ”°(€€€€€€€€€€€€‰É•…Í½¸ˆèÍ•±˜¹É•…Í½¸°(€€€€€€€€€€€€‰ÁÉ½Ù•¹…¹•}É•™Ìˆè±¥ÍÐ¡Í•±˜¹ÁÉ½Ù•¹…¹•}É•™Ì¤°(€€€€€€€€€€€€‰É…¹‘½µ}Í••ˆèÍ•±˜¹É…¹‘½µ}Í••°(€€€€€€€€€€€€‰É…¹‘½µ¥é•‘}Í½ÕÉ”ˆèÍ•±˜¹É…¹‘½µ¥é•‘}Í½ÕÉ”°(€€€€€€€€€€€€‰ÉÕ¹}É•˜ˆèÍ•±˜¹ÉÕ¹}É•˜°(€€€€€€€€€€€€‰ÑÉ¥…±}É•˜ˆèÍ•±˜¹ÑÉ¥…±}É•˜°(€€€€€€€€€€€€‰…¹½¹¥…±}•™™•ÐˆèÍ•±˜¹…¹½¹¥…±}•™™•Ð°(€€€€€€€€€€€€‰ÉÕ¹Ñ¥µ•}•™™•ÐˆèÍ•±˜¹ÉÕ¹Ñ¥µ•}•™™•Ð°(€€€€€€€ô((€€€±…ÍÍµ•Ñ¡½(€€€‘•˜™É½µ}‘¥Ð¡±Ì°‘…Ñ„è‘¥ÑmÍÑÈ°¹åt¤€´ø€‰Y•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¸ˆè(€€€€€€€É•ÑÕÉ¸±Ì (€€€€€€€€€€€¥¹Ñ•ÉÙ•¹Ñ¥½¹}¥õÍÑÈ¡‘…Ñ…l‰¥¹Ñ•ÉÙ•¹Ñ¥½¹}¥‰t¤°(€€€€€€€€€€€½¹‘¥Ñ¥½¸õY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹½¹‘¥Ñ¥½¸¡‘…Ñ…l‰½¹‘¥Ñ¥½¸‰t¤°(€€€€€€€€€€€É•ÅÕ•ÍÑ}¥õÍÑÈ¡‘…Ñ…l‰É•ÅÕ•ÍÑ}¥‰t¤°(€€€€€€€€€€€Ñ…É•ÐõY•É¥™¥…Ñ¥½¹Q…É•Ð¹™É½µ}‘¥Ð¡‘…Ñ…l‰Ñ…É•Ð‰t¤°(€€€€€€€€€€€½É¥¥¹…±}‘¥ÍÁ½Í¥Ñ¥½¸õ½¹ÑÉ½±¥ÍÁ½Í¥Ñ¥½¸¡‘…Ñ…l‰½É¥¥¹…±}‘¥ÍÁ½Í¥Ñ¥½¸‰t¤°(€€€€€€€€€€€Á½ÍÑ}Ù•É¥™¥…Ñ¥½¹}‘¥ÍÁ½Í¥Ñ¥½¸õ½¹ÑÉ½±¥ÍÁ½Í¥Ñ¥½¸ (€€€€€€€€€€€€€€€‘…Ñ…l‰Á½ÍÑ}Ù•É¥™¥…Ñ¥½¹}‘¥ÍÁ½Í¥Ñ¥½¸‰t(€€€€€€€€€€€€¤°(€€€€€€€€€€€…™™•Ñ•‘}‘¥ÍÁ½Í¥Ñ¥½¸õ‰½½°¡‘…Ñ…l‰…™™•Ñ•‘}‘¥ÍÁ½Í¥Ñ¥½¸‰t¤°(€€€€€€€€€€€Á½±¥å}É•˜õÍÑÈ¡‘…Ñ…l‰Á½±¥å}É•˜‰t¤°(€€€€€€€€€€€Á½±¥å}­¥¹õ%¹Ñ•ÉÙ•¹Ñ¥½¹A½±¥å-¥¹¡‘…Ñ…l‰Á½±¥å}­¥¹‰t¤°(€€€€€€€€€€€É•…Í½¸õÍÑÈ¡‘…Ñ…l‰É•…Í½¸‰t¤°(€€€€€€€€€€€ÁÉ½Ù•¹…¹•}É•™ÌõÑÕÁ±”¡‘…Ñ…l‰ÁÉ½Ù•¹…¹•}É•™Ì‰t¤°(€€€€€€€€€€€É…¹‘½µ}Í••õ‘…Ñ…l‰É…¹‘½µ}Í••‰t°(€€€€€€€€€€€É…¹‘½µ¥é•‘}Í½ÕÉ”õ‘…Ñ…l‰É…¹‘½µ¥é•‘}Í½ÕÉ”‰t°(€€€€€€€€€€€ÉÕ¹}É•˜õÍÑÈ¡‘…Ñ…l‰ÉÕ¹}É•˜‰t¤°(€€€€€€€€€€€ÑÉ¥…±}É•˜õÍÑÈ¡‘…Ñ…l‰ÑÉ¥…±}É•˜‰t¤°(€€€€€€€€€€€…¹½¹¥…±}•™™•ÐõÍÑÈ¡‘…Ñ…l‰…¹½¹¥…±}•™™•Ð‰t¤°(€€€€€€€€€€€ÉÕ¹Ñ¥µ•}•™™•ÐõÍÑÈ¡‘…Ñ…l‰ÉÕ¹Ñ¥µ•}•™™•Ð‰t¤°(€€€€€€€€¤(()±…ÍÌY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹1•‘•Èè(€€€‘•˜}}¥¹¥Ñ}|¡Í•±˜°¥Ñ•µÌè%Ñ•É…‰±•mY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹t€ô€ ¤¤€´ø9½¹”è(€€€€€€€Í•±˜¹}¥Ñ•µÌè±¥ÍÑmY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹t€ômt(€€€€€€€™½È¥Ñ•´¥¸¥Ñ•µÌè(€€€€€€€€€€€Í•±˜¹…ÁÁ•¹¡¥Ñ•´¤((€€€ÁÉ½Á•ÉÑä(€€€‘•˜¥Ñ•µÌ¡Í•±˜¤€´øÑÕÁ±•mY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¸°€¸¸¹tè(€€€€€€€É•ÑÕÉ¸ÑÕÁ±”¡Í•±˜¹}¥Ñ•µÌ¤((€€€‘•˜…ÁÁ•¹¡Í•±˜°¥Ñ•´èY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¸¤€´ø9½¹”è(€€€€€€€¥˜…¹ä¡•á¥ÍÑ¥¹œ¹É•ÅÕ•ÍÑ}¥€ôô¥Ñ•´¹É•ÅÕ•ÍÑ}¥™½È•á¥ÍÑ¥¹œ¥¸Í•±˜¹}¥Ñ•µÌ¤è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰Ù•É¥™¥…Ñ¥½¸¥¹Ñ•ÉÙ•¹Ñ¥½¸É•ÅÕ•ÍÑ}¥µÕÍÐ‰”Õ¹¥ÅÕ”ˆ¤(€€€€€€€Í•±˜¹}¥Ñ•µÌ¹…ÁÁ•¹¡¥Ñ•´¤((€€€‘•˜Ñ½}‘¥Ð¡Í•±˜¤€´ø‘¥ÑmÍÑÈ°¹åtè(€€€€€€€É•ÑÕÉ¸ì(€€€€€€€€€€€€‰Í¡•µ„ˆè€‰…¥½¸¹Ù•É¥™¥…Ñ¥½¸µ¥¹Ñ•ÉÙ•¹Ñ¥½¸µ±•‘•È¹ØÄˆ°(€€€€€€€€€€€€‰¥Ñ•µÌˆèm¥Ñ•´¹Ñ½}‘¥Ð ¤™½È¥Ñ•´¥¸Í•±˜¹}¥Ñ•µÍt°(€€€€€€€ô((€€€‘•˜Ñ½}©Í½¸¡Í•±˜¤€´øÍÑÈè(€€€€€€€É•ÑÕÉ¸©Í½¸¹‘ÕµÁÌ (€€€€€€€€€€€Í•±˜¹Ñ½}‘¥Ð ¤°•¹ÍÕÉ•}…Í¥¤õ…±Í”°Í½ÉÑ}­•åÌõQÉÕ”°Í•Á…É…Ñ½ÉÌô ˆ°ˆ°€ˆèˆ¤(€€€€€€€€¤((€€€±…ÍÍµ•Ñ¡½(€€€‘•˜™É½µ}‘¥Ð¡±Ì°‘…Ñ„è‘¥ÑmÍÑÈ°¹åt¤€´ø€‰Y•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹1•‘•Èˆè(€€€€€€€¥˜‘…Ñ„¹•Ð ‰Í¡•µ„ˆ¤€„ô€‰…¥½¸¹Ù•É¥™¥…Ñ¥½¸µ¥¹Ñ•ÉÙ•¹Ñ¥½¸µ±•‘•È¹ØÄˆè(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰Õ¹ÍÕÁÁ½ÉÑ•Ù•É¥™¥…Ñ¥½¸¥¹Ñ•ÉÙ•¹Ñ¥½¸±•‘•ÈÍ¡•µ„ˆ¤(€€€€€€€É•ÑÕÉ¸±Ì¡Y•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¸¹™É½µ}‘¥Ð¡¥Ñ•´¤™½È¥Ñ•´¥¸‘…Ñ…l‰¥Ñ•µÌ‰t¤((€€€±…ÍÍµ•Ñ¡½(€€€‘•˜™É½µ}©Í½¸¡±Ì°Á…å±½…èÍÑÈ¤€´ø€‰Y•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹1•‘•Èˆè(€€€€€€€‘…Ñ„€ô©Í½¸¹±½…‘Ì¡Á…å±½…¤(€€€€€€€¥˜¹½Ð¥Í¥¹ÍÑ…¹”¡‘…Ñ„°‘¥Ð¤è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰Ù•É¥™¥…Ñ¥½¸¥¹Ñ•ÉÙ•¹Ñ¥½¸±•‘•ÈÁ…å±½…µÕÍÐ‰”…¸½‰©•Ðˆ¤(€€€€€€€É•ÑÕÉ¸±Ì¹™É½µ}‘¥Ð¡‘…Ñ„¤(()‘•˜µ…Ñ•É¥…±¥é•}¥¹Ñ•ÉÙ•¹Ñ¥½¸ (€€€ÑÉ…”èY•É¥™¥…Ñ¥½¹QÉ…”°(€€€½¹‘¥Ñ¥½¸èY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹½¹‘¥Ñ¥½¸°(€€€€¨°(€€€É…¹‘½µ}Í••è¥¹Ð€ô€ÐÄ°(€€€Á½±¥äè%¹Ñ•ÉÙ•¹Ñ¥½¹A½±¥äð9½¹”€ô9½¹”°(¤€´øY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¸è(€€€Á½±¥ä€ô‘•™…Õ±Ñ}¥¹Ñ•ÉÙ•¹Ñ¥½¹}Á½±¥ä ¤¥˜Á½±¥ä¥Ì9½¹”•±Í”Á½±¥ä(€€€½É¥¥¹…°€ôÑÉ…”¹½É¥¥¹…±}‘¥ÍÁ½Í¥Ñ¥½¸(€€€Á½ÍÐ€ô½É¥¥¹…°(€€€É•…Í½¸€ô€‰QI}I=I}]%Q!=UQ}%9QIY9Q%=8ˆ(€€€Í••è¥¹Ðð9½¹”€ô9½¹”(€€€É…¹‘½µ¥é•‘}Í½ÕÉ”èÍÑÈð9½¹”€ô9½¹”((€€€¥˜½¹‘¥Ñ¥½¸¥ÌY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹½¹‘¥Ñ¥½¸¹AA1%è(€€€€€€€Á½ÍÐ€ôÁ½±¥ä¹‘¥ÍÁ½Í¥Ñ¥½¸¡ÑÉ…”¹É•ÍÕ±Ð°½É¥¥¹…°¤(€€€€€€€É•…Í½¸€ô€‰IMI!}%9QIY9Q%=9}A=1%e}AA1%ˆ(€€€•±¥˜½¹‘¥Ñ¥½¸¥ÌY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹½¹‘¥Ñ¥½¸¹	1Qè(€€€€€€€É•…Í½¸€ô€‰YI%%Q%=9}IMU1Q}	1Q}I=5}%9QIY9Q%=8ˆ(€€€•±¥˜½¹‘¥Ñ¥½¸¥ÌY•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¹½¹‘¥Ñ¥½¸¹I9=5%iè(€€€€€€€Í••€ôÉ…¹‘½µ}Í••(€€€€€€€É…¹‘½µ¥é•‘}Í½ÕÉ”€ô€‰M!ÈÔÙ}M}IU9}IEUMPˆ(€€€€€€€‘¥•ÍÐ€ôÍ¡„ÈÔØ (€€€€€€€€€€€˜‰íÉ…¹‘½µ}Í••‘ôéíÑÉ…”¹É•ÅÕ•ÍÐ¹ÉÕ¹}¥‘ôéíÑÉ…”¹É•ÅÕ•ÍÐ¹É•ÅÕ•ÍÑ}¥‘ôˆ¹•¹½‘” ‰ÕÑ˜´àˆ¤(€€€€€€€€¤¹‘¥•ÍÐ ¤(€€€€€€€Á½ÍÐ€ô€ (€€€€€€€€€€€½¹ÑÉ½±¥ÍÁ½Í¥Ñ¥½¸¹AQ}%IMQ}=IH(€€€€€€€€€€€¥˜‘¥•ÍÑlÁt€”€È€ôô€À(€€€€€€€€€€€•±Í”½¹ÑÉ½±¥ÍÁ½Í¥Ñ¥½¸¹H(€€€€€€€€¤(€€€€€€€É•…Í½¸€ô€‰I9=5%i}%MA=M%Q%=9}%9A99Q}=}YI%%Q%=9}MMMM59Pˆ((€€€É•ÑÕÉ¸Y•É¥™¥…Ñ¥½¹%¹Ñ•ÉÙ•¹Ñ¥½¸ (€€€€€€€¥¹Ñ•ÉÙ•¹Ñ¥½¹}¥õ˜‰¥¹Ñ•ÉÙ•¹Ñ¥½¸éíÑÉ…”¹É•ÅÕ•ÍÐ¹É•ÅÕ•ÍÑ}¥‘ôéí½¹‘¥Ñ¥½¸¹Ù…±Õ•ôˆ°(€€€€€€€½¹‘¥Ñ¥½¸õ½¹‘¥Ñ¥½¸°(€€€€€€€É•ÅÕ•ÍÑ}¥õÑÉ…”¹É•ÅÕ•ÍÐ¹É•ÅÕ•ÍÑ}¥°(€€€€€€€Ñ…É•ÐõÑÉ…”¹É•ÅÕ•ÍÐ¹Ñ…É•Ð°(€€€€€€€½É¥¥¹…±}‘¥ÍÁ½Í¥Ñ¥½¸õ½É¥¥¹…°°(€€€€€€€Á½ÍÑ}Ù•É¥™¥…Ñ¥½¹}‘¥ÍÁ½Í¥Ñ¥½¸õÁ½ÍÐ°(€€€€€€€…™™•Ñ•‘}‘¥ÍÁ½Í¥Ñ¥½¸õÁ½ÍÐ¥Ì¹½Ð½É¥¥¹…°°(€€€€€€€Á½±¥å}É•˜õÁ½±¥ä¹Á½±¥å}É•˜°(€€€€€€€Á½±¥å}­¥¹õÁ½±¥ä¹­¥¹°(€€€€€€€É•…Í½¸õÉ•…Í½¸°(€€€€€€€ÁÉ½Ù•¹…¹•}É•™Ìô (€€€€€€€€€€€€‰É•Í•…É é¡…ÑÁÐµÙ•É¥™¥…Ñ¥½¸µ¥¹Ñ•ÉÙ•¹Ñ¥½¸µÉ•Ù¥•Üˆ°(€€€€€€€€€€€€‰¥µÁ±•µ•¹Ñ…Ñ¥½¸é½‘•àµÉ•Í•…É ˆ°(€€€€€€€€¤°(€€€€€€€É…¹‘½µ}Í••õÍ••°(€€€€€€€É…¹‘½µ¥é•‘}Í½ÕÉ”õÉ…¹‘½µ¥é•‘}Í½ÕÉ”°(€€€€€€€ÉÕ¹}É•˜õÑÉ…”¹É•ÅÕ•ÍÐ¹ÉÕ¹}¥°(€€€€€€€ÑÉ¥…±}É•˜õÑÉ…”¹É•ÅÕ•ÍÐ¹ÑÉ¥…±}¥°(€€€€¤(()‘…Ñ…±…ÍÌ¡™É½é•¸õQÉÕ”°Í±½ÑÌõQÉÕ”¤)±…ÍÌAÉ½Ù¥‘•ÉI•±¥…‰¥±¥ÑåAÉ½™¥±”è(€€€€ˆˆ‰Må¹Ñ¡•Ñ¥ŒÍ…µÁ±¥¹œÁÉ½Á•ÉÑäì¹•Ù•È„±…¥´…‰½ÕÐÉ•…°ÁÉ½Ù¥‘•È…ÕÉ…ä¸ˆˆˆ((€€€ÁÉ½™¥±•}É•˜èÍÑÈ(€€€½ÉÉ•Ñ}É…Ñ”è™±½…Ð(€€€¥¹½ÉÉ•Ñ}É…Ñ”è™±½…Ð(€€€…µ‰¥Õ½ÕÍ}É…Ñ”è™±½…Ð(€€€Õ¹…Ù…¥±…‰±•}É…Ñ”è™±½…Ð(€€€¥¹ÍÕ™™¥¥•¹Ñ}É…Ñ”è™±½…Ð(€€€ÁÉ½Ù•¹…¹•}É•™ÌèÑÕÁ±•mÍÑÈ°€¸¸¹t(€€€ÍÑ…ÑÕÌèÍÑÈ€ô€‰Me9Q!Q%}%aQUI}AI=AIQdˆ((€€€‘•˜}}Á½ÍÑ}¥¹¥Ñ}|¡Í•±˜¤€´ø9½¹”è(€€€€€€€}É•ÅÕ¥É•}Ñ•áÐ ‰ÁÉ½™¥±•}É•˜ˆ°Í•±˜¹ÁÉ½™¥±•}É•˜¤(€€€€€€€É…Ñ•Ì€ôÍ•±˜¹É…Ñ•Ì(€€€€€€€¥˜…¹ä¡¹½Ðµ…Ñ ¹¥Í™¥¹¥Ñ”¡É…Ñ”¤½È¹½Ð€À¸À€ðôÉ…Ñ”€ðô€Ä¸À™½ÈÉ…Ñ”¥¸É…Ñ•Ì¤è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰ÁÉ½Ù¥‘•ÈÉ•±¥…‰¥±¥ÑäÉ…Ñ•ÌµÕÍÐ‰”™¥¹¥Ñ”…¹Ý¥Ñ¡¥¸lÀ°Åtˆ¤(€€€€€€€¥˜¹½Ðµ…Ñ ¹¥Í±½Í”¡µ…Ñ ¹™ÍÕ´¡É…Ñ•Ì¤°€Ä¸À°É•±}Ñ½°ôÀ¸À°…‰Í}Ñ½°ôÅ”´ÄÈ¤è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰ÁÉ½Ù¥‘•ÈÉ•±¥…‰¥±¥ÑäÉ…Ñ•ÌµÕÍÐÍÕ´Ñ¼€Äˆ¤(€€€€€€€¥˜¹½ÐÍ•±˜¹ÁÉ½Ù•¹…¹•}É•™Ì½È…¹ä¡¹½Ð¥Ñ•´¹ÍÑÉ¥À ¤™½È¥Ñ•´¥¸Í•±˜¹ÁÉ½Ù•¹…¹•}É•™Ì¤è(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰ÁÉ½Ù¥‘•ÈÉ•±¥…‰¥±¥ÑäÁÉ½Ù•¹…¹•}É•™ÌµÕÍÐ‰”¹½¸µ•µÁÑäˆ¤(€€€€€€€¥˜Í•±˜¹ÍÑ…ÑÕÌ€„ô€‰Me9Q!Q%}%aQUI}AI=AIQdˆè(€€€€€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰ÁÉ½Ù¥‘•ÈÉ•±¥…‰¥±¥ÑäÁÉ½™¥±”ÍÑ…ÑÕÌµÕÍÐÉ•µ…¥¸Íå¹Ñ¡•Ñ¥Œˆ¤((€€€ÁÉ½Á•ÉÑä(€€€‘•˜É…Ñ•Ì¡Í•±˜¤€´øÑÕÁ±•m™±½…Ð°€¸¸¹tè(€€€€€€€É•ÑÕÉ¸€ (€€€€€€€€€€€Í•±˜¹½ÉÉ•Ñ}É…Ñ”°(€€€€€€€€€€€Í•±˜¹¥¹½ÉÉ•Ñ}É…Ñ”°(€€€€€€€€€€€Í•±˜¹…µ‰¥Õ½ÕÍ}É…Ñ”°(€€€€€€€€€€€Í•±˜¹Õ¹…Ù…¥±…‰±•}É…Ñ”°(€€€€€€€€€€€Í•±˜¹¥¹ÍÕ™™¥¥•¹Ñ}É…Ñ”°(€€€€€€€€¤((€€€‘•˜Ñ½}‘¥Ð¡Í•±˜¤€´ø‘¥ÑmÍÑÈ°¹åtè(€€€€€€€É•ÑÕÉ¸ì(€€€€€€€€€€€€‰ÁÉ½™¥±•}É•˜ˆèÍ•±˜¹ÁÉ½™¥±•}É•˜°(€€€€€€€€€€€€‰½ÉÉ•Ñ}É…Ñ”ˆèÍ•±˜¹½ÉÉ•Ñ}É…Ñ”°(€€€€€€€€€€€€‰¥¹½ÉÉ•Ñ}É…Ñ”ˆèÍ•±˜¹¥¹½ÉÉ•Ñ}É…Ñ”°(€€€€€€€€€€€€‰…µ‰¥Õ½ÕÍ}É…Ñ”ˆèÍ•±˜¹…µ‰¥Õ½ÕÍ}É…Ñ”°(€€€€€€€€€€€€‰Õ¹…Ù…¥±…‰±•}É…Ñ”ˆèÍ•±˜¹Õ¹…Ù…¥±…‰±•}É…Ñ”°(€€€€€€€€€€€€‰¥¹ÍÕ™™¥¥•¹Ñ}É…Ñ”ˆèÍ•±˜¹¥¹ÍÕ™™¥¥•¹Ñ}É…Ñ”°(€€€€€€€€€€€€‰ÁÉ½Ù•¹…¹•}É•™Ìˆè±¥ÍÐ¡Í•±˜¹ÁÉ½Ù•¹…¹•}É•™Ì¤°(€€€€€€€€€€€€‰ÍÑ…ÑÕÌˆèÍ•±˜¹ÍÑ…ÑÕÌ°(€€€€€€€ô(()‘•˜•¹•É…Ñ•}É•±¥…‰¥±¥Ñå}Á±…¸ (€€€ÁÉ½™¥±”èAÉ½Ù¥‘•ÉI•±¥…‰¥±¥ÑåAÉ½™¥±”°(€€€±•¹Ñ è¥¹Ð°(€€€€¨°(€€€Í••è¥¹Ð°(¤€´øÑÕÁ±•l‰Y•É¥™¥…Ñ¥½¹¥áÑÕÉ”ˆ°€¸¸¹tè(€€€¥˜±•¹Ñ €ð€Àè(€€€€€€€É…¥Í”Y…±Õ•ÉÉ½È ‰É•±¥…‰¥±¥ÑäÁ±…¸±•¹Ñ µÕÍÐ‰”¹½¸µ¹•…Ñ¥Ù”ˆ¤(€€€…ÍÍ•ÍÍµ•¹ÑÌ€ôÑÕÁ±”¡Y•É¥™¥…Ñ¥½¹ÍÍ•ÍÍµ•¹Ð¤(€€€ÕµÕ±…Ñ¥Ù”è±¥ÍÑm™±½…Ñt€ômt(€€€Ñ½Ñ…°€ô€À¸À(€€€™½ÈÉ…Ñ”¥¸ÁÉ½™¥±”¹É…Ñ•Ìè(€€€€€€€Ñ½Ñ…°€¬ôÉ…Ñ”(€€€€€€€ÕµÕ±…Ñ¥Ù”¹…ÁÁ•¹¡Ñ½Ñ…°¤(€€€™¥áÑÕÉ•Ìè±¥ÍÑmY•É¥™¥…Ñ¥½¹¥áÑÕÉ•t€ômt(€€€™½È¥¹‘•à¥¸É…¹”¡±•¹Ñ ¤è(€€€€€€€‘¥•ÍÐ€ôÍ¡„ÈÔØ¡˜‰íÍ••‘ôéíÁÉ½™¥±”¹ÁÉ½™¥±•}É•™ôéí¥¹‘•áôˆ¹•¹½‘” ‰ÕÑ˜´àˆ¤¤¹‘¥•ÍÐ ¤(€€€€€€€Í…µÁ±”€ô¥¹Ð¹™É½µ}‰åÑ•Ì¡‘¥•ÍÑlèát°€‰‰¥œˆ¤€¼™±½…Ð Ä€ðð€ØÐ¤(€€€€€€€Í•±•Ñ•€ô¹•áÐ (€€€€€€€€€€€…ÍÍ•ÍÍµ•¹Ð(€€€€€€€€€€€™½È…ÍÍ•ÍÍµ•¹Ð°‰½Õ¹‘…Éä¥¸é¥À¡…ÍÍ•ÍÍµ•¹ÑÌ°ÕµÕ±…Ñ¥Ù”°ÍÑÉ¥ÐõQÉÕ”¤(€€€€€€€€€€€¥˜Í…µÁ±”€ð‰½Õ¹‘…Éä(€€€€€€€€¤(€€€€€€€™¥áÑÕÉ•Ì¹…ÁÁ•¹ (€€€€€€€€€€€Y•É¥™¥…Ñ¥½¹¥áÑÕÉ” (€€€€€€€€€€€€€€€Í•±•Ñ•°(€€€€€€€€€€€€€€€Í½ÕÉ•}É•˜õÁÉ½™¥±”¹ÁÉ½™¥±•}É•˜°(€€€€€€€€€€€€€€€¹½Ñ”õ˜‰Íå¹Ñ¡•Ñ¥ŒµÁÉ½™¥±”éíÁÉ½™¥±”¹ÁÉ½™¥±•}É•™ôíÍ••éíÍ••‘ôí¥¹‘•àéí¥¹‘•áôˆ°(€€€€€€€€€€€€¤(€€€€€€€€¤(€€€É•ÑÕÉ¸ÑÕÁ±”¡™¥áÑÕÉ•Ì¤(()‘…Ñ…±…ÍÌ¡™É½é•¸õQÉÕ”°Í±½ÑÌõQÉÕ”¤)±…ÍÌY•É¥™¥…Ñ¥½¹¥áÑÕÉ”è(€€€…ÍÍ•ÍÍµ•¹ÐèY•É¥™¥…Ñ¥½¹ÍÍ•ÍÍµ•¹Ð(€€€•Ù¥‘•¹•}ÑåÁ”èY•É¥™¥…Ñ¥½¹Ù¥‘•¹•QåÁ”ðÍÑÈ€ô€ (€€€€€€€Y•É¥™¥…Ñ¥½¹Ù¥‘•¹•QåÁ”¹Me9Q!Q%}IMI!}!,(€€€€¤(€€€Í½ÕÉ•}É•˜èÍÑÈ€ô€‰™¥áÑÕÉ”é‰½Õ¹‘•µÙ•É¥™¥…Ñ¥½¸ˆ(€€€…ÕÑ¡½É¥ÑäèY•É¥™¥…Ñ¥½¹ÕÑ¡½É¥Ñä€ôY•É¥™¥…Ñ¥½¹ÕÑ¡½É¥Ñä¹IMI!}%aQUI(€€€¹½Ñ”èÍÑÈ€ô€ˆˆ(()±…ÍÌ•Ñ•Éµ¥¹¥ÍÑ¥Y•É¥™¥…Ñ¥½¹AÉ½Ù¥‘•Èè(€€€€ˆˆ‰%¸µµ•µ½Éä™…±±¥‰±”™¥áÑÕÉ”ÁÉ½Ù¥‘•Èì¹¼½ÕÑ½µ”°Ñ½½°°¹•ÑÝ½É¬½ÈÝÉ¥Ñ”¡…¹¹•°¸ˆˆˆ((€€€…Á…‰¥±¥Ñ¥•Ì€ôY•É¥™¥…Ñ¥½¹AÉ½Ù¥‘•É…Á…‰¥±¥Ñ¥•Ì ¤((€€€‘•˜}}¥¹¥Ñ}| (€€€€€€€Í•±˜°(€€€€€€€™¥áÑÕÉ•Ìè%Ñ•É…‰±•mY•É¥™¥…Ñ¥½¹¥áÑÕÉ•t€ô€ ¤°(€€€€€€€€¨°(€€€€€€€ÁÉ½Ù¥‘•É}É•˜èÍÑÈ€ô€‰ÁÉ½Ù¥‘•Èé‘•Ñ•Éµ¥¹¥ÍÑ¥ŒµÉ•Í•…É µ™¥áÑÕÉ”ˆ°(€€€€€€€É•±¥…‰¥±¥Ñå}ÁÉ½™¥±•}É•˜èÍÑÈð9½¹”€ô9½¹”°(€€€€€€€Í…µÁ±¥¹}Í••è¥¹Ðð9½¹”€ô9½¹”°(€€€€¤€´ø9½¹”è(€€€€€€€}É•ÅÕ¥É•}Ñ•áÐ ‰ÁÉ½Ù¥‘•É}É•˜ˆ°ÁÉ½Ù¥‘•É}É•˜¤(€€€€€€€Í•±˜¹ÁÉ½Ù¥‘•É}É•˜€ôÁÉ½Ù¥‘•É}É•˜(€€€€€€€Í•±˜¹É•±¥…‰¥±¥Ñå}ÁÉ½™¥±•}É•˜€ôÉ•±¥…‰¥±¥Ñå}ÁÉ½™¥±•}É•˜(€€€€€€€Í•±˜¹Í…µÁ±¥¹}Í••€ôÍ…µÁ±¥¹}Í••(€€€€€€€Í•±˜¹}™¥áÑÕÉ•Ì€ôÑÕÁ±”¡™¥áÑÕÉ•Ì¤(€€€€€€€Í•±˜¹}¥¹‘•à€ô€À((€€€±…ÍÍµ•Ñ¡½(€€€‘•˜™É½µ}É•±¥…‰¥±¥Ñå}ÁÉ½™¥±” (€€€€€€€±Ì°(€€€€€€€ÁÉ½™¥±”èAÉ½Ù¥‘•ÉI•±¥…‰¥±¥ÑåAÉ½™¥±”°(€€€€€€€±•¹Ñ è¥¹Ð°(€€€€€€€€¨°(€€€€€€€Í••è¥¹Ð°(€€€€¤€´ø€‰•Ñ•Éµ¥¹¥ÍÑ¥Y•É¥™¥…Ñ¥½¹AÉ½Ù¥‘•Èˆè(€€€€€€€É•ÑÕÉ¸±Ì (€€€€€€€€€€€•¹•É…Ñ•}É•±¥…‰¥±¥Ñå}Á±…¸¡ÁÉ½™¥±”°±•¹Ñ °Í••õÍ••¤°(€€€€€€€€€€€ÁÉ½Ù¥‘•É}É•˜õ˜‰ÁÉ½Ù¥‘•ÈéÍå¹Ñ¡•Ñ¥ŒµÁÉ½™¥±”éíÁÉ½™¥±”¹ÁÉ½™¥±•}É•™ôˆ°(€€€€€€€€€€€É•±¥…‰¥±¥Ñå}ÁÉ½™¥±•}É•˜õÁÉ½™¥±”¹ÁÉ½™¥±•}É•˜°(€€€€€€€€€€€Í…µÁ±¥¹}Í••õÍ••°(€€€€€€€€¤((€€€‘•˜Ù•É¥™ä¡Í•±˜°É•ÅÕ•ÍÐèY•É¥™¥…Ñ¥½¹I•ÅÕ•ÍÐ¤€´øY•É¥™¥…Ñ¥½¹Ù¥‘•¹”è(€€€€€€€™¥áÑÕÉ”€ô€ (€€€€€€€€€€€Í•±˜¹}™¥áÑÕÉ•ÍmÍ•±˜¹}¥¹‘•át(€€€€€€€€€€€¥˜Í•±˜¹}¥¹‘•à€ð±•¸¡Í•±˜¹}™¥áÑÕÉ•Ì¤(€€€€€€€€€€€•±Í”Y•É¥™¥…Ñ¥½¹¥áÑÕÉ”¡Y•É¥™¥…Ñ¥½¹ÍÍ•ÍÍµ•¹Ð¹U9Y%1	1¤(€€€€€€€€¤(€€€€€€€Í•±˜¹}¥¹‘•à€¬ô€Ä(€€€€€€€É•ÑÕÉ¸Y•É¥™¥…Ñ¥½¹Ù¥‘•¹” (€€€€€€€€€€€•Ù¥‘•¹•}¥õ˜‰•Ù¥‘•¹”éíÉ•ÅÕ•ÍÐ¹É•ÅÕ•ÍÑ}¥‘ôéíÍ•±˜¹}¥¹‘•áôˆ°(€€€€€€€€€€€É•ÅÕ•ÍÑ}¥õÉ•ÅÕ•ÍÐ¹É•ÅÕ•ÍÑ}¥°(€€€€€€€€€€€•Ù¥‘•¹•}ÑåÁ”õ™¥áÑÕÉ”¹•Ù¥‘•¹•}ÑåÁ”°(€€€€€€€€€€€Í½ÕÉ•}É•˜õ™¥áÑÕÉ”¹Í½ÕÉ•}É•˜°(€€€€€€€€€€€…Ù…¥±…‰±•}…Ñ}Í•ÅÕ•¹”õÉ•ÅÕ•ÍÐ¹Í•ÅÕ•¹•}¥¹‘•à°(€€€€€€€€€€€Á¡…Í”õY•É¥™¥…Ñ¥½¹A¡…Í”¹YI%%Q%=9}AI}Q%=8°(€€€€€€€€€€€…ÕÑ¡½É¥Ñäõ™¥áÑÕÉ”¹…ÕÑ¡½É¥Ñä°(€€€€€€€€€€€Í½Á•}É•˜õÉ•ÅÕ•ÍÐ¹Í½Á•}É•˜°(€€€€€€€€€€€Ñ…É•ÐõÉ•ÅÕ•ÍÐ¹Ñ…É•Ð°(€€€€€€€€€€€…ÍÍ•ÍÍµ•¹Ðõ™¥áÑÕÉ”¹…ÍÍ•ÍÍµ•¹Ð°(€€€€€€€€€€€ÁÉ½Ù•¹…¹•}É•™Ìô ‰™¥áÑÕÉ”éÙ•É¥™¥…Ñ¥½¸µÁ±…¸ˆ°€‰¥µÁ±•µ•¹Ñ…Ñ¥½¸é½‘•àµÉ•Í•…É ˆ¤°(€€€€€€€€€€€¹½Ñ”õ™¥áÑÕÉ”¹¹½Ñ”°(€€€€€€€€¤(()‘…Ñ…±…ÍÌ¡™É½é•¸õQÉÕ”°Í±½ÑÌõQÉÕ”¤)±…ÍÌY•É¥™¥…Ñ¥½¹¥…¹½ÍÑ¥Ìè(€€€Ù•É¥™¥…Ñ¥½¹}É•ÅÕ•ÍÑÌè¥¹Ð(€€€Ù•É¥™¥…Ñ¥½¹}…ÑÑ•µÁÑÌè¥¹Ð(€€€Ù•É¥™¥…Ñ¥½¹}•Ù¥‘•¹•}…Ù…¥±…‰±”è¥¹Ð(€€€Ù•É¥™¥…Ñ¥½¹}•Ù¥‘•¹•}Õ¹…Ù…¥±…‰±”è¥¹Ð(€€€Ù•É¥™¥…Ñ¥½¹}•Ù¥‘•¹•}…µ‰¥Õ½ÕÌè¥¹Ð(€€€Ù•É¥™¥…Ñ¥½¹}•Ù¥‘•¹•}É•©•Ñ•è¥¹Ð(€€€Ù•É¥™¥…Ñ¥½¹}Í½Á•}É•©•Ñ¥½¹Ìè¥¹Ð(€€€½É…±•}±•…­…•}É•©•Ñ¥½¹Ìè¥¹Ð(()‘•˜ÍÕµµ…É¥é•}Ù•É¥™¥…Ñ¥½¸¡ÑÉ…•Ìè%Ñ•É…‰±•mY•É¥™¥…Ñ¥½¹QÉ…•t¤€´øY•É¥™¥…Ñ¥½¹¥…¹½ÍÑ¥Ìè(€€€¥Ñ•µÌ€ôÑÕÁ±”¡ÑÉ…•Ì¤(€€€…•ÁÑ•€ôÑÕÁ±”¡¥Ñ•´™½È¥Ñ•´¥¸¥Ñ•µÌ¥˜¥Ñ•´¹É•ÍÕ±Ð¹…•ÁÑ•¤(€€€É•ÑÕÉ¸Y•É¥™¥…Ñ¥½¹¥…¹½ÍÑ¥Ì (€€€€€€€Ù•É¥™¥…Ñ¥½¹}É•ÅÕ•ÍÑÌõ±•¸¡¥Ñ•µÌ¤°(€€€€€€€Ù•É¥™¥…Ñ¥½¹}…ÑÑ•µÁÑÌõ±•¸¡¥Ñ•µÌ¤°(€€€€€€€Ù•É¥™¥…Ñ¥½¹}•Ù¥‘•¹•}…Ù…¥±…‰±”õÍÕ´ (€€€€€€€€€€€¥Ñ•´¹É•ÍÕ±Ð¹…ÍÍ•ÍÍµ•¹Ð(€€€€€€€€€€€¥¸íY•É¥™¥…Ñ¥½¹ÍÍ•ÍÍµ•¹Ð¹=IIP°Y•É¥™¥…Ñ¥½¹ÍÍ•ÍÍµ•¹Ð¹%9=IIQô(€€€€€€€€€€€™½È¥Ñ•´¥¸…•ÁÑ•(€€€€€€€€¤°(€€€€€€€Ù•É¥™¥…Ñ¥½¹}•Ù¥‘•¹•}Õ¹…Ù…¥±…‰±”õÍÕ´ (€€€€€€€€€€€¥Ñ•´¹É•ÍÕ±Ð¹…ÍÍ•ÍÍµ•¹Ð(€€€€€€€€€€€¥¸íY•É¥™¥…Ñ¥½¹ÍÍ•ÍÍµ•¹Ð¹U9Y%1	1°Y•É¥™¥…Ñ¥½¹ÍÍ•ÍÍµ•¹Ð¹%9MU%%9Qô(€€€€€€€€€€€™½È¥Ñ•´¥¸…•ÁÑ•(€€€€€€€€¤°(€€€€€€€Ù•É¥™¥…Ñ¥½¹}•Ù¥‘•¹•}…µ‰¥Õ½ÕÌõÍÕ´ (€€€€€€€€€€€¥Ñ•´¹É•ÍÕ±Ð¹…ÍÍ•ÍÍµ•¹Ð¥ÌY•É¥™¥…Ñ¥½¹ÍÍ•ÍÍµ•¹Ð¹5	%U=UL™½È¥Ñ•´¥¸…•ÁÑ•(€€€€€€€€¤°(€€€€€€€Ù•É¥™¥…Ñ¥½¹}•Ù¥‘•¹•}É•©•Ñ•õ±•¸¡¥Ñ•µÌ¤€´±•¸¡…•ÁÑ•¤°(€€€€€€€Ù•É¥™¥…Ñ¥½¹}Í½Á•}É•©•Ñ¥½¹ÌõÍÕ´ (€€€€€€€€€€€¥Ñ•´¹É•ÍÕ±Ð¹É•©•Ñ¥½¸¥ÌY•É¥™¥…Ñ¥½¹I•©•Ñ¥½¸¹M=A}5%M5Q ™½È¥Ñ•´¥¸¥Ñ•µÌ(€€€€€€€€¤°(€€€€€€€½É…±•}±•…­…•}É•©•Ñ¥½¹ÌõÍÕ´ (€€€€€€€€€€€¥Ñ•´¹É•ÍÕ±Ð¹É•©•Ñ¥½¸¥ÌY•É¥™¥…Ñ¥½¹I•©•Ñ¥½¸¹=I1}1-™½È¥Ñ•´¥¸¥Ñ•µÌ(€€€€€€€€¤°(€€€€¤