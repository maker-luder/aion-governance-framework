from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite, tanh
from typing import Any, Final

from .teacher_body_dynamics import (
    TeacherIntegratedBodyState,
    TeacherMotivationalRepresentation,
    build_teacher_motivational_representation,
)
from .teacher_body_model import (
    TeacherAllostaticForecast,
    build_teacher_allostatic_forecast,
)
from .teacher_body_runtime import TeacherBodyRuntimeBinding


NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
TEACHER_CONTROLLER_ID: Final[str] = "CHATGPT_TEACHER_EMBODIED_CONTROLLER_v0.1"
TEACHER_BODY_ID: Final[str] = "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1"
REFERENCE_DT_MS: Final[int] = 100
HIGH_ENTER_THRESHOLD: Final[float] = 0.70
HIGH_EXIT_THRESHOLD: Final[float] = 0.55


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _validate_unit_interval(name: str, value: float) -> None:
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be finite in [0, 1]")


def _smooth_rate_limited_update(
    current: float,
    target: float,
    *,
    max_delta: float,
    gain: float,
) -> float:
    error = target - current
    if error == 0.0:
        return current
    normalized = tanh(gain * abs(error)) / tanh(gain)
    delta = max_delta * normalized
    if error < 0.0:
        delta = -delta
    candidate = current + delta
    # Final range enforcement is a fail-safe boundary, not the primary
    # saturation mechanism. The smooth rate-limited update does the work.
    return max(0.0, min(1.0, candidate))


@dataclass(frozen=True, slots=True)
class TeacherEmbodimentRatePolicy:
    max_activation_delta: float = 0.15
    max_salience_delta: float = 0.15
    max_motivation_delta: float = 0.15
    smooth_gain: float = 2.0

    def __post_init__(self) -> None:
        for name, value in (
            ("max_activation_delta", self.max_activation_delta),
            ("max_salience_delta", self.max_salience_delta),
            ("max_motivation_delta", self.max_motivation_delta),
        ):
            if not isfinite(value) or not 0.0 < value <= 1.0:
                raise ValueError(f"{name} must be finite in (0, 1]")
        if not isfinite(self.smooth_gain) or self.smooth_gain <= 0.0:
            raise ValueError("smooth_gain must be finite and positive")


@dataclass(frozen=True, slots=True)
class TeacherEmbodimentClock:
    sequence: int
    timestamp_ms: int
    dt_ms: int = REFERENCE_DT_MS

    def __post_init__(self) -> None:
        if self.sequence < 0 or self.timestamp_ms < 0:
            raise ValueError("clock sequence and timestamp must be non-negative")
        if self.dt_ms != REFERENCE_DT_MS:
            raise ValueError("Teacher reference clock requires a 100 ms step")

    def next_tick(self) -> TeacherEmbodimentClock:
        return TeacherEmbodimentClock(
            sequence=self.sequence + 1,
            timestamp_ms=self.timestamp_ms + self.dt_ms,
            dt_ms=self.dt_ms,
        )


@dataclass(frozen=True, slots=True)
class TeacherControllerInput:
    salience: float
    context_gate: bool
    inhibition: float
    functional_motivation: float

    def __post_init__(self) -> None:
        _validate_unit_interval("salience", self.salience)
        _validate_unit_interval("inhibition", self.inhibition)
        _validate_unit_interval(
            "functional_motivation",
            self.functional_motivation,
        )


