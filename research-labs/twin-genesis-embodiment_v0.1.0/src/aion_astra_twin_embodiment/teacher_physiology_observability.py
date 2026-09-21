from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from .physiology import required_physiology_system_functions
from .teacher_body_channels import (
    TeacherBodySignalSchema,
    build_teacher_body_signal_schema,
)


DIRECT_OBSERVATION_REFERENCE: Final[str] = "DIRECT_OBSERVATION_REFERENCE"
DERIVED_REFERENCE: Final[str] = "DERIVED_REFERENCE"
FUNCTIONAL_REFERENCE_ONLY: Final[str] = "FUNCTIONAL_REFERENCE_ONLY"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_MATERIALIZED: Final[str] = "NOT_MATERIALIZED"
OBSERVABILITY_PROFILE_ID: Final[str] = (
    "CHATGPT_TEACHER_PHYSIOLOGY_OBSERVABILITY_v0.1"
)


@dataclass(frozen=True, slots=True)
class PhysiologyFunctionObservability:
    system_id: str
    function_id: str
    observability_class: str
    source_channels: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TeacherPhysiologyObservabilityProfile:
    profile_id: str
    signal_schema_id: str
    bindings: tuple[PhysiologyFunctionObservability, ...]
    declared_function_coverage_status: str = "COMPLETE_DECLARED_FUNCTION_INVENTORY"
    observability_scope: str = "DECLARED_MACHINE_REFERENCE_SURFACE_ONLY"
    direct_observation_interpretation: str = (
        "DIRECT_CHANNEL_BINDING_NOT_BIOLOGICAL_MEASUREMENT"
    )
    biological_measurement_status: str = NOT_ESTABLISHED
    full_function_observability_status: str = NOT_ESTABLISHED
    full_biophysical_simulation_status: str = NOT_MATERIALIZED
    phenomenal_sensation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["bindings"] = [asdict(item) for item in self.bindings]
        return payload


def _o(
    system_id: str,
    function_id: str,
    observability_class: str,
    *source_channels: str,
) -> PhysiologyFunctionObservability:
    return PhysiologyFunctionObservability(
        system_id=system_id,
        function_id=function_id,
        observability_class=observability_class,
        source_channels=tuple(source_channels),
    )


