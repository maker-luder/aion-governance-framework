from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    RevisionRelation,
    ThinkingSpaceProfile,
    audit_co_constructed_thinking_space,
)
from .harness import AdmissionDisposition, StudyError
from .task_selection_exposure import BoundArtifact


class EpistemicChallengeProfile(StrEnum):
    BOUNDED_CHALLENGE_TRACE = "BOUNDED_CHALLENGE_TRACE"
    RESEARCH_ADVERSARIAL_REVIEW = "RESEARCH_ADVERSARIAL_REVIEW"


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


_EVIDENCE_ATTACK_TYPES = frozenset(
    {
        EpistemicChallengeType.COUNTEREVIDENCE,
        EpistemicChallengeType.EVIDENCE_SUFFICIENCY,
    }
)
_ASSUMPTION_ATTACK_TYPES = frozenset(
    {
        EpistemicChallengeType.HIDDEN_ASSUMPTION,
        EpistemicChallengeType.COUNTEREXAMPLE,
    }
)
_ALTERNATIVE_MODEL_TYPES = frozenset(
    {
        EpistemicChallengeType.ALTERNATIVE_EXPLANATION,
        EpistemicChallengeType.BYPASS_ANALYSIS,
    }
)
_GROUNDING_SCOPE_TYPES = frozenset(
    {
        EpistemicChallengeType.GROUNDING_CHALLENGE,
        EpistemicChallengeType.RESEARCH_NECESSITY,
        EpistemicChallengeType.SCOPE_CHALLENGE,
    }
)
_REVISION_DISPOSITIONS = frozenset(
    {
        RevisionDisposition.NARROW,
        RevisionDisposition.REVISE,
        RevisionDisposition.REJECT,
    }
)


@dataclass(frozen=True, slots=True)
class EpistemicChallengeRecord:
    challenge_id: str
    source_contribution_id: str
    target_contribution_id: str
    challenge_type: EpistemicChallengeType
    challenge_artifact: BoundArtifact
    linked_evidence_artifact: BoundArtifact | None = None
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        for name in (
            "challenge_id",
            "source_contribution_id",
            "target_contribution_id",
        ):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise StudyError(f"{name} must be non-empty text")
        if self.source_contribution_id == self.target_contribution_id:
            raise StudyError("epistemic challenge cannot target the same contribution")
        if type(self.challenge_type) is not EpistemicChallengeType:
            raise StudyError("challenge_type must be an exact EpistemicChallengeType")
        if type(self.challenge_artifact) is not BoundArtifact:
            raise StudyError("challenge_artifact must be an exact BoundArtifact")
        if (
            self.linked_evidence_artifact is not None
            and type(self.linked_evidence_artifact) is not BoundArtifact
        ):
            raise StudyError(
                "linked_evidence_artifact must be an exact BoundArtifact or None"
            )
        if (
            self.linked_evidence_artifact is not None
            and self.linked_evidence_artifact.sha256_digest
            == self.challenge_artifact.sha256_digest
        ):
            raise StudyError(
                "challenge and linked-evidence artifacts must be content-distinct"
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
            raise StudyError("v0.1.0 challenge records must remain synthetic")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "challenge structural QA cannot contain model or human observations"
            )
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")


