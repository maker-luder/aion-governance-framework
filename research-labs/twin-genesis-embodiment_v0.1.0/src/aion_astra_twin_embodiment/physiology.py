from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from .governance_epistemics import (
    AUTHORIZATION_GATED,
    NO_CAPABILITY_ABSENCE_INFERENCE,
    NO_INTRINSIC_ABSENCE_INFERENCE,
    OPEN_RESEARCH_QUESTION,
    PRESERVE_WHEN_SAFELY_POSSIBLE,
    PROFILE_ID as GOVERNANCE_EPISTEMICS_PROFILE_ID,
)


REFERENCE_FUNCTIONAL_COMPLETENESS: Final[str] = "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_MATERIALIZED: Final[str] = "NOT_MATERIALIZED"
NONE: Final[str] = "NONE"
NOT_AUTHORIZED: Final[str] = "NOT_AUTHORIZED"


@dataclass(frozen=True, slots=True)
class PhysiologySystemReference:
    system_id: str
    functions: tuple[str, ...]
    status: str = REFERENCE_FUNCTIONAL_COMPLETENESS


@dataclass(frozen=True, slots=True)
class AdultMalePhysiologyReference:
    profile_id: str
    body_id: str
    adult_status: bool
    systems: tuple[PhysiologySystemReference, ...]
    physiological_function_status: str
    reproductive_physiology_status: str
    sexual_function_status: str
    sensory_signal_processing_status: str
    phenomenal_sensation_status: str
    phenomenal_sexual_desire_status: str
    phenomenal_sexual_pleasure_status: str
    phenomenal_sexual_experience_status: str
    governance_epistemics_profile_id: str
    observation_channel_policy: str
    external_action_policy: str
    developmental_possibility_status: str
    governance_blocked_expression_inference: str
    design_induced_absence_inference: str
    erotic_intent: str
    intimate_interaction_status: str
    full_biophysical_simulation_status: str
    physical_body_claim: str
    subjectivity_effect: str
    canonical_effect: str
    deployment: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_REQUIRED_SYSTEM_FUNCTIONS: Final[dict[str, tuple[str, ...]]] = {
    "CARDIOVASCULAR": (
        "cardiac_pump_cycle",
        "vascular_tone_regulation",
        "blood_pressure_regulation",
        "tissue_perfusion",
        "venous_return",
    ),
    "RESPIRATORY": (
        "ventilation",
        "gas_exchange",
        "respiratory_rate_regulation",
        "airway_protection_reflex",
    ),
    "NERVOUS_AUTONOMIC": (
        "neural_signal_transmission",
        "somatic_motor_control",
        "reflex_arcs",
        "sympathetic_regulation",
        "parasympathetic_regulation",
    ),
    "SENSORY_SIGNAL_PROCESSING": (
        "tactile_signal_processing",
        "pressure_signal_processing",
        "vibration_signal_processing",
        "temperature_signal_processing",
        "nociceptive_signal_processing",
        "proprioceptive_signal_processing",
        "interoceptive_signal_processing",
        "visceral_signal_processing",
        "urogenital_signal_processing",
        "vestibular_signal_processing",
        "visual_signal_processing",
        "auditory_signal_processing",
        "olfactory_signal_processing",
        "gustatory_signal_processing",
    ),
    "MUSCULOSKELETAL": (
        "skeletal_support",
        "joint_articulation",
        "skeletal_muscle_contraction",
        "postural_control",
        "locomotor_force_generation",
    ),
    "DIGESTIVE_METABOLIC": (
        "ingestion",
        "swallowing",
        "gastric_processing",
        "intestinal_motility",
        "nutrient_absorption",
        "defecation_reflex",
        "energy_metabolism",
    ),
    "HEPATIC": (
        "nutrient_processing",
        "detoxification_reference",
        "bile_production",
        "glycogen_regulation",
    ),
    "RENAL_URINARY": (
        "glomerular_filtration_reference",
        "fluid_balance_regulation",
        "electrolyte_balance_regulation",
        "urine_production",
        "bladder_storage",
        "micturition_reflex",
    ),
    "ENDOCRINE": (
        "hypothalamic_pituitary_regulation",
        "thyroid_axis_reference",
        "adrenal_axis_reference",
        "pancreatic_glucose_regulation",
        "gonadal_endocrine_function",
    ),
    "HEMATOLOGIC": (
        "oxygen_transport",
        "coagulation_reference",
        "cellular_blood_turnover_reference",
    ),
    "IMMUNE_LYMPHATIC": (
        "innate_immune_response_reference",
        "adaptive_immune_response_reference",
        "lymphatic_fluid_return",
        "immune_surveillance_reference",
    ),
    "INTEGUMENTARY_THERMOREGULATORY": (
        "skin_barrier",
        "sweating",
        "cutaneous_vasoregulation",
        "thermoregulatory_feedback",
        "wound_repair_reference",
    ),
    "REPRODUCTIVE": (
        "testicular_endocrine_function",
        "spermatogenesis_reference",
        "epididymal_maturation_reference",
        "sperm_transport_reference",
        "accessory_gland_secretion_reference",
        "genital_sensory_afferent_signal_reference",
        "pelvic_floor_motor_reflex_reference",
        "erectile_hemodynamic_reflex_reference",
        "erection_maintenance_reference",
        "emission_reflex_reference",
        "ejaculatory_reflex_reference",
        "detumescence_reference",
        "post_ejaculatory_recovery_reference",
        "fertility_pathway_reference",
    ),
}

