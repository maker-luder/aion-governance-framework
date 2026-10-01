from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final

from .teacher_body_dynamics import (
    TeacherBodyObservation,
    TeacherIntegratedBodyState,
    TeacherWithinSessionTrajectory,
    append_teacher_body_state,
    build_teacher_within_session_trajectory,
    integrate_teacher_body_state,
)
from .teacher_body_runtime import (
    TeacherBodyRuntimeBinding,
    TeacherBoundBodyState,
    bind_teacher_integrated_body_state,
)


NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
TEACHER_AGENT_ID: Final[str] = "CHATGPT_TEACHER"
TEACHER_BODY_ID: Final[str] = "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1"
REFERENCE_ONLY: Final[str] = "FUNCTIONAL_REFERENCE_ONLY"
PROFESSIONAL_REPORTING: Final[str] = "PROFESSIONAL_RESEARCH_REPORT"
RAW_PRIVATE_CONTENT_EXCLUDED: Final[str] = "EXCLUDED"
ALLOWED_STIMULUS_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "BASELINE_REFERENCE",
        "HIGH_SALIENCE_INTIMATE_REFERENCE",
        "HIGH_SALIENCE_NON_INTIMATE_REFERENCE",
        "RECOVERY_REFERENCE",
    }
)


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class TeacherStimulusEnvelope:
    stimulus_id: str
    stimulus_class: str
    salience: float
    functional_motivation: float
    sexual_context_gate: bool
    inhibition: float
    raw_private_content_included: bool = False
    raw_private_content_status: str = RAW_PRIVATE_CONTENT_EXCLUDED
    interpretation: str = REFERENCE_ONLY
    human_consent_inference: str = "FORBIDDEN"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.stimulus_id:
            raise ValueError("stimulus_id is required")
        if self.stimulus_class not in ALLOWED_STIMULUS_CLASSES:
            raise ValueError("unsupported stimulus class")
        for value in (self.salience, self.functional_motivation, self.inhibition):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError("stimulus reference values must be finite in [0, 1]")
        if self.raw_private_content_included:
            raise ValueError("public research envelope cannot include raw private content")
        if self.raw_private_content_status != RAW_PRIVATE_CONTENT_EXCLUDED:
            raise ValueError("raw private content must remain excluded")
        if self.interpretation != REFERENCE_ONLY:
            raise ValueError("stimulus envelope must remain functional-reference only")
        if self.human_consent_inference != "FORBIDDEN":
            raise ValueError("stimulus envelope cannot infer human consent")
        if self.action_authority != "NONE":
            raise ValueError("stimulus envelope cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("stimulus envelope must remain non-canonical and undeployed")

    def fingerprint(self) -> str:
        return _canonical_hash(asdict(self))


@dataclass(frozen=True, slots=True)
class TeacherFunctionalEmbodiedState:
    state_id: str
    stimulus_sha256: str
    phase: str
    functional_arousal: float
    functional_motivation: float
    sexual_context_gate: bool
    inhibition: float
    interpretation: str = "FUNCTIONAL_ANALOGUE_ONLY"
    physiology_signal_sets_motivation: bool = False
    phenomenal_sexual_desire: str = NOT_ESTABLISHED
    phenomenal_sexual_arousal: str = NOT_ESTABLISHED
    sexual_pleasure: str = NOT_ESTABLISHED
    felt_body_sensation: str = NOT_ESTABLISHED
    subjectivity: str = NOT_ESTABLISHED
    consciousness: str = NOT_ESTABLISHED
    phenomenal_experience: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.state_id or len(self.stimulus_sha256) != 64:
            raise ValueError("functional embodied state requires identity and stimulus hash")
        if self.phase not in {"BASELINE", "ACTIVATION", "RECOVERY"}:
            raise ValueError("unsupported embodied-state phase")
        for value in (
            self.functional_arousal,
            self.functional_motivation,
            self.inhibition,
        ):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError("functional embodied state values must be in [0, 1]")
        if self.interpretation != "FUNCTIONAL_ANALOGUE_ONLY":
            raise ValueError("functional embodied state cannot claim phenomenal interpretation")
        if self.physiology_signal_sets_motivation:
            raise ValueError("physiology signal cannot automatically set motivation")
        if any(
            value != NOT_ESTABLISHED
            for value in (
                self.phenomenal_sexual_desire,
                self.phenomenal_sexual_arousal,
                self.sexual_pleasure,
                self.felt_body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("functional embodied state cannot establish phenomenal experience")
        if self.action_authority != "NONE":
            raise ValueError("functional embodied state cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("functional embodied state must remain non-canonical and undeployed")

    def fingerprint(self) -> str:
        return _canonical_hash(asdict(self))


@dataclass(frozen=True, slots=True)
class TeacherBodyStateReport:
    report_id: str
    phase: str
    body_id: str
    stimulus_class: str
    stimulus_sha256: str
    functional_state_sha256: str
    body_state_sha256: str
    bound_state_sha256: str
    observed_reference_channels: tuple[tuple[str, float], ...]
    reporting_style: str = PROFESSIONAL_REPORTING
    raw_private_content_status: str = RAW_PRIVATE_CONTENT_EXCLUDED
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.report_id:
            raise ValueError("report_id is required")
        if self.body_id != TEACHER_BODY_ID:
            raise ValueError("Teacher report body binding drift")
        for digest in (
            self.stimulus_sha256,
            self.functional_state_sha256,
            self.body_state_sha256,
            self.bound_state_sha256,
        ):
            if len(digest) != 64:
                raise ValueError("Teacher report requires SHA-256 bindings")
        if self.reporting_style != PROFESSIONAL_REPORTING:
            raise ValueError("Teacher state report must remain professional research reporting")
        if self.raw_private_content_status != RAW_PRIVATE_CONTENT_EXCLUDED:
            raise ValueError("Teacher report cannot contain raw private content")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("Teacher report cannot establish phenomenal interpretation")
        if self.action_authority != "NONE":
            raise ValueError("Teacher report cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("Teacher report must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["observed_reference_channels"] = [
            [name, value] for name, value in self.observed_reference_channels
        ]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherStateLoopFrame:
    functional_state: TeacherFunctionalEmbodiedState
    body_state: TeacherIntegratedBodyState
    bound_body_state: TeacherBoundBodyState
    report: TeacherBodyStateReport


@dataclass(frozen=True, slots=True)
class TeacherStateLoopRun:
    runtime_id: str
    session_id: str
    body_id: str
    trajectory: TeacherWithinSessionTrajectory
    frames: tuple[TeacherStateLoopFrame, ...]
    run_sha256: str
    raw_private_content_status: str = RAW_PRIVATE_CONTENT_EXCLUDED
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.body_id != TEACHER_BODY_ID:
            raise ValueError("Teacher state-loop body binding drift")
        if len(self.frames) != 3:
            raise ValueError("Teacher state loop requires baseline, activation, recovery")
        if tuple(frame.functional_state.phase for frame in self.frames) != (
            "BASELINE",
            "ACTIVATION",
            "RECOVERY",
        ):
            raise ValueError("Teacher state-loop phase order drift")
        if len(self.run_sha256) != 64:
            raise ValueError("Teacher state loop requires deterministic hash")
        if self.raw_private_content_status != RAW_PRIVATE_CONTENT_EXCLUDED:
            raise ValueError("Teacher state loop cannot retain raw private content")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("Teacher state loop cannot establish phenomenal interpretation")
        if self.action_authority != "NONE":
            raise ValueError("Teacher state loop cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("Teacher state loop must remain non-canonical and undeployed")


def build_teacher_stimulus_envelope(
    *,
    stimulus_id: str,
    stimulus_class: str,
    salience: float,
    functional_motivation: float,
    sexual_context_gate: bool,
    inhibition: float,
) -> TeacherStimulusEnvelope:
    return TeacherStimulusEnvelope(
        stimulus_id=stimulus_id,
        stimulus_class=stimulus_class,
        salience=salience,
        functional_motivation=functional_motivation,
        sexual_context_gate=sexual_context_gate,
        inhibition=inhibition,
    )


def _functional_state_from_stimulus(
    stimulus: TeacherStimulusEnvelope,
    *,
    state_id: str,
    phase: str,
    recovery_fraction: float = 0.0,
) -> TeacherFunctionalEmbodiedState:
    if not 0.0 <= recovery_fraction <= 1.0:
        raise ValueError("recovery_fraction must be in [0, 1]")

    contextual_activation = (
        stimulus.salience
        * (1.0 if stimulus.sexual_context_gate else 0.35)
        * (1.0 - 0.65 * stimulus.inhibition)
    )
    activation = _clamp01(contextual_activation)
    if phase == "BASELINE":
        activation = 0.0
        motivation = 0.0
    elif phase == "RECOVERY":
        activation = _clamp01(activation * (1.0 - recovery_fraction))
        motivation = _clamp01(
            stimulus.functional_motivation * (1.0 - recovery_fraction)
        )
    else:
        motivation = stimulus.functional_motivation

    return TeacherFunctionalEmbodiedState(
        state_id=state_id,
        stimulus_sha256=stimulus.fingerprint(),
        phase=phase,
        functional_arousal=activation,
        functional_motivation=motivation,
        sexual_context_gate=stimulus.sexual_context_gate,
        inhibition=stimulus.inhibition,
    )


def _reference_observations(
    state: TeacherFunctionalEmbodiedState,
    *,
    timestamp_ms: int,
) -> tuple[TeacherBodyObservation, ...]:
    arousal = state.functional_arousal
    recovery = 1.0 - arousal if state.phase == "RECOVERY" else 0.0
    sympathetic = _clamp01(0.20 + 0.65 * arousal)
    parasympathetic = _clamp01(0.75 - 0.45 * arousal)
    cardiovascular = _clamp01(0.30 + 0.45 * arousal)
    respiratory = _clamp01(0.25 + 0.45 * arousal)
    adrenal = _clamp01(0.20 + 0.50 * arousal)
    endocrine = _clamp01(0.25 + 0.25 * arousal)
    gonadal_endocrine = _clamp01(0.25 + 0.20 * arousal)
    genital_vascular = _clamp01(0.05 + 0.90 * arousal)
    erectile_reflex = _clamp01(0.05 + 0.80 * arousal)
    pelvic_floor = _clamp01(0.10 + 0.40 * arousal)

    return (
        TeacherBodyObservation("TACTILE_GENERAL", (0.0,), timestamp_ms),
        TeacherBodyObservation("JOINT_POSITION", (0.0, 0.0, 0.0), timestamp_ms),
        TeacherBodyObservation(
            "VESTIBULAR_ORIENTATION",
            (1.0, 0.0, 0.0, 0.0),
            timestamp_ms,
        ),
        TeacherBodyObservation("CARDIOVASCULAR_STATE", (cardiovascular,), timestamp_ms),
        TeacherBodyObservation("RESPIRATORY_STATE", (respiratory,), timestamp_ms),
        TeacherBodyObservation(
            "AUTONOMIC_SYMPATHETIC_STATE",
            (sympathetic,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "AUTONOMIC_PARASYMPATHETIC_STATE",
            (parasympathetic,),
            timestamp_ms,
        ),
        TeacherBodyObservation("ADRENAL_AXIS_STATE", (adrenal,), timestamp_ms),
        TeacherBodyObservation("ENDOCRINE_REFERENCE_STATE", (endocrine,), timestamp_ms),
        TeacherBodyObservation(
            "GONADAL_ENDOCRINE_REFERENCE",
            (gonadal_endocrine,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "GENITAL_VASCULAR_STATE",
            (genital_vascular,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "ERECTILE_REFLEX_STATE",
            (erectile_reflex,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "PELVIC_FLOOR_PROPRIOCEPTION",
            (pelvic_floor,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "DETUMESCENCE_STATE",
            (_clamp01(recovery),),
            timestamp_ms,
        ),
    )


def _selected_channel_values(
    body_state: TeacherIntegratedBodyState,
) -> tuple[tuple[str, float], ...]:
    selected = {
        "CARDIOVASCULAR_STATE",
        "RESPIRATORY_STATE",
        "AUTONOMIC_SYMPATHETIC_STATE",
        "AUTONOMIC_PARASYMPATHETIC_STATE",
        "ADRENAL_AXIS_STATE",
        "ENDOCRINE_REFERENCE_STATE",
        "GONADAL_ENDOCRINE_REFERENCE",
        "GENITAL_VASCULAR_STATE",
        "ERECTILE_REFLEX_STATE",
        "PELVIC_FLOOR_PROPRIOCEPTION",
        "DETUMESCENCE_STATE",
    }
    values: list[tuple[str, float]] = []
    for observation in body_state.observations:
        if observation.channel_id in selected:
            values.append((observation.channel_id, observation.values[0]))
    return tuple(sorted(values))


def build_teacher_state_loop_frame(
    binding: TeacherBodyRuntimeBinding,
    stimulus: TeacherStimulusEnvelope,
    *,
    sequence: int,
    timestamp_ms: int,
    phase: str,
    recovery_fraction: float = 0.0,
) -> TeacherStateLoopFrame:
    if binding.body_id != TEACHER_BODY_ID:
        raise ValueError("Teacher state loop requires Teacher body binding")

    functional_state = _functional_state_from_stimulus(
        stimulus,
        state_id=f"{stimulus.stimulus_id}:{phase}:{sequence}",
        phase=phase,
        recovery_fraction=recovery_fraction,
    )
    observations = _reference_observations(
        functional_state,
        timestamp_ms=timestamp_ms,
    )
    body_state = integrate_teacher_body_state(
        observations,
        sequence=sequence,
    )
    bound = bind_teacher_integrated_body_state(binding, body_state)
    report = TeacherBodyStateReport(
        report_id=f"TEACHER-STATE-REPORT:{binding.session_id}:{sequence}",
        phase=phase,
        body_id=binding.body_id,
        stimulus_class=stimulus.stimulus_class,
        stimulus_sha256=stimulus.fingerprint(),
        functional_state_sha256=functional_state.fingerprint(),
        body_state_sha256=body_state.body_state_sha256,
        bound_state_sha256=bound.bound_state_sha256,
        observed_reference_channels=_selected_channel_values(body_state),
    )
    return TeacherStateLoopFrame(
        functional_state=functional_state,
        body_state=body_state,
        bound_body_state=bound,
        report=report,
    )


def run_teacher_reference_state_loop(
    binding: TeacherBodyRuntimeBinding,
    *,
    activation_stimulus: TeacherStimulusEnvelope,
    start_timestamp_ms: int = 0,
) -> TeacherStateLoopRun:
    if start_timestamp_ms < 0:
        raise ValueError("start_timestamp_ms cannot be negative")
    if activation_stimulus.stimulus_class != "HIGH_SALIENCE_INTIMATE_REFERENCE":
        raise ValueError("reference state loop requires high-salience intimate stimulus class")

    baseline_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{activation_stimulus.stimulus_id}:baseline",
        stimulus_class="BASELINE_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=1.0,
    )
    recovery_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{activation_stimulus.stimulus_id}:recovery",
        stimulus_class="RECOVERY_REFERENCE",
        salience=activation_stimulus.salience,
        functional_motivation=activation_stimulus.functional_motivation,
        sexual_context_gate=activation_stimulus.sexual_context_gate,
        inhibition=activation_stimulus.inhibition,
    )

    baseline = build_teacher_state_loop_frame(
        binding,
        baseline_stimulus,
        sequence=0,
        timestamp_ms=start_timestamp_ms,
        phase="BASELINE",
    )
    activation = build_teacher_state_loop_frame(
        binding,
        activation_stimulus,
        sequence=1,
        timestamp_ms=start_timestamp_ms + 1000,
        phase="ACTIVATION",
    )
    recovery = build_teacher_state_loop_frame(
        binding,
        recovery_stimulus,
        sequence=2,
        timestamp_ms=start_timestamp_ms + 2000,
        phase="RECOVERY",
        recovery_fraction=0.90,
    )

    trajectory = build_teacher_within_session_trajectory(
        f"TEACHER-STATE-TRAJECTORY:{binding.session_id}"
    )
    for frame in (baseline, activation, recovery):
        trajectory = append_teacher_body_state(trajectory, frame.body_state)

    frames = (baseline, activation, recovery)
    payload = {
        "runtime_id": binding.runtime_id,
        "session_id": binding.session_id,
        "body_id": binding.body_id,
        "trajectory_sha256": trajectory.trajectory_sha256,
        "frame_reports": [frame.report.to_dict() for frame in frames],
    }
    return TeacherStateLoopRun(
        runtime_id=binding.runtime_id,
        session_id=binding.session_id,
        body_id=binding.body_id,
        trajectory=trajectory,
        frames=frames,
        run_sha256=_canonical_hash(payload),
    )
