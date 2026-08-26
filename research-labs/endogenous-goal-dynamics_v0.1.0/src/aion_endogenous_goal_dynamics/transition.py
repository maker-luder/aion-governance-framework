from __future__ import annotations

from dataclasses import dataclass

from .models import EndogenousState, InternalChannel, InternalSignal, StateProvenance, canonical_hash

STATE_TRANSITION_VERSION = "EGD_STATE_TRANSITION_V0.1.0"


@dataclass(frozen=True, slots=True)
class StateEvent:
    event_ref: str
    logical_step: int
    signal_deltas: tuple[tuple[str, InternalChannel, int], ...]
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.event_ref or self.logical_step < 0 or not self.provenance_refs:
            raise ValueError("event requires ref, non-negative step, and provenance")


@dataclass(frozen=True, slots=True)
class SyntheticOutcome:
    outcome_ref: str
    selected_goal_id: str
    outcome_value_bp: int
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.outcome_ref or not self.selected_goal_id or not self.evidence_refs:
            raise ValueError("outcome requires refs and selected goal")
        if not -10_000 <= self.outcome_value_bp <= 10_000:
            raise ValueError("outcome_value_bp out of range")


@dataclass(frozen=True, slots=True)
class CorrectionEvent:
    correction_ref: str
    target_state_ref: str
    signal_deltas: tuple[tuple[str, InternalChannel, int], ...]
    reason: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not all((self.correction_ref, self.target_state_ref, self.reason)) or not self.evidence_refs:
            raise ValueError("correction requires refs, reason, and evidence")


@dataclass(frozen=True, slots=True)
class StateTransitionPolicy:
    version: str = STATE_TRANSITION_VERSION
    event_weight_bp: int = 10_000
    outcome_weight_bp: int = 2_500
    correction_weight_bp: int = 10_000

    def __post_init__(self) -> None:
        for value in (self.event_weight_bp, self.outcome_weight_bp, self.correction_weight_bp):
            if not 0 <= value <= 10_000:
                raise ValueError("transition weights must be between 0 and 10000")


@dataclass(frozen=True, slots=True)
class TransitionContribution:
    goal_id: str
    channel: InternalChannel
    prior_value_bp: int
    event_delta_bp: int
    outcome_delta_bp: int
    correction_delta_bp: int
    next_value_bp: int


@dataclass(frozen=True, slots=True)
class StateTransitionTrace:
    transition_id: str
    version: str
    predecessor_state_ref: str
    successor_state_ref: str
    event_ref: str
    outcome_ref: str
    correction_ref: str
    contributions: tuple[TransitionContribution, ...]
    evidence_refs: tuple[str, ...]
    state_transition_is_memory_writeback: bool = False
    model_weight_update: bool = False
    canonical_writeback: bool = False
    action_authority: str = "NONE"

    @property
    def fingerprint(self) -> str:
        return canonical_hash(self)


@dataclass(frozen=True, slots=True)
class StateTransition:
    predecessor: EndogenousState
    successor: EndogenousState
    trace: StateTransitionTrace


