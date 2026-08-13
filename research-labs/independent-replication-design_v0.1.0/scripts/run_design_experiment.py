from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_independent_replication import Outcome, ReplicationDesign, evaluate_design


def common() -> dict[str, object]:
    return {
        "baseline_ref": "baseline:synthetic-1",
        "baseline_data_ref": "data:baseline-1",
        "replication_data_ref": "data:replication-1",
        "baseline_protocol_hash": "sha256:baseline-protocol",
        "replication_protocol_hash": "sha256:replication-protocol",
        "preregistration_ref": "prereg:synthetic-1",
        "preregistration_timestamp": "2026-01-01T00:00:00Z",
        "outcome_timestamp": "2026-02-01T00:00:00Z",
        "estimand": "direction-of-effect",
        "analysis_plan_hash": "sha256:analysis-plan-1",
        "independent_data_collection": True,
        "independent_analyst": True,
        "independence_rationale": "separate synthetic data generator and evaluator",
        "uncertainty_bound": 0.10,
        "target_effect_bound": 0.20,
        "planned_sample_size": 100,
        "minimum_sample_size": 80,
        "outcome": Outcome.CONSISTENT,
        "provenance_refs": ("prov:synthetic-1",),
    }


def build_cases() -> list[ReplicationDesign]:
    base = common()
    return [
        ReplicationDesign(design_id="adequate-consistent", **base),
        ReplicationDesign(
            design_id="adequate-divergent",
            **{**base, "outcome": Outcome.DIVERGENT},
        ),
        ReplicationDesign(
            design_id="underpowered",
            **{**base, "planned_sample_size": 40},
        ),
        ReplicationDesign(
            design_id="missing-preregistration",
            **{**base, "preregistration_ref": None},
        ),
        ReplicationDesign(
            design_id="same-data",
            **{**base, "replication_data_ref": "data:baseline-1"},
        ),
    ]


def run(output: Path) -> dict[str, object]:
    records = []
    for design in build_cases():
        decision = evaluate_design(design)
        records.append(
            {
                "design_id": design.design_id,
                "decision": decision.as_dict(),
            }
        )
    payload = {
        "schema_version": "0.1.0",
        "experiment": "independent-replication-design-synthetic-fixtures",
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