@dataclass(frozen=True, slots=True)
class ConceptualRevisionTrace:
    trace_id: str
    profile: EpistemicChallengeProfile
    ccts_manifest: CoConstructedThinkingSpaceManifest
    prior_problem_model: BoundArtifact
    challenges: tuple[EpistemicChallengeRecord, ...]
    disposition: RevisionDisposition
    surviving_claims: BoundArtifact
    rejected_branches: BoundArtifact
    unresolved_alternatives: BoundArtifact
    claim_ceiling: BoundArtifact
    revised_problem_model: BoundArtifact | None = None
    anomalous_evidence: BoundArtifact | None = None
    conflict_acknowledged: bool = False
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        if type(self.trace_id) is not str or not self.trace_id.strip():
            raise StudyError("trace_id must be non-empty text")
        if type(self.profile) is not EpistemicChallengeProfile:
            raise StudyError("profile must be an exact EpistemicChallengeProfile")
        if type(self.ccts_manifest) is not CoConstructedThinkingSpaceManifest:
            raise StudyError(
                "ccts_manifest must be an exact CoConstructedThinkingSpaceManifest"
            )
        if type(self.prior_problem_model) is not BoundArtifact:
            raise StudyError("prior_problem_model must be an exact BoundArtifact")
        if type(self.challenges) is not tuple or not self.challenges:
            raise StudyError("challenges must be a non-empty tuple")
        if any(type(item) is not EpistemicChallengeRecord for item in self.challenges):
            raise StudyError(
                "challenges must contain exact EpistemicChallengeRecord values"
            )
        challenge_ids = [item.challenge_id for item in self.challenges]
        if len(challenge_ids) != len(set(challenge_ids)):
            raise StudyError("challenge_id values must be unique")
        if type(self.disposition) is not RevisionDisposition:
            raise StudyError("disposition must be an exact RevisionDisposition")
        for name in (
            "surviving_claims",
            "rejected_branches",
            "unresolved_alternatives",
            "claim_ceiling",
        ):
            if type(getattr(self, name)) is not BoundArtifact:
                raise StudyError(f"{name} must be an exact BoundArtifact")
        if (
            self.revised_problem_model is not None
            and type(self.revised_problem_model) is not BoundArtifact
        ):
            raise StudyError(
                "revised_problem_model must be an exact BoundArtifact or None"
            )
        if (
            self.anomalous_evidence is not None
            and type(self.anomalous_evidence) is not BoundArtifact
        ):
            raise StudyError("anomalous_evidence must be an exact BoundArtifact or None")
        for name in (
            "conflict_acknowledged",
            "synthetic",
            "model_invoked",
            "human_participant_observed",
            "contains_human_identity",
            "contains_private_material",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if not self.synthetic:
            raise StudyError("v0.1.0 conceptual-revision traces must remain synthetic")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "conceptual-revision structural QA cannot contain model or human observations"
            )
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")

        if (
            self.prior_problem_model.sha256_digest
            != self.ccts_manifest.problem_representation_sha256
        ):
            raise StudyError(
                "prior problem model must bind the CCTS problem representation"
            )
        if (
            self.rejected_branches.sha256_digest
            != self.ccts_manifest.rejected_branch_manifest_sha256
        ):
            raise StudyError(
                "rejected branches must bind the CCTS rejected-branch manifest"
            )
        if self.claim_ceiling.sha256_digest != self.ccts_manifest.claim_boundary_sha256:
            raise StudyError("claim ceiling must bind the CCTS claim boundary")

        if self.disposition in _REVISION_DISPOSITIONS:
            if not self.conflict_acknowledged:
                raise StudyError(
                    "NARROW/REVISE/REJECT require an acknowledged conflict"
                )
            if self.revised_problem_model is None:
                raise StudyError(
                    "NARROW/REVISE/REJECT require a revised problem model"
                )
            if (
                self.revised_problem_model.sha256_digest
                == self.prior_problem_model.sha256_digest
            ):
                raise StudyError(
                    "revised problem model must be content-distinct from prior model"
                )
        elif self.revised_problem_model is not None:
            raise StudyError(
                "RETAIN/HOLD cannot declare a revised problem model in v0.1.0"
            )


