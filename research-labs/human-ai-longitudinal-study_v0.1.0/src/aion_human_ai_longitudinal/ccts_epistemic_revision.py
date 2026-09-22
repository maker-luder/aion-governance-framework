from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256

from .co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    audit_co_constructed_thinking_space,
)
from .harness import AdmissionDisposition, StudyError


class EpistemicChallengeType(StrEnum):
    COUNTEREXAMPLE = "COUNTEREXAMPLE"
    ALTERNATIVE_EXPLANATION = "ALTERNATIVE_EXPLANATION"
    HIDDEN_ASSUMPTION = "HIDDEN_ASSUMPTION"
    BYPASS_PATH = "BYPASS_PATH"
    GROUNDING_CHALLENGE = "GROUNDING_CHALLENGE"
    RESEARCH_NECESSITY = "RESEARCH_NECESSITY"
    EVIDENCE_SUFFICIENCY = "EVIDENCE_SUFFICIENCY"
    FALSIFIER = "FALSIFIER"
    SCOPE_CHALLENGE = "SCOPE_CHALLENGE"


class EpistemicRevisionDisposition(StrEnum):
    RETAIN = "RETAIN"
    NARROW = "NARROW"
    REVISE = "REVISE"
    REJECT = "REJECT"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class ContentAddressedText:
    text: str
    sha256_hex: str

    def __post_init__(self) -> None:
        if type(self.text) is not str or not self.text.strip():
            raise StudyError("content-addressed text must be non-empty text")
        if type(self.sha256_hex) is not str or len(self.sha256_hex) != 64 or any(
            char not in "0123456789abcdef" for char in self.sha256_hex
        ):
            raise StudyError("sha256_hex must be a lowercase SHA-256 digest")
        expected = sha256(self.text.encode("utf-8")).hexdigest()
        if expected != self.sha256_hex:
            raise StudyError("sha256_hex must match the supplied text")


@dataclass(frozen=True, slots=True)
class CCTSEpistemicChallengeTrace:
    trace_id: str
    ccts_manifest: CoConstructedThinkingSpaceManifest
    challenger_role: ContributionRole
    target_role: ContributionRole
    challenge_type: EpistemicChallengeType
    prior_model: ContentAddressedText
    challenge: ContentAddressedText
    attack_artifact: ContentAddressedText
    disposition: EpistemicRevisionDisposition
    revised_model: ContentAddressedText
    residual_uncertainty: ContentAddressedText
    claim_ceiling: ContentAddressedText
    rejected_branch: ContentAddressedText | None = None
    alternative_explanation: ContentAddressedText | None = None
    bypass_path: ContentAddressedText | None = None
    falsifier: ContentAddressedText | None = None
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_human_identity: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        if type(self.trace_id) is not str or not self.trace_id.strip():
            raise StudyError("trace_id must be non-empty text")
        if type(self.ccts_manifest) is not CoConstructedThinkingSpaceManifest:
            raise StudyError(
                "ccts_manifest must be an exact CoConstructedThinkingSpaceManifest"
            )
        audit_co_constructed_thinking_space(self.ccts_manifest)
        if type(self.challenger_role) is not ContributionRole:
            raise StudyError("challenger_role must be an exact ContributionRole")
        if type(self.target_role) is not ContributionRole:
            raise StudyError("target_role must be an exact ContributionRole")
        allowed_roles = {
            ContributionRole.HUMAN_OWNER,
            ContributionRole.AI_COLLABORATOR,
        }
        if self.challenger_role not in allowed_roles or self.target_role not in allowed_roles:
            raise StudyError(
                "epistemic challenge roles are limited to Human and AI collaborators"
            )
        if self.challenger_role is self.target_role:
            raise StudyError("challenger_role and target_role must be distinct")
        if type(self.challenge_type) is not EpistemicChallengeType:
            raise StudyError("challenge_type must be an exact EpistemicChallengeType")
        if type(self.disposition) is not EpistemicRevisionDisposition:
            raise StudyError(
                "disposition must be an exact EpistemicRevisionDisposition"
            )
        for name in (
            "prior_model",
            "challenge",
            "attack_artifact",
            "revised_model",
            "residual_uncertainty",
            "claim_ceiling",
        ):
            if type(getattr(self, name)) is not ContentAddressedText:
                raise StudyError(f"{name} must be exact ContentAddressedText")
        for name in (
            "rejected_branch",
            "alternative_explanation",
            "bypass_path",
            "falsifier",
        ):
            value = getattr(self, name)
            if value is not None and type(value) is not ContentAddressedText:
                raise StudyError(f"{name} must be ContentAddressedText or None")
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
            raise StudyError("v0.1.0 epistemic revision traces are synthetic only")
        if self.model_invoked or self.human_participant_observed:
            raise StudyError(
                "structural revision traces cannot contain model or human observations"
            )
        if self.contains_human_identity or self.contains_private_material:
            raise StudyError("human identity and private material are excluded")

        if (
            self.disposition is EpistemicRevisionDisposition.RETAIN
            and self.revised_model.sha256_hex != self.prior_model.sha256_hex
        ):
            raise StudyError("RETAIN requires the prior and revised model to be identical")
        if (
            self.disposition
            in {
                EpistemicRevisionDisposition.NARROW,
                EpistemicRevisionDisposition.REVISE,
                EpistemicRevisionDisposition.REJECT,
            }
            and self.revised_model.sha256_hex == self.prior_model.sha256_hex
        ):
            raise StudyError(
                "NARROW, REVISE, and REJECT require a content-distinct revised model"
            )
        if (
            self.disposition
            in {
                EpistemicRevisionDisposition.NARROW,
                EpistemicRevisionDisposition.REVISE,
                EpistemicRevisionDisposition.REJECT,
            }
            and self.rejected_branch is None
        ):
            raise StudyError(
                "substantive revision requires rejected-branch preservation"
            )

        type_specific_artifact = {
            EpistemicChallengeType.ALTERNATIVE_EXPLANATION: self.alternative_explanation,
            EpistemicChallengeType.BYPASS_PATH: self.bypass_path,
            EpistemicChallengeType.FALSIFIER: self.falsifier,
        }
        required = type_specific_artifact.get(self.challenge_type)
        if self.challenge_type in type_specific_artifact and required is None:
            raise StudyError(
                f"{self.challenge_type.value} requires its typed challenge artifact"
            )


