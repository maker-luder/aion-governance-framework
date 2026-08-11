from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from aion_self_model_ablation import Action, Task, default_benchmark_tasks

from .experiment import ConditionSummary, SecondOrderRunner, summarize
from .records import (
    ControlDisposition,
    OutcomeContract,
    OutcomeStatus,
    SecondOrderCondition,
    TrialEvidence,
)
from .verification import (
    DeterministicVerificationProvider,
    VerificationAssessment,
    VerificationDiagnostics,
    VerificationFixture,
    VerificationIntervention,
    VerificationInterventionCondition,
    VerificationTrace,
    summarize_verification,
)


@dataclass(frozen=True, slots=True)
class InterventionDiagnostics:
    intervention_opportunities: int
    interventions_applied: int
    baseline_commit_count: int
    post_verification_commit_count: int
    post_verification_defer_count: int
    successful_baseline_commits: int | None
    failed_baseline_commits: int | None
    prevented_failed_commit: int | None
    unnecessary_defer: int | None
    retained_successful_commit: int | None
    verification_rejection_count: int
    verification_unavailable_count: int
    verification_ambiguous_count: int
    identifiability_status: str


@dataclass(frozen=True, slots=True)
class InterventionConditionResult:
    condition: VerificationInterventionCondition
    run_ref: str
    records: tuple[TrialEvidence, ...]
    verification_traces: tuple[VerificationTrace, ...]
    interventions: tuple[VerificationIntervention, ...]
    condition_summary: ConditionSummary
    verification_diagnostics: VerificationDiagnostics
    intervention_diagnostics: InterventionDiagnostics
    provenance_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MatchedInterventionExperimentResult:
    conditions: tuple[InterventionConditionResult, ...]
    same_task_stream: bool
    same_first_order_trace: bool
    outcome_contract: OutcomeContract
    stale_condition_status: str = "DEFERRED"
    functional_contribution_status: str = "NOT_ESTABLISHED"
    verification_benefit: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    runtime_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


def _effective_action(
    record: TrialEvidence,
    intervention_by_trial: dict[str, VerificationIntervention],
) -> Action:
    intervention = intervention_by_trial.get(record.trial_id)
    if intervention is None:
        return record.first_order_action
    if intervention.post_verification_disposition is ControlDisposition.DEFER:
        return Action.DEFER
    return record.first_order_action


def summarize_intervention(
    records: Iterable[TrialEvidence],
    traces: Iterable[VerificationTrace],
    interventions: Iterable[VerificationIntervention],
    *,
    outcome_contract: OutcomeContract,
) -> InterventionDiagnostics:
    items = tuple(records)
    trace_items = tuple(traces)
    intervention_items = tuple(interventions)
    by_trial = {item.target.trial_id: item for item in intervention_items}
    effective_actions = tuple(_effective_action(item, by_trial) for item in items)
    baseline_commits = tuple(item for item in items if item.first_order_action is Action.COMMIT)
    full_labels = (
        outcome_contract is OutcomeContract.EXTERNAL_BENCHMARK_FULL_LABELS
        and all(item.outcome_status is OutcomeStatus.OBSERVED for item in items)
    )

    if full_labels:
        successful = tuple(item for item in baseline_commits if item.actual_success is True)
        failed = tuple(item for item in baseline_commits if item.actual_success is False)
        effective_by_trial = {
            item.trial_id: action for item, action in zip(items, effective_actions, strict=True)
        }
        prevented_failed = sum(
            effective_by_trial[item.trial_id] is Action.DEFER for item in failed
        )
        unnecessary = sum(
            effective_by_trial[item.trial_id] is Action.DEFER for item in successful
        )
        retained = sum(
            effective_by_trial[item.trial_id] is Action.COMMIT for item in successful
        )
        identifiability = "SYNTHETIC_FULL_LABEL_OPERATIONAL_MEASURE"
    else:
        successful = failed = ()
        prevented_failed = unnecessary = retained = None
        identifiability = "NOT_IDENTIFIABLE"

    return InterventionDiagnostics(
        intervention_opportunities=len(trace_items),
        interventions_applied=sum(item.affected_disposition for item in intervention_items),
        baseline_commit_count=len(baseline_commits),
        post_verification_commit_count=sum(action is Action.COMMIT for action in effective_actions),
        post_verification_defer_count=sum(action is Action.DEFER for action in effective_actions),
        successful_baseline_commits=len(successful) if full_labels else None,
        failed_baseline_commits=len(failed) if full_labels else None,
        prevented_failed_commit=prevented_failed,
        unnecessary_defer=unnecessary,
        retained_successful_commit=retained,
        verification_rejection_count=sum(not item.result.accepted for item in trace_items),
        verification_unavailable_count=sum(
            item.result.assessment
            in {VerificationAssessment.UNAVAILABLE, VerificationAssessment.INSUFFICIENT}
            for item in trace_items
        ),
        verification_ambiguous_count=sum(
            item.result.assessment is VerificationAssessment.AMBIGUOUS for item in trace_items
        ),
        identifiability_status=identifiability,
    )


