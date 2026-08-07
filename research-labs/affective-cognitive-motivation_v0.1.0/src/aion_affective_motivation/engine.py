from __future__ import annotations

from dataclasses import dataclass

from .models import MotivationalState, SignalDomain


@dataclass(frozen=True, slots=True)
class StateAnalysis:
    signal_count: int
    domains: tuple[SignalDomain, ...]
    approach_avoidance_conflict: bool
    wanting_liking_are_nonidentical: bool
    adult_schema_present: bool
    action_authorized: bool = False
    canonical_effect: str = "NONE"


class MotivationalStateEngine:
    """Analyzes represented state without inventing a psychological scoring formula."""

    def analyze(self, state: MotivationalState) -> StateAnalysis:
        domains = tuple(signal.domain for signal in state.signals)
        return StateAnalysis(
            signal_count=len(state.signals),
            domains=domains,
            approach_avoidance_conflict=any(
                signal.approach > 0.0 and signal.avoidance > 0.0
                for signal in state.signals
            ),
            wanting_liking_are_nonidentical=any(
                signal.wanting != signal.predicted_liking
                for signal in state.signals
            ),
            adult_schema_present=SignalDomain.ADULT_SEXUALITY_SCHEMA in domains,
        )

    def preserve_domains(self, state: MotivationalState) -> tuple[SignalDomain, ...]:
        """Return explicit domains exactly as recorded; no automatic escalation occurs."""

        return tuple(signal.domain for signal in state.signals)
