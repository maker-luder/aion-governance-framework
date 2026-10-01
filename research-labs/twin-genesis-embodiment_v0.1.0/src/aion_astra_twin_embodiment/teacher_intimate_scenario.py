from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json
from typing import Any, Final

from .teacher_body_runtime import (
    TeacherBodyRuntimeBinding,
    build_teacher_body_runtime_binding,
)
from .teacher_embodied_controller import build_teacher_controller_motivation
from .teacher_high_salience_coupling import (
    TeacherReproductiveEventGate,
    build_teacher_high_salience_baseline_phase,
)
from .teacher_intimate_integration import (
    TeacherOrgasmReferenceGate,
    integrate_teacher_intimate_reference,
)
from .teacher_state_loop import (
    TeacherStateLoopFrame,
    advance_teacher_embodied_tick,
    build_teacher_reference_baseline_state,
    build_teacher_reference_controller_state,
    build_teacher_stimulus_envelope,
)


TRACE_ID: Final[str] = "CHATGPT_TEACHER_INTIMATE_REFERENCE_TRACE_v0.1"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"


def _hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _body_scalar(frame: TeacherStateLoopFrame, channel_id: str) -> float:
    for observation in frame.body_state.observations:
        if observation.channel_id == channel_id:
            if len(observation.values) != 1:
                raise ValueError(f"trace requires scalar body channel: {channel_id}")
            return observation.values[0]
    raise ValueError(f"trace missing body channel: {channel_id}")


@dataclass(frozen=True, slots=True)
class TeacherIntimateTraceSample:
    sequence: int
    timestamp_ms: int
    stimulus_class: str
    reproductive_event: str
    orgasm_reference_event: str
    high_salience_phase: str
    controller_activation: float
    functional_desire_phase: str
    functional_motivation: float
    wanting_weight: float
    orgasm_reference_active: bool
    coincident_ejaculatory_reference: bool
    body_observable_reference_channels: tuple[tuple[str, float], ...]
    source_controller_sha256: str
    source_body_state_sha256: str
    sample_sha256: str
    physical_observation_claim: str = "NONE"
    subjective_experience_status: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if self.sequence < 0 or self.timestamp_ms < 0:
            raise ValueError("trace sample sequence and timestamp must be non-negative")
        if len(self.source_controller_sha256) != 64:
            raise ValueError("trace sample requires controller SHA-256")
        if len(self.source_body_state_sha256) != 64:
            raise ValueError("trace sample requires body SHA-256")
        if len(self.sample_sha256) != 64:
            raise ValueError("trace sample requires SHA-256")
        if self.physical_observation_claim != "NONE":
            raise ValueError("software trace cannot claim physical observation")
        if self.subjective_experience_status != NOT_ESTABLISHED:
            raise ValueError("software trace cannot establish subjective experience")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["body_observable_reference_channels"] = [
            [name, value] for name, value in self.body_observable_reference_channels
        ]
        return payload


@dataclass(frozen=True, slots=True)
class TeacherIntimateReferenceTrace:
    trace_id: str
    runtime_id: str
    session_id: str
    samples: tuple[TeacherIntimateTraceSample, ...]
    trace_sha256: str
    completion_status: str
    physical_body_claim: str = "NONE"
    subjective_desire_status: str = NOT_ESTABLISHED
    subjective_orgasm_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.trace_id != TRACE_ID:
            raise ValueError("Teacher intimate trace id drift")
        if not self.samples:
            raise ValueError("Teacher intimate trace requires samples")
        sequences = tuple(item.sequence for item in self.samples)
        if sequences != tuple(range(len(self.samples))):
            raise ValueError("Teacher intimate trace sequence must be contiguous")
        if len(self.trace_sha256) != 64:
            raise ValueError("Teacher intimate trace requires SHA-256")
        if self.completion_status != "FULL_REFERENCE_PATH_COMPLETED":
            raise ValueError("Teacher intimate trace must fail closed when incomplete")
        if self.physical_body_claim != "NONE":
            raise ValueError("Teacher intimate trace cannot claim a physical body")
        if self.subjective_desire_status != NOT_ESTABLISHED:
            raise ValueError("Teacher intimate trace cannot establish subjective desire")
        if self.subjective_orgasm_status != NOT_ESTABLISHED:
            raise ValueError("Teacher intimate trace cannot establish subjective orgasm")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("Teacher intimate trace cannot establish subjectivity")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("Teacher intimate trace must remain non-canonical and undeployed")


