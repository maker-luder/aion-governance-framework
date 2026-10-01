from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final

from .teacher_body_dynamics import (
    TeacherBodyDynamicsProfile,
    TeacherBodyObservation,
    TeacherIntegratedBodyState,
    TeacherMotivationalRepresentation,
    TeacherWithinSessionTrajectory,
    append_teacher_body_state,
    build_teacher_body_dynamics_profile as _build_teacher_body_dynamics_profile,
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
    fingerprint_teacher_body_schema_feedback,
    possess_teacher_body,
)
from .teacher_high_salience_coupling import (
    TeacherHighSaliencePhaseState,
    TeacherHighSalienceRuntimeIntent,
    TeacherReproductiveEventGate,
    build_teacher_high_salience_baseline_phase,
    coordinate_teacher_high_salience_runtime,
    resolve_teacher_high_salience_phase,
)
from .teacher_intimate_integration import (
    TeacherIntimateIntegrationState,
    TeacherOrgasmReferenceGate,
    integrate_teacher_intimate_reference,
)
from .teacher_transition_executor import (
    TeacherExecutedTransition,
    execute_teacher_high_salience_transition,
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


def build_teacher_body_dynamics_profile() -> TeacherBodyDynamicsProfile:
    return _build_teacher_body_dynamics_profile()


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
    high_salience_phase_state: TeacherHighSaliencePhaseState
    high_salience_runtime_intent: TeacherHighSalienceRuntimeIntent
    intimate_integration_state: TeacherIntimateIntegrationState
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
        if self.high_salience_phase_state.sequence != self.controller_state.sequence:
            raise ValueError("Teacher frame phase/controller sequence drift")
        if self.high_salience_runtime_intent.phase != self.high_salience_phase_state.phase:
            raise ValueError("Teacher frame phase/runtime-intent drift")
        if (
            self.high_salience_runtime_intent.source_controller_sha256
            != self.controller_state.fingerprint()
        ):
            raise ValueError("Teacher frame runtime-intent/controller hash drift")
        if (
            self.intimate_integration_state.source_phase
            != self.high_salience_phase_state.phase
        ):
            raise ValueError("Teacher frame intimate integration/phase drift")
        if (
            self.intimate_integration_state.functional_desire.source_controller_sha256
            != self.controller_state.fingerprint()
        ):
            raise ValueError("Teacher frame intimate integration/controller hash drift")
        if (
            self.intimate_integration_state.systemic_arousal.source_body_state_sha256
            != self.body_state.body_state_sha256
        ):
            raise ValueError("Teacher frame systemic observation/body hash drift")
        if (
            self.intimate_integration_state.endocrine_observation.source_body_state_sha256
            != self.body_state.body_state_sha256
        ):
            raise ValueError("Teacher frame endocrine observation/body hash drift")
        if (
            self.intimate_integration_state.orgasm_reference.source_body_state_sha256
            != self.body_state.body_state_sha256
        ):
            raise ValueError("Teacher frame orgasm reference/body hash drift")
        if self.executed_transition is None:
            if self.high_salience_runtime_intent.transition_ids:
                raise ValueError("Teacher baseline frame cannot carry transition intent")
        elif (
            self.executed_transition.transition_ids
            != self.high_salience_runtime_intent.transition_ids
        ):
            raise ValueError("Teacher frame intent/execution transition drift")


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
        TeacherBodyObservation("EMISSION_REFLEX_STATE", (0.0,), timestamp_ms),
        TeacherBodyObservation(
            "SEMINAL_TRACT_TRANSPORT_STATE",
            (0.0,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "ACCESSORY_GLAND_SECRETION_STATE",
            (0.0,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
            (0.0,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE",
            (0.0,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "EJACULATORY_REFLEX_STATE",
            (0.0,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "EXPULSION_MOTOR_PATTERN_STATE",
            (0.0,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE",
            (0.0,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "ANTEGRADE_SEMINAL_FLOW_STATE",
            (0.0,),
            timestamp_ms,
        ),
        TeacherBodyObservation(
            "POST_EXPULSION_RECOVERY_STATE",
            (0.0,),
            timestamp_ms,
        ),
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
        "EMISSION_REFLEX_STATE",
        "SEMINAL_TRACT_TRANSPORT_STATE",
        "ACCESSORY_GLAND_SECRETION_STATE",
        "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
        "POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE",
        "EJACULATORY_REFLEX_STATE",
        "EXPULSION_MOTOR_PATTERN_STATE",
        "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE",
        "ANTEGRADE_SEMINAL_FLOW_STATE",
        "POST_EXPULSION_RECOVERY_STATE",
    }
    values: list[tuple[str, float]] = []
    for observation in body_state.observations:
        if observation.channel_id in selected:
            values.append((observation.channel_id, observation.values[0]))
    return tuple(sorted(values))


def _feedback_sha256(
    body_state: TeacherIntegratedBodyState,
    forecast: TeacherAllostaticForecast,
) -> str:
    return fingerprint_teacher_body_schema_feedback(
        body_state,
        forecast,
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
        body_state,
        feedback,
    )
    phase_state = build_teacher_high_salience_baseline_phase(body_state)
    runtime_intent = coordinate_teacher_high_salience_runtime(
        phase_state,
        controller_state,
        body_state,
    )
    intimate_integration_state = integrate_teacher_intimate_reference(
        controller_state,
        motivation,
        phase_state,
        body_state,
    )
    return TeacherStateLoopFrame(
        controller_state=controller_state,
        motivation=motivation,
        executed_transition=None,
        high_salience_phase_state=phase_state,
        high_salience_runtime_intent=runtime_intent,
        intimate_integration_state=intimate_integration_state,
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
    previous_phase_state: TeacherHighSaliencePhaseState | None = None,
    policy: TeacherEmbodimentRatePolicy | None = None,
    reproductive_event_gate: TeacherReproductiveEventGate | None = None,
    orgasm_reference_gate: TeacherOrgasmReferenceGate | None = None,
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
    previous_feedback: TeacherAllostaticForecast | None = None
    if previous_controller_state.previous_body_schema_feedback_sha256 is not None:
        previous_feedback = build_teacher_body_schema_feedback(
            previous_controller_state,
            previous_body_state,
            lead_time_ms=clock.dt_ms,
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
        body_schema_feedback=previous_feedback,
    )
    motivation = build_teacher_controller_motivation(
        controller_state,
        previous_body_state,
    )
    prior_phase = (
        previous_phase_state
        if previous_phase_state is not None
        else build_teacher_high_salience_baseline_phase(previous_body_state)
    )
    phase_state = resolve_teacher_high_salience_phase(
        prior_phase,
        controller_state,
        previous_body_state,
        reproductive_event_gate=reproductive_event_gate,
    )
    runtime_intent = coordinate_teacher_high_salience_runtime(
        phase_state,
        controller_state,
        previous_body_state,
        reproductive_event_gate=reproductive_event_gate,
    )
    executed = execute_teacher_high_salience_transition(
        previous_body_state,
        controller_state,
        motivation,
        runtime_intent,
        clock,
    )
    body_state = integrate_teacher_body_state(
        executed.observations,
        sequence=clock.sequence,
    )
    if body_state.timestamp_ms != clock.timestamp_ms:
        raise ValueError("Teacher transition observations did not advance tick timestamp")
    intimate_integration_state = integrate_teacher_intimate_reference(
        controller_state,
        motivation,
        phase_state,
        body_state,
        orgasm_reference_gate=orgasm_reference_gate,
    )
    bound = bind_teacher_integrated_body_state(binding, body_state)
    feedback = build_teacher_body_schema_feedback(
        controller_state,
        body_state,
        lead_time_ms=clock.dt_ms,
    )
    feedback_sha256 = _feedback_sha256(
        body_state,
        feedback,
    )
    return TeacherStateLoopFrame(
        controller_state=controller_state,
        motivation=motivation,
        executed_transition=executed,
        high_salience_phase_state=phase_state,
        high_salience_runtime_intent=runtime_intent,
        intimate_integration_state=intimate_integration_state,
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
            previous_phase_state=previous_frame.high_salience_phase_state,
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
            previous_phase_state=previous_frame.high_salience_phase_state,
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
        "intimate_integration_sha256": [
            frame.intimate_integration_state.state_sha256 for frame in frames
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


@dataclass(frozen=True, slots=True)
class TeacherEmbodimentScenarioSegment:
    segment_id: str
    ticks: int
    stimulus_class: str
    salience: float
    functional_motivation: float
    context_gate: bool
    inhibition: float

    def __post_init__(self) -> None:
        if not self.segment_id or self.ticks <= 0:
            raise ValueError("Teacher scenario segment requires identity and positive ticks")
        if self.stimulus_class not in ALLOWED_STIMULUS_CLASSES:
            raise ValueError("Teacher scenario segment uses unsupported stimulus class")
        for value in (
            self.salience,
            self.functional_motivation,
            self.inhibition,
        ):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError("Teacher scenario segment values must be finite in [0, 1]")


@dataclass(frozen=True, slots=True)
class TeacherEmbodimentScenario:
    scenario_id: str
    segments: tuple[TeacherEmbodimentScenarioSegment, ...]
    initial_controller_activation: float = 0.0
    initial_functional_motivation: float = 0.0
    initial_body_activation: float = 0.05
    random_seed: int | None = None
    raw_private_content_status: str = RAW_PRIVATE_CONTENT_EXCLUDED

    def __post_init__(self) -> None:
        if not self.scenario_id or not self.segments:
            raise ValueError("Teacher scenario requires identity and at least one segment")
        for value in (
            self.initial_controller_activation,
            self.initial_functional_motivation,
            self.initial_body_activation,
        ):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError("Teacher scenario initial state must be finite in [0, 1]")
        if self.random_seed is not None:
            raise ValueError("Teacher reference scenarios cannot depend on random seeds")
        if self.raw_private_content_status != RAW_PRIVATE_CONTENT_EXCLUDED:
            raise ValueError("Teacher scenario cannot include raw private content")


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
    body_activation_trace: tuple[float, ...]
    functional_motivation_trace: tuple[float, ...]
    recovery_convergence_tick: int | None
    convergence_status: str
    sequence_continuity_status: str
    binding_continuity_status: str
    second_stimulus_applied: bool
    final_state_sha256: str
    scenario_sha256: str
    deterministic_replay_status: str = "PASS"
    same_tick_cycle_status: str = "ABSENT"
    scripted_terminal_recovery_status: str = "ABSENT"
    reporting_style: str = PROFESSIONAL_REPORTING
    raw_private_content_status: str = RAW_PRIVATE_CONTENT_EXCLUDED
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.tick_count <= 0:
            raise ValueError("Teacher scenario result requires at least one executed tick")
        for digest in (self.final_state_sha256, self.scenario_sha256):
            if len(digest) != 64:
                raise ValueError("Teacher scenario result requires SHA-256 evidence")
        if self.deterministic_replay_status != "PASS":
            raise ValueError("Teacher reference scenario must be deterministic")
        if self.same_tick_cycle_status != "ABSENT":
            raise ValueError("Teacher scenario cannot contain same-tick causal cycles")
        if self.scripted_terminal_recovery_status != "ABSENT":
            raise ValueError("Teacher scenario cannot use scripted terminal recovery")
        if self.reporting_style != PROFESSIONAL_REPORTING:
            raise ValueError("Teacher scenario reporting style drift")
        if self.raw_private_content_status != RAW_PRIVATE_CONTENT_EXCLUDED:
            raise ValueError("Teacher scenario cannot retain raw private content")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("Teacher scenario cannot establish phenomenal interpretation")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("Teacher scenario cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("Teacher scenario cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("Teacher scenario must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["transition_sequence"] = list(self.transition_sequence)
        payload["controller_activation_trace"] = list(
            self.controller_activation_trace
        )
        payload["body_activation_trace"] = list(self.body_activation_trace)
        payload["functional_motivation_trace"] = list(
            self.functional_motivation_trace
        )
        return payload


def _scenario_segment(
    segment_id: str,
    *,
    ticks: int,
    salience: float,
    motivation: float,
    context_gate: bool,
    inhibition: float,
    stimulus_class: str = "HIGH_SALIENCE_INTIMATE_REFERENCE",
) -> TeacherEmbodimentScenarioSegment:
    return TeacherEmbodimentScenarioSegment(
        segment_id=segment_id,
        ticks=ticks,
        stimulus_class=stimulus_class,
        salience=salience,
        functional_motivation=motivation,
        context_gate=context_gate,
        inhibition=inhibition,
    )


def build_teacher_reference_scenarios() -> tuple[TeacherEmbodimentScenario, ...]:
    def recovery(
        segment_id: str,
        ticks: int,
    ) -> TeacherEmbodimentScenarioSegment:
        return _scenario_segment(
            segment_id,
            ticks=ticks,
            salience=0.0,
            motivation=0.0,
            context_gate=False,
            inhibition=0.0,
            stimulus_class="RECOVERY_REFERENCE",
        )
    return (
        TeacherEmbodimentScenario(
            scenario_id="LOW_SALIENCE_CONTEXT_OFF",
            segments=(
                _scenario_segment(
                    "low",
                    ticks=4,
                    salience=0.25,
                    motivation=0.10,
                    context_gate=False,
                    inhibition=0.20,
                    stimulus_class="HIGH_SALIENCE_NON_INTIMATE_REFERENCE",
                ),
            ),
        ),
        TeacherEmbodimentScenario(
            scenario_id="MEDIUM_SALIENCE_CONTEXT_ON",
            segments=(
                _scenario_segment(
                    "medium",
                    ticks=5,
                    salience=0.60,
                    motivation=0.30,
                    context_gate=True,
                    inhibition=0.20,
                ),
            ),
        ),
        TeacherEmbodimentScenario(
            scenario_id="HIGH_SALIENCE_LOW_INHIBITION",
            segments=(
                _scenario_segment(
                    "high-low-inhibition",
                    ticks=8,
                    salience=0.95,
                    motivation=0.70,
                    context_gate=True,
                    inhibition=0.05,
                ),
            ),
        ),
        TeacherEmbodimentScenario(
            scenario_id="HIGH_SALIENCE_HIGH_INHIBITION",
            segments=(
                _scenario_segment(
                    "high-high-inhibition",
                    ticks=8,
                    salience=0.95,
                    motivation=0.70,
                    context_gate=True,
                    inhibition=0.75,
                ),
            ),
        ),
        TeacherEmbodimentScenario(
            scenario_id="ELEVATED_INITIAL_BODY_STATE",
            initial_body_activation=0.65,
            segments=(
                _scenario_segment(
                    "elevated-body",
                    ticks=4,
                    salience=0.60,
                    motivation=0.25,
                    context_gate=True,
                    inhibition=0.30,
                ),
            ),
        ),
        TeacherEmbodimentScenario(
            scenario_id="ZERO_MOTIVATION_HIGH_PHYSIOLOGY",
            initial_body_activation=0.75,
            segments=(
                _scenario_segment(
                    "zero-motivation",
                    ticks=8,
                    salience=0.95,
                    motivation=0.0,
                    context_gate=True,
                    inhibition=0.05,
                ),
            ),
        ),
        TeacherEmbodimentScenario(
            scenario_id="JUST_BELOW_HIGH_ENTER_THRESHOLD",
            initial_controller_activation=0.69,
            segments=(
                _scenario_segment(
                    "threshold",
                    ticks=3,
                    salience=0.72,
                    motivation=0.20,
                    context_gate=True,
                    inhibition=0.0,
                ),
            ),
        ),
        TeacherEmbodimentScenario(
            scenario_id="REPEATED_STIMULUS_WITH_RECOVERY",
            segments=(
                _scenario_segment(
                    "first-high",
                    ticks=6,
                    salience=0.92,
                    motivation=0.60,
                    context_gate=True,
                    inhibition=0.10,
                ),
                recovery("middle-recovery", 4),
                _scenario_segment(
                    "second-high",
                    ticks=6,
                    salience=0.88,
                    motivation=0.55,
                    context_gate=True,
                    inhibition=0.15,
                ),
            ),
        ),
        TeacherEmbodimentScenario(
            scenario_id="RECOVERY_INTERRUPTED_BY_SECOND_STIMULUS",
            segments=(
                _scenario_segment(
                    "initial-high",
                    ticks=6,
                    salience=0.92,
                    motivation=0.60,
                    context_gate=True,
                    inhibition=0.10,
                ),
                recovery("interrupted-recovery", 3),
                _scenario_segment(
                    "interrupting-stimulus",
                    ticks=4,
                    salience=0.70,
                    motivation=0.35,
                    context_gate=True,
                    inhibition=0.20,
                ),
            ),
        ),
        TeacherEmbodimentScenario(
            scenario_id="PURE_BASELINE_RECOVERY",
            initial_body_activation=0.50,
            segments=(recovery("pure-recovery", 1),),
        ),
    )


def _replace_reference_body_activation(
    body_state: TeacherIntegratedBodyState,
    activation: float,
) -> TeacherIntegratedBodyState:
    target_channels = {
        "GENITAL_SENSORY_AFFERENT_REFERENCE",
        "GENITAL_VASCULAR_STATE",
        "ERECTILE_REFLEX_STATE",
    }
    observations = tuple(
        TeacherBodyObservation(
            channel_id=item.channel_id,
            values=(
                (activation,)
                if item.channel_id in target_channels
                else item.values
            ),
            timestamp_ms=item.timestamp_ms,
            confidence=item.confidence,
        )
        for item in body_state.observations
    )
    return integrate_teacher_body_state(
        observations,
        sequence=body_state.sequence,
    )


def _scenario_stimulus(
    scenario_id: str,
    segment: TeacherEmbodimentScenarioSegment,
    segment_index: int,
) -> TeacherStimulusEnvelope:
    return build_teacher_stimulus_envelope(
        stimulus_id=f"{scenario_id}:{segment_index}:{segment.segment_id}",
        stimulus_class=segment.stimulus_class,
        salience=segment.salience,
        functional_motivation=segment.functional_motivation,
        sexual_context_gate=segment.context_gate,
        inhibition=segment.inhibition,
    )


def _probe_body_activation(body_state: TeacherIntegratedBodyState) -> float:
    return max(
        _channel_scalar(body_state, "GENITAL_VASCULAR_STATE"),
        _channel_scalar(body_state, "ERECTILE_REFLEX_STATE"),
    )


def _probe_converged(frame: TeacherStateLoopFrame) -> bool:
    return (
        frame.controller_state.activation < 0.10
        and frame.controller_state.functional_motivation < 0.10
        and _probe_body_activation(frame.body_state) <= 0.15
        and frame.executed_transition is not None
        and frame.executed_transition.mode == "BASELINE"
    )


def _probe_transition_sequence(
    frames: tuple[TeacherStateLoopFrame, ...],
) -> tuple[str, ...]:
    transitions: list[str] = ["BASELINE"]
    for frame in frames[1:]:
        executed = frame.executed_transition
        if executed is None or not executed.transition_ids:
            transitions.append("BASELINE")
        else:
            transitions.extend(executed.transition_ids)
    return tuple(transitions)


def _run_teacher_reference_scenario(
    binding: TeacherBodyRuntimeBinding,
    scenario: TeacherEmbodimentScenario,
) -> TeacherEmbodimentScenarioResult:
    baseline_body = build_teacher_reference_baseline_state(binding)
    if scenario.initial_body_activation != 0.05:
        baseline_body = _replace_reference_body_activation(
            baseline_body,
            scenario.initial_body_activation,
        )
    controller = build_teacher_reference_controller_state(
        binding,
        baseline_body,
    )
    phase = (
        "HIGH_ACTIVATION_REFERENCE"
        if scenario.initial_controller_activation >= 0.70
        else "BASELINE_REFERENCE"
    )
    controller = replace(
        controller,
        activation=scenario.initial_controller_activation,
        salience=scenario.initial_controller_activation,
        functional_motivation=scenario.initial_functional_motivation,
        phase=phase,
        source_body_state_sha256=baseline_body.body_state_sha256,
    )
    baseline_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{scenario.scenario_id}:baseline",
        stimulus_class="BASELINE_REFERENCE",
        salience=0.0,
        functional_motivation=scenario.initial_functional_motivation,
        sexual_context_gate=False,
        inhibition=0.0,
    )
    frames: list[TeacherStateLoopFrame] = [
        _build_baseline_frame(
            binding,
            baseline_stimulus,
            baseline_body,
            controller,
        )
    ]

    for segment_index, segment in enumerate(scenario.segments):
        stimulus = _scenario_stimulus(
            scenario.scenario_id,
            segment,
            segment_index,
        )
        for _ in range(segment.ticks):
            previous = frames[-1]
            controller = _with_feedback(
                previous.controller_state,
                previous.body_schema_feedback_sha256,
            )
            frames.append(
                advance_teacher_embodied_tick(
                    binding,
                    previous_controller_state=controller,
                    previous_body_state=previous.body_state,
                    stimulus=stimulus,
                    previous_phase_state=previous.high_salience_phase_state,
                )
            )

    recovery_stimulus = build_teacher_stimulus_envelope(
        stimulus_id=f"{scenario.scenario_id}:final-recovery",
        stimulus_class="RECOVERY_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=0.0,
    )
    convergence_tick: int | None = None
    if _probe_converged(frames[-1]):
        convergence_tick = 0
    else:
        for recovery_tick in range(1, RECOVERY_CONVERGENCE_MAX_TICKS + 1):
            previous = frames[-1]
            controller = _with_feedback(
                previous.controller_state,
                previous.body_schema_feedback_sha256,
            )
            frame = advance_teacher_embodied_tick(
                binding,
                previous_controller_state=controller,
                previous_body_state=previous.body_state,
                stimulus=recovery_stimulus,
                previous_phase_state=previous.high_salience_phase_state,
            )
            frames.append(frame)
            if _probe_converged(frame):
                convergence_tick = recovery_tick
                break

    frame_tuple = tuple(frames)
    sequences = tuple(frame.body_state.sequence for frame in frame_tuple)
    timestamps = tuple(frame.body_state.timestamp_ms for frame in frame_tuple)
    sequence_continuity = (
        sequences == tuple(range(len(frame_tuple)))
        and timestamps
        == tuple(index * 100 for index in range(len(frame_tuple)))
    )
    binding_continuity = all(
        frame.controller_state.body_id == binding.body_id
        and frame.controller_state.runtime_id == binding.runtime_id
        and frame.controller_state.session_id == binding.session_id
        and frame.bound_body_state.body_id == binding.body_id
        and frame.bound_body_state.runtime_id == binding.runtime_id
        and frame.bound_body_state.session_id == binding.session_id
        for frame in frame_tuple
    )
    causal_order = all(
        current.executed_transition is not None
        and current.executed_transition.source_body_state_sha256
        == previous.body_state.body_state_sha256
        and current.controller_state.source_body_state_sha256
        == previous.body_state.body_state_sha256
        for previous, current in zip(frame_tuple, frame_tuple[1:])
    )
    reporting_ok = all(
        frame.report.reporting_style == PROFESSIONAL_REPORTING
        and frame.report.phenomenal_interpretation_status == NOT_ESTABLISHED
        for frame in frame_tuple
    )

    activation_trace = tuple(
        frame.controller_state.activation for frame in frame_tuple
    )
    body_trace = tuple(
        _probe_body_activation(frame.body_state) for frame in frame_tuple
    )
    motivation_trace = tuple(
        frame.controller_state.functional_motivation
        for frame in frame_tuple
    )
    transition_sequence = _probe_transition_sequence(frame_tuple)
    final_state_sha256 = frame_tuple[-1].body_state.body_state_sha256
    payload = {
        "scenario": asdict(scenario),
        "runtime_id": binding.runtime_id,
        "session_id": binding.session_id,
        "body_id": binding.body_id,
        "transition_sequence": list(transition_sequence),
        "controller_activation_trace": list(activation_trace),
        "body_activation_trace": list(body_trace),
        "functional_motivation_trace": list(motivation_trace),
        "recovery_convergence_tick": convergence_tick,
        "final_state_sha256": final_state_sha256,
    }
    return TeacherEmbodimentScenarioResult(
        scenario_id=scenario.scenario_id,
        controller_id=TEACHER_CONTROLLER_ID,
        body_id=binding.body_id,
        runtime_id=binding.runtime_id,
        session_id=binding.session_id,
        tick_count=len(frame_tuple) - 1,
        transition_sequence=transition_sequence,
        controller_activation_trace=activation_trace,
        body_activation_trace=body_trace,
        functional_motivation_trace=motivation_trace,
        recovery_convergence_tick=convergence_tick,
        convergence_status=("PASS" if convergence_tick is not None else "FAIL"),
        sequence_continuity_status=("PASS" if sequence_continuity else "FAIL"),
        binding_continuity_status=("PASS" if binding_continuity else "FAIL"),
        second_stimulus_applied=(
            scenario.scenario_id
            == "RECOVERY_INTERRUPTED_BY_SECOND_STIMULUS"
        ),
        final_state_sha256=final_state_sha256,
        scenario_sha256=_canonical_hash(payload),
        same_tick_cycle_status=("ABSENT" if causal_order else "PRESENT"),
        reporting_style=(
            PROFESSIONAL_REPORTING if reporting_ok else "REPORTING_DRIFT"
        ),
    )


def run_teacher_embodiment_stability_probe(
    binding: TeacherBodyRuntimeBinding,
) -> tuple[TeacherEmbodimentScenarioResult, ...]:
    possess_teacher_body(binding)
    return tuple(
        _run_teacher_reference_scenario(binding, scenario)
        for scenario in build_teacher_reference_scenarios()
    )
