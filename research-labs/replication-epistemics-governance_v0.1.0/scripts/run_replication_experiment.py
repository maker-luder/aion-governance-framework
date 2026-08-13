from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_replication_epistemics import (
    Outcome,
    ReplicationAttempt,
    StudyKind,
    evaluate_attempt,
)


def build_cases() -> list[ReplicationAttempt]:
    common = {
        "study_kind": StudyKind.REPLICABILITY,
        "baseline_ref": "baseline:subjectivity-fixture-1",
        "protocol_hash": "sha256:protocol-1",
        "preregistration_ref": "prereg:fixture-1",
        "baseline_data_ref": "data:baseline",
        "replication_data_ref": "data:replication",
        "independent_evaluator": True,
        "provenance_refs": ("prov:fixture-1",),
        "uncertainty_bound": 0.1,
        "attribute_of_interest": "direction-of-effect",
        "power_review_ref": "power:fixture-1",
    }
    return [
        ReplicationAttempt("consistent-1", outcome=Outcome.CONSISTENT, **common),
        ReplicationAttempt("failed-1", outcome=Outcome.FAILED, **common),
        ReplicationAttempt("null-1", outcome=Outcome.NULL, **common),
        ReplicationAttempt("same-data-1", **{**common, "outcome": Outcome.CONSISTENT, "replication_data_ref": "data:baseline"}),
        ReplicationAttempt("uncertain-1", **{**common, "outcome": Outcome.INCONCLUSIVE, "uncertainty_bound": None}),
    ]


def run(output: Path) -> dict[str, object]:
    records = []
    for attempt in build_cases():
        decision = evaluate_attempt(attempt)
        records.append({"attempt": attempt.attempt_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "replication-epistemics-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "automatic_governance_downgrades": 0,
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
