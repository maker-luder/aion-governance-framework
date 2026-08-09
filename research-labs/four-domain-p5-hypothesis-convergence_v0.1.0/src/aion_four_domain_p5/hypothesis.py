from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


def _require_aware(value: datetime, name: str) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError(f"{name} must be timezone-aware")


class HypothesisState(str, Enum):
    PROPOSED = "PROPOSED"
    REGISTERED = "REGISTERED"
    TESTING = "TESTING"
    SUPPORTED = "SUPPORTED"
    CHALLENGED = "CHALLENGED"
    FALSIFIED = "FALSIFIED"
    INCONCLUSIVE = "INCONCLUSIVE"
    WITHDRAWN = "WITHDRAWN"
    CLOSED = "CLOSED"


_ALLOWED: dict[HypothesisState, frozenset[HypothesisState]] = {
    HypothesisState.PROPOSED: frozenset({HypothesisState.REGISTERED, HypothesisState.WITHDRAWN}),
    HypothesisState.REGISTERED: frozenset({HypothesisState.TESTING, HypothesisState.WITHDRAWN}),
    HypothesisState.TESTING: frozenset({
        HypothesisState.SUPPORTED, HypothesisState.CHALLENGED, HypothesisState.FALSIFIED,
        HypothesisState.INCONCLUSIVE, HypothesisState.WITHDRAWN,
    }),
    HypothesisState.SUPPORTED: frozenset({
        HypothesisState.CHALLENGED, HypothesisState.FALSIFIED,
        HypothesisState.INCONCLUSIVE, HypothesisState.CLOSED,
    }),
    HypothesisState.CHALLENGED: frozenset({
        HypothesisState.SUPPORTED, HypothesisState.FALSIFIED,
        HypothesisState.INCONCLUSIVE, HypothesisState.CLOSED,
    }),
    HypothesisState.FALSIFIED: frozenset({HypothesisState.CHALLENGED, HypothesisState.CLOSED}),
    HypothesisState.INCONCLUSIVE: frozenset({
        HypothesisState.TESTING, HypothesisState.SUPPORTED, HypothesisState.CHALLENGED,
        HypothesisState.FALSIFIED, HypothesisState.CLOSED,
    }),
    HypothesisState.WITHDRAWN: frozenset({HypothesisState.CLOSED}),
    HypothesisState.CLOSED: frozenset(),
}