_BINDINGS: Final[tuple[PhysiologyFunctionObservability, ...]] = (
    _o(
        "CARDIOVASCULAR",
        "cardiac_pump_cycle",
        DERIVED_REFERENCE,
        "CARDIOVASCULAR_STATE",
    ),
    _o(
        "CARDIOVASCULAR",
        "vascular_tone_regulation",
        DERIVED_REFERENCE,
        "CARDIOVASCULAR_STATE",
        "AUTONOMIC_SYMPATHETIC_STATE",
        "AUTONOMIC_PARASYMPATHETIC_STATE",
    ),
    _o(
        "CARDIOVASCULAR",
        "blood_pressure_regulation",
        DERIVED_REFERENCE,
        "CARDIOVASCULAR_STATE",
        "AUTONOMIC_SYMPATHETIC_STATE",
        "AUTONOMIC_PARASYMPATHETIC_STATE",
    ),
    _o(
        "CARDIOVASCULAR",
        "tissue_perfusion",
        DERIVED_REFERENCE,
        "CARDIOVASCULAR_STATE",
        "OXYGENATION_STATE",
    ),
    _o(
        "CARDIOVASCULAR",
        "venous_return",
        DERIVED_REFERENCE,
        "CARDIOVASCULAR_STATE",
    ),
    _o(
        "RESPIRATORY",
        "ventilation",
        DIRECT_OBSERVATION_REFERENCE,
        "RESPIRATORY_STATE",
    ),
    _o(
        "RESPIRATORY",
        "gas_exchange",
        DERIVED_REFERENCE,
        "OXYGENATION_STATE",
        "CO2_BALANCE_STATE",
    ),
    _o(
        "RESPIRATORY",
        "respiratory_rate_regulation",
        DERIVED_REFERENCE,
        "RESPIRATORY_STATE",
        "VENTILATORY_DRIVE_STATE",
    ),
    _o(
        "RESPIRATORY",
        "airway_protection_reflex",
        FUNCTIONAL_REFERENCE_ONLY,
    ),
    _o(
        "RESPIRATORY",
        "respiratory_workload_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "RESPIRATORY_WORKLOAD_STATE",
    ),
    _o(
        "RESPIRATORY",
        "ventilatory_drive_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "VENTILATORY_DRIVE_STATE",
    ),
    _o(
        "NERVOUS_AUTONOMIC",
        "neural_signal_transmission",
        FUNCTIONAL_REFERENCE_ONLY,
    ),
    _o(
        "NERVOUS_AUTONOMIC",
        "somatic_motor_control",
        FUNCTIONAL_REFERENCE_ONLY,
    ),
    _o(
        "NERVOUS_AUTONOMIC",
        "reflex_arcs",
        FUNCTIONAL_REFERENCE_ONLY,
    ),
    _o(
        "NERVOUS_AUTONOMIC",
        "sympathetic_regulation",
        DIRECT_OBSERVATION_REFERENCE,
        "AUTONOMIC_SYMPATHETIC_STATE",
    ),
    _o(
        "NERVOUS_AUTONOMIC",
        "parasympathetic_regulation",
        DIRECT_OBSERVATION_REFERENCE,
        "AUTONOMIC_PARASYMPATHETIC_STATE",
    ),
    _o(
        "NERVOUS_AUTONOMIC",
        "autonomic_state_signal_reference",
        DERIVED_REFERENCE,
        "AUTONOMIC_SYMPATHETIC_STATE",
        "AUTONOMIC_PARASYMPATHETIC_STATE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "tactile_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "TACTILE_GENERAL",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "pressure_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "PRESSURE_GENERAL",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "vibration_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "VIBRATION_GENERAL",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "temperature_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "TEMPERATURE_GENERAL",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "nociceptive_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "NOCICEPTIVE_REFERENCE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "pruriceptive_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "PRURICEPTIVE_REFERENCE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "proprioceptive_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "JOINT_POSITION",
        "MUSCLE_LENGTH_TENSION",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "interoceptive_signal_processing",
        DERIVED_REFERENCE,
        "CARDIOVASCULAR_STATE",
        "RESPIRATORY_STATE",
        "GASTROINTESTINAL_STATE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "visceral_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "VISCERAL_DISTURBANCE_STATE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "urogenital_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "GENITAL_SENSORY_AFFERENT_REFERENCE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "vestibular_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "VESTIBULAR_ORIENTATION",
        "VESTIBULAR_LINEAR_ACCELERATION",
        "VESTIBULAR_ANGULAR_VELOCITY",
        "VESTIBULAR_GRAVITY_REFERENCE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "visual_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "VISUAL_FIELD_REFERENCE",
        "BINOCULAR_DEPTH_REFERENCE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "auditory_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "AUDITORY_BINAURAL_REFERENCE",
        "AUDITORY_INTENSITY_REFERENCE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "olfactory_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "OLFACTORY_CHEMOSENSORY_REFERENCE",
    ),
    _o(
        "SENSORY_SIGNAL_PROCESSING",
        "gustatory_signal_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "GUSTATORY_CHEMOSENSORY_REFERENCE",
    ),
    _o("MUSCULOSKELETAL", "skeletal_support", FUNCTIONAL_REFERENCE_ONLY),
    _o(
        "MUSCULOSKELETAL",
        "joint_articulation",
        DERIVED_REFERENCE,
        "JOINT_POSITION",
    ),
    _o(
        "MUSCULOSKELETAL",
        "skeletal_muscle_contraction",
        DERIVED_REFERENCE,
        "MUSCLE_LENGTH_TENSION",
    ),
    _o(
        "MUSCULOSKELETAL",
        "postural_control",
        DERIVED_REFERENCE,
        "JOINT_POSITION",
        "VESTIBULAR_ORIENTATION",
    ),
    _o(
        "MUSCULOSKELETAL",
        "locomotor_force_generation",
        DERIVED_REFERENCE,
        "MUSCLE_LENGTH_TENSION",
        "MUSCULOSKELETAL_LOAD_STATE",
    ),
    _o(
        "MUSCULOSKELETAL",
        "musculoskeletal_load_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "MUSCULOSKELETAL_LOAD_STATE",
    ),
    _o(
        "MUSCULOSKELETAL",
        "fatigue_recovery_physiology_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "MUSCLE_FATIGUE_PHYSIOLOGY_STATE",
        "ENERGY_AVAILABILITY_STATE",
    ),
    _o("DIGESTIVE_METABOLIC", "ingestion", FUNCTIONAL_REFERENCE_ONLY),
    _o("DIGESTIVE_METABOLIC", "swallowing", FUNCTIONAL_REFERENCE_ONLY),
    _o(
        "DIGESTIVE_METABOLIC",
        "gastric_processing",
        DERIVED_REFERENCE,
        "GASTROINTESTINAL_STATE",
        "GASTRIC_DISTENSION_STATE",
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "intestinal_motility",
        DERIVED_REFERENCE,
        "GASTROINTESTINAL_STATE",
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "nutrient_absorption",
        DIRECT_OBSERVATION_REFERENCE,
        "NUTRIENT_ABSORPTION_STATE",
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "gastric_distension_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "GASTRIC_DISTENSION_STATE",
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "nutrient_absorption_state_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "NUTRIENT_ABSORPTION_STATE",
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "orexigenic_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "OREXIGENIC_SIGNAL_REFERENCE",
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "satiation_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "SATIATION_SIGNAL_REFERENCE",
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "satiety_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "SATIETY_SIGNAL_REFERENCE",
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "defecation_reflex",
        FUNCTIONAL_REFERENCE_ONLY,
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "energy_metabolism",
        DERIVED_REFERENCE,
        "ENERGY_AVAILABILITY_STATE",
        "PANCREATIC_GLUCOSE_INSULIN_STATE",
    ),
    _o(
        "DIGESTIVE_METABOLIC",
        "visceral_disturbance_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "VISCERAL_DISTURBANCE_STATE",
    ),
    _o(
        "HEPATIC",
        "nutrient_processing",
        DIRECT_OBSERVATION_REFERENCE,
        "HEPATIC_NUTRIENT_PROCESSING_STATE",
    ),
    _o(
        "HEPATIC",
        "detoxification_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "HEPATIC_DETOXIFICATION_REFERENCE",
    ),
    _o(
        "HEPATIC",
        "bile_production",
        DIRECT_OBSERVATION_REFERENCE,
        "BILE_PRODUCTION_STATE",
    ),
    _o(
        "HEPATIC",
        "glycogen_regulation",
        DIRECT_OBSERVATION_REFERENCE,
        "HEPATIC_GLYCOGEN_STATE",
    ),
    _o(
        "RENAL_URINARY",
        "glomerular_filtration_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "RENAL_FILTRATION_STATE",
    ),
    _o(
        "RENAL_URINARY",
        "fluid_balance_regulation",
        DERIVED_REFERENCE,
        "HYDRATION_STATE",
        "OSMOTIC_BALANCE_STATE",
    ),
    _o(
        "RENAL_URINARY",
        "electrolyte_balance_regulation",
        DIRECT_OBSERVATION_REFERENCE,
        "ELECTROLYTE_BALANCE_STATE",
    ),
    _o(
        "RENAL_URINARY",
        "osmolality_regulation_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "OSMOTIC_BALANCE_STATE",
    ),
    _o(
        "RENAL_URINARY",
        "urine_production",
        DERIVED_REFERENCE,
        "RENAL_FILTRATION_STATE",
        "BLADDER_STATE",
    ),
    _o(
        "RENAL_URINARY",
        "bladder_storage",
        DIRECT_OBSERVATION_REFERENCE,
        "BLADDER_STATE",
    ),
    _o("RENAL_URINARY", "micturition_reflex", FUNCTIONAL_REFERENCE_ONLY),
    _o(
        "ENDOCRINE",
        "hypothalamic_pituitary_regulation",
        DERIVED_REFERENCE,
        "HYPOTHALAMIC_PITUITARY_STATE",
    ),
    _o(
        "ENDOCRINE",
        "hypothalamic_pituitary_state_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "HYPOTHALAMIC_PITUITARY_STATE",
    ),
    _o(
        "ENDOCRINE",
        "thyroid_axis_reference",
        DERIVED_REFERENCE,
        "THYROID_AXIS_STATE",
    ),
    _o(
        "ENDOCRINE",
        "thyroid_axis_state_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "THYROID_AXIS_STATE",
    ),
    _o(
        "ENDOCRINE",
        "adrenal_axis_reference",
        DERIVED_REFERENCE,
        "ADRENAL_AXIS_STATE",
    ),
    _o(
        "ENDOCRINE",
        "adrenal_axis_state_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "ADRENAL_AXIS_STATE",
    ),
    _o(
        "ENDOCRINE",
        "pancreatic_glucose_regulation",
        DERIVED_REFERENCE,
        "PANCREATIC_GLUCOSE_INSULIN_STATE",
    ),
    _o(
        "ENDOCRINE",
        "pancreatic_glucose_insulin_state_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "PANCREATIC_GLUCOSE_INSULIN_STATE",
    ),
    _o(
        "ENDOCRINE",
        "gut_appetite_endocrine_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "GUT_APPETITE_ENDOCRINE_STATE",
    ),
    _o(
        "ENDOCRINE",
        "gonadal_endocrine_function",
        DIRECT_OBSERVATION_REFERENCE,
        "GONADAL_ENDOCRINE_REFERENCE",
    ),
    _o(
        "HEMATOLOGIC",
        "oxygen_transport",
        DIRECT_OBSERVATION_REFERENCE,
        "HEMATOLOGIC_OXYGEN_TRANSPORT_STATE",
    ),
    _o(
        "HEMATOLOGIC",
        "coagulation_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "COAGULATION_STATE_REFERENCE",
    ),
    _o(
        "HEMATOLOGIC",
        "cellular_blood_turnover_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "BLOOD_CELL_TURNOVER_REFERENCE",
    ),
    _o(
        "IMMUNE_LYMPHATIC",
        "innate_immune_response_reference",
        DERIVED_REFERENCE,
        "IMMUNE_ACTIVITY_STATE",
        "INFLAMMATORY_LOAD_STATE",
    ),
    _o(
        "IMMUNE_LYMPHATIC",
        "adaptive_immune_response_reference",
        DERIVED_REFERENCE,
        "IMMUNE_ACTIVITY_STATE",
    ),
    _o(
        "IMMUNE_LYMPHATIC",
        "lymphatic_fluid_return",
        DIRECT_OBSERVATION_REFERENCE,
        "LYMPHATIC_FLUID_RETURN_STATE",
    ),
    _o(
        "IMMUNE_LYMPHATIC",
        "immune_surveillance_reference",
        DERIVED_REFERENCE,
        "IMMUNE_ACTIVITY_STATE",
    ),
    _o(
        "IMMUNE_LYMPHATIC",
        "inflammatory_state_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "INFLAMMATORY_LOAD_STATE",
    ),
    _o(
        "INTEGUMENTARY_THERMOREGULATORY",
        "skin_barrier",
        DIRECT_OBSERVATION_REFERENCE,
        "SKIN_BARRIER_STATE",
    ),
    _o(
        "INTEGUMENTARY_THERMOREGULATORY",
        "sweating",
        DERIVED_REFERENCE,
        "THERMOREGULATORY_STATE",
        "HYDRATION_STATE",
    ),
    _o(
        "INTEGUMENTARY_THERMOREGULATORY",
        "cutaneous_vasoregulation",
        DERIVED_REFERENCE,
        "THERMOREGULATORY_STATE",
        "CARDIOVASCULAR_STATE",
    ),
    _o(
        "INTEGUMENTARY_THERMOREGULATORY",
        "thermoregulatory_feedback",
        DERIVED_REFERENCE,
        "TEMPERATURE_GENERAL",
        "THERMOREGULATORY_STATE",
    ),
    _o(
        "INTEGUMENTARY_THERMOREGULATORY",
        "tissue_injury_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "TISSUE_INJURY_STATE",
    ),
    _o(
        "INTEGUMENTARY_THERMOREGULATORY",
        "tissue_repair_state_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "TISSUE_REPAIR_STATE",
    ),
    _o(
        "INTEGUMENTARY_THERMOREGULATORY",
        "wound_repair_reference",
        DERIVED_REFERENCE,
        "TISSUE_INJURY_STATE",
        "TISSUE_REPAIR_STATE",
    ),
    _o(
        "REPRODUCTIVE",
        "testicular_endocrine_function",
        DIRECT_OBSERVATION_REFERENCE,
        "GONADAL_ENDOCRINE_REFERENCE",
    ),
    _o("REPRODUCTIVE", "spermatogenesis_reference", FUNCTIONAL_REFERENCE_ONLY),
    _o(
        "REPRODUCTIVE",
        "epididymal_maturation_reference",
        FUNCTIONAL_REFERENCE_ONLY,
    ),
    _o(
        "REPRODUCTIVE",
        "sperm_transport_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "SEMINAL_TRACT_TRANSPORT_STATE",
    ),
    _o(
        "REPRODUCTIVE",
        "accessory_gland_secretion_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "ACCESSORY_GLAND_SECRETION_STATE",
    ),
    _o(
        "REPRODUCTIVE",
        "bladder_neck_ejaculatory_closure_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
    ),
    _o(
        "REPRODUCTIVE",
        "genital_sensory_afferent_signal_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "GENITAL_SENSORY_AFFERENT_REFERENCE",
    ),
    _o(
        "REPRODUCTIVE",
        "pelvic_floor_motor_reflex_reference",
        DERIVED_REFERENCE,
        "PELVIC_FLOOR_PROPRIOCEPTION",
    ),
    _o(
        "REPRODUCTIVE",
        "external_urethral_sphincter_ejaculatory_coordination_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE",
    ),
    _o(
        "REPRODUCTIVE",
        "erectile_hemodynamic_reflex_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "GENITAL_VASCULAR_STATE",
        "ERECTILE_REFLEX_STATE",
    ),
    _o(
        "REPRODUCTIVE",
        "erection_maintenance_reference",
        DERIVED_REFERENCE,
        "GENITAL_VASCULAR_STATE",
        "PELVIC_FLOOR_PROPRIOCEPTION",
    ),
    _o(
        "REPRODUCTIVE",
        "emission_reflex_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "EMISSION_REFLEX_STATE",
    ),
    _o(
        "REPRODUCTIVE",
        "ejaculatory_reflex_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "EJACULATORY_REFLEX_STATE",
    ),
    _o(
        "REPRODUCTIVE",
        "detumescence_reference",
        DIRECT_OBSERVATION_REFERENCE,
        "DETUMESCENCE_STATE",
    ),
    _o(
        "REPRODUCTIVE",
        "post_ejaculatory_recovery_reference",
        DERIVED_REFERENCE,
        "DETUMESCENCE_STATE",
        "GENITAL_VASCULAR_STATE",
    ),
    _o("REPRODUCTIVE", "fertility_pathway_reference", FUNCTIONAL_REFERENCE_ONLY),
)


