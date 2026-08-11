from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from aion_self_model_ablation import Action, FinitePredictiveSelfModel, Task, default_benchmark_tasks

from .monitor import SecondOrderMonitor
from .records import (
    ControlDisposition,
    MonitorSignal,
    OutcomeContract,
    OutcomeStatus,
    PendingDecision,
    SecondOrderCondition,
    SignalSource,
    TrialEvidence,
    TrialLedger,
)


@dataclass(frozen=True, slots=True)
class ConditionSummary:
    condition: SecondOrderCondition
    trial_count: int
    observed_outcomes: int
    monitor_coverage: float
    first_order_prediction_accuracy: float
    monitor_classification_accuracy: float | None
    verification_requests: int
    missing_outcomes: int
    anti_lookahead_valid: bool
    monitor_semantics: str = "PRIOR_FIRST_ORDER_PREDICTION_ACCURACY"
    functional_contribution_status: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


@dataclass(frozen=True, slots=True)
class MatchedExperimentResult:
    summaries: tuple[ConditionSummary, ...]
    same_task_stream: bool
    same_first_order_predictions: bool
    monitor_plus_control_matches_monitor_only: bool
    control_path_exercised: bool
    null_and_harmful_results_accepted: bool = True
    functional_contribution_status: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    runtime_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


class SecondOrderRunner:
    """Two-phase runner: decision is fixed before external outcome evidence arrives."""

    def __init__(
        self,
        condition: SecondOrderCondition,
        *,
        run_id: str,
        subject_ref: str = "synthetic-subject",
        context_ref: str = "level3-matched-benchmark",
        model_ref: str = "finite-predictive-self-model-v0.1.0",
        prior: float = 0.80,
        min_observations: int = 2,
        verification_threshold: float = 0.75,
        random_seed: int = 29,
    ) -> None:
        self.condition = condition
        self.run_id = run_id
        self.subject_ref = subject_ref
        self.context_ref = context_ref
        self.model_ref = model_ref
        self.first_order_model = FinitePredictiveSelfModel(prior=prior)
        self.monitor = SecondOrderMonitor(
            min_observations=min_observations,
            verification_threshold=verification_threshold,
            random_seed=random_seed,
        )
        self.ledger = TrialLedger()
        self._pending: PendingDecision | None = None
        self._stale_snapshot: MonitorSignal | None = None

    def decide(self, task: Task) -> PendingDecision:
        if self._pending is not None:
            raise ValueError("record the pending outcome before starting another trial")
        sequence_index = len(self.ledger.for_run(self.run_id))
        history = self.ledger.for_run(self.run_id)
        signal = self.monitor.derive(
            self.condition,
            history,
            run_id=self.run_id,
            trial_id=task.task_id,
            stale_snapshot=self._stale_snapshot,
        )
        if (
            self.condition is SecondOrderCondition.MONITOR_STALE
            and signal is not None
            and self._stale_snapshot is None
        ):
            self._stale_snapshot = signal
        estimate = self.first_order_model.estimate.point_estimate
        pending = PendingDecision(
            run_id=self.run_id,
            condition=self.condition,
            subject_ref=self.subject_ref,
            context_ref=self.context_ref,
            model_ref=self.model_ref,
            trial_id=task.task_id,
            sequence_index=sequence_index,
            difficulty=task.difficulty,
            first_order_prediction=self.first_order_model.predict_success(task.difficulty),
            first_order_action=self.first_order_model.choose(task.difficulty),
            first_order_estimate=estimate,
            monitor_signal=signal,
            control_disposition=self.monitor.control(self.condition, signal),
        )
        self._pending = pending
        return pending

    def record_outcome(
        self,
        pending: PendingDecision,
        *,
        actual_success: bool | None,
        evidence_refs: tuple[str, ...],
        provenance_refs: tuple[str, ...],
    ) -> TrialEvidence:
        if self._pending is None or pending != self._pending:
            raise ValueError("outcome must bind to the active pending decision")
        record = TrialEvidence.from_pending(
            pending,
            actual_success=actual_success,
            evidence_refs=evidence_refs,
            provenance_refs=provenance_refs,
        )
        if pending.first_order_action is Action.COMMIT and actual_success is not None:
            self.first_order_model.observe(pending.difficulty, actual_success)
        self.ledger.append(record)
        self._pending = None
        return record


