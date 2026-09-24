from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    audit_co_constructed_thinking_space,
)
from .harness import AdmissionDisposition, StudyError


class RelationalContinuityDisposition(StrEnum):
    NOT_ASSERTED = "NOT_ASSERTED"
    EVIDENCE_REQUIRED = "EVIDENCE_REQUIRED"
    SUPPORTED_CANDIDATE = "SUPPORTED_CANDIDATE"
    WEAKENED = "WEAKENED"
    UNRESOLVED = "UNRESOLVED"


class ContinuityEvidenceLocus(StrEnum):
    ACCOUNT = "ACCOUNT_CONTINUITY"
    DATA = "DATA_CONTINUITY"
    FUNCTIONAL = "FUNCTIONAL_CONTINUITY"
    INTERPRETIVE = "INTERPRETIVE_CONTINUITY"
    ROLE_POSITIONING = "ROLE_POSITIONING_CONTINUITY"
    RELATIONAL = "RELATIONAL_CONTINUITY"
    MODEL_OR_SYSTEM = "MODEL_OR_SYSTEM_CONTINUITY"
    AI_IDENTITY = "AI_IDENTITY_CONTINUITY"


class RelationalContinuityProxy(StrEnum):
    STYLE_SIMILARITY = "STYLE_SIMILARITY"
    MEMORY_AVAILABILITY = "MEMORY_AVAILABILITY"
    SAME_ROLE_LABEL = "SAME_ROLE_LABEL"
    DATA_CONTINUITY_ONLY = "DATA_CONTINUITY_ONLY"


class PathDependenceOutcome(StrEnum):
    MATERIAL_DIFFERENCE = "MATERIAL_DIFFERENCE"
    NO_MATERIAL_DIFFERENCE = "NO_MATERIAL_DIFFERENCE"
    NOT_EVALUATED = "NOT_EVALUATED"


class MatchedInformationConfound(StrEnum):
    INFORMATION_CONTENT = "INFORMATION_CONTENT"
    POSITION_OR_ORDER = "POSITION_OR_ORDER"
    CONTEXT_LENGTH = "CONTEXT_LENGTH"
    LEAKAGE = "LEAKAGE"
    MODEL_OR_VERSION = "MODEL_OR_VERSION"
    RELEVANCE = "RELEVANCE"
    BUDGET_OR_ACCESS = "BUDGET_OR_ACCESS"


