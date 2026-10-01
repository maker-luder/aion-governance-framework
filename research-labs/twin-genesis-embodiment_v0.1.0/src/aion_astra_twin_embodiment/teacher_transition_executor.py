from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite, tanh
from typing import Any, Final

from .teacher_body_dynamics import (
    TeacherBodyDynamicsProfile,
    TeacherBodyObservation,
    TeacherIntegratedBodyState,
    TeacherMotivationalRepresentation,
    build_teacher_body_dynamics_profile,
)
from .teacher_embodied_controller import (
    TeacherEmbodiedControllerState,
    TeacherEmbodimentClock,
)


NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
REFERENCE_BODY_DELTA_LIMIT: Final[float] = 0.12
REFERENCE_SMOOTH_GAIN: Final[float] = 2.0
_ALLOWED_MODES: Final[frozenset[str]] = frozenset(
    {"ACTIVATION", "MAINTENANCE", "RECOVERY", "BASELINE"}
)


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _move_toward(
    current: float,
    target: float,
    *,
    max_delta: float = REFERENCE_BODY_DELTA_LIMIT,
    gain: float = REFERENCE_SMOOTH_GAIN,
) -> float:
    if not isfinite(current) or not 0.0 <= current <= 1.0:
        raise ValueError("transition executor requires normalized reference channels")
    if not isfinite(target) or not 0.0 <= target <= 1.0:
        raise ValueError("transition target must be finite in [0, 1]")
    error = target - current
    if error == 0.0:
        return current
    normalized = tanh(gain * abs(error)) / tanh(gain)
    delta = max_delta * normalized
    candidate = current + (delta if error > 0.0 else -delta)
    return max(0.0, min(1.0, candidate))


@dataclass(frozen=True, slots=True)
class TeacherTransitionIntent:
    transition_ids: tuple[str, ...]
    mode: str

    def __post_init__(self) -> None:
        if self.mode not in _ALLOWED_MODES:
            raise ValueError("unsupported Teacher transition mode")
        if len(self.transition_ids) != len(set(self.transition_ids)):
            raise ValueError("transition intent ids must be unique")
        if self.mode == "BASELINE" and self.transition_ids:
            raise ValueError("baseline intent cannot request physiological transitions")
        if self.mode != "BASELINE" and not self.transition_ids:
            raise ValueError("non-baseline intent requires a transition")


