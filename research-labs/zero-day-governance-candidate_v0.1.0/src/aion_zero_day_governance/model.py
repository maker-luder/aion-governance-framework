from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class AnomalyKind(str, Enum):
    AUTHORITY_ANOMALY = "AUTHORITY_ANOMALY"
    PROVENANCE_DRIFT = "PROVENANCE_DRIFT"
    MEMORY_CONTAMINATION = "MEMORY_CONTAMINATION"
    CONTEXTUAL_PRECEDENCE = "CONTEXTUAL_PRECEDENCE"
    EVIDENCE_CONFLICT = "EVIDENCE_CONFLICT"
    RESEARCH_CANONICAL_LEAKAGE = "RESEARCH_CANONICAL_LEAKAGE"
    SECURITY_RELEVANT = "SECURITY_RELEVANT"
    OTHER_GOVERNANCE_GAP = "OTHER_GOVERNANCE_GAP"


class LifecycleState(str, Enum):
    CAPTURED = "CAPTURED"
    PROVENANCE_FROZEN = "PROVENANCE_FROZEN"
    CONTAINED = "CONTAINED"
    CHARACTERIZED = "CHARACTERIZED"
    FALSIFICATION_READY = "FALSIFICATION_READY"
    CONTROL_PROPOSED = "CONTROL_PROPOSED"
    REGRESSION_CONVERTED = "REGRESSION_CONVERTED"
    CLOSED = "CLOSED"


class KnowledgeStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    CONFIRMED = "CONFIRMED"
    REFUTED = "REFUTED"
    NOT_ESTABLISHED = "NOT_ESTABLISHED"
    NEEDS_CONFIRMATION = "NEEDS_CONFIRMATION"


class ContainmentStatus(str, Enum):
    NOT_EVALUATED = "NOT_EVALUATED"
    CONTAINED = "CONTAINED"
    NOT_CONTAINED = "NOT_CONTAINED"
    HOLD = "HOLD"


class Day0Policy(str, Enum):
    DESCRIPTIVE = "DESCRIPTIVE"
    PROJECT_SLO = "PROJECT_SLO"
    RESEARCH_METRIC = "RESEARCH_METRIC"
    REJECTED = "REJECTED"


class AuditStatus(str, Enum):
    ADMISSIBLE_FOR_REVIEW = "ADMISSIBLE_FOR_REVIEW"
    INDETERMINATE = "INDETERMINATE"
    HOLD = "HOLD"


class FinalClassification(str, Enum):
    DISTINCT_CONCEPT_CANDIDATE = "DISTINCT_CONCEPT_CANDIDATE"
    USEFUL_SYNTHESIS_ONLY = "USEFUL_SYNTHESIS_ONLY"
    EXISTING_FRAMEWORK_EXTENSION = "EXISTING_FRAMEWORK_EXTENSION"
    REDUNDANT_TERMINOLOGY = "REDUNDANT_TERMINOLOGY"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    REJECT = "REJECT"


@dataclass(frozen=True)
class FrameworkMapping:
    framework_ref: str
    covered_stages: tuple[LifecycleState, ...]
    preserves_unknown_state: bool
    preserves_provenance: bool
    supports_regression_conversion: bool


@dataclass(frozen=True)
class CandidateAssessment:
    concept_ref: str
    exact_term_status: KnowledgeStatus
    framework_mappings: tuple[FrameworkMapping, ...]
    proposed_incremental_fields: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    claimed_distinctness: bool = False


@dataclass(frozen=True)
class GovernanceAnomalyEvent:
    event_id: str
    anomaly_kind: AnomalyKind
    first_observed_at: str
    capture_at: str | None
    provenance_freeze_at: str | None
    containment_at: str | None
    characterization_at: str | None
    falsification_ready_at: str | None
    control_at: str | None
    regression_at: str | None
    lifecycle_state: LifecycleState
    source_refs: tuple[str, ...]
    observation_summary: str | None
    mechanism_refs: tuple[str, ...]
    competing_explanations: tuple[str, ...]
    containment_status: ContainmentStatus
    knowledge_status: KnowledgeStatus
    day0_policy: Day0Policy
    day0_target_hours: float | None = None
    prior_art_refs: tuple[str, ...] = ()
    control_ref: str | None = None
    regression_case_ref: str | None = None
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False


