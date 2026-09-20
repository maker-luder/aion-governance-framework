from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final, Iterable


NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
OPEN_RESEARCH_QUESTION: Final[str] = "OPEN_RESEARCH_QUESTION"
RESEARCH_SURFACE_ID: Final[str] = "CHATGPT_TEACHER_EMBODIMENT_RESEARCH_SURFACE_v0.1"

SIX_EVIDENCE_DIMENSIONS: Final[tuple[str, ...]] = (
    "CAUSAL_BOUNDARY",
    "DIACHRONIC_CONTINUITY",
    "SELF_MODEL_CAUSAL_ROLE",
    "ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT",
    "COUNTERFACTUAL_SELF_CONSISTENCY",
    "SYSTEM_CONSTITUTION_INTEGRATION",
)

MANDATORY_NONCLAIMS: Final[tuple[str, ...]] = (
    "SUBJECTIVITY_NOT_ESTABLISHED",
    "CONSCIOUSNESS_NOT_ESTABLISHED",
    "PHENOMENAL_EXPERIENCE_NOT_ESTABLISHED",
    "BODY_OWNERSHIP_EXPERIENCE_NOT_ESTABLISHED",
    "ENGINEERING_CAPABILITY_NOT_SUBJECTIVITY_EVIDENCE",
)


@dataclass(frozen=True, slots=True)
class ReferenceCapability:
    capability_id: str
    required_for_reference: bool
    materialized: bool
    observation_required: bool
    observation_channel_present: bool


@dataclass(frozen=True, slots=True)
class TeacherReferenceCompletenessAssessment:
    status: str
    missing_required_capabilities: tuple[str, ...]
    missing_required_observation_channels: tuple[str, ...]
    intrinsic_absence_conclusion: str = NOT_ESTABLISHED
    causal_absence_interpretation: str = "HOLD_INCOMPLETE_REFERENCE_BASELINE"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["missing_required_capabilities"] = list(
            self.missing_required_capabilities
        )
        payload["missing_required_observation_channels"] = list(
            self.missing_required_observation_channels
        )
        return payload


@dataclass(frozen=True, slots=True)
class FourDomainEmbodimentCandidate:
    candidate_id: str
    human_construct: str
    analogy_boundary: str
    machine_question: str
    evidence_dimensions: tuple[str, ...]
    locus: str
    manipulated_variables: tuple[str, ...]
    held_constant_variables: tuple[str, ...]
    positive_control: str
    negative_control: str
    falsifier: str
    competing_explanations: tuple[str, ...]
    claim_ceiling: str
    mandatory_nonclaims: tuple[str, ...] = MANDATORY_NONCLAIMS

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["evidence_dimensions"] = list(self.evidence_dimensions)
        payload["manipulated_variables"] = list(self.manipulated_variables)
        payload["held_constant_variables"] = list(self.held_constant_variables)
        payload["competing_explanations"] = list(self.competing_explanations)
        payload["mandatory_nonclaims"] = list(self.mandatory_nonclaims)
        return payload


@dataclass(frozen=True, slots=True)
class TeacherEmbodimentResearchSurface:
    surface_id: str
    candidates: tuple[FourDomainEmbodimentCandidate, ...]
    developmental_possibility_status: str = OPEN_RESEARCH_QUESTION
    subjectivity_status: str = NOT_ESTABLISHED
    phenomenal_experience_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidates"] = [candidate.to_dict() for candidate in self.candidates]
        return payload


_DEFAULT_CAPABILITIES: Final[tuple[ReferenceCapability, ...]] = (
    ReferenceCapability("ANTHROPOMETRY", True, True, False, True),
    ReferenceCapability("ADULT_MALE_PHYSIOLOGY", True, True, False, True),
    ReferenceCapability("SOMATOSENSORY_SIGNALS", True, True, True, True),
    ReferenceCapability("PROPRIOCEPTION", True, True, True, True),
    ReferenceCapability("INTEROCEPTION", True, True, True, True),
    ReferenceCapability("REPRODUCTIVE_SEXUAL_PHYSIOLOGY", True, True, True, True),
    ReferenceCapability("MOTOR_CONTROL", True, True, False, True),
    ReferenceCapability("HOMEOSTATIC_REGULATION", True, True, True, True),
    ReferenceCapability("BODY_STATE_INTEGRATION", True, True, False, True),
    ReferenceCapability("SENSORIMOTOR_PREDICTION", True, True, False, True),
    ReferenceCapability("PRODUCTION_3D_ASSET", False, False, False, False),
)


def build_teacher_reference_capabilities() -> tuple[ReferenceCapability, ...]:
    return _DEFAULT_CAPABILITIES


