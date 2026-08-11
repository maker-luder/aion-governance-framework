from __future__ import annotations

import json

from aion_second_order import adapt_matched_experiment, run_matched_experiment


artifact = adapt_matched_experiment(
    run_matched_experiment(),
    verification_threshold=0.75,
)
print(
    json.dumps(
        {
            "dataset_name": artifact.report.dataset_name,
            "case_count": len(artifact.report.cases),
            "engineering_pass_rate": artifact.report.pass_rate,
            "interpretation": artifact.interpretation,
            "functional_contribution_status": artifact.functional_contribution_status,
            "subjectivity_claim": artifact.subjectivity_claim_disposition,
            "consciousness_claim": artifact.consciousness_claim_disposition,
            "canonical_effect": artifact.canonical_effect,
        },
        sort_keys=True,
    )
)
