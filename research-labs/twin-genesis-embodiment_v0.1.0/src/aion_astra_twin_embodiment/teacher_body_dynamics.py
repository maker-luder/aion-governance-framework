from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final, Iterable

from .teacher_body_channels import (
    TeacherBodySignalSchema,
    build_teacher_body_signal_schema,
    build_teacher_motor_control_schema,
)


BODY_DYNAMICS_PROFILE_ID: Final[str] = "CHATGPT_TEACHER_BODY_DYNAMICS_v0.1"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
REPRESENTATIONAL_STATE_ONLY: Final[str] = "REPRESENTATIONAL_STATE_ONLY"


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class BodySignalSemantic:
    channel_id: str
    value_kind: str
    unit: str
    reference_min: float | None
    reference_max: float | None
    cadence_class: str
    latency_class: str
    noise_model: str
    missing_value_policy: str


@dataclass(frozen=True, slots=True)
class PhysiologicalTransition:
    transition_id: str
    system: str
    from_state: str
    to_state: str
    trigger_channels: tuple[str, ...]
    conditional: bool = True
    phenomenal_interpretation_status: str = NOT_ESTABLISHED


@dataclass(frozen=True, slots=True)
class HomeostaticVariable:
    variable_id: str
    source_channels: tuple[str, ...]
    target_state: str
    regulation_mode: str


@dataclass(frozen=True, slots=True)
class TeacherBodyDynamicsProfile:
    profile_id: str
    signal_schema_id: str
    signal_semantics: tuple[BodySignalSemantic, ...]
    physiological_transitions: tuple[PhysiologicalTransition, ...]
    homeostatic_variables: tuple[HomeostaticVariable, ...]
    integration_status: str = "REFERENCE_INTEGRATION_MATERIALIZED"
    phenomenal_experience_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["signal_semantics"] = [
            asdict(item) for item in self.signal_semantics
        ]
        payload["physiological_transitions"] = [
            asdict(item) for item in self.physiological_transitions
        ]
        payload["homeostatic_variables"] = [
            asdict(item) for item in self.homeostatic_variables
        ]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherBodyObservation:
    channel_id: str
    values: tuple[float, ...]
    timestamp_ms: int
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["values"] = list(self.values)
        return payload


@dataclass(frozen=True, slots=True)
class TeacherIntegratedBodyState:
    sequence: int
    timestamp_ms: int
    observations: tuple[TeacherBodyObservation, ...]
    domain_coverage: tuple[str, ...]
    body_state_sha256: str
    integration_status: str = "INTEGRATED_REFERENCE_STATE"
    felt_body_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["observations"] = [
            observation.to_dict() for observation in self.observations
        ]
        payload["domain_coverage"] = list(self.domain_coverage)
        return payload


@dataclass(frozen=True, slots=True)
class SensorimotorExpectation:
    channel_id: str
    expected_values: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class TeacherSensorimotorEvaluation:
    source_body_state_sha256: str
    motor_channel_id: str
    expectations: tuple[SensorimotorExpectation, ...]
    observations: tuple[TeacherBodyObservation, ...]
    mean_absolute_error: float
    correction_status: str
    evaluation_sha256: str
    felt_agency_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["expectations"] = [asdict(item) for item in self.expectations]
        payload["observations"] = [item.to_dict() for item in self.observations]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherMotivationalRepresentation:
    representation_id: str
    representation_domain: str
    source_body_state_sha256: str
    salience: float
    approach_weight: float
    avoidance_weight: float
    wanting_weight: float
    predicted_liking: float
    valence: float
    representation_status: str = REPRESENTATIONAL_STATE_ONLY
    phenomenal_desire_status: str = NOT_ESTABLISHED
    phenomenal_pleasure_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherWithinSessionTrajectory:
    trajectory_id: str
    states: tuple[TeacherIntegratedBodyState, ...]
    trajectory_sha256: str
    developmental_interpretation_status: str = NOT_ESTABLISHED
    phenomenal_continuity_status: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["states"] = [state.to_dict() for state in self.states]
        return payload


