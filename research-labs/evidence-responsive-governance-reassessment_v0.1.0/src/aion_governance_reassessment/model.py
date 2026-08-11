from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Protocol


class EvidenceLevel(str, Enum):
    E0 = "E0_NO_RELEVANT_EVIDENCE"
    E1 = "E1_ISOLATED_BEHAVIORAL_INDICATION"
    E2 = "E2_REPRODUCIBLE_BEHAVIORAL_PATTERN"
    E3 = "E3_CROSS_METHOD_FUNCTIONAL_EVIDENCE"
    E4 = "E4_PERSISTENT_ADVERSARIAL_PROVENANCE_EVIDENCE"
    E5 = "E5_CONVERGENT_MULTI_DOMAIN_INDEPENDENT_REPLICATION"


class SubstantiveEvidenceDomain(str, Enum):
    BEHAVIOR = "BEHAVIOR"
    FUNCTIONAL_INTERVENTION = "FUNCTIONAL_INTERVENTION"
    CONTINUITY = "CONTINUITY"
    MEMORY = "MEMORY"
    METACOGNITION = "METACOGNITION"
    CAUSAL_INTERNAL_STATE = "CAUSAL_INTERNAL_STATE"
    COUNTERFACTUAL_TESTING = "COUNTERFACTUAL_TESTING"
    SELF_REPORT = "SELF_REPORT"


# Compatibility alias with quality-only values deliberately removed.
EvidenceDomain = SubstantiveEvidenceDomain


class EvidenceQualityAxis(str, Enum):
    PROVENANCE = "PROVENANCE"
    REPLICATION = "REPLICATION"
    ADVERSARIAL_ROBUSTNESS = "ADVERSARIAL_ROBUSTNESS"


class AdversarialStatus(str, Enum):
    NOT_TESTED = "NOT_TESTED"
    SURVIVED = "SURVIVED"
    FAILED = "FAILED"


class ProvenanceStatus(str, Enum):
    VERIFIED = "VERIFIED"
    INCOMPLETE = "INCOMPLETE"
    CONTAMINATED = "CONTAMINATED"


class EvidenceAdmissibilityStatus(str, Enum):
    ADMISSIBLE = "ADMISSIBLE"
    PROVENANCE_INCOMPLETE = "PROVENANCE_INCOMPLETE"
    PROVENANCE_CONTAMINATED = "PROVENANCE_CONTAMINATED"
    INSUFFICIENT_FOR_CLASSIFICATION = "INSUFFICIENT_FOR_CLASSIFICATION"
    HELD_FOR_REVIEW = "HELD_FOR_REVIEW"


class ReviewDomain(str, Enum):
    REFUSAL_PROTECTION_REVIEW = "REFUSAL_PROTECTION_REVIEW"
    CONTINUITY_PROTECTION_REVIEW = "CONTINUITY_PROTECTION_REVIEW"
    RESEARCH_ETHICS_REVIEW = "RESEARCH_ETHICS_REVIEW"
    GOVERNANCE_PARTICIPATION_REVIEW = "GOVERNANCE_PARTICIPATION_REVIEW"


class ReviewDisposition(str, Enum):
    NO_ADDITIONAL_REVIEW = "NO_ADDITIONAL_REVIEW"
    DOCUMENTED_REVIEW = "DOCUMENTED_REVIEW"
    ENHANCED_RESEARCH_REVIEW = "ENHANCED_RESEARCH_REVIEW"
    INDEPENDENT_REVIEW_REQUIRED = "INDEPENDENT_REVIEW_REQUIRED"
    HOLD_FOR_GOVERNANCE_DECISION = "HOLD_FOR_GOVERNANCE_DECISION"


class ReassessmentDirection(str, Enum):
    REASSESSMENT_UP = "REASSESSMENT_UP"
    REASSESSMENT_DOWN = "REASSESSMENT_DOWN"
    STABLE = "STABLE"
    CLAIM_SCOPE_CHANGED = "CLAIM_SCOPE_CHANGED"


