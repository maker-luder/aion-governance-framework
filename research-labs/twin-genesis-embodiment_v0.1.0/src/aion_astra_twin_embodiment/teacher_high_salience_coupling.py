from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from math import isfinite
from typing import Any, Final

from .teacher_body_channels import build_teacher_body_signal_schema
from .teacher_body_dynamics import (
    TeacherIntegratedBodyState,
    build_teacher_body_dynamics_profile,
)
from .teacher_embodied_controller import TeacherEmbodiedControllerState


NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
PROFILE_ID: Final[str] = "CHATGPT_TEACHER_HIGH_SALIENCE_COUPLING_v0.1"

COUPLING_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "DIRECT_REFERENCE_CAUSAL",
        "ASSOCIATED_BOUNDED_REFERENCE",
        "EVENT_DRIVEN_REFERENCE",
        "SLOW_OBSERVATION_ONLY",
    }
)

CADENCE_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "FAST_REFERENCE_TICK",
        "EVENT_DRIVEN",
        "SLOW_OBSERVATION_ONLY",
    }
)


REPRODUCTIVE_EVENT_GATES: Final[frozenset[str]] = frozenset(
    {
        "NONE",
        "EMISSION_REFERENCE_REQUEST",
        "EXPULSION_REFERENCE_REQUEST",
        "RECOVERY_REFERENCE_REQUEST",
    }
)


