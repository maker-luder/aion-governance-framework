from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_prereg_integrity import (
    AnalysisClass,
    Deviation,
    InterventionPlan,
    PlannedAnalysis,
    PlannedOutcome,
    audit_plan,
)


def base_plan(**changes: object) -> InterventionPlan:
    values: dict[str, object] = {
        "plan_id": "exp-plan",
        "plan_version": "v1",
        "registered_at": 1,
        "intervention_start": 10,
        "immutable_digest": "sha256:exp-plan",
        "protocol_ref": "protocol:exp",
        "outcomes": (
            PlannedOutcome("primary", "primary outcome", True, "increase", "measure:primary"),
            PlannedOutcome("secondary", "secondary outcome", False, "increase", "measure:secondary"),
        ),
        "analyses": (
            PlannedAnalysis("confirmatory", "primary", AnalysisClass.CONFIRMATORY, "method:t", "estimand:primary", "rule:alpha"),
            PlannedAnalysis("exploratory", "secondary", AnalysisClass.EXPLORATORY, "method:describe", "estimand:secondary", "rule:describe"),
        ),
        "deviations": (),
        "report_outcome_ids": frozenset({"primary", "secondary"}),
        "report_analysis_ids": frozenset({"confirmatory", "exploratory"}),
        "exploratory_analysis_ids": frozenset({"exploratory"}),
        "all_results_reported": True,
    }
    values.update(changes)
    return InterventionPlan(**values)


def build_cases() -> list[InterventionPlan]:
    disclosed = Deviation("dev-1", "sample shortfall", 20, "recruitment ended", "reduced precision")
    switched = PlannedAnalysis("confirmatory", "switched", AnalysisClass.CONFIRMATORY, "method:t", "estimand:primary", "rule:alpha")
    return [
        base_plan(plan_id="valid-exploratory-separated"),
        base_plan(plan_id="registration-after-start", registered_at=11),
        base_plan(plan_id="outcome-switch", analyses=(switched,), report_analysis_ids=frozenset({"confirmatory"}), exploratory_analysis_ids=frozenset()),
        base_plan(plan_id="undisclosed-deviation", deviations=(Deviation("dev-hidden", "sample shortfall", None, None, None),)),
        base_plan(plan_id="disclosed-deviation", deviations=(disclosed,)),
        base_plan(plan_id="unreported-results", report_outcome_ids=frozenset({"primary"}), all_results_reported=False),
        base_plan(plan_id="exploratory-mislabeled", exploratory_analysis_ids=frozenset()),
    ]


def run(output: Path) -> dict[str, object]:
    records = []
    for plan in build_cases():
        decision = audit_plan(plan)
        records.append({"plan_id": plan.plan_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "preregistered-intervention-integrity-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "intervention_executed": False,
        "observed_outcomes": False,
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