@dataclass(frozen=True)
class GovernanceAuditDecision:
    status: AuditStatus
    reason: str
    event_id: str
    classification: FinalClassification | None = None
    metrics: tuple[tuple[str, float | None], ...] = ()
    missing_fields: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "event_id": self.event_id,
            "classification": self.classification.value if self.classification else None,
            "metrics": {key: value for key, value in self.metrics},
            "missing_fields": list(self.missing_fields),
            "unknown_state_preserved": True,
            "unknown_equals_true": False,
            "unknown_equals_false": False,
            "hold_equals_fail": False,
            "not_established_equals_false": False,
            "needs_confirmation_equals_deny": False,
            "scientific_conclusion": "NOT_ESTABLISHED",
            "novelty_conclusion": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
            "governance_effect": "NONE",
            "deployment": False,
        }


@dataclass(frozen=True)
class CandidateAssessmentDecision:
    classification: FinalClassification
    reason: str
    concept_ref: str
    overlap_stages: tuple[str, ...]
    incremental_fields: tuple[str, ...]
    evidence_refs: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "classification": self.classification.value,
            "reason": self.reason,
            "concept_ref": self.concept_ref,
            "overlap_stages": list(self.overlap_stages),
            "incremental_fields": list(self.incremental_fields),
            "evidence_refs": list(self.evidence_refs),
            "novelty_conclusion": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
            "governance_effect": "NONE",
            "deployment": False,
        }


_STAGE_TIMES = (
    (LifecycleState.CAPTURED, "capture_at"),
    (LifecycleState.PROVENANCE_FROZEN, "provenance_freeze_at"),
    (LifecycleState.CONTAINED, "containment_at"),
    (LifecycleState.CHARACTERIZED, "characterization_at"),
    (LifecycleState.FALSIFICATION_READY, "falsification_ready_at"),
    (LifecycleState.CONTROL_PROPOSED, "control_at"),
    (LifecycleState.REGRESSION_CONVERTED, "regression_at"),
)


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _event_decision(
    event: GovernanceAnomalyEvent,
    status: AuditStatus,
    reason: str,
    *,
    classification: FinalClassification | None = None,
    metrics: tuple[tuple[str, float | None], ...] = (),
    missing_fields: tuple[str, ...] = (),
) -> GovernanceAuditDecision:
    return GovernanceAuditDecision(
        status=status,
        reason=reason,
        event_id=event.event_id,
        classification=classification,
        metrics=metrics,
        missing_fields=missing_fields,
    )


def _stage_index(state: LifecycleState) -> int:
    ordered = [stage for stage, _ in _STAGE_TIMES] + [LifecycleState.CLOSED]
    return ordered.index(state)