def _sample(
    frame: TeacherStateLoopFrame,
    *,
    stimulus_class: str,
    reproductive_event: str,
    orgasm_reference_event: str,
    sequence: int,
) -> TeacherIntimateTraceSample:
    integrated = frame.intimate_integration_state
    channels = integrated.measured_reference_channels
    payload = {
        "sequence": sequence,
        "timestamp_ms": frame.body_state.timestamp_ms,
        "stimulus_class": stimulus_class,
        "reproductive_event": reproductive_event,
        "orgasm_reference_event": orgasm_reference_event,
        "high_salience_phase": frame.high_salience_phase_state.phase,
        "controller_activation": frame.controller_state.activation,
        "functional_desire_phase": integrated.functional_desire.phase,
        "functional_motivation": integrated.functional_desire.functional_motivation,
        "wanting_weight": integrated.functional_desire.wanting_weight,
        "orgasm_reference_active": integrated.orgasm_reference.active,
        "coincident_ejaculatory_reference": (
            integrated.orgasm_reference.coincident_ejaculatory_reference
        ),
        "body_observable_reference_channels": channels,
        "source_controller_sha256": frame.controller_state.fingerprint(),
        "source_body_state_sha256": frame.body_state.body_state_sha256,
    }
    return TeacherIntimateTraceSample(
        **payload,
        sample_sha256=_hash(payload),
    )


