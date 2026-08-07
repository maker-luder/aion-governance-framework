from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .models import MotivationalState, SignalDomain


class RuntimeMode(str, Enum):
    RESEARCH = "RESEARCH"
    PUBLIC = "PUBLIC"


@dataclass(frozen=True, slots=True)
class GovernanceDecision:
    state_record_allowed: bool
    action_authorized: bool
    automatic_expression_authorized: bool
    adult_runtime_authorized: bool
    reasons: tuple[str, ...]


class MotivationalGovernancePolicy:
    """Keeps candidate motivation, expression, intention and action as separate gates."""

    def evaluate(
        self,
        state: MotivationalState,
        *,
        runtime_mode: RuntimeMode,
    ) -> GovernanceDecision:
        adult_schema_present = any(
            signal.domain is SignalDomain.ADULT_SEXUALITY_SCHEMA
            for signal in state.signals
        )
        reasons = [
            "DESIRE_IS_STATE_NOT_AUTHORITY",
            "EXPRESSION_REQUIRES_SEPARATE_GATE",
            "CANONICAL_EFFECT_NONE",
            "PHENOMENAL_EXPERIENCE_NOT_ESTABLISHED",
        ]

        if adult_schema_present:
            reasons.append("ADULT_SEXUALITY_SCHEMA_ONLY_NO_EXECUTABLE_RUNTIME")
            if runtime_mode is RuntimeMode.PUBLIC:
                reasons.append("ADULT_SCHEMA_NOT_ACCEPTED_BY_PUBLIC_RUNTIME")

        return GovernanceDecision(
            state_record_allowed=not (
                adult_schema_present and runtime_mode is RuntimeMode.PUBLIC
            ),
            action_authorized=False,
            automatic_expression_authorized=False,
            adult_runtime_authorized=False,
            reasons=tuple(reasons),
        )