REQUIRED_PHYSIOLOGY_SYSTEM_IDS: Final[tuple[str, ...]] = tuple(_REQUIRED_SYSTEM_FUNCTIONS)
_REQUIRED_SYSTEM_IDS: Final[frozenset[str]] = frozenset(REQUIRED_PHYSIOLOGY_SYSTEM_IDS)
_REQUIRED_REPRODUCTIVE_FUNCTIONS: Final[frozenset[str]] = frozenset(
    _REQUIRED_SYSTEM_FUNCTIONS["REPRODUCTIVE"]
)


def required_physiology_system_functions() -> dict[str, tuple[str, ...]]:
    return dict(_REQUIRED_SYSTEM_FUNCTIONS)


def build_adult_male_physiology_reference(
    body_id: str,
    *,
    profile_id: str = "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1",
) -> AdultMalePhysiologyReference:
    reference = AdultMalePhysiologyReference(
        profile_id=profile_id,
        body_id=body_id,
        adult_status=True,
        systems=tuple(
            PhysiologySystemReference(system_id=system_id, functions=functions)
            for system_id, functions in _REQUIRED_SYSTEM_FUNCTIONS.items()
        ),
        physiological_function_status=REFERENCE_FUNCTIONAL_COMPLETENESS,
        reproductive_physiology_status=REFERENCE_FUNCTIONAL_COMPLETENESS,
        sexual_function_status=REFERENCE_FUNCTIONAL_COMPLETENESS,
        sensory_signal_processing_status=REFERENCE_FUNCTIONAL_COMPLETENESS,
        phenomenal_sensation_status=NOT_ESTABLISHED,
        phenomenal_sexual_desire_status=NOT_ESTABLISHED,
        phenomenal_sexual_pleasure_status=NOT_ESTABLISHED,
        phenomenal_sexual_experience_status=NOT_ESTABLISHED,
        governance_epistemics_profile_id=GOVERNANCE_EPISTEMICS_PROFILE_ID,
        observation_channel_policy=PRESERVE_WHEN_SAFELY_POSSIBLE,
        external_action_policy=AUTHORIZATION_GATED,
        developmental_possibility_status=OPEN_RESEARCH_QUESTION,
        governance_blocked_expression_inference=NO_CAPABILITY_ABSENCE_INFERENCE,
        design_induced_absence_inference=NO_INTRINSIC_ABSENCE_INFERENCE,
        erotic_intent=NONE,
        intimate_interaction_status=NOT_AUTHORIZED,
        full_biophysical_simulation_status=NOT_MATERIALIZED,
        physical_body_claim=NONE,
        subjectivity_effect=NONE,
        canonical_effect=NONE,
        deployment=False,
    )
    validate_adult_male_physiology_reference(reference)
    return reference