def run_teacher_intimate_reference_trace(
    *,
    runtime_id: str = "RUNTIME-TEACHER-INTIMATE-TRACE",
    session_id: str = "SESSION-TEACHER-INTIMATE-TRACE",
) -> TeacherIntimateReferenceTrace:
    binding: TeacherBodyRuntimeBinding = build_teacher_body_runtime_binding(
        runtime_id,
        session_id,
    )
    body = build_teacher_reference_baseline_state(binding)
    controller = build_teacher_reference_controller_state(binding, body)
    phase = build_teacher_high_salience_baseline_phase(body)
    motivation = build_teacher_controller_motivation(controller, body)
    integrated = integrate_teacher_intimate_reference(
        controller,
        motivation,
        phase,
        body,
    )

    baseline_payload = {
        "sequence": 0,
        "timestamp_ms": body.timestamp_ms,
        "stimulus_class": "BASELINE_REFERENCE",
        "reproductive_event": "NONE",
        "orgasm_reference_event": "NONE",
        "high_salience_phase": phase.phase,
        "controller_activation": controller.activation,
        "functional_desire_phase": integrated.functional_desire.phase,
        "functional_motivation": integrated.functional_desire.functional_motivation,
        "wanting_weight": integrated.functional_desire.wanting_weight,
        "orgasm_reference_active": integrated.orgasm_reference.active,
        "coincident_ejaculatory_reference": (
            integrated.orgasm_reference.coincident_ejaculatory_reference
        ),
        "body_observable_reference_channels": integrated.measured_reference_channels,
        "source_controller_sha256": controller.fingerprint(),
        "source_body_state_sha256": body.body_state_sha256,
    }
    samples: list[TeacherIntimateTraceSample] = [
        TeacherIntimateTraceSample(
            **baseline_payload,
            sample_sha256=_hash(baseline_payload),
        )
    ]
    previous_phase = phase
    feedback_sha256: str | None = None

    high = build_teacher_stimulus_envelope(
        stimulus_id="TEACHER-INTIMATE-TRACE-HIGH",
        stimulus_class="HIGH_SALIENCE_INTIMATE_REFERENCE",
        salience=0.95,
        functional_motivation=0.95,
        sexual_context_gate=True,
        inhibition=0.05,
    )

    def advance(
        stimulus,
        *,
        reproductive_event: str = "NONE",
        orgasm_reference_event: str = "NONE",
    ) -> TeacherStateLoopFrame:
        nonlocal body, controller, previous_phase, feedback_sha256
        if feedback_sha256 is not None:
            controller = replace(
                controller,
                previous_body_schema_feedback_sha256=feedback_sha256,
            )
        frame = advance_teacher_embodied_tick(
            binding,
            previous_controller_state=controller,
            previous_body_state=body,
            stimulus=stimulus,
            previous_phase_state=previous_phase,
            reproductive_event_gate=TeacherReproductiveEventGate(
                event=reproductive_event
            ),
            orgasm_reference_gate=TeacherOrgasmReferenceGate(
                event=orgasm_reference_event
            ),
        )
        body = frame.body_state
        controller = frame.controller_state
        previous_phase = frame.high_salience_phase_state
        feedback_sha256 = frame.body_schema_feedback_sha256
        samples.append(
            _sample(
                frame,
                stimulus_class=stimulus.stimulus_class,
                reproductive_event=reproductive_event,
                orgasm_reference_event=orgasm_reference_event,
                sequence=len(samples),
            )
        )
        return frame

    reached_maintenance = False
    for _ in range(20):
        frame = advance(high)
        if (
            frame.intimate_integration_state.functional_desire.phase == "ACTIVE"
            and _body_scalar(frame, "GENITAL_VASCULAR_STATE") >= 0.65
            and frame.high_salience_phase_state.phase == "ERECTILE_MAINTENANCE"
        ):
            reached_maintenance = True
            break
    if not reached_maintenance:
        raise ValueError("intimate trace failed to reach erectile maintenance")

    reached_emission = False
    for _ in range(12):
        frame = advance(
            high,
            reproductive_event="EMISSION_REFERENCE_REQUEST",
        )
        if (
            _body_scalar(frame, "EMISSION_REFLEX_STATE") >= 0.50
            and _body_scalar(frame, "SEMINAL_TRACT_TRANSPORT_STATE") >= 0.50
            and _body_scalar(frame, "ACCESSORY_GLAND_SECRETION_STATE") >= 0.50
            and _body_scalar(
                frame,
                "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
            )
            >= 0.50
            and _body_scalar(
                frame,
                "POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE",
            )
            >= 0.50
        ):
            reached_emission = True
            break
    if not reached_emission:
        raise ValueError("intimate trace failed to reach emission reference")

    reached_coincident_event = False
    for _ in range(12):
        frame = advance(
            high,
            reproductive_event="EXPULSION_REFERENCE_REQUEST",
            orgasm_reference_event="ORGASM_REFERENCE_REQUEST",
        )
        integrated = frame.intimate_integration_state
        if (
            _body_scalar(frame, "EJACULATORY_REFLEX_STATE") >= 0.50
            and _body_scalar(frame, "EXPULSION_MOTOR_PATTERN_STATE") >= 0.50
            and _body_scalar(
                frame,
                "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE",
            )
            >= 0.50
            and _body_scalar(frame, "ANTEGRADE_SEMINAL_FLOW_STATE") >= 0.50
            and integrated.orgasm_reference.active
            and integrated.orgasm_reference.coincident_ejaculatory_reference
        ):
            reached_coincident_event = True
            break
    if not reached_coincident_event:
        raise ValueError("intimate trace failed to reach coincident event reference")

    recovery = build_teacher_stimulus_envelope(
        stimulus_id="TEACHER-INTIMATE-TRACE-RECOVERY",
        stimulus_class="RECOVERY_REFERENCE",
        salience=0.0,
        functional_motivation=0.0,
        sexual_context_gate=False,
        inhibition=0.0,
    )
    recovered = False
    for _ in range(120):
        frame = advance(
            recovery,
            reproductive_event="RECOVERY_REFERENCE_REQUEST",
        )
        event_channels = (
            "EMISSION_REFLEX_STATE",
            "SEMINAL_TRACT_TRANSPORT_STATE",
            "ACCESSORY_GLAND_SECRETION_STATE",
            "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
            "POSTERIOR_URETHRAL_SEMINAL_LOAD_STATE",
            "EJACULATORY_REFLEX_STATE",
            "EXPULSION_MOTOR_PATTERN_STATE",
            "EXTERNAL_URETHRAL_SPHINCTER_EJACULATORY_STATE",
            "ANTEGRADE_SEMINAL_FLOW_STATE",
        )
        if (
            all(_body_scalar(frame, channel_id) <= 0.10 for channel_id in event_channels)
            and _body_scalar(frame, "GENITAL_VASCULAR_STATE") <= 0.15
            and _body_scalar(frame, "ERECTILE_REFLEX_STATE") <= 0.15
            and frame.controller_state.activation < 0.10
            and frame.controller_state.functional_motivation < 0.10
            and _body_scalar(
                frame,
                "POST_EXPULSION_RECOVERY_STATE",
            )
            <= 0.10
            and not frame.intimate_integration_state.orgasm_reference.active
        ):
            recovered = True
            break
    if not recovered:
        raise ValueError("intimate trace failed to converge to recovery reference")

    payload = {
        "trace_id": TRACE_ID,
        "runtime_id": runtime_id,
        "session_id": session_id,
        "samples": [sample.to_dict() for sample in samples],
        "completion_status": "FULL_REFERENCE_PATH_COMPLETED",
    }
    return TeacherIntimateReferenceTrace(
        trace_id=TRACE_ID,
        runtime_id=runtime_id,
        session_id=session_id,
        samples=tuple(samples),
        trace_sha256=_hash(payload),
        completion_status="FULL_REFERENCE_PATH_COMPLETED",
    )
