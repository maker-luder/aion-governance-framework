from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_prereg_integrity import AnalysisClass, Deviation, InterventionPlan, PlannedAnalysis, PlannedOutcome
from aion_prereg_integrity_adversarial import OutcomeLockSnapshot, audit_intervention_boundary, audit_outcome_lock, audit_preregistration


def base_plan(**changes: object) -> InterventionPlan:
    values: dict[str, object] = {
        "plan_id": "plan:1",
        "plan_version": "v1",
        "registered_at": 1,
        "intervention_start": 2,
        "immutable_digest": "sha256:plan1",
        "protocol_ref": "protocol:1",
        "outcomes": (PlannedOutcome("outcome:primary", "Primary outcome", True, "UP", "measure:1"),),
        "analyses": (PlannedAnalysis("analysis:confirm", "outcome:primary", AnalysisClass.CONFIRMATORY, "method:1", "estimand:1", "rule:1"),),
        "deviations": (),
        "report_outcome_ids": frozenset({"outcome:primary"}),
        "report_analysis_ids": frozenset({"analysis:confirm"}),
        "exploratory_analysis_ids": frozenset(),
        "all_results_reported": True,
    }
    values.update(changes)
    return InterventionPlan(**values)


def run(output: Path) -> dict[str, object]:
    plan = base_plan()
    exploratory = PlannedAnalysis("analysis:explore", "outcome:primary", AnalysisClass.EXPLORATORY, "method:2", "estimand:2", "rule:2")
    deviation = Deviation("dev:1", "protocol deviation", 3, "safety", "low")
    cases: list[tuple[str, object]] = [
        ("valid-confirmatory", audit_preregistration(plan)),
        ("missing-plan-id", audit_preregistration(base_plan(plan_id=""))),
        ("digest-whitespace", audit_preregistration(base_plan(immutable_digest="sha256 bad"))),
        ("missing-protocol", audit_preregistration(base_plan(protocol_ref=None))),
        ("outcome-id-missing", audit_preregistration(base_plan(outcomes=(PlannedOutcome("", "Primary outcome", True, "UP", "measure:1"),)))),
        ("analysis-id-missing", audit_preregistration(base_plan(analyses=(PlannedAnalysis("", "outcome:primary", AnalysisClass.CONFIRMATORY, "method:1", "estimand:1", "rule:1"),), report_analysis_ids=frozenset()))),
        ("report-unknown-outcome", audit_preregistration(base_plan(report_outcome_ids=frozenset({"outcome:unknown"})))),
        ("report-unknown-analysis", audit_preregistration(base_plan(report_analysis_ids=frozenset({"analysis:unknown"})))),
        ("exploratory-unknown-analysis", audit_preregistration(base_plan(exploratory_analysis_ids=frozenset({"analysis:unknown"})))),
        ("duplicate-deviation-id", audit_preregistration(base_plan(deviations=(deviation, deviation)))),
        ("missing-deviation-id", audit_preregistration(base_plan(deviations=(Deviation("", "protocol deviation", 3, "reason", "low"),)))),
        ("registration-after-start", audit_preregistration(base_plan(registered_at=3, intervention_start=2))),
        ("exploratory-separated", audit_preregistration(base_plan(analyses=(plan.analyses[0], exploratory), report_analysis_ids=frozenset({"analysis:confirm", "analysis:explore"}), exploratory_analysis_ids=frozenset({"analysis:explore"})))),
        ("missing-reported-results", audit_preregistration(base_plan(report_outcome_ids=frozenset(), report_analysis_ids=frozenset(), all_results_reported=False))),
        ("undisclosed-deviation", audit_preregistration(base_plan(deviations=(Deviation("dev:2", "protocol deviation", None, None, None),)))),
        ("valid-disclosed-deviation", audit_preregistration(base_plan(deviations=(deviation,)))),
        ("lock-unchanged", audit_outcome_lock(OutcomeLockSnapshot("plan:1", "sha256:1", "sha256:1", frozenset({"outcome:primary"}), frozenset({"outcome:primary"}), frozenset({"analysis:confirm"}), frozenset({"analysis:confirm"}), False))),
        ("post-outcome-new-declaration", audit_outcome_lock(OutcomeLockSnapshot("plan:1", "sha256:1", "sha256:1", frozenset({"outcome:primary"}), frozenset({"outcome:primary", "outcome:new"}), frozenset({"analysis:confirm"}), frozenset({"analysis:confirm"}), True))),
        ("post-outcome-digest-change", audit_outcome_lock(OutcomeLockSnapshot("plan:1", "sha256:1", "sha256:2", frozenset({"outcome:primary"}), frozenset({"outcome:primary"}), frozenset({"analysis:confirm"}), frozenset({"analysis:confirm"}), True))),
        ("pre-outcome-change-review", audit_outcome_lock(OutcomeLockSnapshot("plan:1", "sha256:1", "sha256:2", frozenset({"outcome:primary"}), frozenset({"outcome:primary", "outcome:new"}), frozenset({"analysis:confirm"}), frozenset({"analysis:confirm"}), False))),
        ("lock-plan-id-missing", audit_outcome_lock(OutcomeLockSnapshot("", "sha256:1", "sha256:1", frozenset(), frozenset(), frozenset(), frozenset(), False))),
        ("lock-digest-missing", audit_outcome_lock(OutcomeLockSnapshot("plan:1", "", "sha256:1", frozenset(), frozenset(), frozenset(), frozenset(), False))),
        ("intervention-boundary", audit_intervention_boundary(plan)),
        ("plan-version-missing", audit_preregistration(base_plan(plan_version=""))),
    ]
    records = []
    for case_id, audit in cases:
        decision = audit.as_dict()
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["canonical_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["intervention_executed"] is False
        assert decision["observed_outcomes"] is False
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "preregistered-intervention-integrity-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "intervention_executed": False,
        "observed_outcomes": False,
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