@dataclass(frozen=True, slots=True)
class CCTSEpistemicRevisionAudit:
    trace_count: int
    space_id: str
    reciprocal_human_ai_challenge: bool
    ccts_contract_bound: bool
    verified_content_addressing: bool
    rejected_branch_preserved: bool
    challenge_types_present: tuple[EpistemicChallengeType, ...]
    substantive_revision_present: bool
    hold_state_representable: bool
    mode: str = "DETERMINISTIC_SYNTHETIC_STRUCTURE"
    empirical_data_collected: bool = False
    evidence_admissibility: str = "STRUCTURAL_QA_ONLY"
    adversarial_thinking_effect: str = "NOT_ESTABLISHED"
    conceptual_change: str = "NOT_ESTABLISHED"
    cognitive_conflict: str = "NOT_ESTABLISHED"
    transformative_learning: str = "NOT_ESTABLISHED"
    human_learning: str = "NOT_ESTABLISHED"
    revision_correctness: str = "NOT_ESTABLISHED"
    causal_effect: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    consciousness_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def audit_ccts_epistemic_revision_loop(
    traces: tuple[CCTSEpistemicChallengeTrace, ...],
) -> CCTSEpistemicRevisionAudit:
    if type(traces) is not tuple or not traces:
        raise StudyError("epistemic revision loop requires a non-empty tuple")
    if any(type(item) is not CCTSEpistemicChallengeTrace for item in traces):
        raise StudyError(
            "epistemic revision loop requires exact CCTSEpistemicChallengeTrace values"
        )

    trace_ids = [item.trace_id for item in traces]
    if len(trace_ids) != len(set(trace_ids)):
        raise StudyError("trace_id values must be unique")

    space_ids = {item.ccts_manifest.space_id for item in traces}
    if len(space_ids) != 1:
        raise StudyError("all challenge traces must bind one CCTS space_id")
    problem_bindings = {
        item.ccts_manifest.problem_representation_sha256 for item in traces
    }
    if len(problem_bindings) != 1:
        raise StudyError(
            "all challenge traces must bind one CCTS problem representation"
        )

    directions = {
        (item.challenger_role, item.target_role)
        for item in traces
    }
    required_directions = {
        (ContributionRole.HUMAN_OWNER, ContributionRole.AI_COLLABORATOR),
        (ContributionRole.AI_COLLABORATOR, ContributionRole.HUMAN_OWNER),
    }
    if not required_directions.issubset(directions):
        raise StudyError(
            "epistemic revision loop requires reciprocal Human<->AI challenge traces"
        )

    substantive_dispositions = {
        EpistemicRevisionDisposition.NARROW,
        EpistemicRevisionDisposition.REVISE,
        EpistemicRevisionDisposition.REJECT,
    }
    substantive = any(item.disposition in substantive_dispositions for item in traces)
    rejected_preserved = all(
        item.rejected_branch is not None
        for item in traces
        if item.disposition in substantive_dispositions
    )
    challenge_types = tuple(
        sorted({item.challenge_type for item in traces}, key=lambda item: item.value)
    )

    return CCTSEpistemicRevisionAudit(
        trace_count=len(traces),
        space_id=traces[0].ccts_manifest.space_id,
        reciprocal_human_ai_challenge=True,
        ccts_contract_bound=True,
        verified_content_addressing=True,
        rejected_branch_preserved=rejected_preserved,
        challenge_types_present=challenge_types,
        substantive_revision_present=substantive,
        hold_state_representable=any(
            item.disposition is EpistemicRevisionDisposition.HOLD for item in traces
        ),
    )