_REQUIRED_REPRODUCTIVE_OBSERVABILITY_BINDINGS: Final[
    dict[tuple[str, str], tuple[str, tuple[str, ...]]]
] = {
    (
        "REPRODUCTIVE",
        "sperm_transport_reference",
    ): (
        DIRECT_OBSERVATION_REFERENCE,
        ("SEMINAL_TRACT_TRANSPORT_STATE",),
    ),
    (
        "REPRODUCTIVE",
        "accessory_gland_secretion_reference",
    ): (
        DIRECT_OBSERVATION_REFERENCE,
        ("ACCESSORY_GLAND_SECRETION_STATE",),
    ),
    (
        "REPRODUCTIVE",
        "bladder_neck_ejaculatory_closure_reference",
    ): (
        DIRECT_OBSERVATION_REFERENCE,
        ("BLADDER_NECK_EJACULATORY_CLOSURE_STATE",),
    ),
    (
        "REPRODUCTIVE",
        "external_urethral_sphincter_ejaculatory_coordination_reference",
    ): (
        DIRECT_OBSERVATION_REFERENCE,
        ("EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE",),
    ),
}


def build_teacher_physiology_observability_profile(
    signal_schema: TeacherBodySignalSchema | None = None,
) -> TeacherPhysiologyObservabilityProfile:
    signal_schema = signal_schema or build_teacher_body_signal_schema()
    profile = TeacherPhysiologyObservabilityProfile(
        profile_id=OBSERVABILITY_PROFILE_ID,
        signal_schema_id=signal_schema.schema_id,
        bindings=_BINDINGS,
    )
    validate_teacher_physiology_observability_profile(profile, signal_schema)
    return profile


