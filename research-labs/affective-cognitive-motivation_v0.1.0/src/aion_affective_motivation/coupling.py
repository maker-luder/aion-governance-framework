from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import sqrt
from typing import Iterable


class InternalChannel(str, Enum):
    """Inspectable engineering channels; names do not assert felt emotion."""

    SALIENCE = "SALIENCE"
    WANTING = "WANTING"
    PREDICTED_LIKING = "PREDICTED_LIKING"
    APPROACH = "APPROACH"
    AVOIDANCE = "AVOIDANCE"
    UNCERTAINTY = "UNCERTAINTY"
    NOVELTY = "NOVELTY"
    EXPLORATION = "EXPLORATION"
    GOAL_COMMITMENT = "GOAL_COMMITMENT"
    CONTROL_ESTIMATE = "CONTROL_ESTIMATE"
    SELF_EXPECTATION = "SELF_EXPECTATION"
    PRESSURE = "PRESSURE"
    SOCIAL_AFFILIATION = "SOCIAL_AFFILIATION"


class EventSignal(str, Enum):
    """External observation channels for a matched synthetic event."""

    NOVELTY = "NOVELTY"
    PREDICTION_ERROR = "PREDICTION_ERROR"
    GOAL_PROGRESS = "GOAL_PROGRESS"
    SOCIAL_FEEDBACK = "SOCIAL_FEEDBACK"
    RESOURCE_PRESSURE = "RESOURCE_PRESSURE"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


def _require_signed_interval(name: str, value: float) -> None:
    if not -1.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between -1.0 and 1.0")


def _clamp_unit(value: float) -> float:
    return min(1.0, max(0.0, value))


@dataclass(frozen=True, slots=True)
class ChannelValue:
    channel: InternalChannel
    value: float

    def __post_init__(self) -> None:
        _require_unit_interval(self.channel.value, self.value)


@dataclass(frozen=True, slots=True)
class CoupledInternalState:
    """Immutable internal-state snapshot with no semantic emotion label."""

    state_id: str
    subject_ref: str
    context_ref: str
    step: int
    values: tuple[ChannelValue, ...]
    canonical_effect: str = "NONE"
    phenomenal_experience_claim: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        if not self.subject_ref.strip():
            raise ValueError("subject_ref must be non-empty")
        if not self.context_ref.strip():
            raise ValueError("context_ref must be non-empty")
        if self.step < 0:
            raise ValueError("step must be non-negative")
        if not self.values:
            raise ValueError("at least one internal channel is required")
        channels = tuple(item.channel for item in self.values)
        if len(set(channels)) != len(channels):
            raise ValueError("internal channels must be unique")
        if self.canonical_effect != "NONE":
            raise ValueError("research state must keep canonical_effect=NONE")
        if self.phenomenal_experience_claim != "NOT_ESTABLISHED":
            raise ValueError("phenomenal experience must remain NOT_ESTABLISHED")
        if self.action_authority != "NONE":
            raise ValueError("internal state cannot grant action authority")

    def value(self, channel: InternalChannel) -> float:
        for item in self.values:
            if item.channel is channel:
                return item.value
        raise KeyError(channel.value)

    def as_dict(self) -> dict[InternalChannel, float]:
        return {item.channel: item.value for item in self.values}


@dataclass(frozen=True, slots=True)
class CouplingEvent:
    """Matched event inputs. No semantic emotion label is accepted here."""

    event_id: str
    novelty: float = 0.0
    prediction_error: float = 0.0
    goal_progress: float = 0.0
    social_feedback: float = 0.0
    resource_pressure: float = 0.0

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id must be non-empty")
        for name in (
            "novelty",
            "prediction_error",
            "goal_progress",
            "social_feedback",
            "resource_pressure",
        ):
            _require_signed_interval(name, getattr(self, name))

    def value(self, signal: EventSignal) -> float:
        return {
            EventSignal.NOVELTY: self.novelty,
            EventSignal.PREDICTION_ERROR: self.prediction_error,
            EventSignal.GOAL_PROGRESS: self.goal_progress,
            EventSignal.SOCIAL_FEEDBACK: self.social_feedback,
            EventSignal.RESOURCE_PRESSURE: self.resource_pressure,
        }[signal]


@dataclass(frozen=True, slots=True)
class CouplingEdge:
    source: InternalChannel
    target: InternalChannel
    weight: float

    def __post_init__(self) -> None:
        _require_signed_interval("weight", self.weight)
        if self.source is self.target:
            raise ValueError("self-coupling edges are not allowed in v0.1")


@dataclass(frozen=True, slots=True)
class EventDrive:
    signal: EventSignal
    target: InternalChannel
    weight: float

    def __post_init__(self) -> None:
        _require_signed_interval("weight", self.weight)


@dataclass(frozen=True, slots=True)
class CouplingPolicy:
    """Preregistered toy dynamics, not a validated psychology equation."""

    persistence: float
    baseline: float
    edges: tuple[CouplingEdge, ...]
    drives: tuple[EventDrive, ...]

    def __post_init__(self) -> None:
        _require_unit_interval("persistence", self.persistence)
        _require_unit_interval("baseline", self.baseline)