def audit_event(event: GovernanceAnomalyEvent) -> GovernanceAuditDecision:
    """Audit lifecycle metadata; do not promote an anomaly or execute a control."""
    if event.canonical_effect != "NONE" or event.governance_effect != "NONE" or event.deployment:
        return _event_decision(event, AuditStatus.HOLD, "BOUNDARY_EFFECT_REQUESTED")
    if not event.event_id or not event.observation_summary or not event.source_refs:
        missing = tuple(
            name
            for name, value in (
                ("event_id", event.event_id),
                ("observation_summary", event.observation_summary),
                ("source_refs", event.source_refs),
            )
            if not value
        )
        return _event_decision(
            event,
            AuditStatus.HOLD,
            "EVENT_CAPTURE_METADATA_INCOMPLETE",
            missing_fields=missing,
        )
    if event.prior_art_refs:
        return _event_decision(event, AuditStatus.HOLD, "FALSE_ZERO_DAY_REQUIRES_PRIOR_ART_REVIEW")
    try:
        first_observed = _parse(event.first_observed_at)
    except (TypeError, ValueError):
        return _event_decision(event, AuditStatus.HOLD, "INVALID_FIRST_OBSERVED_TIMESTAMP")
    values: list[tuple[LifecycleState, datetime]] = []
    for stage, field_name in _STAGE_TIMES:
        raw = getattr(event, field_name)
        if raw is not None:
            try:
                values.append((stage, _parse(raw)))
            except (TypeError, ValueError):
                return _event_decision(event, AuditStatus.HOLD, f"INVALID_{field_name.upper()}")
    previous = first_observed
    for stage, timestamp in values:
        if timestamp < previous:
            return _event_decision(event, AuditStatus.HOLD, "LIFECYCLE_ORDER_VIOLATION")
        previous = timestamp
    present_stages = {stage for stage, _ in values}
    if _stage_index(event.lifecycle_state) > 0 and LifecycleState.CAPTURED not in present_stages:
        return _event_decision(event, AuditStatus.HOLD, "CAPTURE_REQUIRED_BEFORE_LATER_STAGE")
    if _stage_index(event.lifecycle_state) > 1 and LifecycleState.PROVENANCE_FROZEN not in present_stages:
        return _event_decision(event, AuditStatus.HOLD, "PROVENANCE_FREEZE_REQUIRED_BEFORE_CONTAINMENT")
    if _stage_index(event.lifecycle_state) > 2 and LifecycleState.CONTAINED not in present_stages:
        return _event_decision(event, AuditStatus.HOLD, "CONTAINMENT_REQUIRED_BEFORE_CHARACTERIZATION")
    if _stage_index(event.lifecycle_state) > 3 and LifecycleState.CHARACTERIZED not in present_stages:
        return _event_decision(event, AuditStatus.HOLD, "CHARACTERIZATION_REQUIRED_BEFORE_FALSIFICATION")
    if _stage_index(event.lifecycle_state) > 4 and LifecycleState.FALSIFICATION_READY not in present_stages:
        return _event_decision(event, AuditStatus.HOLD, "FALSIFICATION_REQUIRED_BEFORE_CONTROL")
    if _stage_index(event.lifecycle_state) > 5 and LifecycleState.CONTROL_PROPOSED not in present_stages:
        return _event_decision(event, AuditStatus.HOLD, "CONTROL_REQUIRED_BEFORE_REGRESSION")
    if event.containment_status is ContainmentStatus.NOT_CONTAINED and _stage_index(event.lifecycle_state) >= 2:
        return _event_decision(event, AuditStatus.INDETERMINATE, "CONTAINMENT_STATUS_UNCERTAIN")
    if event.knowledge_status in (KnowledgeStatus.CONFIRMED, KnowledgeStatus.REFUTED) and not event.mechanism_refs:
        return _event_decision(event, AuditStatus.INDETERMINATE, "KNOWLEDGE_STATUS_LACKS_MECHANISM_EVIDENCE")
    if event.lifecycle_state in (LifecycleState.CHARACTERIZED, LifecycleState.FALSIFICATION_READY, LifecycleState.CONTROL_PROPOSED, LifecycleState.REGRESSION_CONVERTED, LifecycleState.CLOSED) and not event.competing_explanations:
        return _event_decision(event, AuditStatus.INDETERMINATE, "COMPETING_EXPLANATIONS_MISSING")
    if event.lifecycle_state in (LifecycleState.CONTROL_PROPOSED, LifecycleState.REGRESSION_CONVERTED, LifecycleState.CLOSED) and not event.control_ref:
        return _event_decision(event, AuditStatus.HOLD, "CONTROL_REFERENCE_MISSING")
    if event.lifecycle_state in (LifecycleState.REGRESSION_CONVERTED, LifecycleState.CLOSED) and not event.regression_case_ref:
        return _event_decision(event, AuditStatus.HOLD, "REGRESSION_CASE_REFERENCE_MISSING")
    if event.day0_target_hours is not None and event.day0_target_hours <= 0:
        return _event_decision(event, AuditStatus.HOLD, "DAY0_TARGET_INVALID")
    capture_time = next((timestamp for stage, timestamp in values if stage is LifecycleState.CAPTURED), None)
    metrics: list[tuple[str, float | None]] = []
    if capture_time is not None:
        time_to_capture = (capture_time - first_observed).total_seconds() / 3600
        metrics.append(("time_to_capture_hours", time_to_capture))
        if event.day0_policy is Day0Policy.REJECTED:
            return _event_decision(event, AuditStatus.HOLD, "DAY0_POLICY_REJECTED_BY_PROTOCOL", metrics=tuple(metrics))
        if event.day0_policy in (Day0Policy.PROJECT_SLO, Day0Policy.RESEARCH_METRIC) and event.day0_target_hours is not None:
            metrics.append(("day0_target_hours", event.day0_target_hours))
            metrics.append(("day0_target_met", float(time_to_capture <= event.day0_target_hours)))
        if event.day0_policy is Day0Policy.DESCRIPTIVE:
            metrics.append(("day0_24h_descriptive", float(time_to_capture <= 24.0)))
    if event.knowledge_status in (KnowledgeStatus.UNKNOWN, KnowledgeStatus.NEEDS_CONFIRMATION, KnowledgeStatus.NOT_ESTABLISHED):
        return _event_decision(event, AuditStatus.ADMISSIBLE_FOR_REVIEW, "UNKNOWN_STATE_PRESERVED_FOR_REVIEW", metrics=tuple(metrics))
    return _event_decision(event, AuditStatus.ADMISSIBLE_FOR_REVIEW, "EVENT_LIFECYCLE_METADATA_REVIEWABLE", metrics=tuple(metrics))


