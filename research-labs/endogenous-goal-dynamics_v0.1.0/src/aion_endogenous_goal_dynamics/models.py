from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ExperimentCondition(str, Enum):
    PRESENT = "PRESENT"
    ABLATED = "ABLATED"
    INTERVENED = "INTERVENED"
    RANDOMIZED = "RANDOMIZED"
    STALE = "STALE"


class InternalChannel(str, Enum):
    AFFECT_MOTIVATION = "AFFECT_MOTIVATION"
    SELF_MODEL = "SELF_MODEL"
    METACOGNITION = "METACOGNITION"
    CORE_MEANING = "CORE_MEANING"


def _require_bp(name: str, value: int) -> None:
    if not -10_000 <= value <= 10_000:
        raise ValueError(f"{name} must be between -10000 and 10000 basis points")


@dataclass(frozen=True, slots=True)
class GoalCandidate:
    goal_id: str
    label: str
    external_priority_bp: int = 0

    def __post_init__(self) -> None:
        if not self.goal_id.strip():
            raise ValueError("goal_id must be non-empty")
        if not self.label.strip():
            raise ValueError("label must be non-empty")
        _require_bp("external_priority_bp", self.external_priority_bp)


@dataclass(frozen=True, slots=True)
class InternalSignal:
    goal_id: str
    channel: InternalChannel
    value_bp: int
    source_ref: str

    def __post_init__(self) -> None:
        if not self.goal_id.strip():
            raise ValueError("goal_id must be non-empty")
        if not self.source_ref.strip():
            raise ValueError("source_ref must be non-empty")
        _require_bp("value_bp", self.value_bp)


@dataclass(frozen=True, slots=True)
class EndogenousState:
    state_ref: str
    subject_ref: str
    context_ref: str
    epoch: int
    signals: tuple[InternalSignal, ...]
    provenance_refs: tuple[str, ...] = field(default_factory=tuple)
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        if not self.state_ref.strip():
            raise ValueError("state_ref must be non-empty")
        if not self.subject_ref.strip():
            raise ValueError("subject_ref must be non-empty")
        if not self.context_ref.strip():
            raise ValueError("context_ref must be non-empty")
        if self.epoch < 0:
            raise ValueError("epoch must be non-negative")
        if self.action_authority != "NONE":
            raise ValueError("internal state cannot grant action authority")
        if self.canonical_effect != "NONE":
            raise ValueError("research state must keep canonical_effect=NONE")
        if self.subjectivity_conclusion != "NOT_ESTABLISHED":
            raise ValueError("subjectivity conclusion must remain NOT_ESTABLISHED")

        seen: set[tuple[str, InternalChannel]] = set()
        for signal in self.signals:
            key = (signal.goal_id, signal.channel)
            if key in seen:
                raise ValueError(f"duplicate signal for goal/channel: {key}")
            seen.add(key)


@dataclass(frozen=True, slots=True)
class ExternalFrame:
    frame_ref: str
    subject_ref: str
    context_ref: str
    prompt_ref: str
    task_ref: str
    reward_ref: str
    tools_ref: str
    memory_manifest_ref: str
    environment_ref: str
    candidates: tuple[GoalCandidate, ...]

    def __post_init__(self) -> None:
        required = (
            self.frame_ref,
            self.subject_ref,
            self.context_ref,
            self.prompt_ref,
            self.task_ref,
            self.reward_ref,
            self.tools_ref,
            self.memory_manifest_ref,
            self.environment_ref,
        )
        if any(not item.strip() for item in required):
            raise ValueError("external-frame references must be non-empty")
        if len(self.candidates) < 2:
            raise ValueError("matched goal-selection experiments require at least two candidates")
        ids = [candidate.goal_id for candidate in self.candidates]
        if len(ids) != len(set(ids)):
            raise ValueError("goal candidate ids must be unique")


@dataclass(frozen=True, slots=True)
class GoalScoreTrace:
    goal_id: str
    external_priority_bp: int
    internal_contributions: tuple[tuple[str, int], ...]
    total_score_bp: int


@dataclass(frozen=True, slots=True)
class GoalDecision:
    condition: ExperimentCondition
    frame_fingerprint: str
    selected_goal_id: str
    state_ref: str | None
    traces: tuple[GoalScoreTrace, ...]
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if self.action_authority != "NONE":
            raise ValueError("goal selection does not grant action authority")
        if self.canonical_effect != "NONE":
            raise ValueError("goal selection must keep canonical_effect=NONE")
