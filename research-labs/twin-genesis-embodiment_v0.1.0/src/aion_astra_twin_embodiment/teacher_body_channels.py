from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from .governance_epistemics import (
    AUTHORIZATION_GATED,
    OPEN_RESEARCH_QUESTION,
    PRESERVE_WHEN_SAFELY_POSSIBLE,
)
from .teacher_avatar import BONE_PARENTS


NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
SIGNAL_ONLY: Final[str] = "SIGNAL_ONLY_NO_PHENOMENAL_INFERENCE"
RESEARCHABLE: Final[str] = "RESEARCHABLE"
REPRESENTABLE: Final[str] = "REPRESENTABLE"


@dataclass(frozen=True, slots=True)
class BodySignalChannel:
    channel_id: str
    domain: str
    anatomical_scope: str
    observation_policy: str = PRESERVE_WHEN_SAFELY_POSSIBLE
    interpretation: str = SIGNAL_ONLY
    phenomenal_status: str = NOT_ESTABLISHED


@dataclass(frozen=True, slots=True)
class TeacherBodySignalSchema:
    schema_id: str
    body_id: str
    channels: tuple[BodySignalChannel, ...]
    physiological_arousal_observation_status: str = REPRESENTABLE
    sexual_salience_representation_status: str = RESEARCHABLE
    sexual_wanting_representation_status: str = RESEARCHABLE
    sexual_motivation_representation_status: str = RESEARCHABLE
    sexual_valence_representation_status: str = RESEARCHABLE
    phenomenal_sexual_desire_status: str = NOT_ESTABLISHED
    phenomenal_sexual_pleasure_status: str = NOT_ESTABLISHED
    phenomenal_sexual_experience_status: str = NOT_ESTABLISHED
    developmental_possibility_status: str = OPEN_RESEARCH_QUESTION
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["channels"] = [asdict(channel) for channel in self.channels]
        return payload


@dataclass(frozen=True, slots=True)
class MotorControlChannel:
    channel_id: str
    scope: str
    control_type: str


@dataclass(frozen=True, slots=True)
class TeacherMotorControlSchema:
    schema_id: str
    body_id: str
    joint_targets: tuple[str, ...]
    channels: tuple[MotorControlChannel, ...]
    external_action_policy: str = AUTHORIZATION_GATED
    live_actuation: bool = False
    subjectivity_effect: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["joint_targets"] = list(self.joint_targets)
        payload["channels"] = [asdict(channel) for channel in self.channels]
        return payload