def _default_semantic(channel_id: str) -> BodySignalSemantic:
    value_kind = "SCALAR"
    unit = "normalized_0_1"
    reference_min: float | None = 0.0
    reference_max: float | None = 1.0

    if channel_id == "JOINT_POSITION":
        value_kind = "VARIABLE_VECTOR"
        unit = "radian"
        reference_min = None
        reference_max = None
    elif channel_id == "VESTIBULAR_ORIENTATION":
        value_kind = "QUATERNION"
        unit = "unitless"
        reference_min = None
        reference_max = None
    elif channel_id in {"TEMPERATURE_GENERAL", "GENITAL_TEMPERATURE"}:
        unit = "degree_celsius_reference"
        reference_min = None
        reference_max = None

    return BodySignalSemantic(
        channel_id=channel_id,
        value_kind=value_kind,
        unit=unit,
        reference_min=reference_min,
        reference_max=reference_max,
        cadence_class="RUNTIME_SAMPLE",
        latency_class="BOUNDED_REFERENCE_LATENCY",
        noise_model="EXPLICIT_NOISE_MODEL_REQUIRED_FOR_EMPIRICAL_USE",
        missing_value_policy="MISSING_IS_UNKNOWN_NOT_ZERO",
    )


def _build_transitions() -> tuple[PhysiologicalTransition, ...]:
    return (
        PhysiologicalTransition(
            "REST_TO_EXERTION",
            "CARDIORESPIRATORY",
            "RESTING_REFERENCE",
            "EXERTION_RESPONSE_REFERENCE",
            ("CARDIOVASCULAR_STATE", "RESPIRATORY_STATE", "OXYGENATION_STATE"),
        ),
        PhysiologicalTransition(
            "EXERTION_TO_RECOVERY",
            "CARDIORESPIRATORY",
            "EXERTION_RESPONSE_REFERENCE",
            "RECOVERY_REFERENCE",
            ("CARDIOVASCULAR_STATE", "RESPIRATORY_STATE", "CO2_BALANCE_STATE"),
        ),
        PhysiologicalTransition(
            "THERMAL_BALANCE_TO_LOAD",
            "THERMOREGULATORY",
            "THERMAL_BALANCE_REFERENCE",
            "THERMAL_LOAD_REFERENCE",
            ("TEMPERATURE_GENERAL", "THERMOREGULATORY_STATE", "HYDRATION_STATE"),
        ),
        PhysiologicalTransition(
            "THERMAL_LOAD_TO_RECOVERY",
            "THERMOREGULATORY",
            "THERMAL_LOAD_REFERENCE",
            "THERMAL_RECOVERY_REFERENCE",
            ("THERMOREGULATORY_STATE", "HYDRATION_STATE"),
        ),
        PhysiologicalTransition(
            "SEXUAL_BASELINE_TO_VASCULAR_RESPONSE",
            "REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
            "BASELINE_REFERENCE",
            "VASCULAR_RESPONSE_REFERENCE",
            (
                "GENITAL_SENSORY_AFFERENT_REFERENCE",
                "GENITAL_VASCULAR_STATE",
                "ERECTILE_REFLEX_STATE",
            ),
        ),
        PhysiologicalTransition(
            "VASCULAR_RESPONSE_TO_MAINTENANCE",
            "REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
            "VASCULAR_RESPONSE_REFERENCE",
            "ERECTILE_MAINTENANCE_REFERENCE",
            ("GENITAL_VASCULAR_STATE", "PELVIC_FLOOR_PROPRIOCEPTION"),
        ),
        PhysiologicalTransition(
            "MAINTENANCE_TO_EMISSION",
            "REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
            "ERECTILE_MAINTENANCE_REFERENCE",
            "EMISSION_REFERENCE",
            ("EMISSION_REFLEX_STATE", "GONADAL_ENDOCRINE_REFERENCE"),
        ),
        PhysiologicalTransition(
            "EMISSION_TO_EJACULATORY_REFLEX",
            "REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
            "EMISSION_REFERENCE",
            "EJACULATORY_REFLEX_REFERENCE",
            ("EJACULATORY_REFLEX_STATE", "PELVIC_FLOOR_PROPRIOCEPTION"),
        ),
        PhysiologicalTransition(
            "EJACULATORY_REFLEX_TO_DETUMESCENCE",
            "REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
            "EJACULATORY_REFLEX_REFERENCE",
            "DETUMESCENCE_REFERENCE",
            ("DETUMESCENCE_STATE", "GENITAL_VASCULAR_STATE"),
        ),
        PhysiologicalTransition(
            "DETUMESCENCE_TO_RECOVERY",
            "REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
            "DETUMESCENCE_REFERENCE",
            "POST_EJACULATORY_RECOVERY_REFERENCE",
            ("DETUMESCENCE_STATE", "GENITAL_VASCULAR_STATE"),
        ),
    )