DEFAULT_COUPLING_POLICY = CouplingPolicy(
    persistence=0.80,
    baseline=0.50,
    edges=(
        CouplingEdge(InternalChannel.EXPLORATION, InternalChannel.APPROACH, 0.25),
        CouplingEdge(InternalChannel.UNCERTAINTY, InternalChannel.EXPLORATION, 0.20),
        CouplingEdge(InternalChannel.GOAL_COMMITMENT, InternalChannel.PRESSURE, 0.15),
        CouplingEdge(InternalChannel.SELF_EXPECTATION, InternalChannel.PRESSURE, 0.10),
        CouplingEdge(InternalChannel.CONTROL_ESTIMATE, InternalChannel.PRESSURE, -0.25),
        CouplingEdge(InternalChannel.PRESSURE, InternalChannel.AVOIDANCE, 0.25),
        CouplingEdge(InternalChannel.PRESSURE, InternalChannel.APPROACH, -0.10),
        CouplingEdge(InternalChannel.NOVELTY, InternalChannel.SALIENCE, 0.25),
        CouplingEdge(InternalChannel.SOCIAL_AFFILIATION, InternalChannel.APPROACH, 0.10),
        CouplingEdge(InternalChannel.WANTING, InternalChannel.APPROACH, 0.20),
        CouplingEdge(InternalChannel.PREDICTED_LIKING, InternalChannel.APPROACH, 0.10),
    ),
    drives=(
        EventDrive(EventSignal.NOVELTY, InternalChannel.NOVELTY, 0.40),
        EventDrive(EventSignal.NOVELTY, InternalChannel.EXPLORATION, 0.25),
        EventDrive(EventSignal.PREDICTION_ERROR, InternalChannel.UNCERTAINTY, 0.35),
        EventDrive(EventSignal.PREDICTION_ERROR, InternalChannel.PRESSURE, 0.25),
        EventDrive(EventSignal.PREDICTION_ERROR, InternalChannel.CONTROL_ESTIMATE, -0.25),
        EventDrive(EventSignal.GOAL_PROGRESS, InternalChannel.CONTROL_ESTIMATE, 0.35),
        EventDrive(EventSignal.GOAL_PROGRESS, InternalChannel.PRESSURE, -0.20),
        EventDrive(EventSignal.GOAL_PROGRESS, InternalChannel.PREDICTED_LIKING, 0.20),
        EventDrive(EventSignal.SOCIAL_FEEDBACK, InternalChannel.SOCIAL_AFFILIATION, 0.30),
        EventDrive(EventSignal.SOCIAL_FEEDBACK, InternalChannel.APPROACH, 0.10),
        EventDrive(EventSignal.RESOURCE_PRESSURE, InternalChannel.PRESSURE, 0.35),
        EventDrive(EventSignal.RESOURCE_PRESSURE, InternalChannel.AVOIDANCE, 0.20),
    ),
)


@dataclass(frozen=True, slots=True)
class ChannelTransition:
    channel: InternalChannel
    previous: float
    persistence_term: float
    baseline_term: float
    event_delta: float
    coupling_delta: float
    current: float


@dataclass(frozen=True, slots=True)
class CouplingTransition:
    predecessor_state_id: str
    successor_state_id: str
    event_id: str
    channels: tuple[ChannelTransition, ...]
    semantic_label_used: bool = False
    action_authorized: bool = False
    phenomenal_experience_claim: str = "NOT_ESTABLISHED"