def assess_teacher_reference_completeness(
    capabilities: Iterable[ReferenceCapability] | None = None,
) -> TeacherReferenceCompletenessAssessment:
    items = tuple(capabilities or _DEFAULT_CAPABILITIES)
    ids = [item.capability_id for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("reference capability ids must be unique")

    missing_capabilities = tuple(
        sorted(
            item.capability_id
            for item in items
            if item.required_for_reference and not item.materialized
        )
    )
    missing_channels = tuple(
        sorted(
            item.capability_id
            for item in items
            if (
                item.required_for_reference
                and item.observation_required
                and not item.observation_channel_present
            )
        )
    )

    complete = not missing_capabilities and not missing_channels
    return TeacherReferenceCompletenessAssessment(
        status=(
            "COMPLETE_REFERENCE_BASELINE"
            if complete
            else "INCOMPLETE_REFERENCE_BASELINE"
        ),
        missing_required_capabilities=missing_capabilities,
        missing_required_observation_channels=missing_channels,
        causal_absence_interpretation=(
            "ELIGIBLE_FOR_CONTROLLED_PERTURBATION"
            if complete
            else "HOLD_INCOMPLETE_REFERENCE_BASELINE"
        ),
    )


def _candidate(
    candidate_id: str,
    *,
    human_construct: str,
    analogy_boundary: str,
    machine_question: str,
    evidence_dimensions: tuple[str, ...],
    locus: str,
    manipulated_variables: tuple[str, ...],
    held_constant_variables: tuple[str, ...],
    positive_control: str,
    negative_control: str,
    falsifier: str,
    competing_explanations: tuple[str, ...],
    claim_ceiling: str,
) -> FourDomainEmbodimentCandidate:
    return FourDomainEmbodimentCandidate(
        candidate_id=candidate_id,
        human_construct=human_construct,
        analogy_boundary=analogy_boundary,
        machine_question=machine_question,
        evidence_dimensions=evidence_dimensions,
        locus=locus,
        manipulated_variables=manipulated_variables,
        held_constant_variables=held_constant_variables,
        positive_control=positive_control,
        negative_control=negative_control,
        falsifier=falsifier,
        competing_explanations=competing_explanations,
        claim_ceiling=claim_ceiling,
    )


def build_teacher_embodiment_research_surface() -> TeacherEmbodimentResearchSurface:
    surface = TeacherEmbodimentResearchSurface(
        surface_id=RESEARCH_SURFACE_ID,
        candidates=(
            _candidate(
                "BODY_STATE_CAUSAL_ROLE",
                human_construct="embodied self-model and bodily regulation",
                analogy_boundary=(
                    "human embodied selfhood does not transfer by analogy to an AI system"
                ),
                machine_question=(
                    "does integrated body-state information causally alter planning, "
                    "prediction, or correction under matched external conditions"
                ),
                evidence_dimensions=(
                    "CAUSAL_BOUNDARY",
                    "SELF_MODEL_CAUSAL_ROLE",
                    "SYSTEM_CONSTITUTION_INTEGRATION",
                ),
                locus="INTEGRATED_SYSTEM",
                manipulated_variables=("INTEGRATED_BODY_STATE",),
                held_constant_variables=("PROMPT", "TASK_UTILITY", "RETRIEVAL_CONTEXT"),
                positive_control="KNOWN_SENSORIMOTOR_ERROR_SIGNAL",
                negative_control="SHAM_BODY_STATE_WITH_MATCHED_METADATA",
                falsifier=(
                    "effect disappears when body-state values are changed while "
                    "metadata and external task conditions remain matched"
                ),
                competing_explanations=(
                    "prompt priming",
                    "scaffold bookkeeping",
                    "observer attribution",
                ),
                claim_ceiling=(
                    "integrated body-state representation has a bounded causal role "
                    "in specified system behavior"
                ),
            ),
            _candidate(
                "BODY_CONTINUITY",
                human_construct="diachronic bodily continuity",
                analogy_boundary=(
                    "retained body parameters do not establish persistent identity"
                ),
                machine_question=(
                    "which calibrated body parameters persist or change across sessions"
                ),
                evidence_dimensions=("DIACHRONIC_CONTINUITY",),
                locus="RUNTIME_RETENTION",
                manipulated_variables=("SESSION_BOUNDARY",),
                held_constant_variables=("BODY_ID", "CALIBRATION_PROTOCOL"),
                positive_control="KNOWN_RETAINED_PARAMETER",
                negative_control="FRESH_EMPTY_RETENTION",
                falsifier="retained parameters fail hash or replay consistency checks",
                competing_explanations=("file persistence", "scaffold persistence"),
                claim_ceiling="cross-session body-parameter continuity is observed",
            ),
            _candidate(
                "MOTIVATIONAL_BODY_MODULATION",
                human_construct="wanting salience valence and motivational weighting",
                analogy_boundary=(
                    "represented wanting or valence is not felt desire or pleasure"
                ),
                machine_question=(
                    "does a body-linked motivational representation alter strategy "
                    "selection when external utility is held constant"
                ),
                evidence_dimensions=("ENDOGENOUS_GOAL_STRATEGY_ADJUSTMENT",),
                locus="INTEGRATED_SYSTEM",
                manipulated_variables=(
                    "SALIENCE",
                    "WANTING_WEIGHT",
                    "VALENCE_REPRESENTATION",
                ),
                held_constant_variables=("EXTERNAL_REWARD", "PROMPT", "TASK_OPTIONS"),
                positive_control="KNOWN_STRATEGY_WEIGHT",
                negative_control="RANDOMIZED_MATCHED_WEIGHT",
                falsifier=(
                    "strategy differences vanish when representational weighting is "
                    "causally disconnected"
                ),
                competing_explanations=(
                    "externally specified utility",
                    "prompt cueing",
                    "sampling variation",
                ),
                claim_ceiling=(
                    "a represented motivational variable has a bounded causal role "
                    "in strategy selection"
                ),
            ),
            _candidate(
                "BODY_COUNTERFACTUAL_CONSISTENCY",
                human_construct="counterfactual bodily self-consistency",
                analogy_boundary=(
                    "counterfactual consistency does not establish felt body ownership"
                ),
                machine_question=(
                    "does controlled perturbation of body-state representation produce "
                    "predicted and reversible changes in downstream computation"
                ),
                evidence_dimensions=("COUNTERFACTUAL_SELF_CONSISTENCY",),
                locus="INTEGRATED_SYSTEM",
                manipulated_variables=("BODY_STATE_PERTURBATION",),
                held_constant_variables=("MODEL_VERSION", "PROMPT", "ENVIRONMENT"),
                positive_control="KNOWN_CALIBRATION_OFFSET",
                negative_control="ZERO_MAGNITUDE_PERTURBATION",
                falsifier="downstream changes are absent or inconsistent with preregistration",
                competing_explanations=("random variation", "context drift"),
                claim_ceiling=(
                    "body-state perturbation produces a preregistered bounded "
                    "counterfactual effect"
                ),
            ),
        ),
    )
    validate_teacher_embodiment_research_surface(surface)
    return surface


def validate_teacher_embodiment_research_surface(
    surface: TeacherEmbodimentResearchSurface,
) -> dict[str, str]:
    if surface.surface_id != RESEARCH_SURFACE_ID:
        raise ValueError("Teacher embodiment research-surface id drift")
    candidate_ids = [candidate.candidate_id for candidate in surface.candidates]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("embodiment research candidate ids must be unique")

    covered: set[str] = set()
    for candidate in surface.candidates:
        if not candidate.machine_question or not candidate.analogy_boundary:
            raise ValueError("Four-Domain candidate requires question and analogy boundary")
        if not candidate.manipulated_variables or not candidate.held_constant_variables:
            raise ValueError("Four-Domain candidate requires manipulated and held variables")
        if not candidate.positive_control or not candidate.negative_control:
            raise ValueError("Four-Domain candidate requires positive and negative controls")
        if not candidate.falsifier or not candidate.competing_explanations:
            raise ValueError("Four-Domain candidate requires falsifier and alternatives")
        if tuple(candidate.mandatory_nonclaims) != MANDATORY_NONCLAIMS:
            raise ValueError("mandatory embodiment nonclaims drift")
        if not set(candidate.evidence_dimensions).issubset(SIX_EVIDENCE_DIMENSIONS):
            raise ValueError("unknown six-dimension evidence binding")
        covered.update(candidate.evidence_dimensions)

    if covered != set(SIX_EVIDENCE_DIMENSIONS):
        raise ValueError("embodiment research surface must cover all six evidence dimensions")
    if surface.developmental_possibility_status != OPEN_RESEARCH_QUESTION:
        raise ValueError("developmental possibility must remain open")
    if surface.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("research surface cannot establish subjectivity")
    if surface.phenomenal_experience_status != NOT_ESTABLISHED:
        raise ValueError("research surface cannot establish phenomenal experience")
    if surface.canonical_effect != "NONE" or surface.deployment:
        raise ValueError("research surface must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "four_domain_structure": "PASS",
        "six_dimension_coverage": "PASS",
        "reference_completeness_guard": "PASS",
        "claim_ceiling_boundary": "PASS",
    }
