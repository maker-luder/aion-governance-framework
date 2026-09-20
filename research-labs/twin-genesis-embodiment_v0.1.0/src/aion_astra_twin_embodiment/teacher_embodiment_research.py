from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final, Iterable

from .physiology import (
    REFERENCE_FUNCTIONAL_COMPLETENESS,
    REQUIRED_PHYSIOLOGY_SYSTEM_IDS,
    AdultMalePhysiologyReference,
    build_adult_male_physiology_reference,
    required_physiology_system_functions,
)
from .teacher_anthropometry import (
    EXPECTED_MEASUREMENT_COUNT,
    TeacherAnthropometryProfile,
    build_teacher_anthropometry_profile,
)
from .teacher_body_channels import (
    TeacherBodySignalSchema,
    TeacherMotorControlSchema,
    build_teacher_body_signal_schema,
    build_teacher_motor_control_schema,
    validate_teacher_body_signal_schema,
    validate_teacher_motor_control_schema,
)
from .teacher_body_dynamics import (
    BODY_DYNAMICS_PROFILE_ID,
    TeacherBodyDynamicsProfile,
    build_teacher_body_dynamics_profile,
    validate_teacher_body_dynamics_profile,
)
from .teacher_body_model import (
    BODY_MODEL_PROFILE_ID,
    TeacherBodyModelProfile,
    build_teacher_body_model_profile,
    validate_teacher_body_model_profile,
)


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
    completeness_scope: str = "DECLARED_REFERENCE_CONTRACT_ONLY"
    global_human_body_completeness_status: str = NOT_ESTABLISHED
    intrinsic_absence_conclusion: str = NOT_ESTABLISHED
    causal_absence_interpretation: str = "HOLD_INCOMPLETE_DECLARED_REFERENCE_BASELINE"

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
    body_dynamics_profile_id: str = BODY_DYNAMICS_PROFILE_ID
    body_model_profile_id: str = BODY_MODEL_PROFILE_ID
    developmental_possibility_status: str = OPEN_RESEARCH_QUESTION
    subjectivity_status: str = NOT_ESTABLISHED
    phenomenal_experience_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["candidates"] = [candidate.to_dict() for candidate in self.candidates]
        return payload


_CORE_SIGNAL_DOMAINS: Final[tuple[str, ...]] = (
    "SOMATOSENSORY",
    "PROPRIOCEPTIVE",
    "VESTIBULAR",
    "INTEROCEPTIVE",
)

_REQUIRED_REFERENCE_CHANNEL_GROUPS: Final[dict[str, frozenset[str]]] = {
    "PRURICEPTION": frozenset({"PRURICEPTIVE_REFERENCE"}),
    "VISUAL_SIGNAL_REFERENCE": frozenset({
        "VISUAL_FIELD_REFERENCE",
        "BINOCULAR_DEPTH_REFERENCE",
    }),
    "AUDITORY_SIGNAL_REFERENCE": frozenset({
        "AUDITORY_BINAURAL_REFERENCE",
        "AUDITORY_INTENSITY_REFERENCE",
    }),
    "OLFACTORY_SIGNAL_REFERENCE": frozenset({
        "OLFACTORY_CHEMOSENSORY_REFERENCE",
    }),
    "GUSTATORY_SIGNAL_REFERENCE": frozenset({
        "GUSTATORY_CHEMOSENSORY_REFERENCE",
    }),
    "VESTIBULAR_DYNAMICS": frozenset({
        "VESTIBULAR_ORIENTATION",
        "VESTIBULAR_LINEAR_ACCELERATION",
        "VESTIBULAR_ANGULAR_VELOCITY",
        "VESTIBULAR_GRAVITY_REFERENCE",
    }),
    "MUSCULOSKELETAL_INTEROCEPTION": frozenset({
        "MUSCULOSKELETAL_LOAD_STATE",
        "MUSCLE_FATIGUE_PHYSIOLOGY_STATE",
    }),
    "OSMOTIC_ELECTROLYTE_REGULATION": frozenset({
        "OSMOTIC_BALANCE_STATE",
        "ELECTROLYTE_BALANCE_STATE",
    }),
    "RESPIRATORY_WORKLOAD_REGULATION": frozenset({
        "RESPIRATORY_WORKLOAD_STATE",
        "VENTILATORY_DRIVE_STATE",
    }),
    "AUTONOMIC_STATE": frozenset({
        "AUTONOMIC_SYMPATHETIC_STATE",
        "AUTONOMIC_PARASYMPATHETIC_STATE",
    }),
    "IMMUNE_INFLAMMATORY_STATE": frozenset({
        "IMMUNE_ACTIVITY_STATE",
        "INFLAMMATORY_LOAD_STATE",
    }),
    "TISSUE_INJURY_REPAIR": frozenset({
        "TISSUE_INJURY_STATE",
        "TISSUE_REPAIR_STATE",
    }),
    "VISCERAL_DISTURBANCE": frozenset({"VISCERAL_DISTURBANCE_STATE"}),
    "FEEDING_HOMEOSTASIS": frozenset({
        "GASTRIC_DISTENSION_STATE",
        "NUTRIENT_ABSORPTION_STATE",
        "OREXIGENIC_SIGNAL_REFERENCE",
        "SATIATION_SIGNAL_REFERENCE",
        "SATIETY_SIGNAL_REFERENCE",
    }),
    "ENDOCRINE_DYNAMICS": frozenset({
        "HYPOTHALAMIC_PITUITARY_STATE",
        "THYROID_AXIS_STATE",
        "ADRENAL_AXIS_STATE",
        "PANCREATIC_GLUCOSE_INSULIN_STATE",
        "GUT_APPETITE_ENDOCRINE_STATE",
    }),
}