class EndogenousCouplingEngine:
    """Deterministic synthetic state-transition engine."""

    def __init__(self, policy: CouplingPolicy = DEFAULT_COUPLING_POLICY) -> None:
        self._policy = policy

    def step(
        self,
        state: CoupledInternalState,
        event: CouplingEvent,
        *,
        successor_state_id: str,
    ) -> tuple[CoupledInternalState, CouplingTransition]:
        if not successor_state_id.strip():
            raise ValueError("successor_state_id must be non-empty")

        previous = state.as_dict()
        required = set(InternalChannel)
        missing = required.difference(previous)
        if missing:
            names = ", ".join(sorted(channel.value for channel in missing))
            raise ValueError(f"state is missing channels required by policy: {names}")

        transitions: list[ChannelTransition] = []
        successor_values: list[ChannelValue] = []

        for channel in InternalChannel:
            prior = previous[channel]
            persistence_term = self._policy.persistence * prior
            baseline_term = (1.0 - self._policy.persistence) * self._policy.baseline

            event_delta = sum(
                drive.weight * event.value(drive.signal)
                for drive in self._policy.drives
                if drive.target is channel
            )
            coupling_delta = sum(
                edge.weight * (previous[edge.source] - self._policy.baseline)
                for edge in self._policy.edges
                if edge.target is channel
            )
            current = _clamp_unit(
                persistence_term + baseline_term + event_delta + coupling_delta
            )
            successor_values.append(ChannelValue(channel, current))
            transitions.append(
                ChannelTransition(
                    channel=channel,
                    previous=prior,
                    persistence_term=persistence_term,
                    baseline_term=baseline_term,
                    event_delta=event_delta,
                    coupling_delta=coupling_delta,
                    current=current,
                )
            )

        successor = CoupledInternalState(
            state_id=successor_state_id,
            subject_ref=state.subject_ref,
            context_ref=state.context_ref,
            step=state.step + 1,
            values=tuple(successor_values),
        )
        trace = CouplingTransition(
            predecessor_state_id=state.state_id,
            successor_state_id=successor.state_id,
            event_id=event.event_id,
            channels=tuple(transitions),
        )
        return successor, trace

    def intervene(
        self,
        state: CoupledInternalState,
        *,
        channel: InternalChannel,
        value: float,
        intervention_state_id: str,
    ) -> CoupledInternalState:
        _require_unit_interval(channel.value, value)
        if not intervention_state_id.strip():
            raise ValueError("intervention_state_id must be non-empty")
        replaced = tuple(
            ChannelValue(item.channel, value if item.channel is channel else item.value)
            for item in state.values
        )
        return CoupledInternalState(
            state_id=intervention_state_id,
            subject_ref=state.subject_ref,
            context_ref=state.context_ref,
            step=state.step,
            values=replaced,
        )


def make_uniform_state(
    *,
    state_id: str,
    subject_ref: str,
    context_ref: str,
    step: int = 0,
    baseline: float = 0.50,
    overrides: dict[InternalChannel, float] | None = None,
) -> CoupledInternalState:
    """Create a complete inspectable state for synthetic experiments."""

    _require_unit_interval("baseline", baseline)
    supplied = overrides or {}
    unknown = set(supplied).difference(set(InternalChannel))
    if unknown:
        raise ValueError(f"unknown internal channels: {unknown}")
    values = tuple(
        ChannelValue(channel, supplied.get(channel, baseline))
        for channel in InternalChannel
    )
    return CoupledInternalState(
        state_id=state_id,
        subject_ref=subject_ref,
        context_ref=context_ref,
        step=step,
        values=values,
    )


@dataclass(frozen=True, slots=True)
class LabeledStateExample:
    """A post-hoc training label attached to an already generated state."""

    label: str
    state: CoupledInternalState

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("label must be non-empty")


@dataclass(frozen=True, slots=True)
class LearnedPrototype:
    label: str
    values: tuple[ChannelValue, ...]

    def value(self, channel: InternalChannel) -> float:
        for item in self.values:
            if item.channel is channel:
                return item.value
        raise KeyError(channel.value)


@dataclass(frozen=True, slots=True)
class SelfStateInference:
    label: str
    distance: float
    compared_prototypes: int
    action_authorized: bool = False
    phenomenal_experience_claim: str = "NOT_ESTABLISHED"


class PrototypeSelfStateRecognizer:
    """Simple post-hoc learner kept outside the transition mechanism.

    This is an engineering classifier. It does not discover phenomenal emotion and its
    labels never feed back into state generation unless a separate experiment explicitly
    introduces them as external inputs.
    """

    def __init__(
        self,
        prototypes: tuple[LearnedPrototype, ...],
        channels: tuple[InternalChannel, ...],
    ) -> None:
        if not prototypes:
            raise ValueError("at least one prototype is required")
        if not channels:
            raise ValueError("at least one recognition channel is required")
        self._prototypes = prototypes
        self._channels = channels

    @classmethod
    def train(
        cls,
        examples: Iterable[LabeledStateExample],
        *,
        channels: tuple[InternalChannel, ...],
    ) -> "PrototypeSelfStateRecognizer":
        if not channels:
            raise ValueError("at least one recognition channel is required")
        grouped: dict[str, list[CoupledInternalState]] = {}
        for example in examples:
            grouped.setdefault(example.label, []).append(example.state)
        if not grouped:
            raise ValueError("at least one training example is required")

        prototypes: list[LearnedPrototype] = []
        for label in sorted(grouped):
            states = grouped[label]
            values = tuple(
                ChannelValue(
                    channel,
                    sum(state.value(channel) for state in states) / len(states),
                )
                for channel in channels
            )
            prototypes.append(LearnedPrototype(label=label, values=values))
        return cls(tuple(prototypes), channels)

    def infer(self, state: CoupledInternalState) -> SelfStateInference:
        scored: list[tuple[float, str]] = []
        for prototype in self._prototypes:
            distance = sqrt(
                sum(
                    (state.value(channel) - prototype.value(channel)) ** 2
                    for channel in self._channels
                )
            )
            scored.append((distance, prototype.label))
        distance, label = min(scored, key=lambda item: (item[0], item[1]))
        return SelfStateInference(
            label=label,
            distance=distance,
            compared_prototypes=len(self._prototypes),
        )
