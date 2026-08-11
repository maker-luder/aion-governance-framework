from __future__ import annotations

import json

from aion_second_order import SecondOrderCondition, run_threshold_sweep


def main() -> None:
    points = run_threshold_sweep((0.50, 0.60, 0.70, 0.75, 0.80, 0.90))
    payload = []
    for point in points:
        summary = next(
            item
            for item in point.result.summaries
            if item.condition is SecondOrderCondition.MONITOR_PLUS_CONTROL
        )
        payload.append(
            {
                "threshold": point.verification_threshold,
                "verification_requests": summary.verification_requests,
                "trial_count": summary.trial_count,
                "observed_outcomes": summary.observed_outcomes,
                "functional_contribution_status": summary.functional_contribution_status,
                "experiment_status": point.experiment_status,
            }
        )
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
