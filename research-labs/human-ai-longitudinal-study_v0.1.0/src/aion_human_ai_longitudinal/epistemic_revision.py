from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256

from .co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    RevisionRelation,
    audit_co_constructed_thinking_space,
)
from .harness import AdmissionDisposition, StudyError


class EpistemicChallengeType(StrEnum):
    COUNTEREVIDENCE = "COUNTEREVIDENCE"
    COUNTEREXAMPLE = "COUNTEREXAMPLE"
    HIDDEN_ASSUMPTION = "HIDDEN_ASSUMPTION"
    ALTERNATIVE_EXPLANATION = "ALTERNATIVE_EXPLANATION"
    BYPASS_ANALYSIS = "BYPASS_ANALYSIS"
    GROUNDING_CHALLENGE = "GROUNDING_CHALLENGE"
    RESEARCH_NECESSITY = "RESEARCH_NECESSITY"
    EVIDENCE_SUFFICIENCY = "EVIDENCE_SUFFICIENCY"
    FALSIFIER = "FALSIFIER"
    SCOPE_CHALLENGE = "SCOPE_CHALLENGE"


class RevisionDisposition(StrEnum):
    RETAIN = "RETAIN"
    NARROW = "NARROW"
    REVISE = "REVISE"
    REJECT = "REJECT"
    HOLD = "HOLD"


_EVIDENCE_BOUND_CHALLENGES = frozenset(
    {
        EpistemicChallengeType.COUNTEREVIDENCE,
        EpistemicChallengeType.GROUNDING_CHALLENGE,
        EpistemicChallengeType.EVIDENCE_SUFFICIENCY,
    }
)
_ADVERSARIAL_CHALLENGES = frozenset(
    {
        EpistemicChallengeType.COUNTEREVIDENCE,
        EpistemicChallengeType.COUNTEREXAMPLE,
        EpistemicChallengeType.HIDDEN_ASSUMPTION,
        EpistemicChallengeType.ALTERNATIVE_EXPLANATION,
        EpistemicChallengeType.BYPASS_ANALYSIS,
        EpistemicChallengeType.FALSIFIER,
    }
)
_GROUNDING_AND_SCOPE_CHALLENGES = frozenset(
    {
        EpistemicChallengeType.GROUNDING_CHALLENGE,
        EpistemicChallengeType.RESEARCH_NECESSITY,
        EpistemicChallengeType.EVIDENCE_SUFFICIENCY,
        EpistemicChallengeType.SCOPE_CHALLENGE,
    }
)
_MODEL_CHANGING_DISPOSITIONS = frozenset(
    {
        RevisionDisposition.NARROW,
        RevisionDisposition.REVISE,
        RevisionDisposition.REJECT,
    }
)