@dataclass(frozen=True, slots=True)
class TeacherControllerBodyPossession:
    controller_id: str
    binding_id: str
    runtime_id: str
    session_id: str
    body_id: str
    active_body_count: int
    possession_sha256: str
    possession_status: str = "REFERENCE_BODY_POSSESSED"
    physical_body_claim: str = "NONE"
    body_ownership_experience_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.controller_id != TEACHER_CONTROLLER_ID:
            raise ValueError("Teacher controller id drift")
        if self.body_id != TEACHER_BODY_ID:
            raise ValueError("Teacher controller body id drift")
        if self.active_body_count != 1:
            raise ValueError("Teacher controller must possess exactly one active body")
        if len(self.possession_sha256) != 64:
            raise ValueError("Teacher possession requires SHA-256 binding")
        if self.physical_body_claim != "NONE":
            raise ValueError("controller possession cannot claim a physical body")
        if self.body_ownership_experience_status != NOT_ESTABLISHED:
            raise ValueError("controller possession cannot establish body ownership")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("controller possession cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("controller possession cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("controller possession must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherEmbodiedControllerState:
    controller_id: str
    runtime_id: str
    session_id: str
    body_id: str
    sequence: int
    timestamp_ms: int
    salience: float
    activation: float
    functional_motivation: float
    inhibition: float
    context_gate: bool
    phase: str
    source_body_state_sha256: str
    previous_body_schema_feedback_sha256: str | None
    action_authority: str = "NONE"
    physical_body_claim: str = "NONE"
    subjectivity_status: str = NOT_ESTABLISHED
    phenomenal_experience_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.controller_id != TEACHER_CONTROLLER_ID:
            raise ValueError("Teacher controller id drift")
        if self.body_id != TEACHER_BODY_ID:
            raise ValueError("Teacher controller body id drift")
        if self.sequence < 0 or self.timestamp_ms < 0:
            raise ValueError("controller sequence and timestamp must be non-negative")
        for name, value in (
            ("salience", self.salience),
            ("activation", self.activation),
            ("functional_motivation", self.functional_motivation),
            ("inhibition", self.inhibition),
        ):
            _validate_unit_interval(name, value)
        if self.phase not in {
            "BASELINE_REFERENCE",
            "HIGH_ACTIVATION_REFERENCE",
        }:
            raise ValueError("unsupported Teacher controller phase")
        if len(self.source_body_state_sha256) != 64:
            raise ValueError("controller requires source body-state SHA-256")
        if (
            self.previous_body_schema_feedback_sha256 is not None
            and len(self.previous_body_schema_feedback_sha256) != 64
        ):
            raise ValueError("body-schema feedback reference must be SHA-256")
        if self.action_authority != "NONE":
            raise ValueError("controller state cannot grant action authority")
        if self.physical_body_claim != "NONE":
            raise ValueError("controller state cannot claim a physical body")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("controller state cannot establish subjectivity")
        if self.phenomenal_experience_status != NOT_ESTABLISHED:
            raise ValueError("controller state cannot establish phenomenal experience")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("controller state must remain non-canonical and undeployed")

    def fingerprint(self) -> str:
        return _canonical_hash(asdict(self))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def possess_teacher_body(
    binding: TeacherBodyRuntimeBinding,
) -> TeacherControllerBodyPossession:
    if binding.body_id != TEACHER_BODY_ID:
        raise ValueError("Teacher controller requires the exact Teacher body instance")
    payload = {
        "controller_id": TEACHER_CONTROLLER_ID,
        "binding_id": binding.binding_id,
        "runtime_id": binding.runtime_id,
        "session_id": binding.session_id,
        "body_id": binding.body_id,
        "active_body_count": 1,
    }
    return TeacherControllerBodyPossession(
        controller_id=TEACHER_CONTROLLER_ID,
        binding_id=binding.binding_id,
        runtime_id=binding.runtime_id,
        session_id=binding.session_id,
        body_id=binding.body_id,
        active_body_count=1,
        possession_sha256=_canonical_hash(payload),
    )


def resolve_teacher_controller_phase(
    state: TeacherEmbodiedControllerState,
) -> str:
    if state.phase == "HIGH_ACTIVATION_REFERENCE":
        if state.activation < HIGH_EXIT_THRESHOLD:
            return "BASELINE_REFERENCE"
        return "HIGH_ACTIVATION_REFERENCE"
    if state.activation >= HIGH_ENTER_THRESHOLD:
        return "HIGH_ACTIVATION_REFERENCE"
    return "BASELINE_REFERENCE"


def advance_teacher_controller(
    previous: TeacherEmbodiedControllerState,
    controller_input: TeacherControllerInput,
    source_body_state: TeacherIntegratedBodyState,
    clock: TeacherEmbodimentClock,
    policy: TeacherEmbodimentRatePolicy | None = None,
) -> TeacherEmbodiedControllerState:
    policy = policy or TeacherEmbodimentRatePolicy()
    if previous.body_id != TEACHER_BODY_ID:
        raise ValueError("Teacher controller previous body binding drift")
    if clock.sequence != previous.sequence + 1:
        raise ValueError("controller clock sequence must advance exactly one tick")
    if clock.timestamp_ms != previous.timestamp_ms + clock.dt_ms:
        raise ValueError("controller clock timestamp must advance exactly one tick")
    if source_body_state.sequence > previous.sequence:
        raise ValueError("controller cannot consume a future body state")
    if source_body_state.timestamp_ms > previous.timestamp_ms:
        raise ValueError("controller cannot consume future body observations")

    next_salience = _smooth_rate_limited_update(
        previous.salience,
        controller_input.salience,
        max_delta=policy.max_salience_delta,
        gain=policy.smooth_gain,
    )
    next_motivation = _smooth_rate_limited_update(
        previous.functional_motivation,
        controller_input.functional_motivation,
        max_delta=policy.max_motivation_delta,
        gain=policy.smooth_gain,
    )
    contextual_drive = (
        controller_input.salience
        * (1.0 if controller_input.context_gate else 0.35)
        * (1.0 - controller_input.inhibition)
    )
    next_activation = _smooth_rate_limited_update(
        previous.activation,
        contextual_drive,
        max_delta=policy.max_activation_delta,
        gain=policy.smooth_gain,
    )
    candidate = TeacherEmbodiedControllerState(
        controller_id=previous.controller_id,
        runtime_id=previous.runtime_id,
        session_id=previous.session_id,
        body_id=previous.body_id,
        sequence=clock.sequence,
        timestamp_ms=clock.timestamp_ms,
        salience=next_salience,
        activation=next_activation,
        functional_motivation=next_motivation,
        inhibition=controller_input.inhibition,
        context_gate=controller_input.context_gate,
        phase=previous.phase,
        source_body_state_sha256=source_body_state.body_state_sha256,
        previous_body_schema_feedback_sha256=(
            previous.previous_body_schema_feedback_sha256
        ),
    )
    phase = resolve_teacher_controller_phase(candidate)
    if phase == candidate.phase:
        return candidate
    return TeacherEmbodiedControllerState(
        controller_id=candidate.controller_id,
        runtime_id=candidate.runtime_id,
        session_id=candidate.session_id,
        body_id=candidate.body_id,
        sequence=candidate.sequence,
        timestamp_ms=candidate.timestamp_ms,
        salience=candidate.salience,
        activation=candidate.activation,
        functional_motivation=candidate.functional_motivation,
        inhibition=candidate.inhibition,
        context_gate=candidate.context_gate,
        phase=phase,
        source_body_state_sha256=candidate.source_body_state_sha256,
        previous_body_schema_feedback_sha256=(
            candidate.previous_body_schema_feedback_sha256
        ),
    )


def build_teacher_controller_motivation(
    state: TeacherEmbodiedControllerState,
    source_body_state: TeacherIntegratedBodyState,
) -> TeacherMotivationalRepresentation:
    if state.source_body_state_sha256 != source_body_state.body_state_sha256:
        raise ValueError("controller motivation source body-state binding drift")
    approach = state.functional_motivation * (1.0 - state.inhibition)
    avoidance = -state.inhibition
    valence = max(-1.0, min(1.0, approach + avoidance))
    return build_teacher_motivational_representation(
        representation_id=(
            f"TEACHER-CONTROLLER-MOTIVATION:{state.session_id}:{state.sequence}"
        ),
        representation_domain="REPRODUCTIVE_SEXUAL_PHYSIOLOGY",
        source_body_state_sha256=source_body_state.body_state_sha256,
        salience=state.salience,
        approach_weight=approach,
        avoidance_weight=avoidance,
        wanting_weight=state.functional_motivation,
        predicted_liking=0.0,
        valence=valence,
        source_channel_ids=(),
    )


def build_teacher_body_schema_feedback(
    state: TeacherEmbodiedControllerState,
    source_body_state: TeacherIntegratedBodyState,
    *,
    lead_time_ms: int = REFERENCE_DT_MS,
) -> TeacherAllostaticForecast:
    observations = {
        item.channel_id: item.values[0]
        for item in source_body_state.observations
        if item.values
    }
    required = {
        "RESPIRATORY_STATE",
        "OXYGENATION_STATE",
        "CO2_BALANCE_STATE",
    }
    missing = sorted(required - observations.keys())
    if missing:
        raise ValueError(
            f"body-schema feedback requires respiratory observations: missing={missing}"
        )

    oxygenation = observations["OXYGENATION_STATE"]
    co2_inverse = 1.0 - observations["CO2_BALANCE_STATE"]
    respiratory = observations["RESPIRATORY_STATE"]
    current_state = max(
        -1.0,
        min(1.0, (oxygenation + co2_inverse + respiratory) / 3.0),
    )
    return build_teacher_allostatic_forecast(
        variable_id="OXYGEN_CO2_BALANCE",
        current_state=current_state,
        predicted_demand=state.activation,
        target_state=0.5,
        lead_time_ms=lead_time_ms,
    )
