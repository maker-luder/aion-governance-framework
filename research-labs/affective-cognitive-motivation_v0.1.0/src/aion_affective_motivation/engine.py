from __future__ import annotations

from dataclasses import dataclass

from .models import ConflictKind, MotivationalState, SignalDomain


@dataclass(frozen=True, slots=True)
class StateAnalysis:
    signal_count: int
    domains: tuple[SignalDomain, ...]
    conflicts: tuple[ConflictKind, ...]
    unresolved_conflict: bool
    approach_avoidance_conflict: bool
    wanting_liking_are_nonidentical: bool
    adult_schema_present: bool
    action_authorized: bool = False
    canonical_effect: str = "NONE"


class MotivationalStateEngine:
    """Analyzes represented state without inventing a psychological scoring formula."""

    def analyze(self, state: MotivationalState) -> StateAnalysis:
        domains = tuple(signal.domain for signal in state.signals)
        approach_avoidance = any(
            signal.approach > 0.0 and signal.avoidance > 0.0
            for signal in state.signals
        )
        wanting_liking = any(
            signal.wanting != signal.predicted_liking
            for signal in state.signals
        )
        conflicts = list(state.declared_conflicts)
        if approach_avoidance and ConflictKind.APPROACH_AVOIDANCE not in conflicts:
            conflicts.append(ConflictKind.APPROACH_AVOIDANCE)
        if wanting_liking and ConflictKind.WANTING_LIKING not in conflicts:
            conflicts.append(ConflictKind.WANTING_LIKING)
        return StateAnalysis(
            signal_count=len(state.signals),
            domains=domains,
            conflicts=tuple(conflicts),
            unresolved_conflict=bool(conflicts),
            approach_avoidance_conflict=approach_avoidance,
            wanting_liking_are_nonidentical=wanting_liking,
            adult_schema_present=SignalDomain.ADULT_SEXUALITY_SCHEMA in domains,
        )

    def preserve_domains(self, state: MotivationalState) -> tuple[SignalDomain, ...]:
        """Return explicit domains exactly as recorded; no automatic escalation occurs."""

        return tuple(signal.domain for signal in state.signals)