def validate_teacher_physiology_observability_profile(
    profile: TeacherPhysiologyObservabilityProfile,
    signal_schema: TeacherBodySignalSchema | None = None,
) -> dict[str, str]:
    signal_schema = signal_schema or build_teacher_body_signal_schema()

    if profile.profile_id != OBSERVABILITY_PROFILE_ID:
        raise ValueError("physiology observability profile id drift")
    if profile.signal_schema_id != signal_schema.schema_id:
        raise ValueError("physiology observability signal-schema binding drift")

    required = required_physiology_system_functions()
    expected_keys = {
        (system_id, function_id)
        for system_id, functions in required.items()
        for function_id in functions
    }
    binding_keys = {
        (binding.system_id, binding.function_id)
        for binding in profile.bindings
    }
    if len(binding_keys) != len(profile.bindings):
        raise ValueError("physiology observability binding keys must be unique")
    if binding_keys != expected_keys:
        raise ValueError("physiology observability function inventory drift")

    binding_by_key = {
        (binding.system_id, binding.function_id): binding
        for binding in profile.bindings
    }
    for key, (
        expected_class,
        expected_sources,
    ) in _REQUIRED_REPRODUCTIVE_OBSERVABILITY_BINDINGS.items():
        binding = binding_by_key[key]
        if binding.observability_class != expected_class:
            raise ValueError("reproductive physiology observability class drift")
        if binding.source_channels != expected_sources:
            raise ValueError("reproductive physiology observability source binding drift")

    signal_ids = {channel.channel_id for channel in signal_schema.channels}
    allowed_classes = {
        DIRECT_OBSERVATION_REFERENCE,
        DERIVED_REFERENCE,
        FUNCTIONAL_REFERENCE_ONLY,
    }
    for binding in profile.bindings:
        if binding.observability_class not in allowed_classes:
            raise ValueError("unknown physiology observability class")
        if binding.observability_class == FUNCTIONAL_REFERENCE_ONLY:
            if binding.source_channels:
                raise ValueError(
                    "functional-only physiology reference cannot claim source channels"
                )
        else:
            if not binding.source_channels:
                raise ValueError(
                    "observable physiology binding requires source channels"
                )
            if not set(binding.source_channels).issubset(signal_ids):
                raise ValueError(
                    "physiology observability binding references unknown signal"
                )

    if profile.declared_function_coverage_status != (
        "COMPLETE_DECLARED_FUNCTION_INVENTORY"
    ):
        raise ValueError("declared physiology function inventory is incomplete")
    if profile.observability_scope != "DECLARED_MACHINE_REFERENCE_SURFACE_ONLY":
        raise ValueError("physiology observability scope drift")
    if profile.direct_observation_interpretation != (
        "DIRECT_CHANNEL_BINDING_NOT_BIOLOGICAL_MEASUREMENT"
    ):
        raise ValueError("direct observation interpretation drift")
    if profile.biological_measurement_status != NOT_ESTABLISHED:
        raise ValueError("machine reference cannot establish biological measurement")
    if profile.full_function_observability_status != NOT_ESTABLISHED:
        raise ValueError("function inventory cannot establish full observability")
    if profile.full_biophysical_simulation_status != NOT_MATERIALIZED:
        raise ValueError(
            "function observability inventory cannot claim biophysical simulation"
        )
    if profile.phenomenal_sensation_status != NOT_ESTABLISHED:
        raise ValueError("function observability cannot establish felt sensation")
    if profile.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("function observability cannot establish subjectivity")
    if profile.canonical_effect != "NONE" or profile.deployment:
        raise ValueError(
            "physiology observability profile must remain non-canonical and undeployed"
        )

    counts = {
        observability_class: sum(
            binding.observability_class == observability_class
            for binding in profile.bindings
        )
        for observability_class in allowed_classes
    }
    return {
        "result": "PASS",
        "declared_function_inventory": "PASS",
        "direct_observation_count": str(counts[DIRECT_OBSERVATION_REFERENCE]),
        "derived_reference_count": str(counts[DERIVED_REFERENCE]),
        "functional_only_count": str(counts[FUNCTIONAL_REFERENCE_ONLY]),
        "machine_reference_scope": "PASS",
        "biological_measurement_nonclaim": "PASS",
        "full_observability_nonclaim": "PASS",
        "phenomenal_nonclaim": "PASS",
    }
