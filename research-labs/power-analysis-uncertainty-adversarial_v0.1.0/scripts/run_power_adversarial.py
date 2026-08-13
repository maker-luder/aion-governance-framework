from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from aion_power_analysis import PowerPlan
from aion_power_analysis_adversarial import AssumptionSnapshot, audit_assumption_lock, audit_decision_serialization, audit_power_plan


def plan(**changes: object) -> PowerPlan:
    values: dict[str, object] = {
        "plan_id": "power:1",
        "standardized_effect_bound": 0.5,
        "standard_deviation": 1.0,
        "alpha": 0.05,
        "target_power": 0.8,
        "planned_sample_size": 100,
        "two_sided": True,
        "preregistration_ref": "prereg:1",
        "assumption_basis": "prior bounded estimate",
    }
    values.update(changes)
    return PowerPlan(**values)


def run(output: Path) -> dict[str, object]:
    before = AssumptionSnapshot("power:1", 0.5, 1.0, 0.05, 0.8, True)
    cases: list[tuple[str, object]] = [
        ("valid-plan", audit_power_plan(plan())),
        ("plan-id-missing", audit_power_plan(plan(plan_id=""))),
        ("sample-size-type-invalid", audit_power_plan(plan(planned_sample_size=10.5))),
        ("non-finite-input", audit_power_plan(plan(alpha=math.nan))),
        ("prereg-reference-empty", audit_power_plan(plan(preregistration_ref=""))),
        ("assumption-basis-empty", audit_power_plan(plan(assumption_basis=" "))),
        ("missing-effect-input", audit_power_plan(plan(standardized_effect_bound=None))),
        ("non-positive-effect", audit_power_plan(plan(standardized_effect_bound=0.0))),
        ("alpha-out-of-range", audit_power_plan(plan(alpha=1.0))),
        ("unregistered-plan", audit_power_plan(plan(preregistration_ref=None))),
        ("underpowered-plan", audit_power_plan(plan(planned_sample_size=1))),
        ("one-sided-plan", audit_power_plan(plan(two_sided=False))),
        ("decision-serialization", audit_decision_serialization(plan())),
        ("assumption-lock-unchanged", audit_assumption_lock(before, before)),
        ("assumption-change-before-effect", audit_assumption_lock(before, AssumptionSnapshot("power:1", 0.4, 1.0, 0.05, 0.8, True))),
        ("assumption-change-after-effect", audit_assumption_lock(before, AssumptionSnapshot("power:1", 0.4, 1.0, 0.05, 0.8, True, observed_effect=True))),
        ("assumption-plan-mismatch", audit_assumption_lock(before, AssumptionSnapshot("power:2", 0.5, 1.0, 0.05, 0.8, True))),
        ("assumption-nan", audit_assumption_lock(before, AssumptionSnapshot("power:1", math.nan, 1.0, 0.05, 0.8, True))),
        ("missing-sample-size", audit_power_plan(plan(planned_sample_size=None))),
        ("target-power-out-of-range", audit_power_plan(plan(target_power=0.0))),
    ]
    records = []
    for case_id, audit in cases:
        decision = audit.as_dict()
        assert decision["achieved_power"] is None
        assert decision["effect_observed"] is False
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["canonical_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "power-analysis-uncertainty-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "achieved_power_calculated": False,
        "effect_observed": False,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
