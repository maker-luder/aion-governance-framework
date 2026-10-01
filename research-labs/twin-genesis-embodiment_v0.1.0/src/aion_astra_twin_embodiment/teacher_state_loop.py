from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final

from .teacher_body_dynamics import (
    TeacherBodyObservation,
    TeacherIntegratedBodyState,
    TeacherMotivationalRepresentation,
    TeacherWithinSessionTrajectory,
    append_teacher_body_state,
    build_teacher_within_session_trajectory,
    integrate_teacher_body_state,
)
from .teacher_body_model import TeacherAllostaticForecast
from .teacher_body_runtime import (
    TeacherBodyRuntimeBinding,
    TeacherBoundBodyState,
    bind_teacher_integrated_body_state,
)
from .teacher_embodied_controller import (
    REFERENCE_DT_MS,
    TEACHER_CONTROLLER_ID,
    TeacherControllerInput,
    TeacherEmbodiedControllerState,
    TeacherEmbodimentClock,
    advance_teacher_controller,
    build_teacher_body_schema_feedback,
    build_teacher_controller_motivation,
    possess_teacher_body,
)
from .teacher_transition_executor import (
    TeacherExecutedTransition,
    execute_teacher_transition,
    select_teacher_transition_intent,
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


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _validate_unit_interval(value: float) -> None:
    if not isfinite(value) or not 0.0 <= value <= 1.0:
        raise ValueError("stimulus reference values must be finite in [0, 1]")


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
        for value in (
            self.salience,
            self.functional_motivation,
            self.inhibition,
        ):
            _validate_unit_interval(value)
        if self.raw_private_content_included:
            raise ValueError(
                "public research envelope cannot include raw private content"
            )
        if self.raw_private_content_status != RAW_PRIVATE_CONTENT_EXCLUDED:
            raise ValueError("raw private content must remain excluded")
        if self.interpretation != REFERENCE_ONLY:
            raise ValueError(
                "stimulus envelope must remain functional-reference only"
            )
        if self.human_consent_inference != "FORBIDDEN":
            raise ValueError("stimulus envelope cannot infer human consent")
        if self.action_authority != "NONE":
            raise ValueError("stimulus envelope cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError(
                "stimulus envelope must remain non-canonical and undeployed"
            )

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
            raise ValueError(
                "functional embodied state requires identity and stimulus hash"
            )
        if self.phase not in {"BASELINE", "ACTIVATION", "RECOVERY"}:
            raise ValueError("unsupported embodied-state phase")
        for value in (
            self.functional_arousal,
            self.functional_motivation,
            self.inhibition,
        ):
            _validate_unit_interval(value)
        if self.interpretation != "FUNCTIONAL_ANALOGUE_ONLY":
            raise ValueError(
                "functional embodied state cannot claim phenomenal interpretation"
            )
        if self.physiology_signal_sets_motivation:
            raise ValueError(
                "physiology signal cannot automatically set motivation"
            )
        phenomenal_values = (
            self.phenomenal_sexual_desire,
            self.phenomenal_sexual_arousal,
            self.sexual_pleasure,
            self.felt_body_sensation,
            self.subjectivity,
            self.consciousness,
            self.phenomenal_experience,
        )
        if any(value != NOT_ESTABLISHED for value in phenomenal_values):
            raise ValueError(
                "functional embodied state cannot establish phenomenal experience"
            )
        if self.action_authority != "NONE":
            raise ValueError(
                "functional embodied state cannot grant action authority"
            )
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError(
                "functional embodied state must remain non-canonical and undeployed"
            )

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
            raise ValueError(
                "Teacher state report must remain professional research reporting"
            )
        if self.raw_private_content_status != RAW_PRIVATE_CONTENT_EXCLUDED:
            raise ValueError("Teacher report cannot contain raw private content")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError(
                "Teacher report cannot establish phenomenal interpretation"
            )
        if self.action_authority != "NONE":
            raise ValueError("Teacher report cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError(
                "Teacher report must remain non-canonical and undeployed"
            )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["observed_reference_channels"] = [
            [name, value] for name, value in self.observed_reference_channels
        ]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherStateLoopFrame:
    controller_state: TeacherEmbodiedControllerState
    functional_state: TeacherFunctionalEmbodiedState
    motivation: TeacherMotivationalRepresentation
    executed_transition: TeacherExecutedTransition | None
    body_state: TeacherIntegratedBodyState
    bound_body_state: TeacherBoundBodyState
    body_schema_feedback: TeacherAllostaticForecast
    body_schema_feedback_sha256: str
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
        if len(self.frames) < 2:
            raise ValueError("Teacher state loop requires multiple causal frames")
        sequences = tuple(frame.body_state.sequence for frame in self.frames)
        expected = tuple(range(sequences[0], sequences[0] + len(sequences)))
        if sequences != expected:
            raise ValueError("Teacher state-loop sequence continuity drift")
        if len(self.run_sha256) != 64:
            raise ValueError("Teacher state loop requires deterministic hash")
        if self.raw_private_content_status != RAW_PRIVATE_CONTENT_EXCLUDED:
            raise ValueError("Teacher state loop cannot retain raw private content")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError(
                "Teacher state loop cannot establish phenomenal interpretation"
            )
        if self.action_authority != "NONE":
            raise ValueError("Teacher state loop cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError(
                "Teacher state loop must remain non-canonical and undeployed"
            )


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


def build_teacher_reference_baseline_state(
    binding: TeacherBodyRuntimeBinding,
    *,
    timestamp_ms: int = 0,
) -> TeacherIntegratedBodyState:
    if timestamp_ms < 0:
        raise ValueError("baseline timestamp cannot be negative")
    possess_teacher_body(binding)
    if binding.body_id != TEACHER_BODY_ID:
        raise ValueError("Teacher baseline requires exact Teacher body")

    observations = (
        TeacherBodyObservation("TACTILE_GENERAL", (0.0,), timestamp_ms),
        TeacherBodyObservation(
            "JOINT_POSITION",
            (0.0, 0.0, 0.0),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "VESTIBULAR_ORIENTATION",
            (1.0, 0.0, 0.0, 0.0),
            timestamp_ms,
        ),
        TeacherBodyObservation("CARDIOVASCULAR_STATE", (0.20,), timestamp_ms),
        TeacherBodyObservation("RESPIRATORY_STATE", (0.20,), timestamp_ms),
        TeacherBodyObservation("OXYGENATION_STATE", (0.80,), timestamp_ms),
        TeacherBodyObservation("CO2_BALANCE_STATE", (0.20,), timestamp_ms),
        TeacherBodyObservation(
            "AUTONOMIC_SYMPATHETIC_STATE",
            (0.20,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "AUTONOMIC_PARASYMPATHETIC_STATE",
            (0.70,),
            timestamp_ms,
        ),
        TeacherBodyObservation("ADRENAL_AXIS_STATE", (0.20,), timestamp_ms),
        TeacherBodyObservation(
            "ENDOCRINE_REFERENCE_STATE",
            (0.25,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "GONADAL_ENDOCRINE_REFERENCE",
            (0.25,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "GENITAL_SENSORY_AFFERENT_REFERENCE",
            (0.05,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "GENITAL_VASCULAR_STATE",
            (0.05,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "ERECTILE_REFLEX_STATE",
            (0.05,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "PELVIC_FLOOR_PROPRIOCEPTION",
            (0.10,),
            timestamp_ms,
        ),
        TeacherBodyObservation("DETUMESCENCE_STATE", (0.0,), timestamp_ms),
        TeacherBodyObservation("EMISSION_REFLEX_STATE", (0.0,), timestamp_ms),
        TeacherBodyObservation(
            "EJACULATORY_REFLEX_STATE",
            (0.0,),
            timestamp_ms,
        ),
    )
    return integrate_teacher_body_state(observations, sequence=0)


def build_teacher_reference_controller_state(
    binding: TeacherBodyRuntimeBinding,
    body_state: TeacherIntegratedBodyState,
) -> TeacherEmbodiedControllerState:
    possession = possess_teacher_body(binding)
    if body_state.sequence < 0 or body_state.timestamp_ms < 0:
        raise ValueError("Teacher controller requires valid body-state time")
    return TeacherEmbodiedControllerState(
        controller_id=TEACHER_CONTROLLER_ID,
        runtime_id=possession.runtime_id,
        session_id=possession.session_id,
        body_id=possession.body_id,
        sequence=body_state.sequence,
        timestamp_ms=body_state.timestamp_ms,
        salience=0.0,
        activation=0.0,
        functional_motivation=0.0,
        inhibition=0.0,
        context_gate=False,
        phase="BASELINE_REFERENCE",
        source_body_state_sha256=body_state.body_state_sha256,
        previous_body_schema_feedback_sha256=None,
    )


def _phase_for_stimulus(stimulus: TeacherStimulusEnvelope) -> str:
    if stimulus.stimulus_class == "RECOVERY_REFERENCE":
        return "RECOVERY"
    if stimulus.stimulus_class == "BASELINE_REFERENCE":
        return "BASELINE"
    return "ACTIVATION"


def _functional_state_from_controller(
    controller_state: TeacherEmbodiedControllerState,
    stimulus: TeacherStimulusEnvelope,
) -> TeacherFunctionalEmbodiedState:
    phase = _phase_for_stimulus(stimulus)
    return TeacherFunctionalEmbodiedState(
        state_id=(
            f"{stimulus.stimulus_id}:{phase}:{controller_state.sequence}"
        ),
        stimulus_sha256=stimulus.fingerprint(),
        phase=phase,
        functional_arousal=controller_state.activation,
        functional_motivation=controller_state.functional_motivation,
        sexual_context_gate=controller_state.context_gate,
        inhibition=controller_state.inhibition,
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
        if observation.channel_id in selected and observation.values:
            values.append((observation.channel_id, observation.values[0]))
    return tuple(sorted(values))


def _retime_observations(
    observations: tuple[TeacherBodyObservation, ...],
    *,
    timestamp_ms: int,
) -> tuple[TeacherBodyObservation, ...]:
    return tuple(
        TeacherBodyObservation(
            channel_id=item.channel_id,
            values=item.values,
            timestamp_ms=timestamp_ms,
            confidence=item.confidence,
        )
        for item in observations
    )


def _feedback_hash(feedback: TeacherAllostaticForecast) -> str:
    return _canonical_hash(feedback.to_dict())


def _build_report(
    *,
    binding: TeacherBodyRuntimeBinding,
    stimulus: TeacherStimulusEnvelope,
    functional_state: TeacherFunctionalEmbodiedState,
    body_state: TeacherIntegratedBodyState,
    bound: TeacherBoundBodyState,
) -> TeacherBodyStateReport:
    return TeacherBodyStateReport(
        report_id=(
            f"TEACHER-STATE-REPORT:{binding.session_id}:{body_state.sequence}"
        ),
        phase=functional_state.phase,
        body_id=binding.body_id,
        stimulus_class=stimulus.stimulus_class,
        stimulus_sha256=stimulus.fingerprint(),
        functional_state_sha256=functional_state.fingerprint(),
        body_state_sha256=body_state.body_state_sha256,
        bound_state_sha256=bound.bound_state_sha256,
        observed_reference_channels=_selected_channel_values(body_state),
    )


def _build_baseline_frame(
    binding: TeacherBodyRuntimeBinding,
    body_state: TeacherIntegratedBodyState,
    controller_state: TeacherEmbodiedControllerState,
    stimulus: TeacherStimulusEnvelope,
) -> TeacherStateLoopFrame:
    bound = bind_teacher_integrated_body_state(binding, body_state)
    motivation = build_teacher_controller_motivation(
        controller_state,
        body_state,
    )
    feedback = build_teacher_body_schema_feedback(
        controller_state,
        body_state,
        lead_time_ms=REFERENCE_DT_MS,
    )
    functional_state = _functional_state_from_controller(
        controller_state,
        stimulus,
    )
    return TeacherStateLoopFrame(
        controller_state=controller_state,
        functional_state=functional_state,
        motivation=motivation,
        executed_transition=None,
        body_state=body_state,
        bound_body_state=bound,
        body_schema_feedback=feedback,
        body_schema_feedback_sha256=_feedback_hash(feedback),
        report=_build_report(
            binding=binding,
            stimulus=stimulus,
            functional_state=functional_state,
            body_state=body_state,
            bound=bound,
        ),
    )


def advance_teacher_embodied_tick(
    binding: TeacherBodyRuntimeBinding,
    *,
    previous_controller_state: TeacherEmbodiedControllerState,
    previous_body_state: TeacherIntegratedBodyState,
    stimulus: TeacherStimulusEnvelope,
) -> TeacherStateLoopFrame:
    possession = possess_teacher_body(binding)
    if previous_controller_state.runtime_id != possession.runtime_id:
        raise ValueError("Teacher controller runtime binding drift")
    if previous_controller_state.session_id != possession.session_id:
        raise ValueError("Teacher controller session binding drift")
    if previous_controller_state.body_id != possession.body_id:
        raise ValueError("Teacher controller body binding drift")
    if previous_controller_state.sequence != previous_body_state.sequence:
        raise ValueError("previous controller/body sequence drift")
    if previous_controller_state.timestamp_ms != previous_body_state.timestamp_ms:
        raise ValueError("previous controller/body timestamp drift")

    clock = TeacherEmbodimentClock(
        sequence=previous_body_state.sequence + 1,
        timestamp_ms=previous_body_state.timestamp_ms + REFERENCE_DT_MS,
    )
    controller_input = TeacherControllerInput(
        salience=stimulus.salience,
        context_gate=stimulus.sexual_context_gate,
        inhibition=stimulus.inhibition,
        functional_motivation=stimulus.functional_motivation,
    )
    controller_state = advance_teacher_controller(
        previous_controller_state,
        controller_input,
        previous_body_state,
        clock,
    )
    motivation = build_teacher_controller_motivation(
        controller_state,
        previous_body_state,
    )
    intent = select_teacher_transition_intent(
        controller_state,
        previous_body_state,
    )
    executed = execute_teacher_transition(
        previous_body_state,
        controller_state,
        motivation,
        intent,
        clock,
    )
    observed = _retime_observations(
        executed.observations,
        timestamp_ms=clock.timestamp_ms,
    )
    body_state = integrate_teacher_body_state(
        observed,
        sequence=clock.sequence,
    )
    bound = bind_teacher_integrated_body_state(binding, body_state)
    feedback = build_teacher_body_schema_feedback(
        controller_state,
        body_state,
        lead_time_ms=REFERENCE_DT_MS,
    )
    functional_state = _functional_state_from_controller(
        controller_state,
        stimulus,
    )
    report = _build_report(
        binding=binding,
        stimulus=stimulus,
        functional_state=functional_state,
        body_state=body_state,
        bound=bound,
    )
    return TeacherStateLoopFrame(
        controller_state=controller_state,
        functional_state=functional_state,
        motivation=motivation,
        executed_transition=executed,
        body_state=body_state,
        bound_body_state=bound,
        body_schema_feedback=feedback,
        body_schema_feedback_sha256=_feedback_hash(feedback),
        report=report,
    )


def _body_scalar(
    body_state: TeacherIntegratedBodyState,
    channel_id: str,
) -> float:
    for observation in body_state.observations:
        if observation.channel_id == channel_id:
            if len(observation.values) != 1:
                raise ValueError(
                    f"Teacher reference loop requires scalar {channel_id}"
                )
            return observation.values[0]
    raise ValueError(f"Teacher reference loop missing {channel_id}")


def _reference_recovered(frame: TeacherStateLoopFrame) -> bool:
    return (
        frame.controller_state.activation < 0.05
        and frame.controller_state.functional_motivation < 0.05
        and _body_scalar(frame.body_state, "GENITAL_VASCULAR_STATE") <= 0.15
        and _body_scalar(frame.body_state, "ERECTILE_REFLEX_STATE") <= 0.15
    )


def run_teacher_reference_state_loop(
    binding: TeacherBodyRuntimeBinding,
    *,
    activation_stimulus: TeacherStimulusEnvelope,
    start_timestamp_ms: int = 0,
) -> TeacherStateLoopRun:
    if start_timestamp_ms < 0:
        raise ValueError("start_timestamp_ms cannot be negative")
    if activation_stimulus.stimulus_class != (
        "HIGH_SALIENCE_INTIMATE_REFERENCE"
    ):
        raise ValueError(
            "reference state loop requires high-salience intimate stimulus class"
        )

    baseline_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{activation_stimulus.stimulus_id}:baseline",
        stimulus_class="BASELINE_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=0.0,
    )
    recovery_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{activation_stimulus.stimulus_id}:recovery",
        stimulus_class="RECOVERY_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=0.0,
    )

    baseline_body = build_teacher_reference_baseline_state(
        binding,
        timestamp_ms=start_timestamp_ms,
    )
    controller = build_teacher_reference_controller_state(
        binding,
        baseline_body,
    )
    baseline_frame = _build_baseline_frame(
        binding,
        baseline_body,
        controller,
        baseline_stimulus,
    )
    frames: list[TeacherStateLoopFrame] = [baseline_frame]

    current_body = baseline_body
    current_controller = replace(
        controller,
        previous_body_schema_feedback_sha256=(
            baseline_frame.body_schema_feedback_sha256
        ),
    )

    for _ in range(8):
        frame = advance_teacher_embodied_tick(
            binding,
            previous_controller_state=current_controller,
            previous_body_state=current_body,
            stimulus=activation_stimulus,
        )
        frames.append(frame)
        current_body = frame.body_state
        current_controller = replace(
            frame.controller_state,
            previous_body_schema_feedback_sha256=(
                frame.body_schema_feedback_sha256
            ),
        )

    for _ in range(60):
        frame = advance_teacher_embodied_tick(
            binding,
            previous_controller_state=current_controller,
            previous_body_state=current_body,
            stimulus=recovery_stimulus,
        )
        frames.append(frame)
        current_body = frame.body_state
        current_controller = replace(
            frame.controller_state,
            previous_body_schema_feedback_sha256=(
                frame.body_schema_feedback_sha256
            ),
        )
        if _reference_recovered(frame):
            break

    trajectory = build_teacher_within_session_trajectory(
        f"TEACHER-STATE-TRAJECTORY:{binding.session_id}"
    )
    for frame in frames:
        trajectory = append_teacher_body_state(
            trajectory,
            frame.body_state,
        )

    payload = {
        "runtime_id": binding.runtime_id,
        "session_id": binding.session_id,
        "body_id": binding.body_id,
        "trajectory_sha256": trajectory.trajectory_sha256,
        "controller_sha256": frames[-1].controller_state.fingerprint(),
        "frame_reports": [frame.report.to_dict() for frame in frames],
        "transition_sha256": [
            (
                frame.executed_transition.transition_sha256
                if frame.executed_transition is not None
                else None
            )
            for frame in frames
        ],
    }
    return TeacherStateLoopRun(
        runtime_id=binding.runtime_id,
        session_id=binding.session_id,
        body_id=binding.body_id,
        trajectory=trajectory,
        frames=tuple(frames),
        run_sha256=_canonical_hash(payload),
    )