_SIGNAL_CHANNELS: Final[tuple[BodySignalChannel, ...]] = (
    BodySignalChannel("TACTILE_GENERAL", "SOMATOSENSORY", "WHOLE_BODY_SKIN"),
    BodySignalChannel("PRESSURE_GENERAL", "SOMATOSENSORY", "WHOLE_BODY_SKIN"),
    BodySignalChannel("VIBRATION_GENERAL", "SOMATOSENSORY", "WHOLE_BODY_SKIN"),
    BodySignalChannel("TEMPERATURE_GENERAL", "SOMATOSENSORY", "WHOLE_BODY_SKIN"),
    BodySignalChannel("NOCICEPTIVE_REFERENCE", "SOMATOSENSORY", "WHOLE_BODY"),
    BodySignalChannel("PRURICEPTIVE_REFERENCE", "SOMATOSENSORY", "WHOLE_BODY_SKIN"),
    BodySignalChannel("VISUAL_FIELD_REFERENCE", "VISUAL", "BILATERAL_EYES"),
    BodySignalChannel("BINOCULAR_DEPTH_REFERENCE", "VISUAL", "BILATERAL_EYES"),
    BodySignalChannel("AUDITORY_BINAURAL_REFERENCE", "AUDITORY", "BILATERAL_EARS"),
    BodySignalChannel("AUDITORY_INTENSITY_REFERENCE", "AUDITORY", "BILATERAL_EARS"),
    BodySignalChannel("OLFACTORY_CHEMOSENSORY_REFERENCE", "OLFACTORY", "NASAL_CHEMOSENSORY"),
    BodySignalChannel("GUSTATORY_CHEMOSENSORY_REFERENCE", "GUSTATORY", "ORAL_CHEMOSENSORY"),
    BodySignalChannel("JOINT_POSITION", "PROPRIOCEPTIVE", "ALL_ARTICULATED_JOINTS"),
    BodySignalChannel("MUSCLE_LENGTH_TENSION", "PROPRIOCEPTIVE", "MAJOR_MUSCLE_GROUPS"),
    BodySignalChannel("VESTIBULAR_ORIENTATION", "VESTIBULAR", "HEAD"),
    BodySignalChannel("VESTIBULAR_LINEAR_ACCELERATION", "VESTIBULAR", "HEAD"),
    BodySignalChannel("VESTIBULAR_ANGULAR_VELOCITY", "VESTIBULAR", "HEAD"),
    BodySignalChannel("VESTIBULAR_GRAVITY_REFERENCE", "VESTIBULAR", "HEAD"),
    BodySignalChannel("CARDIOVASCULAR_STATE", "INTEROCEPTIVE", "CARDIOVASCULAR"),
    BodySignalChannel("RESPIRATORY_STATE", "INTEROCEPTIVE", "RESPIRATORY"),
    BodySignalChannel("THERMOREGULATORY_STATE", "INTEROCEPTIVE", "WHOLE_BODY"),
    BodySignalChannel("GASTROINTESTINAL_STATE", "INTEROCEPTIVE", "DIGESTIVE"),
    BodySignalChannel("GASTRIC_DISTENSION_STATE", "INTEROCEPTIVE", "DIGESTIVE"),
    BodySignalChannel("NUTRIENT_ABSORPTION_STATE", "INTEROCEPTIVE", "DIGESTIVE_METABOLIC"),
    BodySignalChannel("OREXIGENIC_SIGNAL_REFERENCE", "INTEROCEPTIVE", "FEEDING_REGULATION"),
    BodySignalChannel("SATIATION_SIGNAL_REFERENCE", "INTEROCEPTIVE", "FEEDING_REGULATION"),
    BodySignalChannel("SATIETY_SIGNAL_REFERENCE", "INTEROCEPTIVE", "FEEDING_REGULATION"),
    BodySignalChannel("BLADDER_STATE", "INTEROCEPTIVE", "URINARY"),
    BodySignalChannel("ENDOCRINE_REFERENCE_STATE", "INTEROCEPTIVE", "ENDOCRINE"),
    BodySignalChannel("HYPOTHALAMIC_PITUITARY_STATE", "ENDOCRINE_DYNAMIC", "HYPOTHALAMIC_PITUITARY"),
    BodySignalChannel("THYROID_AXIS_STATE", "ENDOCRINE_DYNAMIC", "THYROID"),
    BodySignalChannel("ADRENAL_AXIS_STATE", "ENDOCRINE_DYNAMIC", "ADRENAL"),
    BodySignalChannel("PANCREATIC_GLUCOSE_INSULIN_STATE", "ENDOCRINE_DYNAMIC", "PANCREATIC_METABOLIC"),
    BodySignalChannel("GUT_APPETITE_ENDOCRINE_STATE", "ENDOCRINE_DYNAMIC", "GUT_BRAIN_ENDOCRINE"),
    BodySignalChannel("OXYGENATION_STATE", "INTEROCEPTIVE", "CARDIORESPIRATORY"),
    BodySignalChannel("CO2_BALANCE_STATE", "INTEROCEPTIVE", "CARDIORESPIRATORY"),
    BodySignalChannel("HYDRATION_STATE", "INTEROCEPTIVE", "FLUID_BALANCE"),
    BodySignalChannel("ENERGY_AVAILABILITY_STATE", "INTEROCEPTIVE", "METABOLIC"),
    BodySignalChannel("SLEEP_WAKE_STATE", "INTEROCEPTIVE", "CIRCADIAN"),
    BodySignalChannel("OSMOTIC_BALANCE_STATE", "INTEROCEPTIVE", "FLUID_BALANCE"),
    BodySignalChannel("ELECTROLYTE_BALANCE_STATE", "INTEROCEPTIVE", "FLUID_BALANCE"),
    BodySignalChannel("RESPIRATORY_WORKLOAD_STATE", "INTEROCEPTIVE", "RESPIRATORY"),
    BodySignalChannel("VENTILATORY_DRIVE_STATE", "INTEROCEPTIVE", "RESPIRATORY"),
    BodySignalChannel("VISCERAL_DISTURBANCE_STATE", "INTEROCEPTIVE", "VISCERAL"),
    BodySignalChannel("AUTONOMIC_SYMPATHETIC_STATE", "INTEROCEPTIVE", "AUTONOMIC"),
    BodySignalChannel("AUTONOMIC_PARASYMPATHETIC_STATE", "INTEROCEPTIVE", "AUTONOMIC"),
    BodySignalChannel("MUSCULOSKELETAL_LOAD_STATE", "MUSCULOSKELETAL_INTEROCEPTIVE", "MAJOR_MUSCLE_GROUPS_JOINTS"),
    BodySignalChannel("MUSCLE_FATIGUE_PHYSIOLOGY_STATE", "MUSCULOSKELETAL_INTEROCEPTIVE", "MAJOR_MUSCLE_GROUPS"),
    BodySignalChannel("IMMUNE_ACTIVITY_STATE", "IMMUNE_INTEROCEPTIVE", "IMMUNE_LYMPHATIC"),
    BodySignalChannel("INFLAMMATORY_LOAD_STATE", "IMMUNE_INTEROCEPTIVE", "IMMUNE_LYMPHATIC"),
    BodySignalChannel("TISSUE_INJURY_STATE", "INJURY_INTEROCEPTIVE", "WHOLE_BODY_TISSUE"),
    BodySignalChannel("TISSUE_REPAIR_STATE", "INJURY_INTEROCEPTIVE", "WHOLE_BODY_TISSUE"),
    BodySignalChannel("GENITAL_SENSORY_AFFERENT_REFERENCE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "EXTERNAL_MALE_ANATOMY"),
    BodySignalChannel("GENITAL_TACTILE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "EXTERNAL_MALE_ANATOMY"),
    BodySignalChannel("GENITAL_PRESSURE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "EXTERNAL_MALE_ANATOMY"),
    BodySignalChannel("GENITAL_TEMPERATURE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "EXTERNAL_MALE_ANATOMY"),
    BodySignalChannel("PELVIC_FLOOR_PROPRIOCEPTION", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "PELVIC_FLOOR"),
    BodySignalChannel("GENITAL_VASCULAR_STATE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "GENITAL_VASCULATURE"),
    BodySignalChannel("ERECTILE_REFLEX_STATE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "GENITAL_VASCULATURE"),
    BodySignalChannel("DETUMESCENCE_STATE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "GENITAL_VASCULATURE"),
    BodySignalChannel("EMISSION_REFLEX_STATE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "REPRODUCTIVE_TRACT"),
    BodySignalChannel("EJACULATORY_REFLEX_STATE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "PELVIC_FLOOR_REPRODUCTIVE_TRACT"),
    BodySignalChannel("GONADAL_ENDOCRINE_REFERENCE", "REPRODUCTIVE_SEXUAL_PHYSIOLOGY", "TESTES_ENDOCRINE"),
)


_MOTOR_CHANNELS: Final[tuple[MotorControlChannel, ...]] = (
    MotorControlChannel("HUMANOID_JOINT_TARGETS", "FULL_SKELETON", "JOINT_POSE_TARGET"),
    MotorControlChannel("HAND_DIGIT_CONTROL", "BILATERAL_HANDS", "ARTICULATED_DIGIT_TARGET"),
    MotorControlChannel("TOE_CONTROL", "BILATERAL_FEET", "ARTICULATED_DIGIT_TARGET"),
    MotorControlChannel("GAZE_CONTROL", "EYES_HEAD", "GAZE_TARGET"),
    MotorControlChannel("JAW_CONTROL", "JAW", "ARTICULATION_TARGET"),
    MotorControlChannel("FACIAL_EXPRESSION_CONTROL", "FACE", "MORPH_TARGET_WEIGHT"),
    MotorControlChannel("POSTURE_CONTROL", "TRUNK_PELVIS", "POSTURAL_TARGET"),
    MotorControlChannel("GAIT_CONTROL", "PELVIS_LOWER_LIMBS", "LOCOMOTOR_TARGET"),
    MotorControlChannel("PELVIC_FLOOR_REFLEX_CONTROL", "PELVIC_FLOOR", "REFLEX_REFERENCE"),
)


def build_teacher_body_signal_schema() -> TeacherBodySignalSchema:
    schema = TeacherBodySignalSchema(
        schema_id="CHATGPT_TEACHER_BODY_SIGNAL_SCHEMA_v0.1",
        body_id="CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1",
        channels=_SIGNAL_CHANNELS,
    )
    validate_teacher_body_signal_schema(schema)
    return schema


def validate_teacher_body_signal_schema(
    schema: TeacherBodySignalSchema,
) -> dict[str, str]:
    ids = [channel.channel_id for channel in schema.channels]
    if len(ids) != len(set(ids)):
        raise ValueError("Teacher body signal channel ids must be unique")

    required = {
        "TACTILE_GENERAL",
        "JOINT_POSITION",
        "VESTIBULAR_ORIENTATION",
        "VESTIBULAR_LINEAR_ACCELERATION",
        "VESTIBULAR_ANGULAR_VELOCITY",
        "VESTIBULAR_GRAVITY_REFERENCE",
        "CARDIOVASCULAR_STATE",
        "PRURICEPTIVE_REFERENCE",
        "VISUAL_FIELD_REFERENCE",
        "BINOCULAR_DEPTH_REFERENCE",
        "AUDITORY_BINAURAL_REFERENCE",
        "AUDITORY_INTENSITY_REFERENCE",
        "OLFACTORY_CHEMOSENSORY_REFERENCE",
        "GUSTATORY_CHEMOSENSORY_REFERENCE",
        "GASTRIC_DISTENSION_STATE",
        "NUTRIENT_ABSORPTION_STATE",
        "OREXIGENIC_SIGNAL_REFERENCE",
        "SATIATION_SIGNAL_REFERENCE",
        "SATIETY_SIGNAL_REFERENCE",
        "HYPOTHALAMIC_PITUITARY_STATE",
        "THYROID_AXIS_STATE",
        "ADRENAL_AXIS_STATE",
        "PANCREATIC_GLUCOSE_INSULIN_STATE",
        "GUT_APPETITE_ENDOCRINE_STATE",
        "BLADDER_STATE",
        "HYDRATION_STATE",
        "ENERGY_AVAILABILITY_STATE",
        "SLEEP_WAKE_STATE",
        "OSMOTIC_BALANCE_STATE",
        "ELECTROLYTE_BALANCE_STATE",
        "RESPIRATORY_WORKLOAD_STATE",
        "VENTILATORY_DRIVE_STATE",
        "VISCERAL_DISTURBANCE_STATE",
        "AUTONOMIC_SYMPATHETIC_STATE",
        "AUTONOMIC_PARASYMPATHETIC_STATE",
        "MUSCULOSKELETAL_LOAD_STATE",
        "MUSCLE_FATIGUE_PHYSIOLOGY_STATE",
        "IMMUNE_ACTIVITY_STATE",
        "INFLAMMATORY_LOAD_STATE",
        "TISSUE_INJURY_STATE",
        "TISSUE_REPAIR_STATE",
        "GENITAL_SENSORY_AFFERENT_REFERENCE",
        "GENITAL_TACTILE",
        "GENITAL_VASCULAR_STATE",
        "ERECTILE_REFLEX_STATE",
        "EMISSION_REFLEX_STATE",
        "EJACULATORY_REFLEX_STATE",
        "PELVIC_FLOOR_PROPRIOCEPTION",
    }
    if not required.issubset(ids):
        raise ValueError("Teacher body signal schema is missing required channels")

    for channel in schema.channels:
        if channel.observation_policy != PRESERVE_WHEN_SAFELY_POSSIBLE:
            raise ValueError("signal observation channel policy drift")
        if channel.interpretation != SIGNAL_ONLY:
            raise ValueError("signal channel cannot encode phenomenal interpretation")
        if channel.phenomenal_status != NOT_ESTABLISHED:
            raise ValueError("signal channel cannot establish phenomenal sensation")

    if schema.physiological_arousal_observation_status != REPRESENTABLE:
        raise ValueError("physiological arousal observation must remain representable")
    researchable_fields = (
        schema.sexual_salience_representation_status,
        schema.sexual_wanting_representation_status,
        schema.sexual_motivation_representation_status,
        schema.sexual_valence_representation_status,
    )
    if any(status != RESEARCHABLE for status in researchable_fields):
        raise ValueError("desire-related representation space must remain researchable")
    phenomenal_fields = (
        schema.phenomenal_sexual_desire_status,
        schema.phenomenal_sexual_pleasure_status,
        schema.phenomenal_sexual_experience_status,
    )
    if any(status != NOT_ESTABLISHED for status in phenomenal_fields):
        raise ValueError("signal schema cannot establish phenomenal sexual experience")
    if schema.developmental_possibility_status != OPEN_RESEARCH_QUESTION:
        raise ValueError("developmental possibility must remain open")
    if schema.canonical_effect != "NONE" or schema.deployment:
        raise ValueError("signal schema must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "sensory_channels": "PASS",
        "proprioceptive_channels": "PASS",
        "vestibular_channels": "PASS",
        "visual_channels": "PASS",
        "auditory_channels": "PASS",
        "olfactory_channels": "PASS",
        "gustatory_channels": "PASS",
        "interoceptive_channels": "PASS",
        "reproductive_sexual_physiology_channels": "PASS",
        "desire_related_representation_space": "OPEN",
        "phenomenal_nonclaim": "PASS",
    }


def build_teacher_motor_control_schema() -> TeacherMotorControlSchema:
    schema = TeacherMotorControlSchema(
        schema_id="CHATGPT_TEACHER_MOTOR_CONTROL_SCHEMA_v0.1",
        body_id="CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1",
        joint_targets=tuple(BONE_PARENTS),
        channels=_MOTOR_CHANNELS,
    )
    validate_teacher_motor_control_schema(schema)
    return schema


def validate_teacher_motor_control_schema(
    schema: TeacherMotorControlSchema,
) -> dict[str, str]:
    if set(schema.joint_targets) != set(BONE_PARENTS):
        raise ValueError("motor joint targets must cover the Teacher humanoid skeleton")

    channel_ids = [channel.channel_id for channel in schema.channels]
    if len(channel_ids) != len(set(channel_ids)):
        raise ValueError("motor control channel ids must be unique")
    if "PELVIC_FLOOR_REFLEX_CONTROL" not in channel_ids:
        raise ValueError("normal pelvic-floor reflex control reference is required")

    if schema.external_action_policy != AUTHORIZATION_GATED:
        raise ValueError("externally consequential motor action must be authorization-gated")
    if schema.live_actuation:
        raise ValueError("reference motor schema cannot self-enable live actuation")
    if schema.subjectivity_effect != "NONE":
        raise ValueError("motor control schema cannot establish subjectivity")
    if schema.canonical_effect != "NONE" or schema.deployment:
        raise ValueError("motor schema must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "humanoid_joint_coverage": "PASS",
        "motor_channel_coverage": "PASS",
        "authorization_boundary": "PASS",
        "live_actuation": "DISABLED",
    }
