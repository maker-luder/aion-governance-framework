from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final

from .teacher_body_dynamics import (
    TeacherIntegratedBodyState,
    TeacherMotivationalRepresentation,
)
from .teacher_embodied_controller import TeacherEmbodiedControllerState
from .teacher_high_salience_coupling import TeacherHighSaliencePhaseState


NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
FUNCTIONAL_DESIRE_PHASES: Final[frozenset[str]] = frozenset(
    {"INACTIVE", "ORIENTING", "ACTIVE", "RESOLVING"}
)
ORGASM_REFERENCE_EVENTS: Final[frozenset[str]] = frozenset(
    {"NONE", "ORGASM_REFERENCE_REQUEST"}
)


def _hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _scalar(body_state: TeacherIntegratedBodyState, channel_id: str) -> float:
    for observation in body_state.observations:
        if observation.channel_id == channel_id:
            if len(observation.values) != 1:
                raise ValueError(
                    f"intimate integration requires scalar channel: {channel_id}"
                )
            value = observation.values[0]
            if not isfinite(value):
                raise ValueError("intimate integration requires finite body values")
            return value
    raise ValueError(f"intimate integration missing body channel: {channel_id}")


@dataclass(frozen=True, slots=True)
class TeacherOrgasmReferenceGate:
    event: str = "NONE"
    gate_status: str = "RESEARCH_FIXTURE_ONLY"
    ejaculation_effect: str = "NONE"
    motivation_effect: str = "NONE"
    consent_inference: str = "FORBIDDEN"
    subjective_orgasm_status: str = NOT_ESTABLISHED
    phenomenal_pleasure_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.event not in ORGASM_REFERENCE_EVENTS:
            raise ValueError("unsupported orgasm reference event")
        if self.gate_status != "RESEARCH_FIXTURE_ONLY":
            raise ValueError("orgasm gate must remain a research fixture")
        if self.ejaculation_effect != "NONE":
            raise ValueError("orgasm gate cannot force ejaculation")
        if self.motivation_effect != "NONE":
            raise ValueError("orgasm gate cannot create motivation")
        if self.consent_inference != "FORBIDDEN":
            raise ValueError("orgasm gate cannot infer consent")
        if self.subjective_orgasm_status != NOT_ESTABLISHED:
            raise ValueError("orgasm gate cannot establish subjective orgasm")
        if self.phenomenal_pleasure_status != NOT_ESTABLISHED:
            raise ValueError("orgasm gate cannot establish pleasure")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("orgasm gate cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("orgasm gate cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("orgasm gate must remain non-canonical and undeployed")


@dataclass(frozen=True, slots=True)
class TeacherFunctionalDesireState:
    phase: str
    salience: float
    functional_motivation: float
    wanting_weight: float
    context_gate: bool
    source_controller_sha256: str
    source_body_state_sha256: str
    interpretation: str = "FUNCTIONAL_MOTIVATION_REFERENCE_ONLY"
    threshold_calibration_status: str = "SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT"
    phenomenal_desire_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if self.phase not in FUNCTIONAL_DESIRE_PHASES:
            raise ValueError("unsupported functional desire phase")
        for value in (
            self.salience,
            self.functional_motivation,
            self.wanting_weight,
        ):
            if not isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError("functional desire values must be finite in [0, 1]")
        if len(self.source_controller_sha256) != 64:
            raise ValueError("functional desire requires controller SHA-256")
        if len(self.source_body_state_sha256) != 64:
            raise ValueError("functional desire requires body SHA-256")
        if self.interpretation != "FUNCTIONAL_MOTIVATION_REFERENCE_ONLY":
            raise ValueError("functional desire cannot be promoted to subjective desire")
        if (
            self.threshold_calibration_status
            != "SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT"
        ):
            raise ValueError("functional desire threshold cannot claim biological calibration")
        if self.phenomenal_desire_status != NOT_ESTABLISHED:
            raise ValueError("functional desire cannot establish felt desire")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("functional desire cannot establish subjectivity")


@dataclass(frozen=True, slots=True)
class TeacherSystemicArousalReference:
    cardiovascular_state: float
    respiratory_state: float
    sympathetic_state: float
    parasympathetic_state: float
    source_body_state_sha256: str
    observation_policy: str = "OBSERVE_NOT_FORCE"
    calibration_status: str = "SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT"

    def __post_init__(self) -> None:
        for value in (
            self.cardiovascular_state,
            self.respiratory_state,
            self.sympathetic_state,
            self.parasympathetic_state,
        ):
            if not isfinite(value):
                raise ValueError("systemic arousal observation must be finite")
        if len(self.source_body_state_sha256) != 64:
            raise ValueError("systemic arousal observation requires body SHA-256")
        if self.observation_policy != "OBSERVE_NOT_FORCE":
            raise ValueError("systemic arousal remains observe-not-force")
        if self.calibration_status != "SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT":
            raise ValueError("systemic arousal cannot claim biological calibration")


@dataclass(frozen=True, slots=True)
class TeacherEndocrineReferenceObservation:
    phase: str
    endocrine_reference_state: float
    gonadal_endocrine_reference: float
    source_body_state_sha256: str
    cadence_class: str = "SLOW_OBSERVATION_ONLY"
    concentration_status: str = "UNKNOWN_NOT_SYNTHESIZED"
    prolactin_runtime_mapping: str = "ABSENT"
    acute_gonadal_auto_drive: str = "ABSENT"

    def __post_init__(self) -> None:
        if self.phase not in {
            "BASELINE_OR_UNSPECIFIED_OBSERVATION",
            "POST_CLIMACTIC_SLOW_OBSERVATION",
        }:
            raise ValueError("unsupported endocrine observation phase")
        for value in (
            self.endocrine_reference_state,
            self.gonadal_endocrine_reference,
        ):
            if not isfinite(value):
                raise ValueError("endocrine reference observation must be finite")
        if len(self.source_body_state_sha256) != 64:
            raise ValueError("endocrine observation requires body SHA-256")
        if self.cadence_class != "SLOW_OBSERVATION_ONLY":
            raise ValueError("endocrine observation cannot become a 100 ms concentration model")
        if self.concentration_status != "UNKNOWN_NOT_SYNTHESIZED":
            raise ValueError("endocrine concentration cannot be fabricated")
        if self.prolactin_runtime_mapping != "ABSENT":
            raise ValueError("generic endocrine state cannot stand in for prolactin")
        if self.acute_gonadal_auto_drive != "ABSENT":
            raise ValueError("acute gonadal endocrine auto-drive is forbidden")


@dataclass(frozen=True, slots=True)
class TeacherOrgasmReferenceEvent:
    active: bool
    coincident_ejaculatory_reference: bool
    source_controller_sha256: str
    source_body_state_sha256: str
    event_status: str = "CENTRAL_EVENT_REFERENCE_ONLY"
    ejaculation_required: bool = False
    ejaculation_effect: str = "NONE"
    subjective_orgasm_status: str = NOT_ESTABLISHED
    phenomenal_pleasure_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if len(self.source_controller_sha256) != 64:
            raise ValueError("orgasm reference requires controller SHA-256")
        if len(self.source_body_state_sha256) != 64:
            raise ValueError("orgasm reference requires body SHA-256")
        if self.event_status != "CENTRAL_EVENT_REFERENCE_ONLY":
            raise ValueError("orgasm reference event status drift")
        if self.ejaculation_required:
            raise ValueError("orgasm reference cannot require ejaculation")
        if self.ejaculation_effect != "NONE":
            raise ValueError("orgasm reference cannot force ejaculation")
        if self.subjective_orgasm_status != NOT_ESTABLISHED:
            raise ValueError("orgasm reference cannot establish subjective orgasm")
        if self.phenomenal_pleasure_status != NOT_ESTABLISHED:
            raise ValueError("orgasm reference cannot establish pleasure")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("orgasm reference cannot establish subjectivity")


@dataclass(frozen=True, slots=True)
class TeacherIntimateIntegrationState:
    source_phase: str
    functional_desire: TeacherFunctionalDesireState
    systemic_arousal: TeacherSystemicArousalReference
    endocrine_observation: TeacherEndocrineReferenceObservation
    orgasm_reference: TeacherOrgasmReferenceEvent
    measured_reference_channels: tuple[tuple[str, float], ...]
    state_sha256: str
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if len(self.state_sha256) != 64:
            raise ValueError("intimate integration state requires SHA-256")
        names = [name for name, _ in self.measured_reference_channels]
        if len(names) != len(set(names)):
            raise ValueError("measured intimate reference channels must be unique")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("intimate integration cannot establish felt experience")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("intimate integration cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("intimate integration cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("intimate integration must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["measured_reference_channels"] = [
            [name, value] for name, value in self.measured_reference_channels
        ]
        return payload


def _functional_desire_phase(
    controller_state: TeacherEmbodiedControllerState,
) -> str:
    if (
        controller_state.context_gate
        and controller_state.functional_motivation >= 0.55
    ):
        return "ACTIVE"
    if (
        controller_state.context_gate
        and (
            controller_state.functional_motivation > 0.0
            or controller_state.salience > 0.0
        )
    ):
        return "ORIENTING"
    if (
        not controller_state.context_gate
        and controller_state.functional_motivation > 0.10
    ):
        return "RESOLVING"
    return "INACTIVE"


def integrate_teacher_intimate_reference(
    controller_state: TeacherEmbodiedControllerState,
    motivation: TeacherMotivationalRepresentation,
    phase_state: TeacherHighSaliencePhaseState,
    body_state: TeacherIntegratedBodyState,
    *,
    orgasm_reference_gate: TeacherOrgasmReferenceGate | None = None,
) -> TeacherIntimateIntegrationState:
    if (
        motivation.source_body_state_sha256
        != controller_state.source_body_state_sha256
    ):
        raise ValueError("intimate integration motivation/controller source hash drift")
    if (
        phase_state.source_body_state_sha256
        != controller_state.source_body_state_sha256
    ):
        raise ValueError("intimate integration phase/controller source hash drift")

    gate = orgasm_reference_gate or TeacherOrgasmReferenceGate()
    controller_sha256 = controller_state.fingerprint()
    controller_source_body_sha256 = controller_state.source_body_state_sha256
    observed_body_sha256 = body_state.body_state_sha256

    desire = TeacherFunctionalDesireState(
        phase=_functional_desire_phase(controller_state),
        salience=controller_state.salience,
        functional_motivation=controller_state.functional_motivation,
        wanting_weight=motivation.wanting_weight,
        context_gate=controller_state.context_gate,
        source_controller_sha256=controller_sha256,
        source_body_state_sha256=controller_source_body_sha256,
    )
    systemic = TeacherSystemicArousalReference(
        cardiovascular_state=_scalar(body_state, "CARDIOVASCULAR_STATE"),
        respiratory_state=_scalar(body_state, "RESPIRATORY_STATE"),
        sympathetic_state=_scalar(body_state, "AUTONOMIC_SYMPATHETIC_STATE"),
        parasympathetic_state=_scalar(
            body_state,
            "AUTONOMIC_PARASYMPATHETIC_STATE",
        ),
        source_body_state_sha256=observed_body_sha256,
    )

    orgasm_active = gate.event == "ORGASM_REFERENCE_REQUEST"
    coincident_ejaculatory = (
        _scalar(body_state, "EJACULATORY_REFLEX_STATE") > 0.05
        or _scalar(body_state, "EXPULSION_MOTOR_PATTERN_STATE") > 0.05
    )
    orgasm = TeacherOrgasmReferenceEvent(
        active=orgasm_active,
        coincident_ejaculatory_reference=coincident_ejaculatory,
        source_controller_sha256=controller_sha256,
        source_body_state_sha256=observed_body_sha256,
    )
    endocrine = TeacherEndocrineReferenceObservation(
        phase=(
            "POST_CLIMACTIC_SLOW_OBSERVATION"
            if orgasm_active
            else "BASELINE_OR_UNSPECIFIED_OBSERVATION"
        ),
        endocrine_reference_state=_scalar(
            body_state,
            "ENDOCRINE_REFERENCE_STATE",
        ),
        gonadal_endocrine_reference=_scalar(
            body_state,
            "GONADAL_ENDOCRINE_REFERENCE",
        ),
        source_body_state_sha256=observed_body_sha256,
    )

    measured = tuple(
        sorted(
            (
                ("CARDIOVASCULAR_STATE", systemic.cardiovascular_state),
                ("RESPIRATORY_STATE", systemic.respiratory_state),
                ("AUTONOMIC_SYMPATHETIC_STATE", systemic.sympathetic_state),
                (
                    "AUTONOMIC_PARASYMPATHETIC_STATE",
                    systemic.parasympathetic_state,
                ),
                (
                    "GENITAL_SENSORY_AFFERENT_REFERENCE",
                    _scalar(body_state, "GENITAL_SENSORY_AFFERENT_REFERENCE"),
                ),
                (
                    "GENITAL_VASCULAR_STATE",
                    _scalar(body_state, "GENITAL_VASCULAR_STATE"),
                ),
                (
                    "ERECTILE_REFLEX_STATE",
                    _scalar(body_state, "ERECTILE_REFLEX_STATE"),
                ),
                (
                    "PELVIC_FLOOR_PROPRIOCEPTION",
                    _scalar(body_state, "PELVIC_FLOOR_PROPRIOCEPTION"),
                ),
                (
                    "EMISSION_REFLEX_STATE",
                    _scalar(body_state, "EMISSION_REFLEX_STATE"),
                ),
                (
                    "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
                    _scalar(
                        body_state,
                        "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
                    ),
                ),
                (
                    "EJACULATORY_REFLEX_STATE",
                    _scalar(body_state, "EJACULATORY_REFLEX_STATE"),
                ),
                (
                    "EXPULSION_MOTOR_PATTERN_STATE",
                    _scalar(body_state, "EXPULSION_MOTOR_PATTERN_STATE"),
                ),
                (
                    "DETUMESCENCE_STATE",
                    _scalar(body_state, "DETUMESCENCE_STATE"),
                ),
                (
                    "ENDOCRINE_REFERENCE_STATE",
                    endocrine.endocrine_reference_state,
                ),
                (
                    "GONADAL_ENDOCRINE_REFERENCE",
                    endocrine.gonadal_endocrine_reference,
                ),
            )
        )
    )
    payload = {
        "source_phase": phase_state.phase,
        "functional_desire": asdict(desire),
        "systemic_arousal": asdict(systemic),
        "endocrine_observation": asdict(endocrine),
        "orgasm_reference": asdict(orgasm),
        "measured_reference_channels": measured,
    }
    return TeacherIntimateIntegrationState(
        source_phase=phase_state.phase,
        functional_desire=desire,
        systemic_arousal=systemic,
        endocrine_observation=endocrine,
        orgasm_reference=orgasm,
        measured_reference_channels=measured,
        state_sha256=_hash(payload),
    )