@dataclass(frozen=True, slots=True)
class HypothesisRecord:
    hypothesis_id: str
    statement_ref: str
    proposed_by: str
    proposed_at: datetime
    falsification_criteria_refs: tuple[str, ...]
    scope_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in ("hypothesis_id", "statement_ref", "proposed_by"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        _require_aware(self.proposed_at, "proposed_at")
        if not self.falsification_criteria_refs:
            raise ValueError("formal hypothesis requires falsification_criteria_refs")


@dataclass(frozen=True, slots=True)
class HypothesisEvent:
    event_id: str
    hypothesis_id: str
    to_state: HypothesisState
    actor_id: str
    actor_role: str
    occurred_at: datetime
    evidence_refs: tuple[str, ...]
    reason_ref: str

    def __post_init__(self) -> None:
        for name in ("event_id", "hypothesis_id", "actor_id", "actor_role", "reason_ref"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        _require_aware(self.occurred_at, "occurred_at")
        if not self.evidence_refs:
            raise ValueError("hypothesis events require evidence_refs")


@dataclass(frozen=True, slots=True)
class HypothesisProjection:
    hypothesis_id: str
    current_state: HypothesisState
    transition_history: tuple[tuple[str, str], ...]
    evidence_refs: tuple[str, ...]
    closed: bool


class HypothesisLifecycleLedger:
    """Append-only hypothesis state history. Evidence states remain revisable, never erased."""

    def __init__(self) -> None:
        self._records: dict[str, HypothesisRecord] = {}
        self._events: dict[str, HypothesisEvent] = {}
        self._by_hypothesis: dict[str, list[str]] = {}

    def create(self, record: HypothesisRecord) -> None:
        if record.hypothesis_id in self._records:
            raise ValueError(f"duplicate hypothesis_id: {record.hypothesis_id}")
        self._records[record.hypothesis_id] = record
        self._by_hypothesis[record.hypothesis_id] = []

    def append(self, event: HypothesisEvent) -> None:
        if event.event_id in self._events:
            raise ValueError(f"duplicate event_id: {event.event_id}")
        if event.hypothesis_id not in self._records:
            raise ValueError("unknown hypothesis_id")
        current = self.current_state(event.hypothesis_id)
        if event.to_state not in _ALLOWED[current]:
            raise ValueError(f"invalid transition: {current.value} -> {event.to_state.value}")
        previous_events = self.events(event.hypothesis_id)
        if previous_events and event.occurred_at < previous_events[-1].occurred_at:
            raise ValueError("events must not move backward in time")
        self._events[event.event_id] = event
        self._by_hypothesis[event.hypothesis_id].append(event.event_id)

    def current_state(self, hypothesis_id: str) -> HypothesisState:
        if hypothesis_id not in self._records:
            raise KeyError(hypothesis_id)
        events = self.events(hypothesis_id)
        return HypothesisState.PROPOSED if not events else events[-1].to_state

    def events(self, hypothesis_id: str) -> tuple[HypothesisEvent, ...]:
        return tuple(
            sorted(
                (self._events[item_id] for item_id in self._by_hypothesis.get(hypothesis_id, [])),
                key=lambda item: (item.occurred_at, item.event_id),
            )
        )

    def project(self, hypothesis_id: str) -> HypothesisProjection:
        events = self.events(hypothesis_id)
        prior = HypothesisState.PROPOSED
        history: list[tuple[str, str]] = []
        evidence: set[str] = set()
        for event in events:
            history.append((prior.value, event.to_state.value))
            evidence.update(event.evidence_refs)
            prior = event.to_state
        return HypothesisProjection(
            hypothesis_id=hypothesis_id,
            current_state=prior,
            transition_history=tuple(history),
            evidence_refs=tuple(sorted(evidence)),
            closed=prior is HypothesisState.CLOSED,
        )


class FalsificationDecision(str, Enum):
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    NOT_TRIGGERED = "NOT_TRIGGERED"
    TRIGGERED = "TRIGGERED"


@dataclass(frozen=True, slots=True)
class FalsificationCriterion:
    criterion_id: str
    hypothesis_id: str
    condition_ref: str
    preregistered_at: datetime
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("criterion_id", "hypothesis_id", "condition_ref"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        _require_aware(self.preregistered_at, "preregistered_at")
        if not self.evidence_refs:
            raise ValueError("criterion requires evidence_refs")


@dataclass(frozen=True, slots=True)
class FalsificationObservation:
    observation_id: str
    criterion_id: str
    observed_at: datetime
    triggered: bool | None
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.observation_id.strip() or not self.criterion_id.strip():
            raise ValueError("observation_id and criterion_id must be non-empty")
        _require_aware(self.observed_at, "observed_at")
        if not self.evidence_refs:
            raise ValueError("observation requires evidence_refs")


@dataclass(frozen=True, slots=True)
class FalsificationReport:
    hypothesis_id: str
    decision: FalsificationDecision
    criterion_count: int
    observed_count: int
    triggered_criteria: tuple[str, ...]
    unresolved_criteria: tuple[str, ...]


class FalsificationTracker:
    def __init__(self) -> None:
        self._criteria: dict[str, FalsificationCriterion] = {}
        self._observations: dict[str, list[FalsificationObservation]] = {}

    def add_criterion(self, criterion: FalsificationCriterion) -> None:
        if criterion.criterion_id in self._criteria:
            raise ValueError(f"duplicate criterion_id: {criterion.criterion_id}")
        self._criteria[criterion.criterion_id] = criterion
        self._observations[criterion.criterion_id] = []

    def observe(self, observation: FalsificationObservation) -> None:
        criterion = self._criteria.get(observation.criterion_id)
        if criterion is None:
            raise ValueError("unknown criterion_id")
        if observation.observed_at < criterion.preregistered_at:
            raise ValueError("observation cannot predate preregistered criterion")
        self._observations[observation.criterion_id].append(observation)

    def assess(self, hypothesis_id: str) -> FalsificationReport:
        criteria = [item for item in self._criteria.values() if item.hypothesis_id == hypothesis_id]
        if not criteria:
            return FalsificationReport(hypothesis_id, FalsificationDecision.INSUFFICIENT_EVIDENCE, 0, 0, (), ())
        triggered: list[str] = []
        unresolved: list[str] = []
        observed_count = 0
        for criterion in criteria:
            observations = sorted(
                self._observations[criterion.criterion_id],
                key=lambda item: (item.observed_at, item.observation_id),
            )
            observed_count += len(observations)
            if not observations or observations[-1].triggered is None:
                unresolved.append(criterion.criterion_id)
            elif observations[-1].triggered:
                triggered.append(criterion.criterion_id)
        if triggered:
            decision = FalsificationDecision.TRIGGERED
        elif unresolved:
            decision = FalsificationDecision.INSUFFICIENT_EVIDENCE
        else:
            decision = FalsificationDecision.NOT_TRIGGERED
        return FalsificationReport(
            hypothesis_id=hypothesis_id,
            decision=decision,
            criterion_count=len(criteria),
            observed_count=observed_count,
            triggered_criteria=tuple(sorted(triggered)),
            unresolved_criteria=tuple(sorted(unresolved)),
        )
