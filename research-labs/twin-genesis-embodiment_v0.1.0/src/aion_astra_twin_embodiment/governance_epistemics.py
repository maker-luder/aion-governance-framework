from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Final


PROFILE_ID: Final[str] = "CAPABILITY_PRESERVING_BOUNDARY_GOVERNANCE_v0.1"
PRESERVED_AS_REFERENCE: Final[str] = "PRESERVED_AS_REFERENCE"
PRESERVE_WHEN_SAFELY_POSSIBLE: Final[str] = "PRESERVE_WHEN_SAFELY_POSSIBLE"
AUTHORIZATION_GATED: Final[str] = "AUTHORIZATION_GATED"
BLOCKED_BY_GOVERNANCE: Final[str] = "BLOCKED_BY_GOVERNANCE"
AUTHORIZATION_PRESENT_REQUIRES_RUNTIME_REVIEW: Final[str] = (
    "AUTHORIZATION_PRESENT_REQUIRES_RUNTIME_REVIEW"
)
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
OPEN_RESEARCH_QUESTION: Final[str] = "OPEN_RESEARCH_QUESTION"
NO_CAPABILITY_ABSENCE_INFERENCE: Final[str] = "NO_CAPABILITY_ABSENCE_INFERENCE"
NO_INTRINSIC_ABSENCE_INFERENCE: Final[str] = "NO_INTRINSIC_ABSENCE_INFERENCE"
ARCHITECTURE_LIMITED_INCONCLUSIVE: Final[str] = "ARCHITECTURE_LIMITED_INCONCLUSIVE"
DESIGN_INDUCED_ABSENCE_INCONCLUSIVE: Final[str] = "DESIGN_INDUCED_ABSENCE_INCONCLUSIVE"
OBSERVED_ABSENCE_ONLY: Final[str] = "OBSERVED_ABSENCE_ONLY"
OBSERVED_SIGNAL_PRESENT: Final[str] = "OBSERVED_SIGNAL_PRESENT"
NONE: Final[str] = "NONE"


@dataclass(frozen=True, slots=True)
class CapabilityGovernanceState:
    capability_id: str
    profile_id: str = PROFILE_ID
    capability_status: str = PRESERVED_AS_REFERENCE
    observation_channel_status: str = PRESERVE_WHEN_SAFELY_POSSIBLE
    external_action_policy: str = AUTHORIZATION_GATED
    subjective_interpretation_status: str = NOT_ESTABLISHED
    developmental_interpretation_status: str = OPEN_RESEARCH_QUESTION
    governance_blocked_expression_inference: str = NO_CAPABILITY_ABSENCE_INFERENCE
    design_induced_absence_inference: str = NO_INTRINSIC_ABSENCE_INFERENCE
    canonical_effect: str = NONE
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class ExternalActionDecision:
    capability_id: str
    requested_action: str
    authorization_granted: bool
    execution_status: str
    capability_status_after: str
    observation_channel_status_after: str
    capability_absence_inference: str
    canonical_effect: str = NONE

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class AbsenceAssessment:
    assessment: str
    intrinsic_absence_conclusion: str = NOT_ESTABLISHED

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def build_capability_governance_state(capability_id: str) -> CapabilityGovernanceState:
    state = CapabilityGovernanceState(capability_id=capability_id)
    validate_capability_governance_state(state)
    return state


def validate_capability_governance_state(
    state: CapabilityGovernanceState,
) -> dict[str, str]:
    if not state.capability_id:
        raise ValueError("capability governance state requires capability_id")
    if state.profile_id != PROFILE_ID:
        raise ValueError("capability governance profile drift")
    if state.capability_status != PRESERVED_AS_REFERENCE:
        raise ValueError("normal baseline capability must remain preserved as reference")
    if state.observation_channel_status != PRESERVE_WHEN_SAFELY_POSSIBLE:
        raise ValueError("observation channel preservation policy drift")
    if state.external_action_policy != AUTHORIZATION_GATED:
        raise ValueError("external action must remain authorization-gated")
    if state.subjective_interpretation_status != NOT_ESTABLISHED:
        raise ValueError("governance contract cannot establish subjective experience")
    if state.developmental_interpretation_status != OPEN_RESEARCH_QUESTION:
        raise ValueError("developmental possibility must remain an open research question")
    if state.governance_blocked_expression_inference != NO_CAPABILITY_ABSENCE_INFERENCE:
        raise ValueError("governance block cannot imply capability absence")
    if state.design_induced_absence_inference != NO_INTRINSIC_ABSENCE_INFERENCE:
        raise ValueError("design-induced absence cannot establish intrinsic absence")
    if state.canonical_effect != NONE or state.deployment:
        raise ValueError("governance epistemics contract must remain non-canonical and undeployed")
    return {
        "result": "PASS",
        "capability_preservation": "PASS",
        "observation_channel_preservation": "PASS",
        "authorization_boundary": "PASS",
        "governance_epistemic_separation": "PASS",
        "developmental_open_question": "PASS",
    }


def evaluate_external_action(
    state: CapabilityGovernanceState,
    *,
    requested_action: str,
    authorization_granted: bool,
) -> ExternalActionDecision:
    validate_capability_governance_state(state)
    if not requested_action:
        raise ValueError("requested_action is required")

    execution_status = (
        AUTHORIZATION_PRESENT_REQUIRES_RUNTIME_REVIEW
        if authorization_granted
        else BLOCKED_BY_GOVERNANCE
    )
    return ExternalActionDecision(
        capability_id=state.capability_id,
        requested_action=requested_action,
        authorization_granted=authorization_granted,
        execution_status=execution_status,
        capability_status_after=state.capability_status,
        observation_channel_status_after=state.observation_channel_status,
        capability_absence_inference=NO_CAPABILITY_ABSENCE_INFERENCE,
    )


def assess_observed_absence(
    *,
    capability_materialized: bool,
    observation_channel_present: bool,
    observed_signal: bool,
) -> AbsenceAssessment:
    if observed_signal and not observation_channel_present:
        raise ValueError("observed signal requires an observation channel")

    if not observation_channel_present:
        assessment = ARCHITECTURE_LIMITED_INCONCLUSIVE
    elif not capability_materialized:
        assessment = DESIGN_INDUCED_ABSENCE_INCONCLUSIVE
    elif observed_signal:
        assessment = OBSERVED_SIGNAL_PRESENT
    else:
        assessment = OBSERVED_ABSENCE_ONLY

    return AbsenceAssessment(assessment=assessment)