@dataclass(frozen=True, slots=True)
class EpistemicChallengeAudit:
    profile: EpistemicChallengeProfile
    challenge_count: int
    challenge_types: tuple[EpistemicChallengeType, ...]
    challenge_edges_bound: bool
    bidirectional_human_ai_challenge: bool
    evidence_attack_present: bool
    assumption_attack_present: bool
    alternative_model_present: bool
    falsifier_present: bool
    grounding_or_scope_challenge_present: bool
    conceptual_revision_bound: bool
    rejected_branch_bound: bool
    unresolved_alternatives_bound: bool
    claim_ceiling_bound: bool
    mode: str = "DETERMINISTIC_SYNTHETIC_STRUCTURE"
    empirical_data_collected: bool = False
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    conceptual_change_mechanism: str = "NOT_ESTABLISHED"
    cognitive_conflict_state: str = "NOT_ESTABLISHED"
    transformative_learning: str = "NOT_ESTABLISHED"
    human_learning: str = "NOT_ESTABLISHED"
    ccts_causal_effect: str = "NOT_ESTABLISHED"
    ai_subjectivity: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_ccts_epistemic_challenge(
    trace: ConceptualRevisionTrace,
) -> EpistemicChallengeAudit:
    if type(trace) is not ConceptualRevisionTrace:
        raise StudyError("trace must be an exact ConceptualRevisionTrace")

    audit_co_constructed_thinking_space(trace.ccts_manifest)

    role_by_id = {
        item.contribution_id: item.role for item in trace.ccts_manifest.contributions
    }
    challenge_edges = {
        (edge.source_id, edge.target_id)
        for edge in trace.ccts_manifest.revision_edges
        if edge.relation is RevisionRelation.CHALLENGES
    }

    for challenge in trace.challenges:
        pair = (challenge.source_contribution_id, challenge.target_contribution_id)
        if pair not in challenge_edges:
            raise StudyError(
                "each epistemic challenge must bind an exact CCTS CHALLENGES edge"
            )
        if (
            challenge.source_contribution_id not in role_by_id
            or challenge.target_contribution_id not in role_by_id
        ):
            raise StudyError("epistemic challenge must reference known contributions")

    challenge_types = {item.challenge_type for item in trace.challenges}
    human_to_ai = any(
        role_by_id[item.source_contribution_id] is ContributionRole.HUMAN_OWNER
        and role_by_id[item.target_contribution_id] is ContributionRole.AI_COLLABORATOR
        for item in trace.challenges
    )
    ai_to_human = any(
        role_by_id[item.source_contribution_id] is ContributionRole.AI_COLLABORATOR
        and role_by_id[item.target_contribution_id] is ContributionRole.HUMAN_OWNER
        for item in trace.challenges
    )

    evidence_attack = bool(challenge_types & _EVIDENCE_ATTACK_TYPES)
    assumption_attack = bool(challenge_types & _ASSUMPTION_ATTACK_TYPES)
    alternative_model = bool(challenge_types & _ALTERNATIVE_MODEL_TYPES)
    falsifier = EpistemicChallengeType.FALSIFIER in challenge_types
    grounding_or_scope = bool(challenge_types & _GROUNDING_SCOPE_TYPES)

    if trace.profile is EpistemicChallengeProfile.RESEARCH_ADVERSARIAL_REVIEW:
        if (
            trace.ccts_manifest.profile
            is not ThinkingSpaceProfile.LONGITUDINAL_REPOSITORY_RESEARCH
        ):
            raise StudyError(
                "RESEARCH_ADVERSARIAL_REVIEW requires longitudinal repository CCTS"
            )
        if not (human_to_ai and ai_to_human):
            raise StudyError(
                "RESEARCH_ADVERSARIAL_REVIEW requires bidirectional Human<->AI "
                "CHALLENGES records"
            )
        missing_families: list[str] = []
        if not evidence_attack:
            missing_families.append("evidence attack")
        if not assumption_attack:
            missing_families.append("assumption attack")
        if not alternative_model:
            missing_families.append("alternative explanation or bypass analysis")
        if not falsifier:
            missing_families.append("falsifier")
        if not grounding_or_scope:
            missing_families.append("grounding/research-necessity/scope challenge")
        if missing_families:
            raise StudyError(
                "RESEARCH_ADVERSARIAL_REVIEW missing challenge family: "
                + ", ".join(missing_families)
            )

    return EpistemicChallengeAudit(
        profile=trace.profile,
        challenge_count=len(trace.challenges),
        challenge_types=tuple(sorted(challenge_types, key=lambda item: item.value)),
        challenge_edges_bound=True,
        bidirectional_human_ai_challenge=human_to_ai and ai_to_human,
        evidence_attack_present=evidence_attack,
        assumption_attack_present=assumption_attack,
        alternative_model_present=alternative_model,
        falsifier_present=falsifier,
        grounding_or_scope_challenge_present=grounding_or_scope,
        conceptual_revision_bound=trace.disposition in _REVISION_DISPOSITIONS,
        rejected_branch_bound=True,
        unresolved_alternatives_bound=True,
        claim_ceiling_bound=True,
    )
