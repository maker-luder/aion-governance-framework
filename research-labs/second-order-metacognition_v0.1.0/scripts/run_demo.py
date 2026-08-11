from __future__ import annotations

import json

from aion_second_order import run_matched_experiment


result = run_matched_experiment()
print(
    json.dumps(
        {
            "same_task_stream": result.same_task_stream,
            "same_first_order_predictions": result.same_first_order_predictions,
            "monitor_plus_control_matches_monitor_only": result.monitor_plus_control_matches_monitor_only,
            "control_path_exercised": result.control_path_exercised,
            "functional_contribution_status": result.functional_contribution_status,
            "canonical_effect": result.canonical_effect,
            "runtime_effect": result.runtime_effect,
            "subjectivity_conclusion": result.subjectivity_conclusion,
        },
        sort_keys=True,
    )
)