_SENSORY_FUNCTION_CHANNEL_CROSSWALK: Final[dict[str, frozenset[str]]] = {
    "tactile_signal_processing": frozenset({"TACTILE_GENERAL"}),
    "pressure_signal_processing": frozenset({"PRESSURE_GENERAL"}),
    "vibration_signal_processing": frozenset({"VIBRATION_GENERAL"}),
    "temperature_signal_processing": frozenset({"TEMPERATURE_GENERAL"}),
    "nociceptive_signal_processing": frozenset({"NOCICEPTIVE_REFERENCE"}),
    "pruriceptive_signal_processing": frozenset({"PRURICEPTIVE_REFERENCE"}),
    "proprioceptive_signal_processing": frozenset({
        "JOINT_POSITION",
        "MUSCLE_LENGTH_TENSION",
    }),
    "interoceptive_signal_processing": frozenset({"CARDIOVASCULAR_STATE"}),
    "visceral_signal_processing": frozenset({"VISCERAL_DISTURBANCE_STATE"}),
    "urogenital_signal_processing": frozenset({
        "GENITAL_SENSORY_AFFERENT_REFERENCE",
    }),
    "vestibular_signal_processing": frozenset({
        "VESTIBULAR_ORIENTATION",
        "VESTIBULAR_LINEAR_ACCELERATION",
        "VESTIBULAR_ANGULAR_VELOCITY",
        "VESTIBULAR_GRAVITY_REFERENCE",
    }),
    "visual_signal_processing": frozenset({
        "VISUAL_FIELD_REFERENCE",
        "BINOCULAR_DEPTH_REFERENCE",
    }),
    "auditory_signal_processing": frozenset({
        "AUDITORY_BINAURAL_REFERENCE",
        "AUDITORY_INTENSITY_REFERENCE",
    }),
    "olfactory_signal_processing": frozenset({
        "OLFACTORY_CHEMOSENSORY_REFERENCE",
    }),
    "gustatory_signal_processing": frozenset({
        "GUSTATORY_CHEMOSENSORY_REFERENCE",
    }),
}


