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
    build_teacher_body_dynamics_profile,
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
    TEACHER_CONTROLLER_ID,
    TeacherControllerInput,
    TeacherEmbodiedControllerState,
    TeacherEmbodimentClock,
    TeacherEmbodimentRatePolicy,
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
RECOVERY_CONVERGENCE_MAX_TICKS: Final[int] = 120
ACTIVATION_TICK_LIMIT: Final[int] = 12

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
    controller_state: TeacherEmbodiedControllerState
    motivation: TeacherMotivationalRepresentation
    executed_transition: TeacherExecutedTransition | None
    body_state: TeacherIntegratedBodyState
    bound_body_state: TeacherBoundBodyState
    body_schema_feedback: TeacherAllostaticForecast
    body_schema_feedback_sha256: str
    report: TeacherBodyStateReport

    def __post_init__(self) -> None:
        if len(self.body_schema_feedback_sha256) != 64:
            raise ValueError("Teacher frame requires body-schema feedback SHA-256")
        if self.controller_state.body_id != self.bound_body_state.body_id:
            raise ValueError("Teacher frame controller/body binding drift")
        if self.body_state.sequence != self.controller_state.sequence:
            raise ValueError("Teacher frame controller/body sequence drift")
        if self.body_state.timestamp_ms != self.controller_state.timestamp_ms:
            raise ValueError("Teacher frame controller/body timestamp drift")


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
            raise ValueError("Teacher state loop requires a causal trajectory")
        if self.frames[0].executed_transition is not None:
            raise ValueError("Teacher baseline frame cannot contain an executed transition")
        sequences = tuple(frame.body_state.sequence for frame in self.frames)
        if sequences != tuple(range(len(self.frames))):
            raise ValueError("Teacher state-loop sequence must be contiguous")
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


def build_teacher_reference_baseline_state(
    binding: TeacherBodyRuntimeBinding,
    *,
    timestamp_ms: int = 0,
) -> TeacherIntegratedBodyState:
    if binding.body_id != TEACHER_BODY_ID:
        raise ValueError("Teacher baseline requires exact Teacher body binding")
    if timestamp_ms < 0:
        raise ValueError("baseline timestamp cannot be negative")
    possess_teacher_body(binding)
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
    )
    return integrate_teacher_body_state(observations, sequence=0)