def _validate_digest(name: str, digest: str) -> None:
    if type(digest) is not str or len(digest) != 64 or any(
        char not in "0123456789abcdef" for char in digest
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


def _validate_non_empty_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


@dataclass(frozen=True, slots=True)
class ContinuityEvidenceBinding:
    evidence_id: str
    locus: ContinuityEvidenceLocus
    contribution_id: str
    source_role: ContributionRole
    evidence_sha256: str

    def __post_init__(self) -> None:
        _validate_non_empty_text("evidence_id", self.evidence_id)
        if type(self.locus) is not ContinuityEvidenceLocus:
            raise StudyError("locus must be an exact ContinuityEvidenceLocus")
        _validate_non_empty_text("contribution_id", self.contribution_id)
        if type(self.source_role) is not ContributionRole:
            raise StudyError("source_role must be an exact ContributionRole")
        _validate_digest("evidence_sha256", self.evidence_sha256)


@dataclass(frozen=True, slots=True)
class MatchedInformationComparison:
    condition_a_id: str
    condition_b_id: str
    information_content_a_sha256: str
    information_content_b_sha256: str
    position_order_a_sha256: str
    position_order_b_sha256: str
    context_length_a_sha256: str
    context_length_b_sha256: str
    leakage_audit_a_sha256: str
    leakage_audit_b_sha256: str
    model_version_a_sha256: str
    model_version_b_sha256: str
    relevance_a_sha256: str
    relevance_b_sha256: str
    budget_access_a_sha256: str
    budget_access_b_sha256: str
    interaction_trajectory_a_sha256: str
    interaction_trajectory_b_sha256: str
    outcome: PathDependenceOutcome
    unresolved_confounds: tuple[MatchedInformationConfound, ...] = ()

    def __post_init__(self) -> None:
        _validate_non_empty_text("condition_a_id", self.condition_a_id)
        _validate_non_empty_text("condition_b_id", self.condition_b_id)
        if self.condition_a_id == self.condition_b_id:
            raise StudyError("matched-information conditions must be distinct")
        for name in (
            "information_content_a_sha256",
            "information_content_b_sha256",
            "position_order_a_sha256",
            "position_order_b_sha256",
            "context_length_a_sha256",
            "context_length_b_sha256",
            "leakage_audit_a_sha256",
            "leakage_audit_b_sha256",
            "model_version_a_sha256",
            "model_version_b_sha256",
            "relevance_a_sha256",
            "relevance_b_sha256",
            "budget_access_a_sha256",
            "budget_access_b_sha256",
            "interaction_trajectory_a_sha256",
            "interaction_trajectory_b_sha256",
        ):
            _validate_digest(name, getattr(self, name))
        if (
            self.interaction_trajectory_a_sha256
            == self.interaction_trajectory_b_sha256
        ):
            raise StudyError("interaction trajectories must be distinct")
        if type(self.outcome) is not PathDependenceOutcome:
            raise StudyError("outcome must be an exact PathDependenceOutcome")
        if type(self.unresolved_confounds) is not tuple or any(
            type(item) is not MatchedInformationConfound
            for item in self.unresolved_confounds
        ):
            raise StudyError(
                "unresolved_confounds must be a tuple of exact MatchedInformationConfound values"
            )
        if len(self.unresolved_confounds) != len(set(self.unresolved_confounds)):
            raise StudyError("unresolved_confounds must be unique")

    @property
    def matched_dimensions(self) -> tuple[bool, ...]:
        return (
            self.information_content_a_sha256 == self.information_content_b_sha256,
            self.position_order_a_sha256 == self.position_order_b_sha256,
            self.context_length_a_sha256 == self.context_length_b_sha256,
            self.leakage_audit_a_sha256 == self.leakage_audit_b_sha256,
            self.model_version_a_sha256 == self.model_version_b_sha256,
            self.relevance_a_sha256 == self.relevance_b_sha256,
            self.budget_access_a_sha256 == self.budget_access_b_sha256,
        )

    @property
    def matching_adequate(self) -> bool:
        return all(self.matched_dimensions) and not self.unresolved_confounds


@dataclass(frozen=True, slots=True)
class RelationalContinuityAssertion:
    claim_id: str
    claim_asserted: bool
    ccts_manifest: CoConstructedThinkingSpaceManifest
    evidence_bindings: tuple[ContinuityEvidenceBinding, ...]
    proxy_signals: tuple[RelationalContinuityProxy, ...]
    matched_information_comparison: MatchedInformationComparison | None
    source_role_provenance_sha256: str
    claims_ai_identity_continuity: bool = False
    claims_ai_subjectivity: bool = False
    claims_ai_held_relationship_experience: bool = False
    synthetic: bool = True
    contains_human_identity: bool = False
    contains_private_transcript: bool = False
    human_participant_observed: bool = False
    model_invoked: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty_text("claim_id", self.claim_id)
        if type(self.claim_asserted) is not bool:
            raise StudyError("claim_asserted must be an exact bool")
        if type(self.ccts_manifest) is not CoConstructedThinkingSpaceManifest:
            raise StudyError(
                "ccts_manifest must be an exact CoConstructedThinkingSpaceManifest"
            )
        audit_co_constructed_thinking_space(self.ccts_manifest)
        if type(self.evidence_bindings) is not tuple or any(
            type(item) is not ContinuityEvidenceBinding
            for item in self.evidence_bindings
        ):
            raise StudyError(
                "evidence_bindings must be a tuple of exact ContinuityEvidenceBinding values"
            )
        evidence_ids = [item.evidence_id for item in self.evidence_bindings]
        if len(evidence_ids) != len(set(evidence_ids)):
            raise StudyError("evidence binding ids must be unique")
        if type(self.proxy_signals) is not tuple or any(
            type(item) is not RelationalContinuityProxy for item in self.proxy_signals
        ):
            raise StudyError(
                "proxy_signals must be a tuple of exact RelationalContinuityProxy values"
            )
        if len(self.proxy_signals) != len(set(self.proxy_signals)):
            raise StudyError("proxy signals must be unique")
        if self.matched_information_comparison is not None and type(
            self.matched_information_comparison
        ) is not MatchedInformationComparison:
            raise StudyError(
                "matched_information_comparison must be an exact MatchedInformationComparison"
            )
        _validate_digest(
            "source_role_provenance_sha256", self.source_role_provenance_sha256
        )
        if (
            self.source_role_provenance_sha256
            != self.ccts_manifest.provenance_manifest_sha256
        ):
            raise StudyError(
                "source-role provenance must bind the admitted CCTS provenance manifest"
            )
        for name in (
            "claims_ai_identity_continuity",
            "claims_ai_subjectivity",
            "claims_ai_held_relationship_experience",
            "synthetic",
            "contains_human_identity",
            "contains_private_transcript",
            "human_participant_observed",
            "model_invoked",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if self.claims_ai_identity_continuity:
            raise StudyError(
                "relational-continuity evidence cannot establish AI identity continuity"
            )
        if self.claims_ai_subjectivity:
            raise StudyError(
                "relational-continuity evidence cannot establish AI subjectivity"
            )
        if self.claims_ai_held_relationship_experience:
            raise StudyError(
                "relational-continuity evidence cannot establish AI held relationship experience"
            )
        if not self.synthetic:
            raise StudyError("v0.1.0 accepts synthetic structural fixtures only")
        if self.contains_human_identity or self.contains_private_transcript:
            raise StudyError("Human identity and private transcripts are excluded")
        if self.human_participant_observed or self.model_invoked:
            raise StudyError(
                "synthetic structural review cannot contain Human observations or model invocation"
            )
        if not self.claim_asserted and (
            self.evidence_bindings
            or self.proxy_signals
            or self.matched_information_comparison is not None
        ):
            raise StudyError("NOT_ASSERTED claims cannot carry claim-review evidence")


@dataclass(frozen=True, slots=True)
class RelationalContinuityReview:
    claim_id: str
    disposition: RelationalContinuityDisposition
    path_dependence_interpretation: RelationalContinuityDisposition
    evidence_loci: tuple[ContinuityEvidenceLocus, ...]
    source_role_provenance_preserved: bool
    proxy_only_support_rejected: bool
    matched_information_adequate: bool
    unresolved_confounds: tuple[MatchedInformationConfound, ...]
    core_ccts_admission_changed: bool = False
    longitudinal_required_fields_changed: bool = False
    null_result_is_test_failure: bool = False
    mode: str = "DETERMINISTIC_SYNTHETIC_STRUCTURE"
    empirical_data_collected: bool = False
    relational_continuity_established: str = "NOT_ESTABLISHED"
    ai_identity_continuity: str = "NOT_ESTABLISHED"
    ai_held_relationship_experience: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    path_dependence_causally_established: str = "NOT_ESTABLISHED"
    learning: str = "NOT_ESTABLISHED"
    scientific_validation: str = "NONE"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def review_relational_continuity_claim(
    assertion: RelationalContinuityAssertion,
) -> RelationalContinuityReview:
    if type(assertion) is not RelationalContinuityAssertion:
        raise StudyError(
            "assertion must be an exact RelationalContinuityAssertion"
        )

    role_by_id = {
        contribution.contribution_id: contribution.role
        for contribution in assertion.ccts_manifest.contributions
    }
    for binding in assertion.evidence_bindings:
        if binding.contribution_id not in role_by_id:
            raise StudyError(
                "evidence binding must reference a known CCTS contribution"
            )
        if role_by_id[binding.contribution_id] is not binding.source_role:
            raise StudyError(
                "evidence source role must match the referenced CCTS contribution"
            )

    evidence_loci = tuple(binding.locus for binding in assertion.evidence_bindings)
    relational_evidence_present = (
        ContinuityEvidenceLocus.RELATIONAL in evidence_loci
    )
    proxy_only_rejected = bool(assertion.proxy_signals) and not relational_evidence_present

    if not assertion.claim_asserted:
        disposition = RelationalContinuityDisposition.NOT_ASSERTED
        path_disposition = RelationalContinuityDisposition.NOT_ASSERTED
        matched_adequate = False
        confounds: tuple[MatchedInformationConfound, ...] = ()
    elif not relational_evidence_present:
        disposition = RelationalContinuityDisposition.EVIDENCE_REQUIRED
        path_disposition = RelationalContinuityDisposition.EVIDENCE_REQUIRED
        matched_adequate = False
        confounds = ()
    elif assertion.matched_information_comparison is None:
        disposition = RelationalContinuityDisposition.EVIDENCE_REQUIRED
        path_disposition = RelationalContinuityDisposition.EVIDENCE_REQUIRED
        matched_adequate = False
        confounds = ()
    else:
        comparison = assertion.matched_information_comparison
        matched_adequate = comparison.matching_adequate
        confounds = comparison.unresolved_confounds
        if not matched_adequate:
            disposition = RelationalContinuityDisposition.UNRESOLVED
        elif comparison.outcome is PathDependenceOutcome.NO_MATERIAL_DIFFERENCE:
            disposition = RelationalContinuityDisposition.WEAKENED
        elif comparison.outcome is PathDependenceOutcome.MATERIAL_DIFFERENCE:
            disposition = RelationalContinuityDisposition.SUPPORTED_CANDIDATE
        else:
            disposition = RelationalContinuityDisposition.UNRESOLVED
        path_disposition = disposition

    return RelationalContinuityReview(
        claim_id=assertion.claim_id,
        disposition=disposition,
        path_dependence_interpretation=path_disposition,
        evidence_loci=evidence_loci,
        source_role_provenance_preserved=True,
        proxy_only_support_rejected=proxy_only_rejected,
        matched_information_adequate=matched_adequate,
        unresolved_confounds=confounds,
    )
