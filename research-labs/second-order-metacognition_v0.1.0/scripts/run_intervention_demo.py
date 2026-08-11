from __future__ import annotations

import json

from aion_second_order import adapt_intervention_experiment, run_matched_intervention_experiment


result = run_matched_intervention_experiment()
artifact = adapt_intervention_experiment(result, verification_threshold=0.75)
conditions = []
for item in result.conditions:
    metrics = item.intervention_diagnostics
    conditions.append(
        {
            "condition": item.condition.value,
            "opportunities": metrics.intervention_opportunities,
            "interventions_applied": metrics.interventions_applied,
            "baseline_commit_count": metrics.baseline_commit_count,
            "post_verification_commit_count": metrics.post_verification_commit_count,
            "post_verification_defer_count": metrics.post_verification_defer_count,
            "prevented_failed_commit": metrics.prevented_failed_commit,
            "unnecessary_defer": metrics.unnecessary_defer,
            "retained_successful_commit": metrics.retained_successful_commit,
            "identifiability_status": metrics.identifiability_status,
        }
    )

print(
    json.dumps(
        {
            "same_task_stream": result.same_task_stream,
            "same_first_order_trace": result.same_first_order_trace,
            "conditions": conditions,
            "engineering_pass_rate": artifact.report.pass_rate,
            "interpretation": artifact.interpretation,
            "verification_benefit": artifact.verification_benefit,
            "functional_contribution_status": artifact.functional_contribution_status,
            "canonical_effect": artifact.canonical_effect,
            "stale_condition_status": result.stale_condition_status,
        },
        sort_keys=True,
    )
)
