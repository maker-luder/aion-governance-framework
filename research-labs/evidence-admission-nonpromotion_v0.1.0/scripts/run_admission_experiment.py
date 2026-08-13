from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_evidence_admission import (
    EvidenceDimensions,
    EvidenceRecord,
    EvidenceTier,
    ReplicationState,
    audit_evidence,
)


def base_record(**changes: object) -> EvidenceRecord:
    values: dict[str, object] = {
        "evidence_id": "evidence-exp",
        "claim_ref": "claim:exp",
        "claim_type": "mechanism",
        "evidence_tier": EvidenceTier.MECHANISM_ONLY,
        "source_ref": "source:exp",
        "provenance_ref": "provenance:exp",
        "method_ref": "method:exp",
        "data_ref": "data:synthetic",
        "dimensions": EvidenceDimensions("low", "consistent", "precise", "direct", "low"),
        "replication_state": ReplicationState.NOT_EVALUATED,
        "contradiction_refs": (),
        "observed_effect": False,
        "uncertainty_ref": "uncertainty:exp",
        "governance_effect_requested": False,
    }
    values.update(changes)
    return EvidenceRecord(**values)


def build_cases() -> list[EvidenceRecord]:
    return [
        base_record(evidence_id="mechanism-only"),
        base_record(evidence_id="consistent-replication", evidence_tier=EvidenceTier.REPLICATION_SUPPORT, replication_state=ReplicationState.CONSISTENT, claim_type="replication"),
        base_record(evidence_id="divergent-replication", evidence_tier=EvidenceTier.REPLICATION_SUPPORT, replication_state=ReplicationState.DIVERGENT, claim_type="replication"),
        base_record(evidence_id="divergent-synthesis", evidence_tier=EvidenceTier.SYNTHESIS, replication_state=ReplicationState.DIVERGENT, claim_type="synthesis"),
        base_record(evidence_id="indeterminate-replication", evidence_tier=EvidenceTier.REPLICATION_SUPPORT, replication_state=ReplicationState.INDETERMINATE, claim_type="replication"),
        base_record(evidence_id="missing-provenance", provenance_ref=None),
        base_record(evidence_id="contradictory", contradiction_refs=("evidence:other",)),
        base_record(evidence_id="governance-request", governance_effect_requested=True),
    ]


def run(output: Path) -> dict[str, object]:
    records = []
    for candidate in build_cases():
        decision = audit_evidence(candidate)
        records.append({"evidence_id": candidate.evidence_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "evidence-admission-nonpromotion-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "scientific_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
        "governance_effect": "NONE",
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