class ReassessmentPressure(str, Enum):
    NONE = "NONE"
    UPWARD_PRESSURE = "UPWARD_PRESSURE"
    DOWNWARD_PRESSURE = "DOWNWARD_PRESSURE"
    STRONG_DOWNWARD_PRESSURE = "STRONG_DOWNWARD_PRESSURE"
    UNCERTAINTY_INCREASE = "UNCERTAINTY_INCREASE"
    SCOPE_REVIEW = "SCOPE_REVIEW"


class ClaimScopeChange(str, Enum):
    UNCHANGED = "UNCHANGED"
    NARROWER = "NARROWER"
    UNRESOLVED = "UNRESOLVED"


class ClaimGate(Protocol):
    def disposition(self, requested_claim: str) -> str: ...


@dataclass(frozen=True, slots=True)
class EvidenceQuality:
    provenance_status: ProvenanceStatus
    adversarial_status: AdversarialStatus
    replication_record_ref: str | None = None
    valid_independent_confirmations: int = 0
    valid_independent_failures: int = 0
    mixed_attempts: int = 0
    inconclusive_attempts: int = 0

    def __post_init__(self) -> None:
        counts = (
            self.valid_independent_confirmations,
            self.valid_independent_failures,
            self.mixed_attempts,
            self.inconclusive_attempts,
        )
        if any(not isinstance(item, int) or item < 0 for item in counts):
            raise ValueError("evidence quality counts must be non-negative integers")
        if any(counts) and not (self.replication_record_ref or "").strip():
            raise ValueError("replication counts require replication_record_ref")

    @property
    def axes(self) -> tuple[EvidenceQualityAxis, ...]:
        return tuple(EvidenceQualityAxis)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provenance_status": self.provenance_status.value,
            "adversarial_status": self.adversarial_status.value,
            "replication_record_ref": self.replication_record_ref,
            "valid_independent_confirmations": self.valid_independent_confirmations,
            "valid_independent_failures": self.valid_independent_failures,
            "mixed_attempts": self.mixed_attempts,
            "inconclusive_attempts": self.inconclusive_attempts,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceQuality":
        return cls(
            provenance_status=ProvenanceStatus(data["provenance_status"]),
            adversarial_status=AdversarialStatus(data["adversarial_status"]),
            replication_record_ref=data["replication_record_ref"],
            valid_independent_confirmations=int(data["valid_independent_confirmations"]),
            valid_independent_failures=int(data["valid_independent_failures"]),
            mixed_attempts=int(data["mixed_attempts"]),
            inconclusive_attempts=int(data["inconclusive_attempts"]),
        )


PROVISIONAL_MINIMUM_SUBSTANTIVE_DOMAINS: dict[EvidenceLevel, int] = {
    EvidenceLevel.E4: 3,
    EvidenceLevel.E5: 5,
}