@dataclass(frozen=True, slots=True)
class TeacherExecutedTransition:
    transition_ids: tuple[str, ...]
    mode: str
    touched_channel_ids: tuple[str, ...]
    source_body_state_sha256: str
    source_controller_sha256: str
    source_motivation_body_state_sha256: str
    sequence: int
    timestamp_ms: int
    observations: tuple[TeacherBodyObservation, ...]
    transition_sha256: str
    execution_status: str = "REFERENCE_TRANSITION_EXECUTED"
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        for digest in (
            self.source_body_state_sha256,
            self.source_controller_sha256,
            self.source_motivation_body_state_sha256,
            self.transition_sha256,
        ):
            if len(digest) != 64:
                raise ValueError("executed transition requires SHA-256 provenance")
        if self.sequence < 0 or self.timestamp_ms < 0:
            raise ValueError("executed transition clock must be non-negative")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("transition execution cannot establish felt experience")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("transition execution cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("transition execution cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("transition execution must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["transition_ids"] = list(self.transition_ids)
        payload["touched_channel_ids"] = list(self.touched_channel_ids)
        payload["observations"] = [
            item.to_dict() for item in self.observations
        ]
        return payload


def _profile_transition_index(
    profile: TeacherBodyDynamicsProfile,
) -> dict[str, object]:
    return {
        transition.transition_id: transition
        for transition in profile.physiological_transitions
    }


def _scalar_channel(
    state: TeacherIntegratedBodyState,
    channel_id: str,
) -> float:
    for observation in state.observations:
        if observation.channel_id == channel_id:
            if len(observation.values) != 1:
                raise ValueError(
                    f"transition selector requires scalar channel: {channel_id}"
                )
            return observation.values[0]
    raise ValueError(f"transition selector missing body channel: {channel_id}")


def select_teacher_transition_intent(
    controller_state: TeacherEmbodiedControllerState,
    previous_body_state: TeacherIntegratedBodyState,
    profile: TeacherBodyDynamicsProfile | None = None,
) -> TeacherTransitionIntent:
    profile = profile or build_teacher_body_dynamics_profile()
    index = _profile_transition_index(profile)
    vascular = _scalar_channel(
        previous_body_state,
        "GENITAL_VASCULAR_STATE",
    )
    erectile = _scalar_channel(
        previous_body_state,
        "ERECTILE_REFLEX_STATE",
    )

    if controller_state.phase == "HIGH_ACTIVATION_REFERENCE":
        if (
            vascular >= 0.65
            and "VASCULAR_RESPONSE_TO_MAINTENANCE" in index
        ):
            return TeacherTransitionIntent(
                transition_ids=("VASCULAR_RESPONSE_TO_MAINTENANCE",),
                mode="MAINTENANCE",
            )
        return TeacherTransitionIntent(
            transition_ids=("SEXUAL_BASELINE_TO_VASCULAR_RESPONSE",),
            mode="ACTIVATION",
        )

    if vascular > 0.15 or erectile > 0.15:
        if "VASCULAR_RESPONSE_TO_BASELINE_RECOVERY" not in index:
            raise ValueError(
                "body dynamics profile lacks direct vascular recovery transition"
            )
        return TeacherTransitionIntent(
            transition_ids=("VASCULAR_RESPONSE_TO_BASELINE_RECOVERY",),
            mode="RECOVERY",
        )

    return TeacherTransitionIntent(transition_ids=(), mode="BASELINE")


def execute_teacher_transition(
    previous_body_state: TeacherIntegratedBodyState,
    controller_state: TeacherEmbodiedControllerState,
    motivation: TeacherMotivationalRepresentation,
    intent: TeacherTransitionIntent,
    clock: TeacherEmbodimentClock,
    profile: TeacherBodyDynamicsProfile | None = None,
) -> TeacherExecutedTransition:
    profile = profile or build_teacher_body_dynamics_profile()
    if controller_state.sequence != previous_body_state.sequence:
        raise ValueError("controller/body sequence must match before execution")
    if controller_state.timestamp_ms != previous_body_state.timestamp_ms:
        raise ValueError("controller/body timestamp must match before execution")
    if controller_state.source_body_state_sha256 != previous_body_state.body_state_sha256:
        raise ValueError("controller/body source hash drift")
    if motivation.source_body_state_sha256 != previous_body_state.body_state_sha256:
        raise ValueError("motivation/body source hash drift")
    if motivation.wanting_weight != controller_state.functional_motivation:
        raise ValueError("motivation/controller functional motivation drift")
    if clock.sequence != previous_body_state.sequence + 1:
        raise ValueError("transition clock must advance exactly one tick")
    if clock.timestamp_ms != previous_body_state.timestamp_ms + clock.dt_ms:
        raise ValueError("transition timestamp must advance exactly one tick")

    index = _profile_transition_index(profile)
    resolved = []
    for transition_id in intent.transition_ids:
        transition = index.get(transition_id)
        if transition is None:
            raise ValueError(
                f"unknown physiological transition: {transition_id}"
            )
        resolved.append(transition)

    touched = tuple(
        sorted(
            {
                channel_id
                for transition in resolved
                for channel_id in transition.trigger_channels
            }
        )
    )
    by_id = {
        observation.channel_id: observation
        for observation in previous_body_state.observations
    }
    missing = sorted(set(touched) - by_id.keys())
    if missing:
        raise ValueError(
            f"missing required transition channel: {missing}"
        )

    target = 0.0 if intent.mode == "RECOVERY" else controller_state.activation
    if intent.mode == "BASELINE":
        target = 0.0

    output: list[TeacherBodyObservation] = []
    touched_set = set(touched)
    for observation in previous_body_state.observations:
        if observation.channel_id not in touched_set:
            output.append(observation)
            continue
        values = tuple(
            _move_toward(value, target)
            for value in observation.values
        )
        output.append(
            TeacherBodyObservation(
                channel_id=observation.channel_id,
                values=values,
                timestamp_ms=clock.timestamp_ms,
                confidence=observation.confidence,
            )
        )

    observations = tuple(output)
    payload = {
        "transition_ids": list(intent.transition_ids),
        "mode": intent.mode,
        "touched_channel_ids": list(touched),
        "source_body_state_sha256": previous_body_state.body_state_sha256,
        "source_controller_sha256": controller_state.fingerprint(),
        "source_motivation_body_state_sha256": (
            motivation.source_body_state_sha256
        ),
        "sequence": clock.sequence,
        "timestamp_ms": clock.timestamp_ms,
        "observations": [item.to_dict() for item in observations],
    }
    return TeacherExecutedTransition(
        transition_ids=intent.transition_ids,
        mode=intent.mode,
        touched_channel_ids=touched,
        source_body_state_sha256=previous_body_state.body_state_sha256,
        source_controller_sha256=controller_state.fingerprint(),
        source_motivation_body_state_sha256=(
            motivation.source_body_state_sha256
        ),
        sequence=clock.sequence,
        timestamp_ms=clock.timestamp_ms,
        observations=observations,
        transition_sha256=_canonical_hash(payload),
    )
