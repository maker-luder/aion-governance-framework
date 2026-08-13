from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED = {
    "valid-candidate": ("PASS_CANDIDATE", "REVIEW_ONLY", "MATCHED_CAUSAL_PATTERN_OBSERVED"),
    "study-id-missing": ("INVALID", "HOLD", "STUDY_ID_MISSING"),
    "non-synthetic-blocked": ("INVALID", "HOLD", "NON_SYNTHETIC_EXECUTION_NOT_PERMITTED"),
    "preregistration-missing": ("UNKNOWN", "INDETERMINATE", "PREREGISTRATION_REFERENCE_MISSING"),
    "assumption-basis-missing": ("UNKNOWN", "HOLD", "ASSUMPTION_BASIS_MISSING"),
    "observation-set-empty": ("INVALID", "HOLD", "OBSERVATION_SET_EMPTY"),
    "non-finite-score": ("INVALID", "HOLD", "SCORE_NON_FINITE_OR_INVALID"),
    "duplicate-condition": ("INVALID", "HOLD", "DUPLICATE_MATCHED_CONDITION"),
    "missing-condition": ("HOLD", "HOLD", "INCOMPLETE_MATCHED_CONDITIONS"),
    "random-control-confound": ("HOLD", "HOLD", "RANDOM_CONTROL_TOO_LARGE"),
    "directional-inconsistency": ("HOLD", "HOLD", "INTERVENTION_DIRECTION_NOT_REPLICATED"),
    "protocol-lock-unchanged": ("PASS_CANDIDATE", "REVIEW_ONLY", "PROTOCOL_LOCK_UNCHANGED"),
    "protocol-change-before-outcome": ("UNKNOWN", "INDETERMINATE", "PROTOCOL_CHANGE_REQUIRES_REVIEW"),
    "protocol-change-after-outcome": ("INVALID", "HOLD", "PROTOCOL_MUTATION_AFTER_OUTCOME"),
    "protocol-condition-incomplete": ("INVALID", "HOLD", "PROTOCOL_CONDITION_SET_INCOMPLETE"),
    "protocol-effect-invalid": ("INVALID", "HOLD", "PROTOCOL_EFFECT_BOUND_INVALID"),
    "study-batch-valid": ("PASS_CANDIDATE", "REVIEW_ONLY", "STUDY_BATCH_REVIEW_ONLY"),
    "study-batch-duplicate": ("INVALID", "HOLD", "STUDY_BATCH_DUPLICATE_ID"),
    "study-batch-empty": ("UNKNOWN", "HOLD", "STUDY_BATCH_EMPTY"),
    "replicate-id-invalid": ("INVALID", "HOLD", "REPLICATE_ID_INVALID"),
}


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_fixture.py FIXTURE")
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    assert payload["case_count"] == len(EXPECTED)
    for field, expected in {
        "model_execution": False,
        "intervention_executed": False,
        "observed_result": "NOT_EVALUATED",
        "causal_conclusion": "NOT_ESTABLISHED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "consciousness_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }.items():
        assert payload[field] == expected, (field, payload[field])
    records = {record["case_id"]: record["decision"] for record in payload["records"]}
    assert set(records) == set(EXPECTED)
    for case_id, (status, disposition, reason) in EXPECTED.items():
        decision = records[case_id]
        assert (decision["status"], decision["disposition"]) == (status, disposition), (case_id, decision)
        assert reason in decision["reasons"], (case_id, decision)
        for field, expected in {
            "synthetic_fixture": True,
            "model_execution": False,
            "intervention_executed": False,
            "observed_result": "NOT_EVALUATED",
            "causal_conclusion": "NOT_ESTABLISHED",
            "scientific_conclusion": "NOT_ESTABLISHED",
            "subjectivity_conclusion": "NOT_ESTABLISHED",
            "consciousness_conclusion": "NOT_ESTABLISHED",
            "identity_continuity_conclusion": "NOT_ESTABLISHED",
            "canonical_effect": "NONE",
            "governance_effect": "NONE",
            "deployment": False,
        }.items():
            assert decision[field] == expected, (case_id, field, decision[field])
        print(case_id, status, disposition, reason)
    print("fixture assertions: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