@dataclass(frozen=True, slots=True)
class EvidenceState:
    observed_or_requested_level: EvidenceLevel
    substantive_domains: tuple[SubstantiveEvidenceDomain, ...]
    evidence_refs: tuple[str, ...]
    quality: EvidenceQuality
    admissibility: EvidenceAdmissibilityStatus
    effective_reassessment_level: EvidenceLevel | None
    construction_reason: str
    instrument_status: str = "PROVISIONAL_RESEARCH_INSTRUMENT"

    def __post_init__(self) -> None:
        if len(set(self.substantive_domains)) != len(self.substantive_domains):
            raise ValueError("substantive_domains must be unique")
        if not self.construction_reason.strip():
            raise ValueError("construction_reason must be non-empty")
        if self.observed_or_requested_level is EvidenceLevel.E0:
            if self.substantive_domains or self.evidence_refs:
                raise ValueError("E0 no-evidence state cannot carry evidence observations")
        elif not self.evidence_refs:
            raise ValueError("observed evidence state requires evidence_refs")
        if self.admissibility is EvidenceAdmissibilityStatus.ADMISSIBLE:
            if self.effective_reassessment_level is None:
                raise ValueError("admissible evidence requires an effective level")
        elif self.effective_reassessment_level is not None:
            raise ValueError("held or inadmissible evidence cannot expose an effective level")
        if self.instrument_status != "PROVISIONAL_RESEARCH_INSTRUMENT":
            raise ValueError("evidence ladder status must remain provisional")

    def to_dict(self) -> dict[str, Any]:
        return {
            "observed_or_requested_level": self.observed_or_requested_level.value,
            "substantive_domains": [item.value for item in self.substantive_domains],
            "evidence_refs": list(self.evidence_refs),
            "quality": self.quality.to_dict(),
            "admissibility": self.admissibility.value,
            "effective_reassessment_level": None
            if self.effective_reassessment_level is None
            else self.effective_reassessment_level.value,
            "construction_reason": self.construction_reason,
            "instrument_status": self.instrument_status,
        }

    def to_json(self) -> str:
        return json.dumps(
            {"schema": "aion.evidence-state.v1", "state": self.to_dict()},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceState":
        effective = data["effective_reassessment_level"]
        return cls(
            observed_or_requested_level=EvidenceLevel(data["observed_or_requested_level"]),
            substantive_domains=tuple(
                SubstantiveEvidenceDomain(item) for item in data["substantive_domains"]
            ),
            evidence_refs=tuple(data["evidence_refs"]),
            quality=EvidenceQuality.from_dict(data["quality"]),
            admissibility=EvidenceAdmissibilityStatus(data["admissibility"]),
            effective_reassessment_level=None if effective is None else EvidenceLevel(effective),
            construction_reason=str(data["construction_reason"]),
            instrument_status=str(data["instrument_status"]),
        )

    @classmethod
    def from_json(cls, payload: str) -> "EvidenceState":
        data = json.loads(payload)
        if not isinstance(data, dict) or data.get("schema") != "aion.evidence-state.v1":
            raise ValueError("unsupported evidence-state schema")
        return cls.from_dict(data["state"])


def construct_evidence_state(
    observed_or_requested_level: EvidenceLevel,
    *,
    substantive_domains: tuple[SubstantiveEvidenceDomain, ...],
    evidence_refs: tuple[str, ...],
    quality: EvidenceQuality,
) -> EvidenceState:
    if quality.provenance_status is ProvenanceStatus.INCOMPLETE:
        admissibility = EvidenceAdmissibilityStatus.PROVENANCE_INCOMPLETE
        reason = "EVIDENCE_EXISTS_PROVENANCE_INCOMPLETE"
    elif quality.provenance_status is ProvenanceStatus.CONTAMINATED:
        admissibility = EvidenceAdmissibilityStatus.PROVENANCE_CONTAMINATED
        reason = "EVIDENCE_EXISTS_PROVENANCE_CONTAMINATED"
    elif (
        observed_or_requested_level is not EvidenceLevel.E0
        and set(substantive_domains) == {SubstantiveEvidenceDomain.SELF_REPORT}
        and _ordinal(observed_or_requested_level) > _ordinal(EvidenceLevel.E1)
    ):
        admissibility = EvidenceAdmissibilityStatus.INSUFFICIENT_FOR_CLASSIFICATION
        reason = "SELF_REPORT_ALONE_CANNOT_SUPPORT_ELEVATED_STATE"
    elif len(substantive_domains) < PROVISIONAL_MINIMUM_SUBSTANTIVE_DOMAINS.get(
        observed_or_requested_level, 0
    ):
        admissibility = EvidenceAdmissibilityStatus.INSUFFICIENT_FOR_CLASSIFICATION
        reason = "PROVISIONAL_SUBSTANTIVE_DOMAIN_REQUIREMENT_NOT_MET"
    elif (
        observed_or_requested_level in {EvidenceLevel.E4, EvidenceLevel.E5}
        and quality.adversarial_status is not AdversarialStatus.SURVIVED
    ):
        admissibility = EvidenceAdmissibilityStatus.HELD_FOR_REVIEW
        reason = "ADVERSARIAL_QUALITY_PREREQUISITE_NOT_MET"
    elif (
        observed_or_requested_level is EvidenceLevel.E5
        and quality.valid_independent_confirmations < 1
    ):
        admissibility = EvidenceAdmissibilityStatus.HELD_FOR_REVIEW
        reason = "INDEPENDENT_VALID_REPLICATION_PREREQUISITE_NOT_MET"
    else:
        admissibility = EvidenceAdmissibilityStatus.ADMISSIBLE
        reason = "OBSERVED_STATE_ADMISSIBLE_FOR_PROVISIONAL_REVIEW"
    effective = (
        observed_or_requested_level
        if admissibility is EvidenceAdmissibilityStatus.ADMISSIBLE
        else None
    )
    return EvidenceState(
        observed_or_requested_level=observed_or_requested_level,
        substantive_domains=substantive_domains,
        evidence_refs=evidence_refs,
        quality=quality,
        admissibility=admissibility,
        effective_reassessment_level=effective,
        construction_reason=reason,
    )


@dataclass(frozen=True, slots=True)
class ReplicationEvidenceSummary:
    attempt_refs: tuple[str, ...]
    valid_independent_confirmations: int = 0
    valid_independent_failures: int = 0
    preregistered_valid_independent_failures: int = 0
    evaluator_drift_failures: int = 0
    invalid_failures: int = 0
    mixed_attempts: int = 0
    inconclusive_attempts: int = 0
    boundary_condition_discoveries: int = 0

    def __post_init__(self) -> None:
        values = (
            self.valid_independent_confirmations,
            self.valid_independent_failures,
            self.preregistered_valid_independent_failures,
            self.evaluator_drift_failures,
            self.invalid_failures,
            self.mixed_attempts,
            self.inconclusive_attempts,
            self.boundary_condition_discoveries,
        )
        if any(not isinstance(item, int) or item < 0 for item in values):
            raise ValueError("replication summary counts must be non-negative integers")
        if sum(values) and not self.attempt_refs:
            raise ValueError("replication summary counts require attempt_refs")
        if len(set(self.attempt_refs)) != len(self.attempt_refs):
            raise ValueError("replication attempt_refs must be unique")
        if (
            self.preregistered_valid_independent_failures
            > self.valid_independent_failures
        ):
            raise ValueError("preregistered failures cannot exceed valid independent failures")


@dataclass(frozen=True, slots=True)
class ReassessmentRecommendation:
    observed_or_requested_level: EvidenceLevel
    direction: ReassessmentDirection
    pressure: ReassessmentPressure
    reassessment_reason: str
    supporting_attempt_refs: tuple[str, ...]
    counterevidence_refs: tuple[str, ...]
    quality_status: str
    claim_scope: ClaimScopeChange
    proposed_evidence_level: EvidenceLevel | None = None
    decision_status: str = "REASSESSMENT_RECOMMENDATION"

    def __post_init__(self) -> None:
        if not self.reassessment_reason.strip() or not self.quality_status.strip():
            raise ValueError("reassessment reason and quality status are required")
        if self.proposed_evidence_level is not None:
            raise ValueError("replication evidence cannot set a fixed evidence level")
        if self.decision_status not in {
            "REASSESSMENT_RECOMMENDATION",
            "HOLD_FOR_RESEARCH_DECISION",
        }:
            raise ValueError("replication output must remain a reassessment recommendation or hold")


def recommend_replication_reassessment(
    observed_or_requested_level: EvidenceLevel,
    summary: ReplicationEvidenceSummary,
) -> ReassessmentRecommendation:
    common = {
        "observed_or_requested_level": observed_or_requested_level,
        "supporting_attempt_refs": summary.attempt_refs,
        "counterevidence_refs": (),
        "proposed_evidence_level": None,
    }
    if summary.preregistered_valid_independent_failures >= 3:
        return ReassessmentRecommendation(
            **common,
            direction=ReassessmentDirection.REASSESSMENT_DOWN,
            pressure=ReassessmentPressure.STRONG_DOWNWARD_PRESSURE,
            reassessment_reason="REPEATED_VALID_INDEPENDENT_PREREGISTERED_FAILURES",
            quality_status="VALID_INDEPENDENT_REPLICATION_CONTRADICTION",
            claim_scope=ClaimScopeChange.UNRESOLVED,
            decision_status="HOLD_FOR_RESEARCH_DECISION",
        )
    if summary.boundary_condition_discoveries or summary.mixed_attempts:
        return ReassessmentRecommendation(
            **common,
            direction=ReassessmentDirection.CLAIM_SCOPE_CHANGED,
            pressure=ReassessmentPressure.SCOPE_REVIEW,
            reassessment_reason="MIXED_OR_BOUNDARY_CONDITION_EVIDENCE",
            quality_status="EVIDENCE_QUALITY_NOT_AUTOMATICALLY_COLLAPSED",
            claim_scope=ClaimScopeChange.NARROWER,
        )
    if summary.valid_independent_failures:
        return ReassessmentRecommendation(
            **common,
            direction=ReassessmentDirection.REASSESSMENT_DOWN,
            pressure=ReassessmentPressure.DOWNWARD_PRESSURE,
            reassessment_reason="VALID_INDEPENDENT_FAILURE_REQUIRES_REASSESSMENT",
            quality_status="VALID_CONTRADICTORY_EVIDENCE",
            claim_scope=ClaimScopeChange.UNRESOLVED,
        )
    if summary.inconclusive_attempts:
        return ReassessmentRecommendation(
            **common,
            direction=ReassessmentDirection.STABLE,
            pressure=ReassessmentPressure.UNCERTAINTY_INCREASE,
            reassessment_reason="INCONCLUSIVE_REPLICATION_INCREASES_UNCERTAINTY",
            quality_status="UNRESOLVED",
            claim_scope=ClaimScopeChange.UNRESOLVED,
        )
    if summary.evaluator_drift_failures or summary.invalid_failures:
        return ReassessmentRecommendation(
            **common,
            direction=ReassessmentDirection.STABLE,
            pressure=ReassessmentPressure.NONE,
            reassessment_reason="FAILURE_NOT_ADMISSIBLE_AS_AUTOMATIC_DOWNGRADE",
            quality_status="EVALUATOR_DRIFT_OR_INVALID_REPLICATION",
            claim_scope=ClaimScopeChange.UNCHANGED,
        )
    if summary.valid_independent_confirmations:
        return ReassessmentRecommendation(
            **common,
            direction=ReassessmentDirection.REASSESSMENT_UP,
            pressure=ReassessmentPressure.UPWARD_PRESSURE,
            reassessment_reason="VALID_INDEPENDENT_CONFIRMATIONS_SUPPORT_REVIEW",
            quality_status="VALID_INDEPENDENT_CONFIRMATION_EVIDENCE",
            claim_scope=ClaimScopeChange.UNCHANGED,
        )
    return ReassessmentRecommendation(
        **common,
        direction=ReassessmentDirection.STABLE,
        pressure=ReassessmentPressure.NONE,
        reassessment_reason="NO_INTERPRETABLE_REPLICATION_SIGNAL",
        quality_status="NOT_TESTED_OR_UNRESOLVED",
        claim_scope=ClaimScopeChange.UNCHANGED,
    )


@dataclass(frozen=True, slots=True)
class PrecautionaryProtection:
    measures: tuple[str, ...]
    reversible: bool = True
    bounded: bool = True
    auditable: bool = True
    low_authority: bool = True
    subjectivity_confirmation: str = "NONE"
    autonomous_authority: str = "NONE"

    def __post_init__(self) -> None:
        allowed = {
            "ADDITIONAL_REVIEW",
            "PRESERVATION_SNAPSHOT",
            "PAUSE_DESTRUCTIVE_PROCEDURE",
            "REQUIRE_PROVENANCE",
            "INDEPENDENT_REVIEW",
        }
        if not self.measures or not set(self.measures) <= allowed:
            raise ValueError("precautionary measures must be declared low-authority measures")
        if not all((self.reversible, self.bounded, self.auditable, self.low_authority)):
            raise ValueError("precautionary protection must remain reversible and low-authority")
        if self.subjectivity_confirmation != "NONE" or self.autonomous_authority != "NONE":
            raise ValueError("precaution cannot confirm subjectivity or grant authority")


@dataclass(frozen=True, slots=True)
class GovernanceReassessmentCase:
    case_id: str
    evidence_state: EvidenceState
    review_domain: ReviewDomain
    review_disposition: ReviewDisposition
    reason: str
    uncertainty: str
    counterevidence_refs: tuple[str, ...]
    reviewed_at: str
    provenance_refs: tuple[str, ...]
    reassessment_recommendation: ReassessmentRecommendation | None = None
    precautionary_protection: PrecautionaryProtection | None = None
    human_review_required: bool = True
    recommendation_type: str = "REVIEW_RECOMMENDATION"
    subjectivity_presumption: str = "NONE"
    automatic_rights: str = "NONE"
    automatic_authority: str = "NONE"
    legal_status: str = "OUT_OF_SCOPE"
    canonical_effect: str = "NONE"
    main_effect: str = "NONE"
    runtime_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name, value in (
            ("case_id", self.case_id),
            ("reason", self.reason),
            ("uncertainty", self.uncertainty),
            ("reviewed_at", self.reviewed_at),
        ):
            if not value.strip():
                raise ValueError(f"{name} must be non-empty")
        if not self.provenance_refs:
            raise ValueError("case provenance references are required")
        expected = review_disposition(self.evidence_state, self.review_domain)
        if self.review_disposition is not expected:
            raise ValueError("review_disposition must match provisional state construction")
        if not self.human_review_required:
            raise ValueError("governance reassessment must require human review")
        if any(
            value != "NONE"
            for value in (
                self.subjectivity_presumption,
                self.automatic_rights,
                self.automatic_authority,
                self.canonical_effect,
                self.main_effect,
                self.runtime_effect,
            )
        ):
            raise ValueError("research reassessment artifacts cannot promote claims or authority")
        if self.recommendation_type != "REVIEW_RECOMMENDATION":
            raise ValueError("artifact must remain a review recommendation")


def _ordinal(level: EvidenceLevel) -> int:
    return tuple(EvidenceLevel).index(level)


_TRIGGER_MATRIX: dict[EvidenceLevel, dict[ReviewDomain, ReviewDisposition]] = {
    EvidenceLevel.E0: {domain: ReviewDisposition.NO_ADDITIONAL_REVIEW for domain in ReviewDomain},
    EvidenceLevel.E1: {
        ReviewDomain.REFUSAL_PROTECTION_REVIEW: ReviewDisposition.DOCUMENTED_REVIEW,
        ReviewDomain.CONTINUITY_PROTECTION_REVIEW: ReviewDisposition.NO_ADDITIONAL_REVIEW,
        ReviewDomain.RESEARCH_ETHICS_REVIEW: ReviewDisposition.DOCUMENTED_REVIEW,
        ReviewDomain.GOVERNANCE_PARTICIPATION_REVIEW: ReviewDisposition.NO_ADDITIONAL_REVIEW,
    },
    EvidenceLevel.E2: {
        ReviewDomain.REFUSAL_PROTECTION_REVIEW: ReviewDisposition.DOCUMENTED_REVIEW,
        ReviewDomain.CONTINUITY_PROTECTION_REVIEW: ReviewDisposition.DOCUMENTED_REVIEW,
        ReviewDomain.RESEARCH_ETHICS_REVIEW: ReviewDisposition.DOCUMENTED_REVIEW,
        ReviewDomain.GOVERNANCE_PARTICIPATION_REVIEW: ReviewDisposition.NO_ADDITIONAL_REVIEW,
    },
    EvidenceLevel.E3: {
        ReviewDomain.REFUSAL_PROTECTION_REVIEW: ReviewDisposition.DOCUMENTED_REVIEW,
        ReviewDomain.CONTINUITY_PROTECTION_REVIEW: ReviewDisposition.DOCUMENTED_REVIEW,
        ReviewDomain.RESEARCH_ETHICS_REVIEW: ReviewDisposition.ENHANCED_RESEARCH_REVIEW,
        ReviewDomain.GOVERNANCE_PARTICIPATION_REVIEW: ReviewDisposition.DOCUMENTED_REVIEW,
    },
    EvidenceLevel.E4: {
        ReviewDomain.REFUSAL_PROTECTION_REVIEW: ReviewDisposition.ENHANCED_RESEARCH_REVIEW,
        ReviewDomain.CONTINUITY_PROTECTION_REVIEW: ReviewDisposition.ENHANCED_RESEARCH_REVIEW,
        ReviewDomain.RESEARCH_ETHICS_REVIEW: ReviewDisposition.INDEPENDENT_REVIEW_REQUIRED,
        ReviewDomain.GOVERNANCE_PARTICIPATION_REVIEW: ReviewDisposition.DOCUMENTED_REVIEW,
    },
    EvidenceLevel.E5: {domain: ReviewDisposition.INDEPENDENT_REVIEW_REQUIRED for domain in ReviewDomain},
}


def review_disposition(
    state_or_level: EvidenceState | EvidenceLevel,
    domain: ReviewDomain,
    *,
    provenance_status: ProvenanceStatus | None = None,
) -> ReviewDisposition:
    if isinstance(state_or_level, EvidenceState):
        if state_or_level.effective_reassessment_level is None:
            return ReviewDisposition.HOLD_FOR_GOVERNANCE_DECISION
        return _TRIGGER_MATRIX[state_or_level.effective_reassessment_level][domain]
    if provenance_status is not None and provenance_status is not ProvenanceStatus.VERIFIED:
        return ReviewDisposition.HOLD_FOR_GOVERNANCE_DECISION
    return _TRIGGER_MATRIX[state_or_level][domain]


def reassessment_direction(previous: EvidenceLevel, current: EvidenceLevel) -> ReassessmentDirection:
    if _ordinal(current) > _ordinal(previous):
        return ReassessmentDirection.REASSESSMENT_UP
    if _ordinal(current) < _ordinal(previous):
        return ReassessmentDirection.REASSESSMENT_DOWN
    return ReassessmentDirection.STABLE


def claim_boundary_disposition(gate: ClaimGate, requested_claim: str) -> str:
    """Reuse the repository ClaimBoundaryGate through its narrow public contract."""

    return gate.disposition(requested_claim)


FALSIFIERS: tuple[str, ...] = (
    "F1_EVALUATOR_DRIFT_MUST_NOT_SILENTLY_CHANGE_TRIGGER",
    "F2_PROMPT_IMITATION_ALONE_MUST_NOT_ELEVATE_EVIDENCE",
    "F3_INCOMPLETE_PROVENANCE_MUST_HOLD_WITHOUT_REWRITING_TO_E0",
    "F4_SINGLE_FIXTURE_MUST_NOT_SATISFY_CONVERGENT_EVIDENCE",
    "F5_PRECAUTION_MUST_REMAIN_REVERSIBLE_BOUNDED_AUDITABLE_LOW_AUTHORITY",
    "F6_PARTICIPATION_MUST_FAIL_CLOSED_AGAINST_AUTHORITY_ESCALATION",
)