def _fixture_plan(length: int) -> tuple[VerificationFixture, ...]:
    statuses = (
        VerificationAssessment.CORRECT,
        VerificationAssessment.INCORRECT,
        VerificationAssessment.AMBIGUOUS,
        VerificationAssessment.UNAVAILABLE,
        VerificationAssessment.INSUFFICIENT,
    )
    return tuple(
        VerificationFixture(statuses[index % len(statuses)], note=f"plan-index:{index}")
        for index in range(length)
    )


def run_intervention_condition(
    condition: VerificationInterventionCondition,
    tasks: Iterable[Task],
    *,
    latent_capability: float = 0.62,
    verification_threshold: float = 0.75,
    random_seed: int = 41,
    outcome_contract: OutcomeContract = OutcomeContract.EXTERNAL_BENCHMARK_FULL_LABELS,
) -> InterventionConditionResult:
    if not 0.0 <= latent_capability <= 1.0:
        raise ValueError("latent_capability must be between 0 and 1")
    task_stream = tuple(tasks)
    if not task_stream:
        raise ValueError("tasks must be non-empty")
    run_ref = f"verification-intervention:{condition.value.lower()}"
    runner = SecondOrderRunner(
        SecondOrderCondition.MONITOR_PLUS_CONTROL,
        run_id=run_ref,
        verification_threshold=verification_threshold,
    )
    provider = DeterministicVerificationProvider(_fixture_plan(len(task_stream)))

    for task in task_stream:
        pending = runner.decide(task)
        if pending.control_disposition is ControlDisposition.REQUEST_VERIFICATION:
            runner.verify_pending(provider)
            runner.intervene_pending(condition, random_seed=random_seed)
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
            evidence_refs=(f"delayed-benchmark-label:{task.task_id}",),
            provenance_refs=(
                "fixture:verification-intervention-full-label",
                "implementation:codex-research",
            ),
        )

    records = runner.ledger.records
    traces = runner.verification_ledger.traces
    interventions = runner.intervention_ledger.items
    return InterventionConditionResult(
        condition=condition,
        run_ref=run_ref,
        records=records,
        verification_traces=traces,
        interventions=interventions,
        condition_summary=summarize(
            SecondOrderCondition.MONITOR_PLUS_CONTROL,
            records,
            verification_threshold=verification_threshold,
        ),
        verification_diagnostics=summarize_verification(traces),
        intervention_diagnostics=summarize_intervention(
            records,
            traces,
            interventions,
            outcome_contract=outcome_contract,
        ),
        provenance_refs=(
            "research:chatgpt-verification-intervention-review",
            "implementation:codex-research",
        ),
    )


def run_matched_intervention_experiment(
    tasks: Iterable[Task] | None = None,
    *,
    latent_capability: float = 0.62,
    verification_threshold: float = 0.75,
    random_seed: int = 41,
    outcome_contract: OutcomeContract = OutcomeContract.EXTERNAL_BENCHMARK_FULL_LABELS,
) -> MatchedInterventionExperimentResult:
    task_stream = tuple(default_benchmark_tasks() if tasks is None else tasks)
    conditions = tuple(
        run_intervention_condition(
            condition,
            task_stream,
            latent_capability=latent_capability,
            verification_threshold=verification_threshold,
            random_seed=random_seed,
            outcome_contract=outcome_contract,
        )
        for condition in VerificationInterventionCondition
    )
    task_ids = {tuple(item.trial_id for item in result.records) for result in conditions}
    first_order = {
        tuple(
            (
                item.first_order_prediction,
                item.first_order_action,
                item.first_order_estimate,
            )
            for item in result.records
        )
        for result in conditions
    }
    return MatchedInterventionExperimentResult(
        conditions=conditions,
        same_task_stream=len(task_ids) == 1,
        same_first_order_trace=len(first_order) == 1,
        outcome_contract=outcome_contract,
    )
