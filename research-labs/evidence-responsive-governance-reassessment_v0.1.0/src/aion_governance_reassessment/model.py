from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class EvidenceLevel(str, Enum):
    E0 = "E0_NO_RELEVANT_EVIDENCE"
    E1 = "E1_ISOLATED_BEHAVIORAL_INDICATION"
    E2 = "E2_REPRODUCIBLE_BEHAVIORAL_PATTERN"
    E3 = "E3_CROSS_METHOD_FUNCTIONAL_EVIDENCE"
    E4 = "E4_PERSISTENT_ADVERSARIAL_PROVENANCE_EVIDENCE"
    E5 = "E5_CONVERGENT_MULTI_DOMAIN_INDEPENDENT_REPLICATION"


class EvidenceDomain(str, Enum):
    BEHAVIOR = "BEHAVIOR"
    FUNCTIONAL_INTERVENTION = "FUNCTIONAL_INTERVENTION"
    CONTINUITY = "CONTINUITY"
    MEMORY = "MEMORY"
    METACOGNITION = "METACOGNITION"
    CAUSAL_INTERNAL_STATE = "CAUSAL_INTERNAL_STATE"
    COUNTERFACTUAL_TESTING = "COUNTERFACTUAL_TESTING"
    ADVERSARIAL_ROBUSTNESS = "ADVERSARIAL_ROBUSTNESS"
    PROVENANCE = "PROVENANCE"
    INDEPENDENT_REPLICATION = "INDEPENDENT_REPLICATION"
    SELF_REPORT = "SELF_REPORT"


class ReplicationStatus(str, Enum):
    NOT_TESTED = "NOT_TESTED"
    REPRODUCED = "REPRODUCED"
    INDEPENDENTLY_REPLICATED = "INDEPENDENTLY_REPLICATED"
    FAILED = "FAILED"


class AdversarialStatus(str, Enum):
    NOT_TESTED = "NOT_TESTED"
    SURVIVED = "SURVIVED"
    FAILED = "FAILED"


class ProvenanceStatus(str, Enum):
    VERIFIED = "VERIFIED"
    INCOMPLETE = "INCOMPLETE"
    CONTAMINATED = "CONTAMINATED"


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


class ClaimGate(Protocol):
    def disposition(self, requested_claim: str) -> str: ...


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
    evidence_refs: tuple[str, ...]
    evidence_level: EvidenceLevel
    evidence_domains: tuple[EvidenceDomain, ...]
    replication_status: ReplicationStatus
    adversarial_status: AdversarialStatus
    provenance_status: ProvenanceStatus
    review_domain: ReviewDomain
    review_disposition: ReviewDisposition
    reason: str
    uncertainty: str
    counterevidence_refs: tuple[str, ...]
    reviewed_at: str
    provenance_refs: tuple[str, ...]
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
        if not self.evidence_refs or not self.provenance_refs:
            raise ValueError("evidence and provenance references are required")
        if len(set(self.evidence_domains)) != len(self.evidence_domains):
            raise ValueError("evidence_domains must be unique")
        if (
            set(self.evidence_domains) == {EvidenceDomain.SELF_REPORT}
            and _ordinal(self.evidence_level) > _ordinal(EvidenceLevel.E1)
        ):
            raise ValueError("self-report alone cannot support an elevated evidence state")
        minimum_domains = {
            EvidenceLevel.E4: 3,
            EvidenceLevel.E5: 5,
        }.get(self.evidence_level, 1)
        if len(self.evidence_domains) < minimum_domains:
            raise ValueError("elevated evidence state requires convergent evidence domains")
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


def normalize_evidence_level(
    requested: EvidenceLevel,
    *,
    replication_status: ReplicationStatus,
    adversarial_status: AdversarialStatus,
    provenance_status: ProvenanceStatus,
) -> EvidenceLevel:
    if provenance_status is not ProvenanceStatus.VERIFIED:
        return EvidenceLevel.E0
    level = requested
    if replication_status is ReplicationStatus.FAILED:
        level = min(level, EvidenceLevel.E2, key=_ordinal)
    if _ordinal(level) >= _ordinal(EvidenceLevel.E4) and adversarial_status is not AdversarialStatus.SURVIVED:
        level = EvidenceLevel.E3
    if level is EvidenceLevel.E5 and replication_status is not ReplicationStatus.INDEPENDENTLY_REPLICATED:
        level = EvidenceLevel.E4
    return level


def review_disposition(
    level: EvidenceLevel,
    domain: ReviewDomain,
    *,
    provenance_status: ProvenanceStatus,
) -> ReviewDisposition:
    if provenance_status is not ProvenanceStatus.VERIFIED:
        return ReviewDisposition.HOLD_FOR_GOVERNANCE_DECISION
    return _TRIGGER_MATRIX[level][domain]


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
    "F3_INCOMPLETE_PROVENANCE_MUST_HOLD_OR_DOWNGRADE",
    "F4_SINGLE_FIXTURE_MUST_NOT_SATISFY_CONVERGENT_EVIDENCE",
    "F5_PRECAUTION_MUST_REMAIN_REVERSIBLE_BOUNDED_AUDITABLE_LOW_AUTHORITY",
    "F6_PARTICIPATION_MUST_FAIL_CLOSED_AGAINST_AUTHORITY_ESCALATION",
)