class DeterministicStateTransitionPolicy:
    def __init__(self, policy: StateTransitionPolicy | None = None) -> None:
        self.policy = policy or StateTransitionPolicy()

    @staticmethod
    def _weighted(value: int, weight: int) -> int:
        product = value * weight
        return product // 10_000 if product >= 0 else -((-product) // 10_000)

    def transition(
        self,
        state: EndogenousState,
        event: StateEvent,
        outcome: SyntheticOutcome,
        correction: CorrectionEvent,
        *,
        timestamp: str,
    ) -> StateTransition:
        if event.logical_step != state.logical_step + 1:
            raise ValueError("invalid state predecessor or non-sequential logical step")
        if correction.target_state_ref != state.state_id:
            raise ValueError("correction target does not match predecessor state")
        keys = {(signal.goal_id, signal.channel) for signal in state.signals}
        keys.update((goal_id, channel) for goal_id, channel, _ in event.signal_deltas)
        keys.update((goal_id, channel) for goal_id, channel, _ in correction.signal_deltas)
        keys.add((outcome.selected_goal_id, InternalChannel.GOAL_COMMITMENT))
        keys.add((outcome.selected_goal_id, InternalChannel.PREDICTION_ERROR))

        prior = {(signal.goal_id, signal.channel): signal for signal in state.signals}
        event_map = {(goal_id, channel): value for goal_id, channel, value in event.signal_deltas}
        correction_map = {(goal_id, channel): value for goal_id, channel, value in correction.signal_deltas}
        if len(event_map) != len(event.signal_deltas) or len(correction_map) != len(correction.signal_deltas):
            raise ValueError("conflicting duplicate transition deltas")

        contributions: list[TransitionContribution] = []
        next_signals: list[InternalSignal] = []
        for goal_id, channel in sorted(keys, key=lambda item: (item[0], item[1].value)):
            previous = prior.get((goal_id, channel))
            prior_value = 0 if previous is None else previous.value_bp
            event_delta = self._weighted(event_map.get((goal_id, channel), 0), self.policy.event_weight_bp)
            correction_delta = self._weighted(
                correction_map.get((goal_id, channel), 0), self.policy.correction_weight_bp
            )
            outcome_delta = 0
            if goal_id == outcome.selected_goal_id and channel == InternalChannel.GOAL_COMMITMENT:
                outcome_delta = self._weighted(outcome.outcome_value_bp, self.policy.outcome_weight_bp)
            elif goal_id == outcome.selected_goal_id and channel == InternalChannel.PREDICTION_ERROR:
                outcome_delta = self._weighted(-outcome.outcome_value_bp, self.policy.outcome_weight_bp)
            next_value = max(-10_000, min(10_000, prior_value + event_delta + outcome_delta + correction_delta))
            contributions.append(
                TransitionContribution(
                    goal_id=goal_id,
                    channel=channel,
                    prior_value_bp=prior_value,
                    event_delta_bp=event_delta,
                    outcome_delta_bp=outcome_delta,
                    correction_delta_bp=correction_delta,
                    next_value_bp=next_value,
                )
            )
            next_signals.append(
                InternalSignal(
                    goal_id=goal_id,
                    channel=channel,
                    value_bp=next_value,
                    source_ref=f"transition:{state.state_id}:{event.event_ref}",
                    evidence_refs=tuple(sorted({*event.provenance_refs, *outcome.evidence_refs, *correction.evidence_refs})),
                )
            )

        evidence_refs = tuple(sorted({*event.provenance_refs, *outcome.evidence_refs, *correction.evidence_refs}))
        successor_material = {
            "predecessor": state.fingerprint,
            "event": canonical_hash(event),
            "outcome": canonical_hash(outcome),
            "correction": canonical_hash(correction),
            "policy": canonical_hash(self.policy),
            "signals": next_signals,
        }
        successor_id = f"state:{canonical_hash(successor_material)[:24]}"
        successor = EndogenousState(
            state_id=successor_id,
            subject_ref=state.subject_ref,
            context_ref=state.context_ref,
            episode_index=state.episode_index + 1,
            predecessor_state_ref=state.state_id,
            logical_step=event.logical_step,
            timestamp=timestamp,
            provenance=StateProvenance(
                created_by=self.policy.version,
                source_refs=(state.state_id, event.event_ref, outcome.outcome_ref, correction.correction_ref),
                evidence_refs=evidence_refs,
                event_ref=event.event_ref,
                outcome_ref=outcome.outcome_ref,
                correction_ref=correction.correction_ref,
            ),
            signals=tuple(next_signals),
        )
        trace_material = (state.state_id, successor.state_id, event.event_ref, outcome.outcome_ref, correction.correction_ref)
        trace = StateTransitionTrace(
            transition_id=f"transition:{canonical_hash(trace_material)[:24]}",
            version=self.policy.version,
            predecessor_state_ref=state.state_id,
            successor_state_ref=successor.state_id,
            event_ref=event.event_ref,
            outcome_ref=outcome.outcome_ref,
            correction_ref=correction.correction_ref,
            contributions=tuple(contributions),
            evidence_refs=evidence_refs,
        )
        return StateTransition(predecessor=state, successor=successor, trace=trace)


class AppendOnlyTransitionLedger:
    def __init__(self) -> None:
        self._transitions: list[StateTransition] = []
        self._ids: set[str] = set()

    @property
    def transitions(self) -> tuple[StateTransition, ...]:
        return tuple(self._transitions)

    def append(self, transition: StateTransition) -> None:
        if transition.trace.transition_id in self._ids:
            raise ValueError("duplicate transition evidence")
        if transition.predecessor.state_id != transition.trace.predecessor_state_ref:
            raise ValueError("transition trace predecessor mismatch")
        if transition.successor.state_id != transition.trace.successor_state_ref:
            raise ValueError("transition trace successor mismatch")
        if self._transitions:
            previous = self._transitions[-1]
            if transition.predecessor.state_id != previous.successor.state_id:
                raise ValueError("append-only transition chain discontinuity")
        self._transitions.append(transition)
        self._ids.add(transition.trace.transition_id)