def _validate_digest(name: str, digest: str) -> None:
    if type(digest) is not str or len(digest) != 64 or any(
        char not in "0123456789abcdef" for char in digest
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


def _validate_content_address(name: str, text: str, digest: str) -> None:
    if type(text) is not str or not text.strip():
        raise StudyError(f"{name}_text must be non-empty text")
    _validate_digest(f"{name}_sha256", digest)
    if sha256(text.encode("utf-8")).hexdigest() != digest:
        raise StudyError(f"{name}_sha256 must match {name}_text")


@dataclass(frozen=True, slots=True)
class ConceptualRevisionTrace:
    trace_id: str
    ccts_space_id: str
    problem_representation_sha256: str
    source_contribution_id: str
    target_contribution_id: str
    revised_contribution_id: str
    challenge_types: frozenset[EpistemicChallengeType]
    disposition: RevisionDisposition
    prior_model_text: str
    prior_model_sha256: str
    challenge_text: str
    challenge_sha256: str
    revised_model_text: str
    revised_model_sha256: str
    surviving_claims_text: str
    surviving_claims_sha256: str
    rejected_branches_text: str
    rejected_branches_sha256: str
    unresolved_alternatives_text: str
    unresolved_alternatives_sha256: str
    claim_ceiling_text: str
    claim_ceiling_sha256: str
    anomalous_evidence_sha256s: tuple[str, ...] = ()
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        for name in (
            "trace_id",
            "ccts_space_id",
            "source_contribution_id",
            "target_contribution_id",
            "revised_contribution_id",
        ):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise StudyError(f"{name} must be non-empty text")
        if len(
            {
                self.source_contribution_id,
                self.target_contribution_id,
                self.revised_contribution_id,
            }
        ) != 3:
            raise StudyError(
                "source, target, and revised contribution ids must be distinct"
            )
        _validate_digest(
            "problem_representation_sha256", self.problem_representation_sha256
        )
        if type(self.challenge_types) is not frozenset or not self.challenge_types:
            raise StudyError("challenge_types must be a non-empty frozenset")
        if any(type(item) is not EpistemicChallengeType for item in self.challenge_types):
            raise StudyError(
                "challenge_types must contain exact EpistemicChallengeType values"
            )
        if type(self.disposition) is not RevisionDisposition:
            raise StudyError("disposition must be an exact RevisionDisposition")
        for name in (
            "prior_model",
            "challenge",
            "revised_model",
            "surviving_claims",
            "rejected_branches",
            "unresolved_alternatives",
            "claim_ceiling",
        ):
            _validate_content_address(
                name,
                getattr(self, f"{name}_text"),
                getattr(self, f"{name}_sha256"),
            )
        if type(self.anomalous_evidence_sha256s) is not tuple:
            raise StudyError("anomalous_evidence_sha256s must be an exact tuple")
        for digest in self.anomalous_evidence_sha256s:
            _validate_digest("anomalous_evidence_sha256s item", digest)
        if self.challenge_types & _EVIDENCE_BOUND_CHALLENGES:
            if not self.anomalous_evidence_sha256s:
                raise StudyError(
                    "evidence-bound challenge types require anomalous evidence bindings"
                )
        if self.disposition is RevisionDisposition.RETAIN:
            if self.prior_model_sha256 != self.revised_model_sha256:
                raise StudyError("RETAIN requires identical prior and revised models")
        elif self.disposition in _MODEL_CHANGING_DISPOSITIONS:
            if self.prior_model_sha256 == self.revised_model_sha256:
                raise StudyError(
                    "model-changing disposition requires a content-distinct revised model"
                )
        for name in (
            "synthetic",
            "model_invoked",
            "human_participant_observed",
            "contains_human_identity",
            "contains_private_material",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.synthetic:
            raise StudyError("v0.1.0 accepts synthetic revision traces only")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "structural revision traces cannot contain model or human observations"
            )
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")


@dataclass(frozen=True, slots=True)
class EpistemicRevisionAudit:
    trace_count: int
    reciprocal_challenge_bound: bool
    challenge_edges_bound: bool
    revision_edges_bound: bool
    graph_content_bound: bool
    adversarial_challenge_present: bool
    grounding_or_scope_challenge_present: bool
    conceptual_revision_trace_present: bool
    rejected_branch_content_bound: bool
    claim_ceiling_content_bound: bool
    unresolved_alternatives_explicit: bool
    mode: str = "DETERMINISTIC_SYNTHETIC_STRUCTURE"
    empirical_data_collected: bool = False
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    human_conceptual_change: str = "NOT_ESTABLISHED"
    cognitive_conflict: str = "NOT_ESTABLISHED"
    schema_accommodation: str = "NOT_ESTABLISHED"
    transformative_learning: str = "NOT_ESTABLISHED"
    threshold_concept: str = "NOT_ESTABLISHED"
    human_learning: str = "NOT_ESTABLISHED"
    ccts_causal_effect: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if type(self.trace_count) is not int or self.trace_count < 1:
            raise StudyError("trace_count must be a positive exact integer")

        structural_flags = (
            "reciprocal_challenge_bound",
            "challenge_edges_bound",
            "revision_edges_bound",
            "graph_content_bound",
            "adversarial_challenge_present",
            "grounding_or_scope_challenge_present",
            "conceptual_revision_trace_present",
            "rejected_branch_content_bound",
            "claim_ceiling_content_bound",
            "unresolved_alternatives_explicit",
        )
        for name in structural_flags:
            value = getattr(self, name)
            if type(value) is not bool:
                raise StudyError(f"{name} must be an exact bool")
            if not value:
                raise StudyError("structural audit flags must remain true")

        if self.mode != "DETERMINISTIC_SYNTHETIC_STRUCTURE":
            raise StudyError("mode must remain DETERMINISTIC_SYNTHETIC_STRUCTURE")
        if type(self.empirical_data_collected) is not bool:
            raise StudyError("empirical_data_collected must be an exact bool")
        if self.empirical_data_collected:
            raise StudyError("empirical_data_collected must remain false")
        if self.evidence_admissibility != "STRUCTURAL_QA_ONLY":
            raise StudyError("evidence_admissibility must remain STRUCTURAL_QA_ONLY")

        for name in (
            "human_conceptual_change",
            "cognitive_conflict",
            "schema_accommodation",
            "transformative_learning",
            "threshold_concept",
            "human_learning",
            "ccts_causal_effect",
            "subjectivity_conclusion",
            "consciousness_conclusion",
            "phenomenal_experience_conclusion",
        ):
            if getattr(self, name) != "NOT_ESTABLISHED":
                raise StudyError(f"{name} must remain NOT_ESTABLISHED")

        if (
            type(self.scientific_disposition) is not AdmissionDisposition
            or self.scientific_disposition is not AdmissionDisposition.HOLD
        ):
            raise StudyError("scientific_disposition must remain HOLD")
        if self.canonical_effect != "NONE":
            raise StudyError("canonical_effect must remain NONE")
        if type(self.deployment) is not bool:
            raise StudyError("deployment must be an exact bool")
        if self.deployment:
            raise StudyError("deployment must remain false")


def audit_ccts_epistemic_revision_loop(
    manifest: CoConstructedThinkingSpaceManifest,
    traces: tuple[ConceptualRevisionTrace, ...],
) -> EpistemicRevisionAudit:
    if type(manifest) is not CoConstructedThinkingSpaceManifest:
        raise StudyError("manifest must be an exact CoConstructedThinkingSpaceManifest")
    audit_co_constructed_thinking_space(manifest)
    if type(traces) is not tuple or not traces:
        raise StudyError("revision loop requires a non-empty tuple of traces")
    if any(type(trace) is not ConceptualRevisionTrace for trace in traces):
        raise StudyError("traces must contain exact ConceptualRevisionTrace values")

    trace_ids = [trace.trace_id for trace in traces]
    if len(trace_ids) != len(set(trace_ids)):
        raise StudyError("trace_id values must be unique")

    contribution_by_id = {
        item.contribution_id: item for item in manifest.contributions
    }
    challenge_edges = {
        (edge.source_id, edge.target_id)
        for edge in manifest.revision_edges
        if edge.relation is RevisionRelation.CHALLENGES
    }
    revision_edges = {
        (edge.source_id, edge.target_id)
        for edge in manifest.revision_edges
        if edge.relation is RevisionRelation.REVISES
    }

    directions: set[tuple[ContributionRole, ContributionRole]] = set()
    for trace in traces:
        if trace.ccts_space_id != manifest.space_id:
            raise StudyError("trace must bind the audited CCTS space_id")
        if (
            trace.problem_representation_sha256
            != manifest.problem_representation_sha256
        ):
            raise StudyError("trace must bind the CCTS problem representation")
        referenced_ids = {
            trace.source_contribution_id,
            trace.target_contribution_id,
            trace.revised_contribution_id,
        }
        if not referenced_ids.issubset(contribution_by_id):
            raise StudyError("trace must reference known CCTS contributions")

        challenge_edge = (
            trace.source_contribution_id,
            trace.target_contribution_id,
        )
        if challenge_edge not in challenge_edges:
            raise StudyError(
                "trace must bind an existing CCTS CHALLENGES revision edge"
            )

        model_revision_edge = (
            trace.target_contribution_id,
            trace.revised_contribution_id,
        )
        if model_revision_edge not in revision_edges:
            raise StudyError(
                "trace must bind an existing target-to-revised CCTS REVISES edge"
            )

        source = contribution_by_id[trace.source_contribution_id]
        target = contribution_by_id[trace.target_contribution_id]
        revised = contribution_by_id[trace.revised_contribution_id]
        if source.payload_sha256 != trace.challenge_sha256:
            raise StudyError(
                "challenge content must bind the source CCTS contribution payload"
            )
        if target.payload_sha256 != trace.prior_model_sha256:
            raise StudyError(
                "prior-model content must bind the target CCTS contribution payload"
            )
        if revised.payload_sha256 != trace.revised_model_sha256:
            raise StudyError(
                "revised-model content must bind the revised CCTS contribution payload"
            )
        if revised.role is not target.role:
            raise StudyError(
                "revised contribution must preserve the target contribution role"
            )

        directions.add((source.role, target.role))
        if trace.rejected_branches_sha256 != manifest.rejected_branch_manifest_sha256:
            raise StudyError(
                "trace rejected-branch content must bind the CCTS rejected-branch manifest"
            )
        if trace.claim_ceiling_sha256 != manifest.claim_boundary_sha256:
            raise StudyError(
                "trace claim-ceiling content must bind the CCTS claim boundary"
            )

    required_directions = {
        (ContributionRole.HUMAN_OWNER, ContributionRole.AI_COLLABORATOR),
        (ContributionRole.AI_COLLABORATOR, ContributionRole.HUMAN_OWNER),
    }
    if not required_directions.issubset(directions):
        raise StudyError(
            "epistemic revision loop requires reciprocal Human<->AI CHALLENGES traces"
        )

    adversarial = any(
        bool(trace.challenge_types & _ADVERSARIAL_CHALLENGES) for trace in traces
    )
    if not adversarial:
        raise StudyError("revision loop requires an adversarial challenge type")

    grounding_or_scope = any(
        bool(trace.challenge_types & _GROUNDING_AND_SCOPE_CHALLENGES)
        for trace in traces
    )
    if not grounding_or_scope:
        raise StudyError(
            "revision loop requires a grounding, evidence, necessity, or scope challenge"
        )

    conceptual_revision = any(
        trace.disposition in _MODEL_CHANGING_DISPOSITIONS for trace in traces
    )
    if not conceptual_revision:
        raise StudyError(
            "revision loop requires at least one model-changing disposition"
        )

    return EpistemicRevisionAudit(
        trace_count=len(traces),
        reciprocal_challenge_bound=True,
        challenge_edges_bound=True,
        revision_edges_bound=True,
        graph_content_bound=True,
        adversarial_challenge_present=True,
        grounding_or_scope_challenge_present=True,
        conceptual_revision_trace_present=True,
        rejected_branch_content_bound=True,
        claim_ceiling_content_bound=True,
        unresolved_alternatives_explicit=True,
    )