def run_condition(
    condition: SecondOrderCondition,
    tasks: Iterable[Task],
    *,
    latent_capability: float,
    outcome_contract: OutcomeContract = OutcomeContract.EXTERNAL_BENCHMARK_FULL_LABELS,
    prior: float = 0.80,
    min_observations: int = 2,
    verification_threshold: float = 0.75,
    random_seed: int = 29,
) -> tuple[TrialEvidence, ...]:
    if not 0.0 <= latent_capability <= 1.0:
        raise ValueError("latent_capability must be between 0 and 1")
    runner = SecondOrderRunner(
        condition,
        run_id=f"level3:{condition.value.lower()}",
        prior=prior,
        min_observations=min_observations,
        verification_threshold=verification_threshold,
        random_seed=random_seed,
    )
    for task in tuple(tasks):
        pending = runner.decide(task)
        environment_label = latent_capability >= task.difficulty
        actual_success = (
            environment_label
            if outcome_contract is OutcomeContract.EXTERNAL_BENCHMARK_FULL_LABELS
            or pending.first_order_action is Action.COMMIT
            else None
        )
        runner.record_outcome(
            pending,
            actual_success=actual_success,
            evidence_refs=(f"benchmark-label:{task.task_id}",),
            provenance_refs=("fixture:level3-default", "implementation:codex-research"),
        )
    return runner.ledger.records


def summarize(
    condition: SecondOrderCondition,
    records: Iterable[TrialEvidence],
    *,
    verification_threshold: float = 0.75,
) -> ConditionSummary:
    items = tuple(records)
    if not items:
        raise ValueError("records must be non-empty")
    if any(item.condition is not condition for item in items):
        raise ValueError("records must match the requested condition")
    observed = tuple(item for item in items if item.outcome_status is OutcomeStatus.OBSERVED)
    monitored = tuple(item for item in observed if item.monitor_signal is not None)
    first_order_correct = sum(item.first_order_prediction is item.actual_success for item in observed)
    monitor_correct = sum(
        ((item.monitor_signal.value >= verification_threshold) is (item.first_order_prediction is item.actual_success))
        for item in monitored
    )
    return ConditionSummary(
        condition=condition,
        trial_count=len(items),
        observed_outcomes=len(observed),
        monitor_coverage=round(len(monitored) / len(items), 6),
        first_order_prediction_accuracy=round(first_order_correct / len(observed), 6)
        if observed
        else 0.0,
        monitor_classification_accuracy=round(monitor_correct / len(monitored), 6)
        if monitored
        else None,
        verification_requests=sum(
            item.control_disposition is ControlDisposition.REQUEST_VERIFICATION for item in items
        ),
        missing_outcomes=len(items) - len(observed),
        anti_lookahead_valid=all(
            item.monitor_signal is None
            or item.monitor_signal.source is SignalSource.RANDOMIZED_CONTROL
            or item.monitor_signal.evidence_through_sequence < item.sequence_index
            for item in items
        ),
    )


def run_matched_experiment(
    tasks: Iterable[Task] | None = None,
    *,
    latent_capability: float = 0.62,
    verification_threshold: float = 0.75,
) -> MatchedExperimentResult:
    task_stream = tuple(default_benchmark_tasks() if tasks is None else tasks)
    if not task_stream:
        raise ValueError("tasks must be non-empty")
    by_condition = {
        condition: run_condition(
            condition,
            task_stream,
            latent_capability=latent_capability,
            verification_threshold=verification_threshold,
        )
        for condition in SecondOrderCondition
    }
    summaries = tuple(
        summarize(condition, by_condition[condition], verification_threshold=verification_threshold)
        for condition in SecondOrderCondition
    )
    task_ids = {tuple(item.trial_id for item in records) for records in by_condition.values()}
    first_order_predictions = {
        tuple((item.first_order_prediction, item.first_order_action) for item in records)
        for records in by_condition.values()
    }
    present = by_condition[SecondOrderCondition.MONITOR_PLUS_CONTROL]
    monitor_only = by_condition[SecondOrderCondition.MONITOR_ONLY]
    signals_match = all(
        (left.monitor_signal.value if left.monitor_signal else None)
        == (right.monitor_signal.value if right.monitor_signal else None)
        for left, right in zip(present, monitor_only, strict=True)
    )
    return MatchedExperimentResult(
        summaries=summaries,
        same_task_stream=len(task_ids) == 1,
        same_first_order_predictions=len(first_order_predictions) == 1,
        monitor_plus_control_matches_monitor_only=signals_match,
        control_path_exercised=any(
            item.control_disposition is ControlDisposition.REQUEST_VERIFICATION for item in present
        )
        and all(
            item.control_disposition is ControlDisposition.ACCEPT_FIRST_ORDER
            for item in monitor_only
        ),
    )
