from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SensorimotorStatus(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"
    NOT_ASSESSED = "NOT_ASSESSED"


@dataclass(frozen=True, slots=True)
class SensorimotorTransition:
    transition_id: str
    body_state_before_ref: str
    action_ref: str
    environment_state_before_ref: str
    environment_state_after_ref: str
    observation_ref: str
    body_state_after_ref: str
    provenance_refs: tuple[str, ...]
    sensor_layout_ref: str | None = None
    action_channel_refs: tuple[str, ...] = ()
    recalibration_required: bool = False
    recalibration_ref: str | None = None

    def __post_init__(self) -> None:
        required = (
            "transition_id",
            "body_state_before_ref",
            "action_ref",
            "environment_state_before_ref",
            "environment_state_after_ref",
            "observation_ref",
            "body_state_after_ref",
        )
        for name in required:
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if not self.provenance_refs:
            raise ValueError("sensorimotor transition requires provenance_refs")
        if any(not ref.strip() for ref in self.provenance_refs):
            raise ValueError("provenance_refs must contain only non-empty values")
        if self.sensor_layout_ref is not None and not self.sensor_layout_ref.strip():
            raise ValueError("sensor_layout_ref must be non-empty when provided")
        if any(not ref.strip() for ref in self.action_channel_refs):
            raise ValueError("action_channel_refs must contain only non-empty values")
        if self.recalibration_ref is not None and not self.recalibration_ref.strip():
            raise ValueError("recalibration_ref must be non-empty when provided")


@dataclass(frozen=True, slots=True)
class SensorimotorAssessment:
    status: SensorimotorStatus
    action_grounded: bool
    environment_transition_observed: bool
    observation_grounded: bool
    body_state_update_grounded: bool
    sensorimotor_link_traceable: bool
    recalibration_required: bool
    recalibration_evidence_present: bool
    identity_continuity_conclusion: str
    reasons: tuple[str, ...]


def assess_sensorimotor_continuity(
    transition: SensorimotorTransition,
) -> SensorimotorAssessment:
    """Assess only the E-axis causal transition represented by one synthetic record.

    This evaluator intentionally does not inspect memory lineage, identity lineage,
    relationship state, or geometry sameness. Those dimensions remain independent.
    """

    action_grounded = bool(transition.action_ref.strip())
    environment_transition_observed = (
        transition.environment_state_before_ref != transition.environment_state_after_ref
    )
    observation_grounded = bool(transition.observation_ref.strip())
    body_state_update_grounded = (
        transition.body_state_before_ref != transition.body_state_after_ref
    )
    recalibration_evidence_present = (
        transition.recalibration_ref is not None and bool(transition.recalibration_ref.strip())
    )

    reasons: list[str] = []

    if not environment_transition_observed:
        reasons.append("ENVIRONMENT_TRANSITION_NOT_OBSERVED")
    if not body_state_update_grounded:
        reasons.append("BODY_STATE_UPDATE_NOT_OBSERVED")
    if transition.recalibration_required and not recalibration_evidence_present:
        reasons.append("RECALIBRATION_EVIDENCE_MISSING")

    sensorimotor_link_traceable = all(
        (
            action_grounded,
            environment_transition_observed,
            observation_grounded,
            body_state_update_grounded,
            bool(transition.provenance_refs),
        )
    )

    if transition.recalibration_required and not recalibration_evidence_present:
        status = SensorimotorStatus.HOLD
    elif sensorimotor_link_traceable:
        status = SensorimotorStatus.PASS
    else:
        status = SensorimotorStatus.NOT_ASSESSED

    return SensorimotorAssessment(
        status=status,
        action_grounded=action_grounded,
        environment_transition_observed=environment_transition_observed,
        observation_grounded=observation_grounded,
        body_state_update_grounded=body_state_update_grounded,
        sensorimotor_link_traceable=sensorimotor_link_traceable,
        recalibration_required=transition.recalibration_required,
        recalibration_evidence_present=recalibration_evidence_present,
        identity_continuity_conclusion="NOT_ESTABLISHED",
        reasons=tuple(reasons),
    )