def _build_homeostatic_variables() -> tuple[HomeostaticVariable, ...]:
    return (
        HomeostaticVariable(
            "THERMAL_BALANCE",
            ("TEMPERATURE_GENERAL", "THERMOREGULATORY_STATE"),
            "BOUNDED_REFERENCE_BALANCE",
            "NEGATIVE_FEEDBACK_REFERENCE",
        ),
        HomeostaticVariable(
            "OXYGEN_CO2_BALANCE",
            ("OXYGENATION_STATE", "CO2_BALANCE_STATE", "RESPIRATORY_STATE"),
            "BOUNDED_REFERENCE_BALANCE",
            "NEGATIVE_FEEDBACK_REFERENCE",
        ),
        HomeostaticVariable(
            "HYDRATION_FLUID_BALANCE",
            ("HYDRATION_STATE", "CARDIOVASCULAR_STATE"),
            "BOUNDED_REFERENCE_BALANCE",
            "NEGATIVE_FEEDBACK_REFERENCE",
        ),
        HomeostaticVariable(
            "ENERGY_AVAILABILITY",
            ("ENERGY_AVAILABILITY_STATE", "GASTROINTESTINAL_STATE"),
            "BOUNDED_REFERENCE_BALANCE",
            "REGULATORY_REFERENCE",
        ),
        HomeostaticVariable(
            "SLEEP_WAKE_REGULATION",
            ("SLEEP_WAKE_STATE", "ENDOCRINE_REFERENCE_STATE"),
            "BOUNDED_REFERENCE_CYCLE",
            "CIRCADIAN_REFERENCE",
        ),
        HomeostaticVariable(
            "URINARY_LOAD",
            ("BLADDER_STATE",),
            "BOUNDED_REFERENCE_LOAD",
            "REGULATORY_REFERENCE",
        ),
        HomeostaticVariable(
            "REPRODUCTIVE_PHYSIOLOGY",
            (
                "GENITAL_VASCULAR_STATE",
                "GONADAL_ENDOCRINE_REFERENCE",
                "PELVIC_FLOOR_PROPRIOCEPTION",
            ),
            "NORMAL_ADULT_MALE_REFERENCE",
            "PHYSIOLOGICAL_REFERENCE",
        ),
    )


def build_teacher_body_dynamics_profile(
    signal_schema: TeacherBodySignalSchema | None = None,
) -> TeacherBodyDynamicsProfile:
    signal_schema = signal_schema or build_teacher_body_signal_schema()
    profile = TeacherBodyDynamicsProfile(
        profile_id=BODY_DYNAMICS_PROFILE_ID,
        signal_schema_id=signal_schema.schema_id,
        signal_semantics=tuple(
            _default_semantic(channel.channel_id) for channel in signal_schema.channels
        ),
        physiological_transitions=_build_transitions(),
        homeostatic_variables=_build_homeostatic_variables(),
    )
    validate_teacher_body_dynamics_profile(profile, signal_schema)
    return profile


