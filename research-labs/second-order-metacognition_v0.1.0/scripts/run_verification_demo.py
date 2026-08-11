from __future__ import annotations

import json

from aion_second_order import (
    DeterministicVerificationProvider,
    SecondOrderCondition,
    SecondOrderRunner,
    VerificationAssessment,
    VerificationFixture,
    summarize_verification,
)
from aion_self_model_ablation import Task


runner = SecondOrderRunner(SecondOrderCondition.MONITOR_PLUS_CONTROL, run_id="verification-demo")
for task, outcome in ((Task("d0", 0.50), True), (Task("d1", 0.75), False)):
    pending = runner.decide(task)
    runner.record_outcome(
        pending,
        actual_success=outcome,
        evidence_refs=(f"delayed-label:{task.task_id}",),
        provenance_refs=("fixture:verification-demo-history",),
    )

pending = runner.decide(Task("d2", 0.60))
trace = runner.verify_pending(
    DeterministicVerificationProvider(
        (VerificationFixture(VerificationAssessment.INCORRECT, note="fallible fixture"),)
    )
)
diagnostics = summarize_verification(runner.verification_ledger.traces)

print(
    json.dumps(
        {
            "request_id": trace.request.request_id,
            "provider_ref": trace.provider_ref,
            "assessment": trace.result.assessment.value if trace.result.assessment else None,
            "accepted": trace.result.accepted,
            "affected_disposition": trace.affected_disposition,
            "verification_attempts": diagnostics.verification_attempts,
            "oracle_leakage_rejections": diagnostics.oracle_leakage_rejections,
            "canonical_effect": "NONE",
            "functional_contribution_status": "NOT_ESTABLISHED",
        },
        sort_keys=True,
    )
)