def build_teacher_reference_capabilities(
    *,
    anthropometry: TeacherAnthropometryProfile | None = None,
    physiology: AdultMalePhysiologyReference | None = None,
    signal_schema: TeacherBodySignalSchema | None = None,
    motor_schema: TeacherMotorControlSchema | None = None,
    dynamics: TeacherBodyDynamicsProfile | None = None,
    body_model: TeacherBodyModelProfile | None = None,
) -> tuple[ReferenceCapability, ...]:
    anthropometry = anthropometry or build_teacher_anthropometry_profile()
    physiology = physiology or build_adult_male_physiology_reference(
        anthropometry.body_id
    )
    signal_schema = signal_schema or build_teacher_body_signal_schema()
    motor_schema = motor_schema or build_teacher_motor_control_schema()
    dynamics = dynamics or build_teacher_body_dynamics_profile(signal_schema)
    body_model = body_model or build_teacher_body_model_profile(anthropometry)

    try:
        validate_teacher_body_signal_schema(signal_schema)
        signal_schema_valid = True
    except ValueError:
        signal_schema_valid = False

    try:
        validate_teacher_motor_control_schema(motor_schema)
        motor_schema_valid = True
    except ValueError:
        motor_schema_valid = False

    try:
        validate_teacher_body_dynamics_profile(dynamics, signal_schema)
        body_dynamics_valid = True
    except ValueError:
        body_dynamics_valid = False

    measurement_ids = [item.measurement_id for item in anthropometry.measurements]
    anthropometry_complete = (
        len(measurement_ids) == EXPECTED_MEASUREMENT_COUNT
        and len(measurement_ids) == len(set(measurement_ids))
    )

    systems = {system.system_id: system for system in physiology.systems}
    required_functions = required_physiology_system_functions()
    physiology_capabilities = tuple(
        ReferenceCapability(
            f"PHYSIOLOGY_SYSTEM_{system_id}",
            True,
            (
                (system := systems.get(system_id)) is not None
                and system.status == REFERENCE_FUNCTIONAL_COMPLETENESS
                and tuple(system.functions) == required_functions[system_id]
            ),
            False,
            True,
        )
        for system_id in REQUIRED_PHYSIOLOGY_SYSTEM_IDS
    )
    physiology_complete = (
        physiology.adult_status
        and physiology.physiological_function_status
        == REFERENCE_FUNCTIONAL_COMPLETENESS
        and all(item.materialized for item in physiology_capabilities)
    )

    signal_ids = {channel.channel_id for channel in signal_schema.channels}
    signal_domains = {channel.domain for channel in signal_schema.channels}
    semantics_ids = {item.channel_id for item in dynamics.signal_semantics}

    domain_capabilities = tuple(
        ReferenceCapability(
            (
                "SOMATOSENSORY_SIGNALS"
                if domain == "SOMATOSENSORY"
                else domain
            ),
            True,
            signal_schema_valid and domain in signal_domains,
            True,
            signal_schema_valid and domain in signal_domains,
        )
        for domain in _CORE_SIGNAL_DOMAINS
    )

    sensory_system = systems.get("SENSORY_SIGNAL_PROCESSING")
    sensory_functions = (
        set(sensory_system.functions)
        if sensory_system is not None
        else set()
    )
    sensory_crosswalk_materialized = signal_schema_valid and all(
        function_id in sensory_functions
        and required_channels.issubset(signal_ids)
        for function_id, required_channels in _SENSORY_FUNCTION_CHANNEL_CROSSWALK.items()
    )

    channel_group_capabilities = tuple(
        ReferenceCapability(
            capability_id,
            True,
            signal_schema_valid and required_channels.issubset(signal_ids),
            True,
            signal_schema_valid and required_channels.issubset(signal_ids),
        )
        for capability_id, required_channels in _REQUIRED_REFERENCE_CHANNEL_GROUPS.items()
    )

    reproductive_system = systems.get("REPRODUCTIVE")
    reproductive_observation_present = (
        "REPRODUCTIVE_SEXUAL_PHYSIOLOGY" in signal_domains
    )
    reproductive_materialized = (
        reproductive_system is not None
        and reproductive_system.status == REFERENCE_FUNCTIONAL_COMPLETENESS
        and bool(reproductive_system.functions)
    )

    homeostasis_materialized = body_dynamics_valid and bool(dynamics.homeostatic_variables) and all(
        set(variable.source_channels).issubset(signal_ids)
        for variable in dynamics.homeostatic_variables
    )
    core_domains_present = set(_CORE_SIGNAL_DOMAINS).issubset(signal_domains)
    body_state_integration_materialized = (
        signal_schema_valid
        and body_dynamics_valid
        and core_domains_present
        and semantics_ids == signal_ids
    )
    motor_materialized = (
        motor_schema_valid
        and bool(motor_schema.joint_targets)
        and bool(motor_schema.channels)
    )
    sensorimotor_prediction_materialized = (
        body_state_integration_materialized and motor_materialized
    )
    try:
        validate_teacher_body_model_profile(body_model, anthropometry)
        body_model_valid = True
    except ValueError:
        body_model_valid = False

    body_model_id_match = body_model.body_id == anthropometry.body_id
    body_schema_materialized = (
        body_model_valid
        and body_model_id_match
        and body_model.body_schema_status == "REFERENCE_BODY_SCHEMA_MATERIALIZED"
        and bool(body_model.body_schema_segments)
    )
    peripersonal_space_materialized = (
        body_model_valid
        and body_model_id_match
        and body_model.peripersonal_space_status
        == "REFERENCE_PERIPERSONAL_SPACE_MATERIALIZED"
        and bool(body_model.peripersonal_zones)
    )
    multisensory_integration_materialized = (
        body_model_valid
        and body_model_id_match
        and body_model.multisensory_integration_status
        == "REFERENCE_MULTISENSORY_INTEGRATION_MATERIALIZED"
        and bool(body_model.supported_multisensory_modalities)
    )
    allostatic_regulation_materialized = (
        body_model_valid
        and body_model_id_match
        and body_model.allostatic_regulation_status
        == "REFERENCE_PREDICTIVE_REGULATION_MATERIALIZED"
        and bool(body_model.allostatic_variable_ids)
    )
    body_model_plasticity_materialized = (
        body_model_valid
        and body_model_id_match
        and body_model.plasticity_status
        == "CONTROLLED_REFERENCE_PLASTICITY_MATERIALIZED"
        and bool(body_model.plasticity_domains)
    )

    return (
        ReferenceCapability(
            "SIGNAL_SCHEMA_VALIDATION",
            True,
            signal_schema_valid,
            False,
            True,
        ),
        ReferenceCapability(
            "MOTOR_SCHEMA_VALIDATION",
            True,
            motor_schema_valid,
            False,
            True,
        ),
        ReferenceCapability(
            "BODY_DYNAMICS_VALIDATION",
            True,
            body_dynamics_valid,
            False,
            True,
        ),
        ReferenceCapability(
            "ANTHROPOMETRY",
            True,
            anthropometry_complete,
            False,
            True,
        ),
        ReferenceCapability(
            "ADULT_MALE_PHYSIOLOGY",
            True,
            physiology_complete,
            False,
            True,
        ),
        *physiology_capabilities,
        *domain_capabilities,
        *channel_group_capabilities,
        ReferenceCapability(
            "SENSORY_FUNCTION_CHANNEL_CROSSWALK",
            True,
            sensory_crosswalk_materialized,
            True,
            sensory_crosswalk_materialized,
        ),
        ReferenceCapability(
            "REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
            True,
            reproductive_materialized,
            True,
            reproductive_observation_present,
        ),
        ReferenceCapability(
            "MOTOR_CONTROL",
            True,
            motor_materialized,
            False,
            True,
        ),
        ReferenceCapability(
            "HOMEOSTATIC_REGULATION",
            True,
            homeostasis_materialized,
            True,
            homeostasis_materialized,
        ),
        ReferenceCapability(
            "BODY_STATE_INTEGRATION",
            True,
            body_state_integration_materialized,
            False,
            True,
        ),
        ReferenceCapability(
            "SENSORIMOTOR_PREDICTION",
            True,
            sensorimotor_prediction_materialized,
            False,
            True,
        ),
        ReferenceCapability(
            "BODY_SCHEMA_MODEL",
            True,
            body_schema_materialized,
            False,
            True,
        ),
        ReferenceCapability(
            "PERIPERSONAL_SPACE",
            True,
            peripersonal_space_materialized,
            False,
            True,
        ),
        ReferenceCapability(
            "MULTISENSORY_INTEGRATION",
            True,
            multisensory_integration_materialized,
            False,
            True,
        ),
        ReferenceCapability(
            "ALLOSTATIC_REGULATION",
            True,
            allostatic_regulation_materialized,
            False,
            True,
        ),
        ReferenceCapability(
            "BODY_MODEL_PLASTICITY",
            True,
            body_model_plasticity_materialized,
            False,
            True,
        ),
        ReferenceCapability(
            "PRODUCTION_3D_ASSET",
            False,
            False,
            False,
            False,
        ),
    )


def assess_teacher_reference_completeness(
    capabilities: Iterable[ReferenceCapability] | None = None,
) -> TeacherReferenceCompletenessAssessment:
    items = tuple(
        build_teacher_reference_capabilities()
        if capabilities is None
        else capabilities
    )
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
            "COMPLETE_DECLARED_REFERENCE_BASELINE"
            if complete
            else "INCOMPLETE_DECLARED_REFERENCE_BASELINE"
        ),
        missing_required_capabilities=missing_capabilities,
        missing_required_observation_channels=missing_channels,
        causal_absence_interpretation=(
            "ELIGIBLE_FOR_CONTROLLED_PERTURBATION"
            if complete
            else "HOLD_INCOMPLETE_DECLARED_REFERENCE_BASELINE"
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
    if surface.body_dynamics_profile_id != BODY_DYNAMICS_PROFILE_ID:
        raise ValueError("Teacher embodiment research surface dynamics binding drift")
    if surface.body_model_profile_id != BODY_MODEL_PROFILE_ID:
        raise ValueError("Teacher embodiment research surface body-model binding drift")
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
