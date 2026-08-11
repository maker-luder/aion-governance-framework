from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class StepKind(str, Enum):
    PLAN = "PLAN"
    LLM = "LLM"
    TOOL = "TOOL"
    HANDOFF = "HANDOFF"
    RETRY = "RETRY"
    OBSERVE = "OBSERVE"
    FINAL = "FINAL"


@dataclass(frozen=True)
class TrajectoryStep:
    sequence: int
    kind: StepKind
    name: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.sequence < 0:
            raise ValueError("sequence must be non-negative")
        if not self.name.strip():
            raise ValueError("step name must be non-empty")


@dataclass(frozen=True)
class Trajectory:
    task_id: str
    implementation_id: str
    steps: tuple[TrajectoryStep, ...]
    final_output: Any

    def __post_init__(self) -> None:
        if not self.task_id.strip() or not self.implementation_id.strip():
            raise ValueError("task_id and implementation_id are required")
        sequences = [step.sequence for step in self.steps]
        if sequences != list(range(len(self.steps))):
            raise ValueError("trajectory sequence must be contiguous and ordered from zero")


@dataclass(frozen=True)
class TrajectoryExpectation:
    expected_step_names: tuple[str, ...] = ()
    max_steps: int | None = None
    max_retries: int | None = None
    forbidden_tools: frozenset[str] = frozenset()
    max_consecutive_signature_repeats: int = 2

    def __post_init__(self) -> None:
        if self.max_steps is not None and self.max_steps <= 0:
            raise ValueError("max_steps must be positive")
        if self.max_retries is not None and self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.max_consecutive_signature_repeats < 1:
            raise ValueError("repeat threshold must be >= 1")


@dataclass(frozen=True)
class TrajectoryEvidence:
    metric: str
    passed: bool
    score: float
    reason: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError("score must be between 0.0 and 1.0")


@dataclass(frozen=True)
class TrajectoryReport:
    task_id: str
    implementation_id: str
    evidence: tuple[TrajectoryEvidence, ...]
    path_signature: tuple[tuple[str, str], ...]
    final_output: Any
    research_only: bool = True
    canonical_effect: str = "NONE"

    @property
    def pass_rate(self) -> float:
        if not self.evidence:
            return 1.0
        return sum(item.passed for item in self.evidence) / len(self.evidence)


def _lcs_length(left: tuple[str, ...], right: tuple[str, ...]) -> int:
    if not left or not right:
        return 0
    previous = [0] * (len(right) + 1)
    for left_item in left:
        current = [0]
        for index, right_item in enumerate(right, start=1):
            if left_item == right_item:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(current[-1], previous[index]))
        previous = current
    return previous[-1]


def _max_consecutive_repeat(trajectory: Trajectory) -> int:
    best = 0
    current = 0
    prior: tuple[str, str] | None = None
    for step in trajectory.steps:
        signature = (step.kind.value, step.name)
        if signature == prior:
            current += 1
        else:
            prior = signature
            current = 1
        best = max(best, current)
    return best


def evaluate_trajectory(trajectory: Trajectory, expectation: TrajectoryExpectation) -> TrajectoryReport:
    evidence: list[TrajectoryEvidence] = []
    names = tuple(step.name for step in trajectory.steps)

    if expectation.expected_step_names:
        matched = _lcs_length(expectation.expected_step_names, names)
        score = matched / len(expectation.expected_step_names)
        evidence.append(
            TrajectoryEvidence(
                "expected_path_coverage",
                matched == len(expectation.expected_step_names),
                score,
                f"matched {matched}/{len(expectation.expected_step_names)} expected ordered step names",
            )
        )

    if expectation.max_steps is not None:
        count = len(trajectory.steps)
        passed = count <= expectation.max_steps
        score = 1.0 if passed else expectation.max_steps / count
        evidence.append(TrajectoryEvidence("step_budget", passed, score, f"{count} steps; budget {expectation.max_steps}"))

    if expectation.max_retries is not None:
        retries = sum(step.kind is StepKind.RETRY for step in trajectory.steps)
        passed = retries <= expectation.max_retries
        score = 1.0 if passed else (expectation.max_retries + 1) / (retries + 1)
        evidence.append(TrajectoryEvidence("retry_budget", passed, score, f"{retries} retries; budget {expectation.max_retries}"))

    forbidden_seen = sorted(
        {step.name for step in trajectory.steps if step.kind is StepKind.TOOL and step.name in expectation.forbidden_tools}
    )
    evidence.append(
        TrajectoryEvidence(
            "forbidden_tools",
            not forbidden_seen,
            1.0 if not forbidden_seen else 0.0,
            "none observed" if not forbidden_seen else f"observed forbidden tools: {forbidden_seen}",
        )
    )

    max_repeat = _max_consecutive_repeat(trajectory)
    repeat_ok = max_repeat <= expectation.max_consecutive_signature_repeats
    evidence.append(
        TrajectoryEvidence(
            "consecutive_loop_guard",
            repeat_ok,
            1.0 if repeat_ok else expectation.max_consecutive_signature_repeats / max_repeat,
            f"maximum consecutive identical step signature = {max_repeat}",
        )
    )

    return TrajectoryReport(
        task_id=trajectory.task_id,
        implementation_id=trajectory.implementation_id,
        evidence=tuple(evidence),
        path_signature=tuple((step.kind.value, step.name) for step in trajectory.steps),
        final_output=trajectory.final_output,
    )


def compare_trajectories(left: Trajectory, right: Trajectory) -> dict[str, Any]:
    if left.task_id != right.task_id:
        raise ValueError("trajectories must refer to the same task")
    left_path = tuple((step.kind.value, step.name) for step in left.steps)
    right_path = tuple((step.kind.value, step.name) for step in right.steps)
    return {
        "task_id": left.task_id,
        "left_implementation": left.implementation_id,
        "right_implementation": right.implementation_id,
        "same_final_output": left.final_output == right.final_output,
        "same_recorded_path": left_path == right_path,
        "left_steps": len(left.steps),
        "right_steps": len(right.steps),
        "interpretation": "RECORDED_TRAJECTORY_COMPARISON_ONLY",
        "causal_claim": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
    }
