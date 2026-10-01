from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final

from .teacher_body_channels import build_teacher_body_signal_schema


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
