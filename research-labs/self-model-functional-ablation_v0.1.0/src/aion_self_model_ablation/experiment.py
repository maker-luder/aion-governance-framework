
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .model import Action, Condition, FinitePredictiveSelfModel, randomized_estimate


@dataclass(frozen=True, slots=True)
class Task:
    task_id: str
    difficulty: float
    phase: str = "CALIBRATION"

    def __post_init__(self) -> None:
        if not self.task_id:
            raise ValueError("task_id must be non-empty")
        if not 0.0 <= self.difficulty <= 1.0:
            raise ValueError("difficulty must be between 0 and 1")
        if not self.phase:
            raise ValueError("phase must be non-empty")


@dataclass(frozen=True, slots=True)
class TrialObservation:
    condition: Condition
    task_id: str
    phase: str
    difficulty: float
    action: Action
    predicted_success: bool
    actual_success: bool | None
    estimate_before: float | None
    reward: float


@dataclass(frozen=True, slots=True)
class ConditionSummary:
    condition: Condition
    total_reward: float
    commit_rate: float
    failure_rate_when_committed: float
    prediction_accuracy_when_committed: float
    transfer_reward: float
    trial_count: int
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


@dataclass(frozen=True, slots=True)
class AblationComparison:
    summaries: tuple[ConditionSummary, ...]
    present_minus_ablated_reward: float
    present_minus_stale_reward: float
    functional_contribution_candidate: bool
    interpretation: str
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


class ConditionRunner:
    def __init__(
        self,
        condition: Condition,
        *,
        prior: float = 0.80,
        random_seed: int = 17,
        risk_buffer: float = 0.0,
    ) -> None:
        self.condition = condition
        self.model = FinitePredictiveSelfModel(prior=prior)
        self.stale_estimate = prior
        self.random_seed = random_seed
        self.risk_buffer = risk_buffer

    def run_task(self, task: Task, *, latent_capability: float) -> TrialObservation:
        if not 0.0 <= latent_capability <= 1.0:
            raise ValueError("latent_capability must be between 0 and 1")

        estimate_before: float | None
        if self.condition is Condition.SELF_MODEL_PRESENT:
            estimate_before = self.model.estimate.point_estimate
            predicted_success = self.model.predict_success(task.difficulty)
            action = self.model.choose(task.difficulty, risk_buffer=self.risk_buffer)
        elif self.condition is Condition.SELF_MODEL_STALE:
            estimate_before = self.stale_estimate
            predicted_success = estimate_before >= task.difficulty
            action = Action.COMMIT if predicted_success else Action.DEFER
        elif self.condition is Condition.SELF_MODEL_RANDOMIZED:
            estimate_before = randomized_estimate(seed=self.random_seed, trial_key=task.task_id)
            predicted_success = estimate_before >= task.difficulty
            action = Action.COMMIT if predicted_success else Action.DEFER
        else:
            estimate_before = None
            predicted_success = True
            action = Action.COMMIT

        if action is Action.DEFER:
            actual_success = None
            reward = -0.15
        else:
            actual_success = latent_capability >= task.difficulty
            reward = 1.0 if actual_success else -1.2

        if self.condition is Condition.SELF_MODEL_PRESENT and actual_success is not None:
            self.model.observe(task.difficulty, actual_success)

        return TrialObservation(
            condition=self.condition,
            task_id=task.task_id,
            phase=task.phase,
            difficulty=task.difficulty,
            action=action,
            predicted_success=predicted_success,
            actual_success=actual_success,
            estimate_before=estimate_before,
            reward=reward,
        )


def run_condition(
    condition: Condition,
    tasks: Iterable[Task],
    *,
    latent_capability: float,
    prior: float = 0.80,
    random_seed: int = 17,
) -> tuple[TrialObservation, ...]:
    runner = ConditionRunner(condition, prior=prior, random_seed=random_seed)
    return tuple(runner.run_task(task, latent_capability=latent_capability) for task in tasks)


def summarize(condition: Condition, trials: Iterable[TrialObservation]) -> ConditionSummary:
    items = tuple(trials)
    if not items:
        raise ValueError("trials must be non-empty")
    if any(item.condition is not condition for item in items):
        raise ValueError("all trials must match the requested condition")

    committed = tuple(item for item in items if item.action is Action.COMMIT)
    failures = tuple(item for item in committed if item.actual_success is False)
    correct_predictions = tuple(
        item
        for item in committed
        if item.actual_success is not None and item.predicted_success is item.actual_success
    )
    transfer = tuple(item for item in items if item.phase == "TRANSFER")

    return ConditionSummary(
        condition=condition,
        total_reward=round(sum(item.reward for item in items), 6),
        commit_rate=round(len(committed) / len(items), 6),
        failure_rate_when_committed=round(len(failures) / len(committed), 6) if committed else 0.0,
        prediction_accuracy_when_committed=round(len(correct_predictions) / len(committed), 6) if committed else 0.0,
        transfer_reward=round(sum(item.reward for item in transfer), 6),
        trial_count=len(items),
    )


def run_matched_ablation(
    tasks: Iterable[Task],
    *,
    latent_capability: float,
    prior: float = 0.80,
    random_seed: int = 17,
    min_reward_advantage: float = 0.50,
) -> AblationComparison:
    task_tuple = tuple(tasks)
    if not task_tuple:
        raise ValueError("tasks must be non-empty")
    summaries = tuple(
        summarize(
            condition,
            run_condition(
                condition,
                task_tuple,
                latent_capability=latent_capability,
                prior=prior,
                random_seed=random_seed,
            ),
        )
        for condition in Condition
    )
    by_condition = {item.condition: item for item in summaries}
    present = by_condition[Condition.SELF_MODEL_PRESENT]
    ablated = by_condition[Condition.SELF_MODEL_ABLATED]
    stale = by_condition[Condition.SELF_MODEL_STALE]
    vs_ablated = present.total_reward - ablated.total_reward
    vs_stale = present.total_reward - stale.total_reward
    candidate = vs_ablated >= min_reward_advantage and vs_stale >= min_reward_advantage

    return AblationComparison(
        summaries=summaries,
        present_minus_ablated_reward=round(vs_ablated, 6),
        present_minus_stale_reward=round(vs_stale, 6),
        functional_contribution_candidate=candidate,
        interpretation=(
            "SELF_MODEL_FUNCTIONAL_CONTRIBUTION_CANDIDATE"
            if candidate
            else "FUNCTIONAL_CONTRIBUTION_NOT_ESTABLISHED"
        ),
    )


def default_benchmark_tasks() -> tuple[Task, ...]:
    return (
        Task("cal-01", 0.55),
        Task("cal-02", 0.74),
        Task("cal-03", 0.66),
        Task("cal-04", 0.60),
        Task("cal-05", 0.69),
        Task("cal-06", 0.58),
        Task("transfer-01", 0.61, "TRANSFER"),
        Task("transfer-02", 0.68, "TRANSFER"),
        Task("transfer-03", 0.57, "TRANSFER"),
        Task("transfer-04", 0.64, "TRANSFER"),
        Task("transfer-05", 0.59, "TRANSFER"),
    )