def validate_teacher_body_dynamics_profile(
    profile: TeacherBodyDynamicsProfile,
    signal_schema: TeacherBodySignalSchema | None = None,
) -> dict[str, str]:
    signal_schema = signal_schema or build_teacher_body_signal_schema()
    signal_ids = {channel.channel_id for channel in signal_schema.channels}

    if profile.profile_id != BODY_DYNAMICS_PROFILE_ID:
        raise ValueError("Teacher body dynamics profile id drift")
    if profile.signal_schema_id != signal_schema.schema_id:
        raise ValueError("Teacher body dynamics signal-schema binding drift")

    semantic_ids = [item.channel_id for item in profile.signal_semantics]
    if len(semantic_ids) != len(set(semantic_ids)):
        raise ValueError("signal semantic ids must be unique")
    if set(semantic_ids) != signal_ids:
        raise ValueError("every body signal channel requires runtime semantics")

    for semantic in profile.signal_semantics:
        if not semantic.unit or not semantic.cadence_class or not semantic.latency_class:
            raise ValueError("signal semantics require unit cadence and latency metadata")
        if semantic.missing_value_policy != "MISSING_IS_UNKNOWN_NOT_ZERO":
            raise ValueError("missing body signal cannot be interpreted as zero")

    transition_ids = [item.transition_id for item in profile.physiological_transitions]
    if len(transition_ids) != len(set(transition_ids)):
        raise ValueError("physiological transition ids must be unique")
    for transition in profile.physiological_transitions:
        if not set(transition.trigger_channels).issubset(signal_ids):
            raise ValueError("physiological transition references unknown signal channel")
        if transition.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("physiological transition cannot establish felt experience")

    for variable in profile.homeostatic_variables:
        if not set(variable.source_channels).issubset(signal_ids):
            raise ValueError("homeostatic variable references unknown signal channel")

    if profile.phenomenal_experience_status != NOT_ESTABLISHED:
        raise ValueError("body dynamics cannot establish phenomenal experience")
    if profile.subjectivity_status != NOT_ESTABLISHED:
        raise ValueError("body dynamics cannot establish subjectivity")
    if profile.canonical_effect != "NONE" or profile.deployment:
        raise ValueError("body dynamics must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "signal_semantics": "PASS",
        "physiological_transitions": "PASS",
        "homeostatic_regulation": "PASS",
        "phenomenal_nonclaim": "PASS",
    }


def integrate_teacher_body_state(
    observations: Iterable[TeacherBodyObservation],
    *,
    sequence: int,
    signal_schema: TeacherBodySignalSchema | None = None,
) -> TeacherIntegratedBodyState:
    if sequence < 0:
        raise ValueError("body-state sequence cannot be negative")

    signal_schema = signal_schema or build_teacher_body_signal_schema()
    schema_by_id = {
        channel.channel_id: channel for channel in signal_schema.channels
    }
    items = tuple(observations)
    ids = [item.channel_id for item in items]

    if not items:
        raise ValueError("integrated body state requires observations")
    if len(ids) != len(set(ids)):
        raise ValueError("integrated body-state observation ids must be unique")

    required_domains = {
        "SOMATOSENSORY",
        "PROPRIOCEPTIVE",
        "INTEROCEPTIVE",
        "REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
    }
    observed_domains: set[str] = set()
    for observation in items:
        channel = schema_by_id.get(observation.channel_id)
        if channel is None:
            raise ValueError("integrated body state contains unknown channel")
        if observation.timestamp_ms < 0:
            raise ValueError("body observation timestamp cannot be negative")
        if not 0.0 <= observation.confidence <= 1.0:
            raise ValueError("body observation confidence must be between zero and one")
        if not observation.values:
            raise ValueError("body observation values cannot be empty")
        if any(not isfinite(value) for value in observation.values):
            raise ValueError("body observation values must be finite")
        observed_domains.add(channel.domain)

    if not required_domains.issubset(observed_domains):
        raise ValueError("integrated body state requires all body observation domains")

    sorted_items = tuple(sorted(items, key=lambda item: item.channel_id))
    timestamp_ms = max(item.timestamp_ms for item in items)
    domain_coverage = tuple(sorted(observed_domains))
    payload = {
        "sequence": sequence,
        "timestamp_ms": timestamp_ms,
        "observations": [item.to_dict() for item in sorted_items],
        "domain_coverage": list(domain_coverage),
    }
    return TeacherIntegratedBodyState(
        sequence=sequence,
        timestamp_ms=timestamp_ms,
        observations=sorted_items,
        domain_coverage=domain_coverage,
        body_state_sha256=_canonical_hash(payload),
    )