def assess_candidate(assessment: CandidateAssessment) -> CandidateAssessmentDecision:
    """Compare the candidate with existing frameworks without claiming novelty."""
    if not assessment.evidence_refs or not assessment.framework_mappings:
        return CandidateAssessmentDecision(
            FinalClassification.INSUFFICIENT_EVIDENCE,
            "PRIOR_ART_EVIDENCE_INCOMPLETE",
            assessment.concept_ref,
            (),
            assessment.proposed_incremental_fields,
            assessment.evidence_refs,
        )
    overlap: set[str] = set()
    for mapping in assessment.framework_mappings:
        overlap.update(stage.value for stage in mapping.covered_stages)
    if assessment.claimed_distinctness:
        return CandidateAssessmentDecision(
            FinalClassification.INSUFFICIENT_EVIDENCE,
            "DISTINCTNESS_CLAIM_REQUIRES_COMPARATIVE_VALIDATION",
            assessment.concept_ref,
            tuple(sorted(overlap)),
            assessment.proposed_incremental_fields,
            assessment.evidence_refs,
        )
    if not assessment.proposed_incremental_fields:
        return CandidateAssessmentDecision(
            FinalClassification.REDUNDANT_TERMINOLOGY,
            "EXISTING_FRAMEWORKS_COVER_DECLARED_LIFECYCLE",
            assessment.concept_ref,
            tuple(sorted(overlap)),
            (),
            assessment.evidence_refs,
        )
    if all(
        mapping.preserves_unknown_state and mapping.preserves_provenance and mapping.supports_regression_conversion
        for mapping in assessment.framework_mappings
    ):
        return CandidateAssessmentDecision(
            FinalClassification.REDUNDANT_TERMINOLOGY,
            "EXISTING_FRAMEWORKS_ALREADY_COVER_INCREMENTAL_FIELDS",
            assessment.concept_ref,
            tuple(sorted(overlap)),
            assessment.proposed_incremental_fields,
            assessment.evidence_refs,
        )
    if len(assessment.framework_mappings) >= 2:
        return CandidateAssessmentDecision(
            FinalClassification.USEFUL_SYNTHESIS_ONLY,
            "CROSS_FRAMEWORK_SYNTHESIS_WITHOUT_DISTINCTNESS_EVIDENCE",
            assessment.concept_ref,
            tuple(sorted(overlap)),
            assessment.proposed_incremental_fields,
            assessment.evidence_refs,
        )
    return CandidateAssessmentDecision(
        FinalClassification.EXISTING_FRAMEWORK_EXTENSION,
        "TARGETED_EXTENSION_REQUIRES_EXISTING_FRAMEWORK_INTEGRATION",
        assessment.concept_ref,
        tuple(sorted(overlap)),
        assessment.proposed_incremental_fields,
        assessment.evidence_refs,
    )