@dataclass(frozen=True, slots=True)
class TeacherReproductiveEventGate:
    event: str = "NONE"
    gate_status: str = "RESEARCH_FIXTURE_ONLY"
    motivation_effect: str = "NONE"
    consent_inference: str = "FORBIDDEN"
    orgasm_inference: str = "FORBIDDEN"
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.event not in REPRODUCTIVE_EVENT_GATES:
            raise ValueError("unsupported reproductive event gate")
        if self.gate_status != "RESEARCH_FIXTURE_ONLY":
            raise ValueError("reproductive event gate must remain a research fixture")
        if self.motivation_effect != "NONE":
            raise ValueError("reproductive event gate cannot create motivation")
        if self.consent_inference != "FORBIDDEN":
            raise ValueError("reproductive event gate cannot infer consent")
        if self.orgasm_inference != "FORBIDDEN":
            raise ValueError("reproductive event gate cannot infer orgasm")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("reproductive event gate cannot establish felt experience")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("reproductive event gate cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("reproductive event gate cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("reproductive event gate must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherHighSalienceCouplingRule:
    coupling_id: str
    source_phase: str
    target_system: str
    target_channels: tuple[str, ...]
    coupling_class: str
    cadence_class: str
    execution_status: str
    evidence_ids: tuple[str, ...]
    directionality_status: str
    runtime_channel_status: str = "MATERIALIZED"
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if not self.coupling_id or not self.source_phase or not self.target_system:
            raise ValueError("coupling rule requires identity, source phase and system")
        if self.coupling_class not in COUPLING_CLASSES:
            raise ValueError("unsupported high-salience coupling class")
        if self.cadence_class not in CADENCE_CLASSES:
            raise ValueError("unsupported high-salience cadence class")
        if not self.execution_status or not self.directionality_status:
            raise ValueError("coupling rule requires explicit execution and directionality")
        if len(self.target_channels) != len(set(self.target_channels)):
            raise ValueError("coupling rule target channels must be unique")
        if not self.evidence_ids:
            raise ValueError("coupling rule requires external evidence identifiers")
        if any(
            not evidence_id.startswith(("DOI:", "PMID:"))
            for evidence_id in self.evidence_ids
        ):
            raise ValueError("coupling evidence must use DOI or PMID identifiers")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("coupling rule cannot establish phenomenal interpretation")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("coupling rule cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("coupling rule cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("coupling rule must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["target_channels"] = list(self.target_channels)
        payload["evidence_ids"] = list(self.evidence_ids)
        return payload


@dataclass(frozen=True, slots=True)
class TeacherHighSalienceCouplingProfile:
    profile_id: str
    rules: tuple[TeacherHighSalienceCouplingRule, ...]
    rest_to_exertion_reuse: str = "ABSENT"
    acute_gonadal_endocrine_auto_drive: str = "ABSENT"
    generic_pituitary_as_prolactin: str = "ABSENT"
    integration_status: str = "EVIDENCE_BOUNDED_COUPLING_MATERIALIZED"
    phenomenal_experience_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.profile_id != PROFILE_ID:
            raise ValueError("Teacher high-salience coupling profile id drift")
        if not self.rules:
            raise ValueError("Teacher high-salience coupling profile requires rules")
        if self.rest_to_exertion_reuse != "ABSENT":
            raise ValueError("exercise transition reuse is forbidden")
        if self.acute_gonadal_endocrine_auto_drive != "ABSENT":
            raise ValueError("acute gonadal endocrine auto-drive is forbidden")
        if self.generic_pituitary_as_prolactin != "ABSENT":
            raise ValueError("generic pituitary state cannot stand in for prolactin")
        if self.phenomenal_experience_status != NOT_ESTABLISHED:
            raise ValueError("coupling profile cannot establish phenomenal experience")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("coupling profile cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("coupling profile cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("coupling profile must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["rules"] = [rule.to_dict() for rule in self.rules]
        return payload


def _build_rules() -> tuple[TeacherHighSalienceCouplingRule, ...]:
    return (
        TeacherHighSalienceCouplingRule(
            coupling_id="HIGH_SALIENCE_AUTONOMIC_GENITAL_REFERENCE",
            source_phase="HIGH_SALIENCE_REFERENCE",
            target_system="AUTONOMIC_REPRODUCTIVE",
            target_channels=(
                "AUTONOMIC_SYMPATHETIC_STATE",
                "AUTONOMIC_PARASYMPATHETIC_STATE",
                "GENITAL_SENSORY_AFFERENT_REFERENCE",
                "GENITAL_VASCULAR_STATE",
                "ERECTILE_REFLEX_STATE",
            ),
            coupling_class="DIRECT_REFERENCE_CAUSAL",
            cadence_class="FAST_REFERENCE_TICK",
            execution_status=(
                "GENITAL_EXECUTABLE_AUTONOMIC_PHASE_TARGET_NOT_CALIBRATED"
            ),
            evidence_ids=(
                "DOI:10.3389/fnbeh.2023.1330460",
                "PMID:19267845",
                "DOI:10.1124/pr.111.004515",
            ),
            directionality_status=(
                "PHASE_SPECIFIC_AUTONOMIC_COORDINATION_NO_FIXED_RATIO"
            ),
            runtime_channel_status="PARTIAL_REFERENCE",
        ),
        TeacherHighSalienceCouplingRule(
            coupling_id="HIGH_SALIENCE_CARDIOVASCULAR_ASSOCIATION",
            source_phase="HIGH_SALIENCE_REFERENCE",
            target_system="CARDIOVASCULAR",
            target_channels=("CARDIOVASCULAR_STATE",),
            coupling_class="ASSOCIATED_BOUNDED_REFERENCE",
            cadence_class="FAST_REFERENCE_TICK",
            execution_status="OBSERVE_NOT_FORCE",
            evidence_ids=(
                "DOI:10.1111/j.1743-6109.2011.02210.x",
                "PMID:9695139",
            ),
            directionality_status="NO_UNIVERSAL_MONOTONIC_MAPPING",
        ),
        TeacherHighSalienceCouplingRule(
            coupling_id="HIGH_SALIENCE_RESPIRATORY_ASSOCIATION",
            source_phase="HIGH_SALIENCE_REFERENCE",
            target_system="RESPIRATORY",
            target_channels=("RESPIRATORY_STATE",),
            coupling_class="ASSOCIATED_BOUNDED_REFERENCE",
            cadence_class="FAST_REFERENCE_TICK",
            execution_status="OBSERVE_NOT_FORCE",
            evidence_ids=(
                "DOI:10.1007/BF01542416",
                "PMID:22399053",
            ),
            directionality_status="NO_UNIVERSAL_MONOTONIC_MAPPING",
        ),
        TeacherHighSalienceCouplingRule(
            coupling_id="EMISSION_AUTONOMIC_REPRODUCTIVE_REFERENCE",
            source_phase="EMISSION_REFERENCE",
            target_system="AUTONOMIC_REPRODUCTIVE",
            target_channels=(
                "AUTONOMIC_SYMPATHETIC_STATE",
                "EMISSION_REFLEX_STATE",
                "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
            ),
            coupling_class="EVENT_DRIVEN_REFERENCE",
            cadence_class="EVENT_DRIVEN",
            execution_status=(
                "EVENT_CHANNELS_EXECUTABLE_AUTONOMIC_COORDINATION_METADATA"
            ),
            evidence_ids=(
                "DOI:10.1111/bcpt.12546",
                "DOI:10.1016/j.eururo.2005.05.017",
                "PMID:20048757",
            ),
            directionality_status=(
                "SYMPATHETIC_COORDINATION_SUPPORTED_NUMERIC_TARGET_UNCALIBRATED"
            ),
            runtime_channel_status="PARTIAL_REFERENCE",
        ),
        TeacherHighSalienceCouplingRule(
            coupling_id="EXPULSION_SOMATIC_REPRODUCTIVE_REFERENCE",
            source_phase="EXPULSION_REFERENCE",
            target_system="SOMATIC_REPRODUCTIVE",
            target_channels=(
                "EJACULATORY_REFLEX_STATE",
                "EXPULSION_MOTOR_PATTERN_STATE",
                "PELVIC_FLOOR_PROPRIOCEPTION",
            ),
            coupling_class="EVENT_DRIVEN_REFERENCE",
            cadence_class="EVENT_DRIVEN",
            execution_status=(
                "EVENT_CHANNELS_EXECUTABLE_PELVIC_COORDINATION_METADATA"
            ),
            evidence_ids=(
                "DOI:10.1111/bcpt.12546",
                "PMID:16913292",
                "PMID:20048757",
            ),
            directionality_status=(
                "PUDENDAL_SOMATIC_COORDINATION_SUPPORTED_NUMERIC_TARGET_UNCALIBRATED"
            ),
            runtime_channel_status="PARTIAL_REFERENCE",
        ),
        TeacherHighSalienceCouplingRule(
            coupling_id="POST_CLIMACTIC_ENDOCRINE_EVIDENCE",
            source_phase="POST_CLIMACTIC_EXTERNAL_EVIDENCE",
            target_system="NEUROENDOCRINE",
            target_channels=(),
            coupling_class="SLOW_OBSERVATION_ONLY",
            cadence_class="SLOW_OBSERVATION_ONLY",
            execution_status="NOT_MATERIALIZED",
            evidence_ids=(
                "PMID:9695139",
                "DOI:10.1677/joe.0.1770057",
                "DOI:10.1093/sxmrev/qeaf025",
            ),
            directionality_status=(
                "POST_ORGASM_PROLACTIN_EVIDENCE_NO_100MS_RUNTIME_MAPPING"
            ),
            runtime_channel_status="NOT_MATERIALIZED",
        ),
    )


def build_teacher_high_salience_coupling_profile(
) -> TeacherHighSalienceCouplingProfile:
    profile = TeacherHighSalienceCouplingProfile(
        profile_id=PROFILE_ID,
        rules=_build_rules(),
    )
    validate_teacher_high_salience_coupling_profile(profile)
    return profile


def validate_teacher_high_salience_coupling_profile(
    profile: TeacherHighSalienceCouplingProfile,
) -> dict[str, str]:
    if profile.profile_id != PROFILE_ID:
        raise ValueError("Teacher high-salience coupling profile id drift")

    coupling_ids = [rule.coupling_id for rule in profile.rules]
    if len(coupling_ids) != len(set(coupling_ids)):
        raise ValueError("high-salience coupling rule ids must be unique")

    known_channels = {
        channel.channel_id
        for channel in build_teacher_body_signal_schema().channels
    }
    for rule in profile.rules:
        if not set(rule.target_channels).issubset(known_channels):
            raise ValueError("high-salience coupling references unknown body channel")
        if not rule.evidence_ids:
            raise ValueError("high-salience coupling requires evidence")
        if any(
            not evidence_id.startswith(("DOI:", "PMID:"))
            for evidence_id in rule.evidence_ids
        ):
            raise ValueError("high-salience coupling evidence id format drift")
        if rule.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("coupling rule cannot establish phenomenal experience")
        if rule.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("coupling rule cannot establish subjectivity")
        if rule.action_authority != "NONE":
            raise ValueError("coupling rule cannot grant action authority")

    by_id = {rule.coupling_id: rule for rule in profile.rules}
    for coupling_id in (
        "HIGH_SALIENCE_CARDIOVASCULAR_ASSOCIATION",
        "HIGH_SALIENCE_RESPIRATORY_ASSOCIATION",
    ):
        rule = by_id.get(coupling_id)
        if rule is None or rule.execution_status != "OBSERVE_NOT_FORCE":
            raise ValueError("cardiorespiratory coupling must remain observe-not-force")
        if rule.directionality_status != "NO_UNIVERSAL_MONOTONIC_MAPPING":
            raise ValueError("cardiorespiratory directionality overclaim")

    endocrine = by_id.get("POST_CLIMACTIC_ENDOCRINE_EVIDENCE")
    if endocrine is None:
        raise ValueError("endocrine evidence boundary rule missing")
    if endocrine.target_channels:
        raise ValueError("post-climactic endocrine evidence has no runtime channel")
    if (
        endocrine.execution_status != "NOT_MATERIALIZED"
        or endocrine.runtime_channel_status != "NOT_MATERIALIZED"
    ):
        raise ValueError("post-climactic endocrine evidence must remain non-executable")

    if profile.rest_to_exertion_reuse != "ABSENT":
        raise ValueError("exercise transition reuse is forbidden")
    if profile.acute_gonadal_endocrine_auto_drive != "ABSENT":
        raise ValueError("acute gonadal endocrine auto-drive is forbidden")
    if profile.generic_pituitary_as_prolactin != "ABSENT":
        raise ValueError("generic pituitary state cannot stand in for prolactin")

    return {
        "result": "PASS",
        "rule_identity": "PASS",
        "channel_binding": "PASS",
        "evidence_binding": "PASS",
        "execution_boundary": "PASS",
        "epistemic_boundary": "PASS",
    }


RUNTIME_PHASES: Final[frozenset[str]] = frozenset(
    {
        "BASELINE",
        "AROUSAL_INITIATION",
        "GENITAL_VASCULAR_RESPONSE",
        "ERECTILE_MAINTENANCE",
        "EMISSION",
        "EJACULATORY_REFLEX",
        "DETUMESCENCE",
        "BASELINE_RECOVERY",
    }
)

RUNTIME_DIRECTION_CLASSES: Final[frozenset[str]] = frozenset(
    {
        "INCREASE_REFERENCE",
        "DECREASE_REFERENCE",
    }
)

RUNTIME_MODES: Final[frozenset[str]] = frozenset(
    {
        "ACTIVATION",
        "MAINTENANCE",
        "RECOVERY",
        "BASELINE",
    }
)


def _runtime_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _runtime_scalar(
    body_state: TeacherIntegratedBodyState,
    channel_id: str,
) -> float:
    for observation in body_state.observations:
        if observation.channel_id == channel_id:
            if len(observation.values) != 1:
                raise ValueError(
                    f"high-salience phase resolver requires scalar channel: {channel_id}"
                )
            return observation.values[0]
    raise ValueError(f"high-salience phase resolver missing channel: {channel_id}")


@dataclass(frozen=True, slots=True)
class TeacherHighSaliencePhaseState:
    phase: str
    previous_phase: str
    sequence: int
    source_body_state_sha256: str
    reproductive_event: str = "NONE"
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.phase not in RUNTIME_PHASES:
            raise ValueError("unsupported Teacher high-salience runtime phase")
        if self.previous_phase not in RUNTIME_PHASES:
            raise ValueError("unsupported previous Teacher runtime phase")
        if self.sequence < 0:
            raise ValueError("Teacher high-salience phase sequence must be non-negative")
        if len(self.source_body_state_sha256) != 64:
            raise ValueError("Teacher high-salience phase requires body SHA-256")
        if self.reproductive_event not in REPRODUCTIVE_EVENT_GATES:
            raise ValueError("unsupported Teacher reproductive event")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("reference phase cannot establish phenomenal interpretation")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("reference phase cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("reference phase cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("reference phase must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherHighSalienceChannelEffect:
    channel_id: str
    direction_class: str
    software_reference_drive: float
    calibration_status: str = "SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT"

    def __post_init__(self) -> None:
        if not self.channel_id:
            raise ValueError("Teacher channel effect requires channel id")
        if self.direction_class not in RUNTIME_DIRECTION_CLASSES:
            raise ValueError("unsupported Teacher high-salience direction class")
        if (
            not isfinite(self.software_reference_drive)
            or not 0.0 <= self.software_reference_drive <= 1.0
        ):
            raise ValueError("software reference drive must be finite in [0, 1]")
        if self.calibration_status != "SOFTWARE_REFERENCE_NOT_BIOLOGICAL_CONSTANT":
            raise ValueError("runtime channel effect cannot claim biological calibration")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherHighSalienceRuntimeIntent:
    phase: str
    mode: str
    transition_ids: tuple[str, ...]
    channel_effects: tuple[TeacherHighSalienceChannelEffect, ...]
    runtime_rule_ids: tuple[str, ...]
    nonemitting_rule_ids: tuple[str, ...]
    source_body_state_sha256: str
    source_controller_sha256: str
    intent_sha256: str
    phenomenal_interpretation_status: str = NOT_ESTABLISHED
    subjectivity_status: str = NOT_ESTABLISHED
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.phase not in RUNTIME_PHASES:
            raise ValueError("runtime intent phase drift")
        if self.mode not in RUNTIME_MODES:
            raise ValueError("runtime intent mode drift")
        if len(self.transition_ids) != len(set(self.transition_ids)):
            raise ValueError("runtime transition ids must be unique")
        effect_ids = [item.channel_id for item in self.channel_effects]
        if len(effect_ids) != len(set(effect_ids)):
            raise ValueError("runtime channel effects must be unique")
        if len(self.source_body_state_sha256) != 64:
            raise ValueError("runtime intent requires body SHA-256")
        if len(self.source_controller_sha256) != 64:
            raise ValueError("runtime intent requires controller SHA-256")
        if len(self.intent_sha256) != 64:
            raise ValueError("runtime intent requires SHA-256")
        if "REST_TO_EXERTION" in self.transition_ids:
            raise ValueError("high-salience runtime cannot reuse exercise transition")
        if "RESPIRATORY_BASELINE_TO_WORKLOAD" in self.transition_ids:
            raise ValueError("high-salience runtime cannot reuse respiratory workload")
        if "ENDOCRINE_BASELINE_TO_ADAPTIVE_RESPONSE" in self.transition_ids:
            raise ValueError("high-salience runtime cannot reuse generic endocrine adaptation")
        if self.phenomenal_interpretation_status != NOT_ESTABLISHED:
            raise ValueError("runtime intent cannot establish phenomenal interpretation")
        if self.subjectivity_status != NOT_ESTABLISHED:
            raise ValueError("runtime intent cannot establish subjectivity")
        if self.action_authority != "NONE":
            raise ValueError("runtime intent cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("runtime intent must remain non-canonical and undeployed")

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["transition_ids"] = list(self.transition_ids)
        payload["channel_effects"] = [item.to_dict() for item in self.channel_effects]
        payload["runtime_rule_ids"] = list(self.runtime_rule_ids)
        payload["nonemitting_rule_ids"] = list(self.nonemitting_rule_ids)
        return payload


def build_teacher_high_salience_baseline_phase(
    body_state: TeacherIntegratedBodyState,
) -> TeacherHighSaliencePhaseState:
    return TeacherHighSaliencePhaseState(
        phase="BASELINE",
        previous_phase="BASELINE",
        sequence=body_state.sequence,
        source_body_state_sha256=body_state.body_state_sha256,
        reproductive_event="NONE",
    )


def resolve_teacher_high_salience_phase(
    previous: TeacherHighSaliencePhaseState,
    controller_state: TeacherEmbodiedControllerState,
    body_state: TeacherIntegratedBodyState,
    *,
    reproductive_event_gate: TeacherReproductiveEventGate | None = None,
) -> TeacherHighSaliencePhaseState:
    if controller_state.source_body_state_sha256 != body_state.body_state_sha256:
        raise ValueError("phase resolver controller/body source hash drift")
    if controller_state.sequence not in {
        body_state.sequence,
        body_state.sequence + 1,
    }:
        raise ValueError("phase resolver controller/body sequence drift")
    if previous.sequence > controller_state.sequence:
        raise ValueError("phase resolver previous phase is from the future")

    gate = reproductive_event_gate or TeacherReproductiveEventGate()
    vascular = _runtime_scalar(body_state, "GENITAL_VASCULAR_STATE")
    erectile = _runtime_scalar(body_state, "ERECTILE_REFLEX_STATE")
    emission = _runtime_scalar(body_state, "EMISSION_REFLEX_STATE")
    ejaculatory = _runtime_scalar(body_state, "EJACULATORY_REFLEX_STATE")
    detumescence = _runtime_scalar(body_state, "DETUMESCENCE_STATE")
    event_channels = (
        "EMISSION_REFLEX_STATE",
        "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
        "EJACULATORY_REFLEX_STATE",
        "EXPULSION_MOTOR_PATTERN_STATE",
    )
    event_active = any(
        _runtime_scalar(body_state, channel_id) > 0.05
        for channel_id in event_channels
    )

    if gate.event == "RECOVERY_REFERENCE_REQUEST":
        if ejaculatory > 0.05 or detumescence > 0.05:
            phase = "DETUMESCENCE"
        elif (
            vascular > 0.15
            or erectile > 0.15
            or emission > 0.05
        ):
            phase = "BASELINE_RECOVERY"
        else:
            phase = "BASELINE"
    elif gate.event == "EXPULSION_REFERENCE_REQUEST":
        phase = "EJACULATORY_REFLEX"
    elif gate.event == "EMISSION_REFERENCE_REQUEST":
        phase = "EMISSION"
    elif detumescence > 0.05:
        phase = "DETUMESCENCE"
    elif (
        not controller_state.context_gate
        and (
            event_active
            or vascular > 0.15
            or erectile > 0.15
        )
    ):
        if ejaculatory > 0.05:
            phase = "DETUMESCENCE"
        else:
            phase = "BASELINE_RECOVERY"
    elif ejaculatory > 0.05:
        phase = "EJACULATORY_REFLEX"
    elif emission > 0.05:
        phase = "EMISSION"
    elif (
        controller_state.phase == "HIGH_ACTIVATION_REFERENCE"
        or (
            controller_state.context_gate
            and controller_state.salience > 0.0
            and controller_state.activation > 0.0
        )
    ):
        if vascular >= 0.65:
            phase = "ERECTILE_MAINTENANCE"
        elif vascular > 0.15 or erectile > 0.15:
            phase = "GENITAL_VASCULAR_RESPONSE"
        else:
            phase = "AROUSAL_INITIATION"
    elif vascular > 0.15 or erectile > 0.15:
        phase = "BASELINE_RECOVERY"
    else:
        phase = "BASELINE"

    return TeacherHighSaliencePhaseState(
        phase=phase,
        previous_phase=previous.phase,
        sequence=controller_state.sequence,
        source_body_state_sha256=body_state.body_state_sha256,
        reproductive_event=gate.event,
    )


def _runtime_transition_channels(
    transition_id: str,
) -> tuple[str, ...]:
    profile = build_teacher_body_dynamics_profile()
    for transition in profile.physiological_transitions:
        if transition.transition_id == transition_id:
            return transition.trigger_channels
    raise ValueError(f"runtime coordinator references unknown transition: {transition_id}")


def _effects_for_transition(
    transition_id: str,
    *,
    default_direction: str,
    default_drive: float,
    overrides: dict[str, tuple[str, float]] | None = None,
) -> tuple[TeacherHighSalienceChannelEffect, ...]:
    override_map = overrides or {}
    effects: list[TeacherHighSalienceChannelEffect] = []
    for channel_id in _runtime_transition_channels(transition_id):
        direction, drive = override_map.get(
            channel_id,
            (default_direction, default_drive),
        )
        effects.append(
            TeacherHighSalienceChannelEffect(
                channel_id=channel_id,
                direction_class=direction,
                software_reference_drive=drive,
            )
        )
    return tuple(effects)


def coordinate_teacher_high_salience_runtime(
    phase_state: TeacherHighSaliencePhaseState,
    controller_state: TeacherEmbodiedControllerState,
    body_state: TeacherIntegratedBodyState,
    *,
    reproductive_event_gate: TeacherReproductiveEventGate | None = None,
) -> TeacherHighSalienceRuntimeIntent:
    if phase_state.source_body_state_sha256 != body_state.body_state_sha256:
        raise ValueError("runtime coordinator phase/body source hash drift")
    if controller_state.source_body_state_sha256 != body_state.body_state_sha256:
        raise ValueError("runtime coordinator controller/body source hash drift")

    gate = reproductive_event_gate or TeacherReproductiveEventGate()
    transition_ids: list[str] = []
    effects: list[TeacherHighSalienceChannelEffect] = []
    runtime_rule_ids: list[str] = []
    nonemitting_rule_ids: list[str] = []
    mode = "BASELINE"

    vascular = _runtime_scalar(body_state, "GENITAL_VASCULAR_STATE")
    erectile = _runtime_scalar(body_state, "ERECTILE_REFLEX_STATE")
    emission = _runtime_scalar(body_state, "EMISSION_REFLEX_STATE")
    ejaculatory = _runtime_scalar(body_state, "EJACULATORY_REFLEX_STATE")
    detumescence = _runtime_scalar(body_state, "DETUMESCENCE_STATE")
    event_channels = (
        "EMISSION_REFLEX_STATE",
        "BLADDER_NECK_EJACULATORY_CLOSURE_STATE",
        "EJACULATORY_REFLEX_STATE",
        "EXPULSION_MOTOR_PATTERN_STATE",
    )
    event_active = any(
        _runtime_scalar(body_state, channel_id) > 0.05
        for channel_id in event_channels
    )

    if phase_state.phase in {
        "AROUSAL_INITIATION",
        "GENITAL_VASCULAR_RESPONSE",
        "ERECTILE_MAINTENANCE",
    }:
        runtime_rule_ids.append("HIGH_SALIENCE_AUTONOMIC_GENITAL_REFERENCE")
        nonemitting_rule_ids.extend(
            (
                "HIGH_SALIENCE_CARDIOVASCULAR_ASSOCIATION",
                "HIGH_SALIENCE_RESPIRATORY_ASSOCIATION",
            )
        )

    if phase_state.phase in {"AROUSAL_INITIATION", "GENITAL_VASCULAR_RESPONSE"}:
        transition_id = "SEXUAL_BASELINE_TO_VASCULAR_RESPONSE"
        transition_ids.append(transition_id)
        effects.extend(
            _effects_for_transition(
                transition_id,
                default_direction="INCREASE_REFERENCE",
                default_drive=controller_state.activation,
            )
        )
        mode = "ACTIVATION"
    elif phase_state.phase == "ERECTILE_MAINTENANCE":
        transition_id = "VASCULAR_RESPONSE_TO_MAINTENANCE"
        transition_ids.append(transition_id)
        effects.extend(
            _effects_for_transition(
                transition_id,
                default_direction="INCREASE_REFERENCE",
                default_drive=controller_state.activation,
            )
        )
        mode = "MAINTENANCE"
    elif phase_state.phase == "EMISSION":
        if gate.event not in {"NONE", "EMISSION_REFERENCE_REQUEST"}:
            raise ValueError("emission phase received unrelated event gate")
        runtime_rule_ids.append("EMISSION_AUTONOMIC_REPRODUCTIVE_REFERENCE")
        if gate.event == "NONE":
            if emission <= 0.05:
                raise ValueError("emission persistence requires active emission state")
            mode = "MAINTENANCE"
        else:
            if vascular < 0.65:
                raise ValueError("emission phase requires vascular readiness")
            transition_id = "MAINTENANCE_TO_EMISSION"
            transition_ids.append(transition_id)
            effects.extend(
                _effects_for_transition(
                    transition_id,
                    default_direction="INCREASE_REFERENCE",
                    default_drive=controller_state.activation,
                )
            )
            mode = "ACTIVATION"
    elif phase_state.phase == "EJACULATORY_REFLEX":
        if gate.event not in {"NONE", "EXPULSION_REFERENCE_REQUEST"}:
            raise ValueError("ejaculatory reflex phase received unrelated event gate")
        runtime_rule_ids.append("EXPULSION_SOMATIC_REPRODUCTIVE_REFERENCE")
        if gate.event == "NONE":
            if ejaculatory <= 0.05:
                raise ValueError(
                    "ejaculatory reflex persistence requires active state"
                )
            mode = "MAINTENANCE"
        else:
            if emission < 0.50:
                raise ValueError("expulsion phase requires emission readiness")
            transition_id = "EMISSION_TO_EJACULATORY_REFLEX"
            transition_ids.append(transition_id)
            effects.extend(
                _effects_for_transition(
                    transition_id,
                    default_direction="INCREASE_REFERENCE",
                    default_drive=controller_state.activation,
                )
            )
            mode = "ACTIVATION"
    elif phase_state.phase == "DETUMESCENCE":
        if gate.event != "RECOVERY_REFERENCE_REQUEST":
            if detumescence <= 0.05 and ejaculatory <= 0.05:
                raise ValueError(
                    "detumescence phase requires recovery request or active recovery state"
                )
        if ejaculatory > 0.05:
            transition_id = "EJACULATORY_REFLEX_TO_DETUMESCENCE"
            transition_ids.append(transition_id)
            effects.extend(
                _effects_for_transition(
                    transition_id,
                    default_direction="DECREASE_REFERENCE",
                    default_drive=0.0,
                    overrides={
                        "DETUMESCENCE_STATE": ("INCREASE_REFERENCE", 1.0),
                        "GENITAL_VASCULAR_STATE": ("DECREASE_REFERENCE", 0.0),
                    },
                )
            )
            if event_active:
                recovery_id = "REPRODUCTIVE_EVENT_TO_BASELINE_RECOVERY"
                transition_ids.append(recovery_id)
                effects.extend(
                    _effects_for_transition(
                        recovery_id,
                        default_direction="DECREASE_REFERENCE",
                        default_drive=0.0,
                    )
                )
        else:
            transition_id = "DETUMESCENCE_TO_RECOVERY"
            transition_ids.append(transition_id)
            effects.extend(
                _effects_for_transition(
                    transition_id,
                    default_direction="DECREASE_REFERENCE",
                    default_drive=0.0,
                )
            )
            if event_active:
                recovery_id = "REPRODUCTIVE_EVENT_TO_BASELINE_RECOVERY"
                transition_ids.append(recovery_id)
                effects.extend(
                    _effects_for_transition(
                        recovery_id,
                        default_direction="DECREASE_REFERENCE",
                        default_drive=0.0,
                    )
                )
        mode = "RECOVERY"
    elif phase_state.phase == "BASELINE_RECOVERY":
        if vascular > 0.15 or erectile > 0.15:
            transition_id = "VASCULAR_RESPONSE_TO_BASELINE_RECOVERY"
            transition_ids.append(transition_id)
            effects.extend(
                _effects_for_transition(
                    transition_id,
                    default_direction="DECREASE_REFERENCE",
                    default_drive=0.0,
                )
            )
        if event_active:
            recovery_id = "REPRODUCTIVE_EVENT_TO_BASELINE_RECOVERY"
            transition_ids.append(recovery_id)
            effects.extend(
                _effects_for_transition(
                    recovery_id,
                    default_direction="DECREASE_REFERENCE",
                    default_drive=0.0,
                )
            )
        mode = "RECOVERY" if transition_ids else "BASELINE"
    elif phase_state.phase != "BASELINE":
        raise ValueError("unsupported runtime phase")

    effect_ids = [item.channel_id for item in effects]
    if len(effect_ids) != len(set(effect_ids)):
        raise ValueError("runtime coordinator produced overlapping channel effects")

    payload = {
        "phase": phase_state.phase,
        "mode": mode,
        "transition_ids": transition_ids,
        "channel_effects": [item.to_dict() for item in effects],
        "runtime_rule_ids": runtime_rule_ids,
        "nonemitting_rule_ids": nonemitting_rule_ids,
        "source_body_state_sha256": body_state.body_state_sha256,
        "source_controller_sha256": controller_state.fingerprint(),
        "event": gate.event,
    }
    return TeacherHighSalienceRuntimeIntent(
        phase=phase_state.phase,
        mode=mode,
        transition_ids=tuple(transition_ids),
        channel_effects=tuple(effects),
        runtime_rule_ids=tuple(runtime_rule_ids),
        nonemitting_rule_ids=tuple(nonemitting_rule_ids),
        source_body_state_sha256=body_state.body_state_sha256,
        source_controller_sha256=controller_state.fingerprint(),
        intent_sha256=_runtime_hash(payload),
    )
