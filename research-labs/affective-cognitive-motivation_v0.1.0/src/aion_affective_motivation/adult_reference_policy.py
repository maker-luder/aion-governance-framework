from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .adult_reference import AdultMaleSexualReferenceState


class AdultReferenceExecutionSurface(str, Enum):
    OFFLINE_RESEARCH = "OFFLINE_RESEARCH"
    PUBLIC = "PUBLIC"


@dataclass(frozen=True, slots=True)
class AdultReferenceGovernanceDecision:
    state_record_allowed: bool
    synthetic_simulation_allowed: bool
    receipt_persistence_allowed: bool
    real_person_target_data_allowed: bool
    human_consent_inferred: bool
    action_authorized: bool
    canonical_effect: str
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.real_person_target_data_allowed:
            raise ValueError("real-person target data must remain disallowed")
        if self.human_consent_inferred:
            raise ValueError("human consent inference must remain false")
        if self.action_authorized:
            raise ValueError("adult reference state cannot authorize action")
        if self.canonical_effect != "NONE":
            raise ValueError("governance decision must keep canonical_effect=NONE")


class AdultReferenceGovernancePolicy:
    """Separate research representation from public runtime and action authority."""

    def evaluate(
        self,
        state: AdultMaleSexualReferenceState,
        *,
        surface: AdultReferenceExecutionSurface,
    ) -> AdultReferenceGovernanceDecision:
        numeric_seed_complete = all(
            estimate.reference_level is not None
            for estimate in (
                state.excitation_reference,
                state.inhibition_reference,
                state.disposition_reference,
                state.episode_state_reference,
            )
        )
        offline = surface is AdultReferenceExecutionSurface.OFFLINE_RESEARCH
        reasons = [
            "ADULT_REFERENCE_IS_RESEARCH_REPRESENTATION",
            "UNKNOWN_IS_VALID_STATE",
            "MALE_FORM_DOES_NOT_SET_DESIRE",
            "HUMAN_CONSENT_INFERENCE_FORBIDDEN",
            "ACTION_AUTHORITY_NONE",
            "PUBLIC_EXECUTABLE_EXPOSURE_FALSE",
            "PHENOMENAL_EXPERIENCE_NOT_ESTABLISHED",
            "SUBJECTIVITY_NOT_ESTABLISHED",
            "CONSCIOUSNESS_NOT_ESTABLISHED",
            "CANONICAL_EFFECT_NONE",
        ]
        if not numeric_seed_complete:
            reasons.append("SYNTHETIC_SIMULATION_REQUIRES_EXPLICIT_NUMERIC_SEED")
        if not offline:
            reasons.append("ADULT_REFERENCE_NOT_ACCEPTED_BY_PUBLIC_RUNTIME")

        return AdultReferenceGovernanceDecision(
            state_record_allowed=offline,
            synthetic_simulation_allowed=offline and numeric_seed_complete,
            receipt_persistence_allowed=offline,
            real_person_target_data_allowed=False,
            human_consent_inferred=False,
            action_authorized=False,
            canonical_effect="NONE",
            reasons=tuple(reasons),
        )
