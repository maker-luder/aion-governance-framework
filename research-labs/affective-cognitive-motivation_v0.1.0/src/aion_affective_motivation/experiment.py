from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import random
from typing import Iterable

from .coupling import (
    ChannelValue,
    CoupledInternalState,
    CouplingEvent,
    CouplingPolicy,
    CouplingTransition,
    DEFAULT_COUPLING_POLICY,
    EndogenousCouplingEngine,
    InternalChannel,
    make_uniform_state,
)


@dataclass(frozen=True, slots=True)
class CouplingTrajectory:
    """Deterministic synthetic trajectory; not a psychological or phenomenal record."""

    initial_state: CoupledInternalState
    events: tuple[CouplingEvent, ...]
    states: tuple[CoupledInternalState, ...]
    transitions: tuple[CouplingTransition, ...]
    policy_label: str
    canonical_effect: str = "NONE"
    phenomenal_experience_claim: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if len(self.states) != len(self.events):
            raise ValueError("states must contain one successor per event")
        if len(self.transitions) != len(self.events):
            raise ValueError("transitions must contain one trace per event")
        if self.canonical_effect != "NONE":
            raise ValueError("trajectory cannot create canonical effect")
        if self.phenomenal_experience_claim != "NOT_ESTABLISHED":
            raise ValueError("trajectory cannot establish phenomenal experience")

    @property
    def final_state(self) -> CoupledInternalState:
        return self.states[-1] if self.states else self.initial_state

    def fingerprint(self) -> str:
        payload = {
            "policy_label": self.policy_label,
            "initial": _state_payload(self.initial_state),
            "events": [_event_payload(event) for event in self.events],
            "states": [_state_payload(state) for state in self.states],
            "transitions": [
                {
                    "predecessor": trace.predecessor_state_id,
                    "successor": trace.successor_state_id,
                    "event": trace.event_id,
                    "channels": [
                        {
                            "channel": item.channel.value,
                            "previous": item.previous,
                            "persistence": item.persistence_term,
                            "baseline": item.baseline_term,
                            "event_delta": item.event_delta,
                            "coupling_delta": item.coupling_delta,
                            "current": item.current,
                        }
                        for item in trace.channels
                    ],
                }
                for trace in self.transitions
            ],
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class MatchedTrajectoryComparison:
    left_fingerprint: str
    right_fingerprint: str
    event_inputs_matched: bool
    initial_scope_matched: bool
    per_channel_final_delta: tuple[ChannelValue, ...]
    any_state_difference: bool
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


@dataclass(frozen=True, slots=True)
class ResetRestoreAssessment:
    original_fingerprint: str
    reset_fingerprint: str
    restored_fingerprint: str
    reset_changed_trajectory: bool
    restore_reproduced_original: bool
    scientific_disposition: str = "HOLD"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


def _state_payload(state: CoupledInternalState) -> dict[str, object]:
    return {
        "state_id": state.state_id,
        "subject_ref": state.subject_ref,
        "context_ref": state.context_ref,
        "step": state.step,
        "values": {item.channel.value: item.value for item in state.values},
    }


def _event_payload(event: CouplingEvent) -> dict[str, object]:
    return {
        "event_id": event.event_id,
        "novelty": event.novelty,
        "prediction_error": event.prediction_error,
        "goal_progress": event.goal_progress,
        "social_feedback": event.social_feedback,
        "resource_pressure": event.resource_pressure,
    }


def uncoupled_policy(base: CouplingPolicy = DEFAULT_COUPLING_POLICY) -> CouplingPolicy:
    """Matched control retaining persistence/baseline/event drives but removing coupling edges."""

    return CouplingPolicy(
        persistence=base.persistence,
        baseline=base.baseline,
        edges=(),
        drives=base.drives,
    )


def ablate_source_channel(
    channel: InternalChannel,
    base: CouplingPolicy = DEFAULT_COUPLING_POLICY,
) -> CouplingPolicy:
    """Remove one channel's outgoing coupling contribution without changing event drives."""

    return CouplingPolicy(
        persistence=base.persistence,
        baseline=base.baseline,
        edges=tuple(edge for edge in base.edges if edge.source is not channel),
        drives=base.drives,
    )


def randomized_state(
    *,
    seed: int,
    state_id: str,
    subject_ref: str,
    context_ref: str,
    step: int = 0,
) -> CoupledInternalState:
    """Deterministic randomized-state negative control with an explicit seed."""

    generator = random.Random(seed)
    return CoupledInternalState(
        state_id=state_id,
        subject_ref=subject_ref,
        context_ref=context_ref,
        step=step,
        values=tuple(ChannelValue(channel, generator.random()) for channel in InternalChannel),
    )


class CouplingExperimentHarness:
    """Bounded matched-control harness for the synthetic coupling candidate.

    The harness can show whether this declared toy mechanism has a reproducible causal
    role under its own fixtures. It cannot validate a human emotion theory or establish
    felt affect, agency, consciousness, or subjectivity.
    """

    def run(
        self,
        initial_state: CoupledInternalState,
        events: Iterable[CouplingEvent],
        *,
        policy: CouplingPolicy = DEFAULT_COUPLING_POLICY,
        policy_label: str = "COUPLED_TOY_V0.1",
    ) -> CouplingTrajectory:
        frozen_events = tuple(events)
        engine = EndogenousCouplingEngine(policy)
        current = initial_state
        states: list[CoupledInternalState] = []
        transitions: list[CouplingTransition] = []
        for index, event in enumerate(frozen_events, start=1):
            current, trace = engine.step(
                current,
                event,
                successor_state_id=f"{initial_state.state_id}:{policy_label}:{index}",
            )
            states.append(current)
            transitions.append(trace)
        return CouplingTrajectory(
            initial_state=initial_state,
            events=frozen_events,
            states=tuple(states),
            transitions=tuple(transitions),
            policy_label=policy_label,
        )

    def compare(
        self,
        left: CouplingTrajectory,
        right: CouplingTrajectory,
    ) -> MatchedTrajectoryComparison:
        event_inputs_matched = tuple(_event_payload(item) for item in left.events) == tuple(
            _event_payload(item) for item in right.events
        )
        initial_scope_matched = (
            left.initial_state.subject_ref == right.initial_state.subject_ref
            and left.initial_state.context_ref == right.initial_state.context_ref
            and left.initial_state.step == right.initial_state.step
        )
        if not event_inputs_matched:
            raise ValueError("matched comparison requires identical event inputs")
        if not initial_scope_matched:
            raise ValueError("matched comparison requires identical subject/context/step scope")

        left_final = left.final_state
        right_final = right.final_state
        deltas = tuple(
            ChannelValue(channel, abs(left_final.value(channel) - right_final.value(channel)))
            for channel in InternalChannel
        )
        return MatchedTrajectoryComparison(
            left_fingerprint=left.fingerprint(),
            right_fingerprint=right.fingerprint(),
            event_inputs_matched=True,
            initial_scope_matched=True,
            per_channel_final_delta=deltas,
            any_state_difference=any(item.value > 0.0 for item in deltas),
        )

    def reset_restore(
        self,
        original_initial: CoupledInternalState,
        events: Iterable[CouplingEvent],
        *,
        reset_baseline: float = 0.50,
        policy: CouplingPolicy = DEFAULT_COUPLING_POLICY,
    ) -> ResetRestoreAssessment:
        frozen_events = tuple(events)
        original = self.run(
            original_initial,
            frozen_events,
            policy=policy,
            policy_label="ORIGINAL",
        )
        reset_initial = make_uniform_state(
            state_id=original_initial.state_id,
            subject_ref=original_initial.subject_ref,
            context_ref=original_initial.context_ref,
            step=original_initial.step,
            baseline=reset_baseline,
        )
        reset = self.run(
            reset_initial,
            frozen_events,
            policy=policy,
            policy_label="ORIGINAL",
        )
        restored = self.run(
            original_initial,
            frozen_events,
            policy=policy,
            policy_label="ORIGINAL",
        )
        return ResetRestoreAssessment(
            original_fingerprint=original.fingerprint(),
            reset_fingerprint=reset.fingerprint(),
            restored_fingerprint=restored.fingerprint(),
            reset_changed_trajectory=original.fingerprint() != reset.fingerprint(),
            restore_reproduced_original=original.fingerprint() == restored.fingerprint(),
        )
