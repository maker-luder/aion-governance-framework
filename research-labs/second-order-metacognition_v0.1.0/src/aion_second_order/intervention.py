from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from typing import Any, Iterable

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
    InterventionPolicy,
    InterventionPolicyKind,
    ProviderReliabilityProfile,
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
    verification_cost_units: int
    intervention_cost_units: int
    decision_step_count: int
    synthetic_latency_steps: int
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
    provider_profile_ref: str
    provider_sampling_seed: int | None
    policy_ref: str
    policy_kind: InterventionPolicyKind
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.run_ref.strip() or not self.provider_profile_ref.strip():
            raise ValueError("run_ref and provider_profile_ref must be non-empty")
        if not self.policy_ref.strip() or not self.provenance_refs:
            raise ValueError("policy and result provenance must be explicit")

    def to_dict(self) -> dict[str, Any]:
        summary = asdict(self.condition_summary)
        summary["condition"] = self.condition_summary.condition.value
        return {
            "schema": "aion.intervention-condition-result.v1",
            "condition": self.condition.value,
            "run_ref": self.run_ref,
            "records": [item.to_dict() for item in self.records],
            "verification_traces": [item.to_dict() for item in self.verification_traces],
            "interventions": [item.to_dict() for item in self.interventions],
            "condition_summary": summary,
            "verification_diagnostics": asdict(self.verification_diagnostics),
            "intervention_diagnostics": asdict(self.intervention_diagnostics),
            "provider_profile_ref": self.provider_profile_ref,
            "provider_sampling_seed": self.provider_sampling_seed,
            "policy_ref": self.policy_ref,
            "policy_kind": self.policy_kind.value,
            "provenance_refs": list(self.provenance_refs),
        }

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "InterventionConditionResult":
        if data.get("schema") != "aion.intervention-condition-result.v1":
            raise ValueError("unsupported intervention condition result schema")
        summary_data = dict(data["condition_summary"])
        summary_data["condition"] = SecondOrderCondition(summary_data["condition"])
        return cls(
            condition=VerificationInterventionCondition(data["condition"]),
            run_ref=str(data["run_ref"]),
            records=tuple(TrialEvidence.from_dict(item) for item in data["records"]),
            verification_traces=tuple(
                VerificationTrace.from_dict(item) for item in data["verification_traces"]
            ),
            interventions=tuple(
                VerificationIntervention.from_dict(item) for item in data["interventions"]
            ),
            condition_summary=ConditionSummary(**summary_data),
            verification_diagnostics=VerificationDiagnostics(
                **data["verification_diagnostics"]
            ),
            intervention_diagnostics=InterventionDiagnostics(
                **data["intervention_diagnostics"]
            ),
            provider_profile_ref=str(data["provider_profile_ref"]),
            provider_sampling_seed=data["provider_sampling_seed"],
            policy_ref=str(data["policy_ref"]),
            policy_kind=InterventionPolicyKind(data["policy_kind"]),
            provenance_refs=tuple(data["provenance_refs"]),
        )

    @classmethod
    def from_json(cls, payload: str) -> "InterventionConditionResult":
        data = json.loads(payload)
        if not isinstance(data, dict):
            raise ValueError("intervention condition result payload must be an object")
        return cls.from_dict(data)


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
        verification_cost_units=len(trace_items),
        intervention_cost_units=sum(
            item.condition
            in {
                VerificationInterventionCondition.APPLIED,
                VerificationInterventionCondition.RANDOMIZED,
            }
            for item in intervention_items
        ),
        decision_step_count=len(items) + len(trace_items) + len(intervention_items),
        synthetic_latency_steps=len(trace_items) + len(intervention_items),
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
    provider_profile: ProviderReliabilityProfile | None = None,
    provider_sampling_seed: int = 101,
    policy: InterventionPolicy | None = None,
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
    if provider_profile is None:
        provider = DeterministicVerificationProvider(_fixture_plan(len(task_stream)))
        provider_profile_ref = "fixture:explicit-cyclic-plan:v0.1.x"
        sampling_seed: int | None = None
    else:
        provider = DeterministicVerificationProvider.from_reliability_profile(
            provider_profile,
            len(task_stream),
            seed=provider_sampling_seed,
        )
        provider_profile_ref = provider_profile.profile_ref
        sampling_seed = provider_sampling_seed
    effective_policy = policy
    if effective_policy is None:
        from .verification import default_intervention_policy

        effective_policy = default_intervention_policy()

    for task in task_stream:
        pending = runner.decide(task)
        if pending.control_disposition is ControlDisposition.REQUEST_VERIFICATION:
            runner.verify_pending(provider)
            runner.intervene_pending(
                condition, random_seed=random_seed, policy=effective_policy
            )
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
        provider_profile_ref=provider_profile_ref,
        provider_sampling_seed=sampling_seed,
        policy_ref=effective_policy.policy_ref,
        policy_kind=effective_policy.kind,
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
    provider_profile: ProviderReliabilityProfile | None = None,
    provider_sampling_seed: int = 101,
    policy: InterventionPolicy | None = None,
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
            provider_profile=provider_profile,
            provider_sampling_seed=provider_sampling_seed,
            policy=policy,
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