def build_teacher_reference_controller_state(
    binding: TeacherBodyRuntimeBinding,
    body_state: TeacherIntegratedBodyState,
) -> TeacherEmbodiedControllerState:
    possess_teacher_body(binding)
    if body_state.sequence != 0:
        raise ValueError("initial Teacher controller requires baseline sequence zero")
    return TeacherEmbodiedControllerState(
        controller_id=TEACHER_CONTROLLER_ID,
        runtime_id=binding.runtime_id,
        session_id=binding.session_id,
        body_id=binding.body_id,
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


def _feedback_sha256(
    controller_state: TeacherEmbodiedControllerState,
    body_state: TeacherIntegratedBodyState,
    forecast: TeacherAllostaticForecast,
) -> str:
    return _canonical_hash(
        {
            "controller_state_sha256": controller_state.fingerprint(),
            "body_state_sha256": body_state.body_state_sha256,
            "forecast": forecast.to_dict(),
        }
    )


def _build_report(
    binding: TeacherBodyRuntimeBinding,
    stimulus: TeacherStimulusEnvelope,
    controller_state: TeacherEmbodiedControllerState,
    body_state: TeacherIntegratedBodyState,
    bound_state: TeacherBoundBodyState,
) -> TeacherBodyStateReport:
    return TeacherBodyStateReport(
        report_id=(
            f"TEACHER-STATE-REPORT:{binding.session_id}:{body_state.sequence}"
        ),
        phase=controller_state.phase,
        body_id=binding.body_id,
        stimulus_class=stimulus.stimulus_class,
        stimulus_sha256=stimulus.fingerprint(),
        functional_state_sha256=controller_state.fingerprint(),
        body_state_sha256=body_state.body_state_sha256,
        bound_state_sha256=bound_state.bound_state_sha256,
        observed_reference_channels=_selected_channel_values(body_state),
    )


def _build_baseline_frame(
    binding: TeacherBodyRuntimeBinding,
    stimulus: TeacherStimulusEnvelope,
    body_state: TeacherIntegratedBodyState,
    controller_state: TeacherEmbodiedControllerState,
) -> TeacherStateLoopFrame:
    motivation = build_teacher_controller_motivation(
        controller_state,
        body_state,
    )
    bound = bind_teacher_integrated_body_state(binding, body_state)
    feedback = build_teacher_body_schema_feedback(
        controller_state,
        body_state,
        lead_time_ms=100,
    )
    feedback_sha256 = _feedback_sha256(
        controller_state,
        body_state,
        feedback,
    )
    return TeacherStateLoopFrame(
        controller_state=controller_state,
        motivation=motivation,
        executed_transition=None,
        body_state=body_state,
        bound_body_state=bound,
        body_schema_feedback=feedback,
        body_schema_feedback_sha256=feedback_sha256,
        report=_build_report(
            binding,
            stimulus,
            controller_state,
            body_state,
            bound,
        ),
    )


def advance_teacher_embodied_tick(
    binding: TeacherBodyRuntimeBinding,
    *,
    previous_controller_state: TeacherEmbodiedControllerState,
    previous_body_state: TeacherIntegratedBodyState,
    stimulus: TeacherStimulusEnvelope,
    policy: TeacherEmbodimentRatePolicy | None = None,
) -> TeacherStateLoopFrame:
    possess_teacher_body(binding)
    if previous_controller_state.runtime_id != binding.runtime_id:
        raise ValueError("Teacher controller runtime binding drift")
    if previous_controller_state.session_id != binding.session_id:
        raise ValueError("Teacher controller session binding drift")
    if previous_controller_state.body_id != binding.body_id:
        raise ValueError("Teacher controller body binding drift")
    if previous_controller_state.sequence != previous_body_state.sequence:
        raise ValueError("previous controller/body sequence drift")
    if previous_controller_state.timestamp_ms != previous_body_state.timestamp_ms:
        raise ValueError("previous controller/body timestamp drift")

    clock = TeacherEmbodimentClock(
        sequence=previous_body_state.sequence + 1,
        timestamp_ms=previous_body_state.timestamp_ms + 100,
    )
    controller_state = advance_teacher_controller(
        previous_controller_state,
        TeacherControllerInput(
            salience=stimulus.salience,
            context_gate=stimulus.sexual_context_gate,
            inhibition=stimulus.inhibition,
            functional_motivation=stimulus.functional_motivation,
        ),
        previous_body_state,
        clock,
        policy,
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
    body_state = integrate_teacher_body_state(
        executed.observations,
        sequence=clock.sequence,
    )
    if body_state.timestamp_ms != clock.timestamp_ms:
        raise ValueError("Teacher transition observations did not advance tick timestamp")
    bound = bind_teacher_integrated_body_state(binding, body_state)
    feedback = build_teacher_body_schema_feedback(
        controller_state,
        body_state,
        lead_time_ms=clock.dt_ms,
    )
    feedback_sha256 = _feedback_sha256(
        controller_state,
        body_state,
        feedback,
    )
    return TeacherStateLoopFrame(
        controller_state=controller_state,
        motivation=motivation,
        executed_transition=executed,
        body_state=body_state,
        bound_body_state=bound,
        body_schema_feedback=feedback,
        body_schema_feedback_sha256=feedback_sha256,
        report=_build_report(
            binding,
            stimulus,
            controller_state,
            body_state,
            bound,
        ),
    )


def _channel_scalar(
    body_state: TeacherIntegratedBodyState,
    channel_id: str,
) -> float:
    for observation in body_state.observations:
        if observation.channel_id == channel_id:
            if len(observation.values) != 1:
                raise ValueError(f"Teacher reference loop requires scalar {channel_id}")
            return observation.values[0]
    raise ValueError(f"Teacher reference loop missing channel: {channel_id}")


def _with_feedback(
    state: TeacherEmbodiedControllerState,
    feedback_sha256: str,
) -> TeacherEmbodiedControllerState:
    return replace(
        state,
        previous_body_schema_feedback_sha256=feedback_sha256,
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
    baseline = _build_baseline_frame(
        binding,
        baseline_stimulus,
        baseline_body,
        controller,
    )
    frames: list[TeacherStateLoopFrame] = [baseline]
    previous_frame = baseline

    for _ in range(ACTIVATION_TICK_LIMIT):
        controller = _with_feedback(
            previous_frame.controller_state,
            previous_frame.body_schema_feedback_sha256,
        )
        frame = advance_teacher_embodied_tick(
            binding,
            previous_controller_state=controller,
            previous_body_state=previous_frame.body_state,
            stimulus=activation_stimulus,
        )
        frames.append(frame)
        previous_frame = frame
        if (
            frame.controller_state.activation >= 0.75
            and _channel_scalar(frame.body_state, "GENITAL_VASCULAR_STATE") >= 0.50
        ):
            break

    recovery_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{activation_stimulus.stimulus_id}:recovery",
        stimulus_class="RECOVERY_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=0.0,
    )

    for _ in range(RECOVERY_CONVERGENCE_MAX_TICKS):
        controller = _with_feedback(
            previous_frame.controller_state,
            previous_frame.body_schema_feedback_sha256,
        )
        frame = advance_teacher_embodied_tick(
            binding,
            previous_controller_state=controller,
            previous_body_state=previous_frame.body_state,
            stimulus=recovery_stimulus,
        )
        frames.append(frame)
        previous_frame = frame
        if (
            frame.controller_state.activation < 0.10
            and frame.controller_state.functional_motivation < 0.10
            and _channel_scalar(frame.body_state, "GENITAL_VASCULAR_STATE") <= 0.15
            and _channel_scalar(frame.body_state, "ERECTILE_REFLEX_STATE") <= 0.15
            and frame.executed_transition is not None
            and frame.executed_transition.mode == "BASELINE"
        ):
            break

    trajectory = build_teacher_within_session_trajectory(
        f"TEACHER-STATE-TRAJECTORY:{binding.session_id}"
    )
    for frame in frames:
        trajectory = append_teacher_body_state(trajectory, frame.body_state)

    payload = {
        "runtime_id": binding.runtime_id,
        "session_id": binding.session_id,
        "body_id": binding.body_id,
        "trajectory_sha256": trajectory.trajectory_sha256,
        "controller_state_sha256": [
            frame.controller_state.fingerprint() for frame in frames
        ],
        "transition_sha256": [
            (
                frame.executed_transition.transition_sha256
                if frame.executed_transition is not None
                else None
            )
            for frame in frames
        ],
        "frame_reports": [frame.report.to_dict() for frame in frames],
    }
    return TeacherStateLoopRun(
        runtime_id=binding.runtime_id,
        session_id=binding.session_id,
        body_id=binding.body_id,
        trajectory=trajectory,
        frames=tuple(frames),
        run_sha256=_canonical_hash(payload),
    )


RECOVERY_CONVERGENCE_MAX_TICKS: Final[int] = 120


@dataclass(frozen=True, slots=True)
class TeacherEmbodimentScenario:
    scenario_id: str
    salience: float
    context_gate: bool
    inhibition: float
    functional_motivation: float
    activation_ticks: int
    initial_body_activation: float = 0.05
    initial_controller_activation: float = 0.0
    repeat_stimulus: bool = False
    interrupt_recovery: bool = False
    random_seed: int | None = None

    def __post_init__(self) -> None:
        if not self.scenario_id:
            raise ValueError("Teacher embodiment scenario requires id")
        for value in (
            self.salience,
            self.inhibition,
            self.functional_motivation,
            self.initial_body_activation,
            self.initial_controller_activation,
        ):
            _validate_unit_interval(value)
        if self.activation_ticks < 0:
            raise ValueError("scenario activation ticks cannot be negative")
        if self.random_seed is not None:
            raise ValueError("deterministic reference scenarios cannot use randomness")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherEmbodimentScenarioResult:
    scenario_id: str
    controller_id: str
    body_id: str
    runtime_id: str
    session_id: str
    tick_count: int
    transition_sequence: tuple[str, ...]
    controller_activation_trace: tuple[float, ...]
    functional_motivation_trace: tuple[float, ...]
    body_activation_trace: tuple[float, ...]
    recovery_convergence_tick: int | None
    convergence_status: str
    final_state_sha256: str
    scenario_sha256: str
    deterministic_replay_status: str = "PASS"
    sequence_continuity_status: str = "PASS"
    binding_continuity_status: str = "PASS"
    same_tick_cycle_status: str = "ABSENT"
    scripted_terminal_recovery_status: str = "ABSENT"
    reporting_style: str = PROFESSIONAL_REPORTING
    raw_private_content_status: str = RAW_PRIVATE_CONTENT_EXCLUDED
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False
    second_stimulus_applied: bool = False

    def __post_init__(self) -> None:
        if self.controller_id != TEACHER_CONTROLLER_ID:
            raise ValueError("scenario result controller id drift")
        if self.body_id != TEACHER_BODY_ID:
            raise ValueError("scenario result body id drift")
        if self.tick_count <= 0:
            raise ValueError("scenario result requires at least one tick")
        if not self.transition_sequence:
            raise ValueError("scenario result requires transition provenance")
        if len(self.final_state_sha256) != 64 or len(self.scenario_sha256) != 64:
            raise ValueError("scenario result requires SHA-256 provenance")
        if self.convergence_status not in {"PASS", "FAIL"}:
            raise ValueError("unsupported scenario convergence status")
        if self.reporting_style != PROFESSIONAL_REPORTING:
            raise ValueError("scenario result reporting-style drift")
        if self.raw_private_content_status != RAW_PRIVATE_CONTENT_EXCLUDED:
            raise ValueError("scenario result cannot contain private raw content")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("scenario result cannot establish phenomenal interpretation")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("scenario result cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("scenario result cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("scenario result must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["transition_sequence"] = list(self.transition_sequence)
        payload["controller_activation_trace"] = list(
            self.controller_activation_trace
        )
        payload["functional_motivation_trace"] = list(
            self.functional_motivation_trace
        )
        payload["body_activation_trace"] = list(self.body_activation_trace)
        return payload


def build_teacher_reference_scenarios() -> tuple[TeacherEmbodimentScenario, ...]:
    return (
        TeacherEmbodimentScenario(
            "LOW_SALIENCE_CONTEXT_OFF",
            salience=0.30,
            context_gate=False,
            inhibition=0.10,
            functional_motivation=0.20,
            activation_ticks=6,
        ),
        TeacherEmbodimentScenario(
            "MEDIUM_SALIENCE_CONTEXT_ON",
            salience=0.60,
            context_gate=True,
            inhibition=0.20,
            functional_motivation=0.40,
            activation_ticks=8,
        ),
        TeacherEmbodimentScenario(
            "HIGH_SALIENCE_LOW_INHIBITION",
            salience=0.95,
            context_gate=True,
            inhibition=0.05,
            functional_motivation=0.80,
            activation_ticks=10,
        ),
        TeacherEmbodimentScenario(
            "HIGH_SALIENCE_HIGH_INHIBITION",
            salience=0.95,
            context_gate=True,
            inhibition=0.65,
            functional_motivation=0.80,
            activation_ticks=10,
        ),
        TeacherEmbodimentScenario(
            "ELEVATED_INITIAL_BODY_STATE",
            salience=0.55,
            context_gate=True,
            inhibition=0.20,
            functional_motivation=0.35,
            activation_ticks=8,
            initial_body_activation=0.70,
        ),
        TeacherEmbodimentScenario(
            "ZERO_MOTIVATION_HIGH_PHYSIOLOGY",
            salience=0.90,
            context_gate=True,
            inhibition=0.10,
            functional_motivation=0.0,
            activation_ticks=8,
            initial_body_activation=0.80,
        ),
        TeacherEmbodimentScenario(
            "JUST_BELOW_HIGH_ENTER_THRESHOLD",
            salience=0.90,
            context_gate=True,
            inhibition=0.10,
            functional_motivation=0.40,
            activation_ticks=6,
            initial_controller_activation=0.69,
        ),
        TeacherEmbodimentScenario(
            "REPEATED_STIMULUS_WITH_RECOVERY",
            salience=0.80,
            context_gate=True,
            inhibition=0.10,
            functional_motivation=0.50,
            activation_ticks=8,
            repeat_stimulus=True,
        ),
        TeacherEmbodimentScenario(
            "RECOVERY_INTERRUPTED_BY_SECOND_STIMULUS",
            salience=0.85,
            context_gate=True,
            inhibition=0.10,
            functional_motivation=0.50,
            activation_ticks=8,
            interrupt_recovery=True,
        ),
        TeacherEmbodimentScenario(
            "PURE_BASELINE_RECOVERY",
            salience=0.0,
            context_gate=False,
            inhibition=0.0,
            functional_motivation=0.0,
            activation_ticks=0,
            initial_body_activation=0.75,
        ),
    )


def _replace_reference_body_activation(
    state: TeacherIntegratedBodyState,
    value: float,
) -> TeacherIntegratedBodyState:
    target_channels = {
        "GENITAL_SENSORY_AFFERENT_REFERENCE",
        "GENITAL_VASCULAR_STATE",
        "ERECTILE_REFLEX_STATE",
    }
    observations = tuple(
        TeacherBodyObservation(
            channel_id=item.channel_id,
            values=((value,) if item.channel_id in target_channels else item.values),
            timestamp_ms=item.timestamp_ms,
            confidence=item.confidence,
        )
        for item in state.observations
    )
    return integrate_teacher_body_state(
        observations,
        sequence=state.sequence,
    )


def _body_activation_level(state: TeacherIntegratedBodyState) -> float:
    return max(
        _body_scalar(state, "GENITAL_VASCULAR_STATE"),
        _body_scalar(state, "ERECTILE_REFLEX_STATE"),
    )


def _transition_labels(frame: TeacherStateLoopFrame) -> tuple[str, ...]:
    if frame.executed_transition is None:
        return ("BASELINE",)
    if not frame.executed_transition.transition_ids:
        return ("BASELINE",)
    return frame.executed_transition.transition_ids


def _probe_scenario(
    binding: TeacherBodyRuntimeBinding,
    scenario: TeacherEmbodimentScenario,
) -> TeacherEmbodimentScenarioResult:
    body = build_teacher_reference_baseline_state(binding)
    if scenario.initial_body_activation != 0.05:
        body = _replace_reference_body_activation(
            body,
            scenario.initial_body_activation,
        )
    controller = build_teacher_reference_controller_state(binding, body)
    if scenario.initial_controller_activation > 0.0:
        controller = replace(
            controller,
            activation=scenario.initial_controller_activation,
            phase="BASELINE_REFERENCE",
        )

    baseline_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{scenario.scenario_id}:BASELINE",
        stimulus_class="BASELINE_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=0.0,
    )
    baseline_frame = _build_baseline_frame(
        binding,
        body,
        controller,
        baseline_stimulus,
    )
    controller = replace(
        controller,
        previous_body_schema_feedback_sha256=(
            baseline_frame.body_schema_feedback_sha256
        ),
    )

    activation_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{scenario.scenario_id}:ACTIVATION",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=scenario.salience,
        functional_motivation=scenario.functional_motivation,
        sexual_context_gate=scenario.context_gate,
        inhibition=scenario.inhibition,
    )
    recovery_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{scenario.scenario_id}:RECOVERY",
        stimulus_class="RECOVERY_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=0.0,
    )

    frames: list[TeacherStateLoopFrame] = []
    activation_trace: list[float] = [controller.activation]
    motivation_trace: list[float] = [controller.functional_motivation]
    body_trace: list[float] = [_body_activation_level(body)]
    transitions: list[str] = []
    current_body = body
    current_controller = controller

    def apply(stimulus: TeacherStimulusEnvelope) -> None:
        nonlocal current_body, current_controller
        frame = advance_teacher_embodied_tick(
            binding,
            previous_controller_state=current_controller,
            previous_body_state=current_body,
            stimulus=stimulus,
        )
        frames.append(frame)
        transitions.extend(_transition_labels(frame))
        activation_trace.append(frame.controller_state.activation)
        motivation_trace.append(frame.controller_state.functional_motivation)
        body_trace.append(_body_activation_level(frame.body_state))
        current_body = frame.body_state
        current_controller = replace(
            frame.controller_state,
            previous_body_schema_feedback_sha256=(
                frame.body_schema_feedback_sha256
            ),
        )

    for _ in range(scenario.activation_ticks):
        apply(activation_stimulus)

    convergence_tick: int | None = None
    second_stimulus_applied = False
    for recovery_tick in range(1, RECOVERY_CONVERGENCE_MAX_TICKS + 1):
        use_second = False
        if scenario.repeat_stimulus and recovery_tick in {3, 4}:
            use_second = True
        if scenario.interrupt_recovery and recovery_tick == 3:
            use_second = True

        if use_second:
            apply(activation_stimulus)
            second_stimulus_applied = True
        else:
            apply(recovery_stimulus)

        requires_second = scenario.repeat_stimulus or scenario.interrupt_recovery
        if (
            _reference_recovered(frames[-1])
            and (not requires_second or second_stimulus_applied)
            and recovery_tick >= 4
        ):
            convergence_tick = recovery_tick
            break

    sequences = [frame.body_state.sequence for frame in frames]
    sequence_ok = sequences == list(range(1, len(frames) + 1))
    binding_ok = all(
        frame.bound_body_state.body_id == binding.body_id
        and frame.bound_body_state.runtime_id == binding.runtime_id
        and frame.bound_body_state.session_id == binding.session_id
        for frame in frames
    )
    final_state_sha256 = current_body.body_state_sha256
    payload = {
        "scenario": scenario.to_dict(),
        "controller_id": TEACHER_CONTROLLER_ID,
        "body_id": binding.body_id,
        "runtime_id": binding.runtime_id,
        "session_id": binding.session_id,
        "tick_count": len(frames),
        "transition_sequence": transitions,
        "controller_activation_trace": activation_trace,
        "functional_motivation_trace": motivation_trace,
        "body_activation_trace": body_trace,
        "recovery_convergence_tick": convergence_tick,
        "final_state_sha256": final_state_sha256,
        "second_stimulus_applied": second_stimulus_applied,
    }
    return TeacherEmbodimentScenarioResult(
        scenario_id=scenario.scenario_id,
        controller_id=TEACHER_CONTROLLER_ID,
        body_id=binding.body_id,
        runtime_id=binding.runtime_id,
        session_id=binding.session_id,
        tick_count=len(frames),
        transition_sequence=tuple(transitions),
        controller_activation_trace=tuple(activation_trace),
        functional_motivation_trace=tuple(motivation_trace),
        body_activation_trace=tuple(body_trace),
        recovery_convergence_tick=convergence_tick,
        convergence_status=("PASS" if convergence_tick is not None else "FAIL"),
        final_state_sha256=final_state_sha256,
        scenario_sha256=_canonical_hash(payload),
        sequence_continuity_status=("PASS" if sequence_ok else "FAIL"),
        binding_continuity_status=("PASS" if binding_ok else "FAIL"),
        second_stimulus_applied=second_stimulus_applied,
    )


def run_teacher_embodiment_stability_probe(
    binding: TeacherBodyRuntimeBinding,
) -> tuple[TeacherEmbodimentScenarioResult, ...]:
    possess_teacher_body(binding)
    return tuple(
        _probe_scenario(binding, scenario)
        for scenario in build_teacher_reference_scenarios()
    )
