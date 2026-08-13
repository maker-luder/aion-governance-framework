from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "valid-plan": ("ADEQUATE", "PLANNING_REVIEW", "ASSUMPTION_DEPENDENT_PLAN_MEETS_DECLARED_TARGET"),
    "plan-id-missing": ("INVALID", "HOLD", "PLAN_ID_MISSING"),
    "sample-size-type-invalid": ("INVALID", "HOLD", "SAMPLE_SIZE_TYPE_INVALID"),
    "non-finite-input": ("INVALID", "HOLD", "NON_FINITE_PLANNING_INPUT"),
    "prereg-reference-empty": ("UNKNOWN", "INDETERMINATE", "PREREGISTRATION_REFERENCE_EMPTY"),
    "assumption-basis-empty": ("UNKNOWN", "HOLD", "ASSUMPTION_BASIS_EMPTY"),
    "missing-effect-input": ("UNKNOWN", "HOLD", "MISSING_POWER_PLANNING_INPUT"),
    "non-positive-effect": ("INVALID", "HOLD", "NON_POSITIVE_SAMPLE_OR_EFFECT_INPUT"),
    "alpha-out-of-range": ("INVALID", "HOLD", "ALPHA_OR_TARGET_POWER_OUT_OF_RANGE"),
    "unregistered-plan": ("UNKNOWN", "INDETERMINATE", "POWER_PLAN_NOT_PREREGISTERED"),
    "underpowered-plan": ("UNDERPOWERED", "INDETERMINATE", "PLANNED_SAMPLE_BELOW_ASSUMPTION_DEPENDENT_REQUIREMENT"),
    "one-sided-plan": ("ADEQUATE", "PLANNING_REVIEW", "ASSUMPTION_DEPENDENT_PLAN_MEETS_DECLARED_TARGET"),
    "decision-serialization": ("ADEQUATE", "PLANNING_REVIEW", "ASSUMPTION_DEPENDENT_PLAN_MEETS_DECLARED_TARGET"),
    "assumption-lock-unchanged": ("ADEQUATE", "PLANNING_REVIEW", "ASSUMPTION_LOCK_UNCHANGED"),
    "assumption-change-before-effect": ("UNKNOWN", "INDETERMINATE", "ASSUMPTION_CHANGE_REQUIRES_REVIEW"),
    "assumption-change-after-effect": ("INVALID", "HOLD", "ASSUMPTION_MUTATION_AFTER_OUTCOME"),
    "assumption-plan-mismatch": ("INVALID", "HOLD", "ASSUMPTION_PLAN_ID_MISMATCH"),
    "assumption-nan": ("INVALID", "HOLD", "ASSUMPTION_NON_FINITE"),
    "missing-sample-size": ("UNKNOWN", "HOLD", "MISSING_POWER_PLANNING_INPUT"),
    "target-power-out-of-range": ("INVALID", "HOLD", "ALPHA_OR_TARGET_POWER_OUT_OF_RANGE"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_fixture.py FIXTURE")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert data["case_count"] == len(EXPECTED)
    assert data["achieved_power_calculated"] is False
    assert data["effect_observed"] is False
    assert data["model_execution"] is False
    assert data["observed_result"] == "NOT_EVALUATED"
    assert data["scientific_conclusion"] == "NOT_ESTABLISHED"
    assert data["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert data["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
    assert data["canonical_effect"] == "NONE"
    assert data["governance_effect"] == "NONE"
    assert data["deployment"] is False
    actual = {record["case_id"]: record["decision"] for record in data["records"]}
    assert set(actual) == set(EXPECTED)
    for case_id, (status, disposition, reason) in EXPECTED.items():
        decision = actual[case_id]
        assert (decision["status"], decision["disposition"], decision["reason"]) == (status, disposition, reason), (case_id, decision)
        assert decision["achieved_power"] is None
        assert decision["effect_observed"] is False
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["canonical_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
        print(case_id, status, disposition, reason)
    print("fixture assertions: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