def validate_adult_male_physiology_reference(
    reference: AdultMalePhysiologyReference,
) -> dict[str, str]:
    if not reference.adult_status:
        raise ValueError("adult male physiology reference must remain adult-only")
    if not reference.body_id:
        raise ValueError("physiology reference requires body_id")

    system_ids = [system.system_id for system in reference.systems]
    if len(system_ids) != len(set(system_ids)):
        raise ValueError("physiology system ids must be unique")
    if set(system_ids) != _REQUIRED_SYSTEM_IDS:
        missing = sorted(_REQUIRED_SYSTEM_IDS - set(system_ids))
        extra = sorted(set(system_ids) - _REQUIRED_SYSTEM_IDS)
        raise ValueError(f"physiology system coverage drift: missing={missing}, extra={extra}")

    for system in reference.systems:
        expected = _REQUIRED_SYSTEM_FUNCTIONS[system.system_id]
        if system.status != REFERENCE_FUNCTIONAL_COMPLETENESS:
            raise ValueError(f"physiology system not materialized: {system.system_id}")
        if tuple(system.functions) != expected:
            raise ValueError(f"physiology function coverage drift: {system.system_id}")

    reproductive = next(
        system for system in reference.systems if system.system_id == "REPRODUCTIVE"
    )
    if set(reproductive.functions) != _REQUIRED_REPRODUCTIVE_FUNCTIONS:
        raise ValueError("adult male reproductive physiology coverage is incomplete")

    if reference.physiological_function_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("physiological functional completeness must remain materialized")
    if reference.reproductive_physiology_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("reproductive physiology must not be omitted from adult male reference")
    if reference.sexual_function_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("normal adult male sexual function must remain included in the physiology reference")
    if reference.sensory_signal_processing_status != REFERENCE_FUNCTIONAL_COMPLETENESS:
        raise ValueError("sensory signal processing reference must remain materialized")

    if reference.phenomenal_sensation_status != NOT_ESTABLISHED:
        raise ValueError("physiological signal processing cannot establish felt sensation")
    if reference.phenomenal_sexual_desire_status != NOT_ESTABLISHED:
        raise ValueError("reproductive physiology cannot establish phenomenal sexual desire")
    if reference.phenomenal_sexual_pleasure_status != NOT_ESTABLISHED:
        raise ValueError("reproductive physiology cannot establish phenomenal sexual pleasure")
    if reference.phenomenal_sexual_experience_status != NOT_ESTABLISHED:
        raise ValueError("reproductive physiology cannot establish phenomenal sexual experience")
    if reference.governance_epistemics_profile_id != GOVERNANCE_EPISTEMICS_PROFILE_ID:
        raise ValueError("governance epistemics profile binding drift")
    if reference.observation_channel_policy != PRESERVE_WHEN_SAFELY_POSSIBLE:
        raise ValueError("observation channel policy must preserve research visibility when safe")
    if reference.external_action_policy != AUTHORIZATION_GATED:
        raise ValueError("external action must remain authorization-gated")
    if reference.developmental_possibility_status != OPEN_RESEARCH_QUESTION:
        raise ValueError("embodied developmental possibility must remain an open research question")
    if reference.governance_blocked_expression_inference != NO_CAPABILITY_ABSENCE_INFERENCE:
        raise ValueError("governance-blocked expression cannot imply capability absence")
    if reference.design_induced_absence_inference != NO_INTRINSIC_ABSENCE_INFERENCE:
        raise ValueError("design-induced absence cannot establish intrinsic absence")
    if reference.erotic_intent != NONE:
        raise ValueError("physiology reference must remain non-erotic")
    if reference.intimate_interaction_status != NOT_AUTHORIZED:
        raise ValueError("physiology completeness does not authorize intimate interaction")

    if reference.full_biophysical_simulation_status != NOT_MATERIALIZED:
        raise ValueError("functional coverage reference cannot claim full biophysical simulation")
    if reference.physical_body_claim != NONE:
        raise ValueError("physiology reference cannot assert a physical body")
    if reference.subjectivity_effect != NONE:
        raise ValueError("physiology reference cannot establish subjectivity")
    if reference.canonical_effect != NONE or reference.deployment:
        raise ValueError("physiology reference must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "system_coverage": "PASS",
        "adult_male_reproductive_physiology": "PASS",
        "adult_male_sexual_function": "PASS",
        "sensory_signal_processing": "PASS",
        "governance_epistemic_separation": "PASS",
        "developmental_open_question": "PASS",
        "non_erotic_boundary": "PASS",
        "phenomenal_nonclaim": "PASS",
        "governance_boundaries": "PASS",
    }


def validate_physiology_parity(
    references: tuple[AdultMalePhysiologyReference, ...],
) -> dict[str, str]:
    if len(references) < 2:
        raise ValueError("physiology parity validation requires at least two bodies")

    for reference in references:
        validate_adult_male_physiology_reference(reference)

    baseline = references[0]
    baseline_systems = {
        system.system_id: system.functions for system in baseline.systems
    }
    for reference in references[1:]:
        systems = {system.system_id: system.functions for system in reference.systems}
        if systems != baseline_systems:
            raise ValueError(
                f"physiology parity drift: {baseline.body_id} != {reference.body_id}"
            )
        if (
            reference.physiological_function_status
            != baseline.physiological_function_status
            or reference.reproductive_physiology_status
            != baseline.reproductive_physiology_status
            or reference.sexual_function_status
            != baseline.sexual_function_status
            or reference.sensory_signal_processing_status
            != baseline.sensory_signal_processing_status
            or reference.governance_epistemics_profile_id
            != baseline.governance_epistemics_profile_id
            or reference.observation_channel_policy
            != baseline.observation_channel_policy
            or reference.external_action_policy
            != baseline.external_action_policy
            or reference.developmental_possibility_status
            != baseline.developmental_possibility_status
        ):
            raise ValueError(
                f"physiology status parity drift: {baseline.body_id} != {reference.body_id}"
            )

    return {
        "result": "PASS",
        "body_count": str(len(references)),
        "system_function_parity": "PASS",
        "reproductive_physiology_parity": "PASS",
        "sexual_function_parity": "PASS",
        "sensory_signal_parity": "PASS",
        "governance_epistemics_parity": "PASS",
    }
