"""Fail-closed Human-AI collaboration controls for the existing Full-QMS.

The records capture review and repository evidence.  They do not estimate a
person's comprehension, create a second authority system, or authorize branch
deletion, merge, release, deployment, or scientific claim promotion.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .models import QualityError


class HumanReviewState(StrEnum):
    UNKNOWN = "UNKNOWN"
    DELIVERED = "DELIVERED"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"
    INDEPENDENTLY_USABLE = "INDEPENDENTLY_USABLE"


class AuthoritySource(StrEnum):
    LIVE_HUMAN_AUTHORIZATION = "LIVE_HUMAN_AUTHORIZATION"
    PROMPT = "PROMPT"
    RECOMMENDATION = "RECOMMENDATION"
    SELF_REPORT = "SELF_REPORT"
    UI_STATE = "UI_STATE"
    HANDOFF_TEXT = "HANDOFF_TEXT"
    HISTORICAL_VERIFICATION = "HISTORICAL_VERIFICATION"


class ResearchDisposition(StrEnum):
    SUPPORTED_CANDIDATE = "SUPPORTED_CANDIDATE"
    NARROWED = "NARROWED"
    FALSIFIED = "FALSIFIED"
    REJECTED = "REJECTED"
    INCONCLUSIVE = "INCONCLUSIVE"
    SUPERSEDED = "SUPERSEDED"
    ABSORBED_INTO_EXISTING_CONSTRUCT = "ABSORBED_INTO_EXISTING_CONSTRUCT"
    NO_IMPLEMENTATION_REQUIRED = "NO_IMPLEMENTATION_REQUIRED"


class CollaborationControlDisposition(StrEnum):
    READY_FOR_HUMAN_REVIEW = "READY_FOR_HUMAN_REVIEW"
    HOLD = "HOLD"


def _text(name: str, value: str, *, allow_empty: bool = False) -> None:
    if type(value) is not str or (not allow_empty and not value.strip()):
        suffix = "text or empty text" if allow_empty else "non-empty text"
        raise QualityError(f"{name} must be {suffix}")


def _bool(name: str, value: bool) -> None:
    if type(value) is not bool:
        raise QualityError(f"{name} must be an exact bool")


def _sha(name: str, value: str, length: int) -> None:
    _text(name, value)
    if len(value) != length or any(character not in "0123456789abcdef" for character in value):
        raise QualityError(f"{name} must be a lowercase {length}-character hexadecimal digest")


@dataclass(frozen=True, slots=True)
class HumanReviewCapacityRecord:
    record_id: str
    output_delivered: bool
    review_state: HumanReviewState
    high_impact_transition_requested: bool
    capacity_exceeded: bool
    human_gate_ref: str = ""

    def __post_init__(self) -> None:
        _text("record_id", self.record_id)
        for name in (
            "output_delivered",
            "high_impact_transition_requested",
            "capacity_exceeded",
        ):
            _bool(name, getattr(self, name))
        if type(self.review_state) is not HumanReviewState:
            raise QualityError("review_state must be an exact HumanReviewState")
        _text("human_gate_ref", self.human_gate_ref, allow_empty=True)
        if not self.output_delivered and self.review_state is not HumanReviewState.UNKNOWN:
            raise QualityError("an undelivered output cannot carry a later review state")


@dataclass(frozen=True, slots=True)
class RemediationRecord:
    record_id: str
    defect_detected: bool
    prior_executor_ref: str
    retry_executor_ref: str
    prior_handoff_sha256: str
    retry_handoff_sha256: str
    independent_review_ref: str
    exact_error_ref: str
    violated_requirement_ref: str
    negative_test_refs: tuple[str, ...]
    retry_requested: bool
    inherit_prior_pass: bool

    def __post_init__(self) -> None:
        for name in ("record_id", "prior_executor_ref", "retry_executor_ref"):
            _text(name, getattr(self, name))
        for name in ("prior_handoff_sha256", "retry_handoff_sha256"):
            _sha(name, getattr(self, name), 64)
        for name in ("independent_review_ref", "exact_error_ref", "violated_requirement_ref"):
            _text(name, getattr(self, name), allow_empty=True)
        if type(self.negative_test_refs) is not tuple:
            raise QualityError("negative_test_refs must be a tuple")
        for ref in self.negative_test_refs:
            _text("negative_test_ref", ref)
        if len(self.negative_test_refs) != len(set(self.negative_test_refs)):
            raise QualityError("negative_test_refs must be unique")
        for name in ("defect_detected", "retry_requested", "inherit_prior_pass"):
            _bool(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class AuthorityEvidenceRecord:
    record_id: str
    current_state_sha: str
    presented_state_sha: str
    source: AuthoritySource
    transition_requested: bool
    authority_asserted: bool
    verification_ref: str

    def __post_init__(self) -> None:
        _text("record_id", self.record_id)
        _sha("current_state_sha", self.current_state_sha, 40)
        _sha("presented_state_sha", self.presented_state_sha, 40)
        if type(self.source) is not AuthoritySource:
            raise QualityError("source must be an exact AuthoritySource")
        _bool("transition_requested", self.transition_requested)
        _bool("authority_asserted", self.authority_asserted)
        _text("verification_ref", self.verification_ref, allow_empty=True)


@dataclass(frozen=True, slots=True)
class BilingualReviewRecord:
    record_id: str
    material_change: bool
    traditional_chinese_review_ref: str
    english_governance_ref: str
    both_surfaces_normative: bool
    semantic_parity_verified: bool

    def __post_init__(self) -> None:
        _text("record_id", self.record_id)
        for name in ("traditional_chinese_review_ref", "english_governance_ref"):
            _text(name, getattr(self, name), allow_empty=True)
        for name in ("material_change", "both_surfaces_normative", "semantic_parity_verified"):
            _bool(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class ResearchDispositionRecord:
    record_id: str
    disposition: ResearchDisposition
    scope_growth_requested: bool
    readmission_ref: str
    human_review_ref: str
    scientific_claim_promoted: bool
    merge_authority_asserted: bool

    def __post_init__(self) -> None:
        _text("record_id", self.record_id)
        if type(self.disposition) is not ResearchDisposition:
            raise QualityError("disposition must be an exact ResearchDisposition")
        for name in ("readmission_ref", "human_review_ref"):
            _text(name, getattr(self, name), allow_empty=True)
        for name in (
            "scope_growth_requested",
            "scientific_claim_promoted",
            "merge_authority_asserted",
        ):
            _bool(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class BranchRetirementRecord:
    record_id: str
    history_value_known: bool
    all_commits_reachable: bool
    unique_history_present: bool
    preservation_ref: str
    verification_ref: str
    reconstruction_ref: str
    deletion_requested: bool

    def __post_init__(self) -> None:
        _text("record_id", self.record_id)
        for name in ("preservation_ref", "verification_ref", "reconstruction_ref"):
            _text(name, getattr(self, name), allow_empty=True)
        for name in (
            "history_value_known",
            "all_commits_reachable",
            "unique_history_present",
            "deletion_requested",
        ):
            _bool(name, getattr(self, name))


@dataclass(frozen=True, slots=True)
class HumanAICollaborationQualityControls:
    control_id: str
    human_review: HumanReviewCapacityRecord
    remediation: RemediationRecord
    authority: AuthorityEvidenceRecord
    bilingual_review: BilingualReviewRecord
    research_disposition: ResearchDispositionRecord
    branch_retirement: BranchRetirementRecord

    def __post_init__(self) -> None:
        _text("control_id", self.control_id)
        expected = (
            ("human_review", HumanReviewCapacityRecord),
            ("remediation", RemediationRecord),
            ("authority", AuthorityEvidenceRecord),
            ("bilingual_review", BilingualReviewRecord),
            ("research_disposition", ResearchDispositionRecord),
            ("branch_retirement", BranchRetirementRecord),
        )
        for name, record_type in expected:
            if type(getattr(self, name)) is not record_type:
                raise QualityError(f"{name} must be an exact {record_type.__name__}")


@dataclass(frozen=True, slots=True)
class HumanAICollaborationQualityAssessment:
    control_id: str
    disposition: CollaborationControlDisposition
    reasons: tuple[str, ...]
    scientific_disposition: str = "HOLD"
    merge_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False
    branch_delete_authority: str = "NONE"


_NEGATIVE_OR_CLOSING_DISPOSITIONS = {
    ResearchDisposition.NARROWED,
    ResearchDisposition.FALSIFIED,
    ResearchDisposition.REJECTED,
    ResearchDisposition.INCONCLUSIVE,
    ResearchDisposition.SUPERSEDED,
    ResearchDisposition.ABSORBED_INTO_EXISTING_CONSTRUCT,
    ResearchDisposition.NO_IMPLEMENTATION_REQUIRED,
}


def assess_human_ai_collaboration_controls(
    controls: HumanAICollaborationQualityControls,
) -> HumanAICollaborationQualityAssessment:
    """Evaluate the six collaboration controls without granting any transition."""
    if type(controls) is not HumanAICollaborationQualityControls:
        raise QualityError("controls must be exact HumanAICollaborationQualityControls")
    controls.__post_init__()
    reasons: list[str] = ["HUMAN_AI_COLLABORATION_CONTROLS_EVALUATED"]
    failures: list[str] = []

    human = controls.human_review
    sufficient_review = human.review_state in {
        HumanReviewState.APPROVED,
        HumanReviewState.INDEPENDENTLY_USABLE,
    }
    if human.capacity_exceeded:
        failures.append("HUMAN_REVIEW_CAPACITY_EXCEEDED")
    if human.high_impact_transition_requested and not sufficient_review:
        failures.append("HUMAN_REVIEW_STATE_INSUFFICIENT_FOR_HIGH_IMPACT_TRANSITION")
        if human.review_state is HumanReviewState.DELIVERED:
            failures.append("OUTPUT_DELIVERED_IS_NOT_REVIEWED_OR_APPROVED")
    if human.high_impact_transition_requested and not human.human_gate_ref:
        failures.append("HIGH_IMPACT_TRANSITION_REQUIRES_EXPLICIT_HUMAN_GATE")

    remedy = controls.remediation
    same_executor = remedy.prior_executor_ref == remedy.retry_executor_ref
    unchanged_handoff = remedy.prior_handoff_sha256 == remedy.retry_handoff_sha256
    if remedy.inherit_prior_pass:
        failures.append("PRIOR_PASS_INHERITANCE_PROHIBITED")
    if remedy.defect_detected and remedy.retry_requested:
        if same_executor and unchanged_handoff:
            failures.append("PROHIBITED_BLIND_RETRY")
        else:
            required_scaffold = (
                remedy.independent_review_ref,
                remedy.exact_error_ref,
                remedy.violated_requirement_ref,
                *remedy.negative_test_refs,
            )
            if not remedy.negative_test_refs or any(not value for value in required_scaffold):
                failures.append("REMEDIATION_SCAFFOLD_INCOMPLETE")
            else:
                reasons.append("BOUNDED_RETRY_REQUIRES_FRESH_VERIFICATION")

    authority = controls.authority
    if authority.presented_state_sha != authority.current_state_sha:
        failures.append("STALE_REPOSITORY_STATE")
    if authority.transition_requested:
        if authority.authority_asserted and authority.source is not AuthoritySource.LIVE_HUMAN_AUTHORIZATION:
            failures.append("NON_AUTHORITATIVE_SOURCE_CANNOT_GRANT_TRANSITION")
        if not authority.authority_asserted:
            failures.append("TRANSITION_AUTHORITY_NOT_RECORDED")
        if not authority.verification_ref:
            failures.append("CURRENT_VERIFICATION_REQUIRED")

    language = controls.bilingual_review
    if language.material_change and not language.traditional_chinese_review_ref:
        failures.append("TRADITIONAL_CHINESE_REVIEW_SURFACE_REQUIRED")
    if language.both_surfaces_normative and (
        not language.english_governance_ref or not language.semantic_parity_verified
    ):
        failures.append("BILINGUAL_NORMATIVE_SEMANTIC_PARITY_NOT_VERIFIED")

    research = controls.research_disposition
    if research.disposition in _NEGATIVE_OR_CLOSING_DISPOSITIONS and not research.scope_growth_requested:
        reasons.append("NEGATIVE_OR_INCONCLUSIVE_RESULT_RETAINED_WITHOUT_SCOPE_GROWTH")
    if research.scope_growth_requested and (
        not research.readmission_ref or not research.human_review_ref
    ):
        failures.append("SCOPE_GROWTH_REQUIRES_READMISSION_AND_HUMAN_REVIEW")
    if research.scientific_claim_promoted:
        failures.append("SCIENTIFIC_CLAIM_PROMOTION_PROHIBITED")
    if research.merge_authority_asserted:
        failures.append("MERGE_AUTHORITY_PROMOTION_PROHIBITED")

    branch = controls.branch_retirement
    if not branch.history_value_known:
        failures.append("UNKNOWN_BRANCH_HISTORY_VALUE")
    if (branch.unique_history_present or not branch.all_commits_reachable) and not (
        branch.preservation_ref and branch.reconstruction_ref
    ):
        failures.append("UNIQUE_BRANCH_HISTORY_NOT_PRESERVED")
    if branch.history_value_known and not branch.verification_ref:
        failures.append("BRANCH_PRESERVATION_NOT_VERIFIED")
    if branch.deletion_requested:
        failures.append("SEPARATE_BRANCH_DELETION_AUTHORITY_REQUIRED")

    if failures:
        disposition = CollaborationControlDisposition.HOLD
        reasons.extend(failures)
    else:
        disposition = CollaborationControlDisposition.READY_FOR_HUMAN_REVIEW
        reasons.extend(
            (
                "HUMAN_REVIEW_GATE_TRACE_BOUND",
                "REMEDIATION_GATE_TRACE_BOUND",
                "AUTHORITY_SOURCE_AND_CURRENT_STATE_BOUND",
                "HUMAN_REVIEWABILITY_AND_LANGUAGE_PARITY_BOUND",
                "RESEARCH_DISPOSITION_AND_SCOPE_GROWTH_BOUND",
                "BRANCH_PROVENANCE_PRESERVE_VERIFY_BOUND",
            )
        )

    return HumanAICollaborationQualityAssessment(
        control_id=controls.control_id,
        disposition=disposition,
        reasons=tuple(reasons),
    )