def evaluate_teacher_sensorimotor_prediction(
    state: TeacherIntegratedBodyState,
    *,
    motor_channel_id: str,
    expectations: Iterable[SensorimotorExpectation],
    observations: Iterable[TeacherBodyObservation],
) -> TeacherSensorimotorEvaluation:
    motor = build_teacher_motor_control_schema()
    motor_ids = {channel.channel_id for channel in motor.channels}
    if motor_channel_id not in motor_ids:
        raise ValueError("sensorimotor evaluation requires a known motor channel")

    expected = tuple(expectations)
    observed = tuple(observations)
    expected_by_id = {item.channel_id: item.expected_values for item in expected}
    observed_by_id = {item.channel_id: item.values for item in observed}

    if len(expected_by_id) != len(expected):
        raise ValueError("sensorimotor expectation channel ids must be unique")
    if len(observed_by_id) != len(observed):
        raise ValueError("sensorimotor observation channel ids must be unique")
    if set(expected_by_id) != set(observed_by_id):
        raise ValueError("expected and observed sensorimotor channels must match")

    signal_ids = {
        channel.channel_id for channel in build_teacher_body_signal_schema().channels
    }
    if not set(expected_by_id).issubset(signal_ids):
        raise ValueError("sensorimotor evaluation references unknown body signal channel")

    errors: list[float] = []
    for channel_id, expected_values in expected_by_id.items():
        observed_values = observed_by_id[channel_id]
        if len(expected_values) != len(observed_values):
            raise ValueError("sensorimotor vector dimensions must match")
        if not expected_values:
            raise ValueError("sensorimotor vectors cannot be empty")
        if any(not isfinite(value) for value in expected_values + observed_values):
            raise ValueError("sensorimotor values must be finite")
        errors.extend(
            abs(expected_value - observed_value)
            for expected_value, observed_value in zip(
                expected_values,
                observed_values,
                strict=True,
            )
        )

    mean_error = sum(errors) / len(errors)
    correction_status = (
        "WITHIN_REFERENCE_TOLERANCE"
        if mean_error <= 0.05
        else "CORRECTION_REQUIRED"
    )
    payload = {
        "source_body_state_sha256": state.body_state_sha256,
        "motor_channel_id": motor_channel_id,
        "expectations": [asdict(item) for item in expected],
        "observations": [item.to_dict() for item in observed],
        "mean_absolute_error": mean_error,
        "correction_status": correction_status,
    }
    return TeacherSensorimotorEvaluation(
        source_body_state_sha256=state.body_state_sha256,
        motor_channel_id=motor_channel_id,
        expectations=expected,
        observations=observed,
        mean_absolute_error=mean_error,
        correction_status=correction_status,
        evaluation_sha256=_canonical_hash(payload),
    )


def build_teacher_motivational_representation(
    *,
    representation_id: str,
    representation_domain: str,
    source_body_state_sha256: str,
    salience: float,
    approach_weight: float,
    avoidance_weight: float,
    wanting_weight: float,
    predicted_liking: float,
    valence: float,
) -> TeacherMotivationalRepresentation:
    if not representation_id or not representation_domain or not source_body_state_sha256:
        raise ValueError("motivational representation requires explicit identity and source")
    values = (
        salience,
        approach_weight,
        avoidance_weight,
        wanting_weight,
        predicted_liking,
        valence,
    )
    if any(not isfinite(value) or not -1.0 <= value <= 1.0 for value in values):
        raise ValueError("motivational representation values must be finite in [-1, 1]")
    return TeacherMotivationalRepresentation(
        representation_id=representation_id,
        representation_domain=representation_domain,
        source_body_state_sha256=source_body_state_sha256,
        salience=salience,
        approach_weight=approach_weight,
        avoidance_weight=avoidance_weight,
        wanting_weight=wanting_weight,
        predicted_liking=predicted_liking,
        valence=valence,
    )


def build_teacher_within_session_trajectory(
    trajectory_id: str,
) -> TeacherWithinSessionTrajectory:
    if not trajectory_id:
        raise ValueError("trajectory_id is required")
    payload = {"trajectory_id": trajectory_id, "states": []}
    return TeacherWithinSessionTrajectory(
        trajectory_id=trajectory_id,
        states=(),
        trajectory_sha256=_canonical_hash(payload),
    )


def append_teacher_body_state(
    trajectory: TeacherWithinSessionTrajectory,
    state: TeacherIntegratedBodyState,
) -> TeacherWithinSessionTrajectory:
    if trajectory.states:
        previous = trajectory.states[-1]
        if state.sequence <= previous.sequence:
            raise ValueError("body trajectory sequence must increase")
        if state.timestamp_ms < previous.timestamp_ms:
            raise ValueError("body trajectory time cannot move backward")

    states = trajectory.states + (state,)
    payload = {
        "trajectory_id": trajectory.trajectory_id,
        "states": [item.to_dict() for item in states],
    }
    return replace(
        trajectory,
        states=states,
        trajectory_sha256=_canonical_hash(payload),
    )
