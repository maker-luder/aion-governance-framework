from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_power_analysis import PowerPlan, evaluate_plan


def plan(plan_id: str, **changes: object) -> PowerPlan:
    values: dict[str, object] = {
        "plan_id": plan_id,
        "standardized_effect_bound": 0.30,
        "standard_deviation": 1.0,
        "alpha": 0.05,
        "target_power": 0.80,
        "planned_sample_size": 200,
        "two_sided": True,
        "preregistration_ref": "prereg:power-1",
        "assumption_basis": "bounded pilot estimate, deliberately conservative",
    }
    values.update(changes)
    return PowerPlan(**values)


def build_cases() -> list[PowerPlan]:
    return [
        plan("adequate"),
        plan("underpowered", planned_sample_size=10),
        plan("smaller-effect-sensitivity", standardized_effect_bound=0.15, planned_sample_size=200),
        plan("missing-input", standardized_effect_bound=None),
        plan("invalid-alpha", alpha=1.0),
        plan("unregistered", preregistration_ref=None),
    ]


def run(output: Path) -> dict[str, object]:
    records = []
    for candidate in build_cases():
        decision = evaluate_plan(candidate)
        records.append({"plan_id": candidate.plan_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "power-analysis-uncertainty-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "achieved_power_calculated": False,
        "effect_observed": False,
        "scientific_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
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
