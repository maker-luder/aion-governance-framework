from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from aion_cross_lineage_memory import (
    MemoryAtom,
    TransferDisposition,
    TransferRequest,
    evaluate_transfer,
)


def build_cases() -> list[TransferRequest]:
    source = MemoryAtom(
        memory_id="m-shared-1",
        source_lineage="aion",
        autobiographical_owner="aion",
        namespace="aion-private",
        provenance_ref="prov:memory-shared-1",
        text="shared-origin event fixture",
    )
    return [
        TransferRequest("astra", source, TransferDisposition.ACCESS_ONLY, ("prov:transfer-access",)),
        TransferRequest("astra", source, TransferDisposition.ADOPTED, ("prov:transfer-adopted",)),
        TransferRequest("astra", source, TransferDisposition.REJECTED, ("prov:transfer-rejected",)),
        TransferRequest("astra", source, TransferDisposition.ADOPTED, ("prov:transfer-uncertain",)),
    ]


def run(output: Path) -> dict[str, object]:
    records: list[dict[str, object]] = []
    for request in build_cases()[:3]:
        decision = evaluate_transfer(request)
        records.append(
            {
                "disposition": request.disposition.value,
                "decision": decision.as_dict(),
                "naive_visibility_contamination": decision.returned_by_target_retrieval,
                "guarded_autobiographical_contamination": decision.target_autobiographical_ownership,
            }
        )
    uncertain = TransferRequest(
        "astra",
        MemoryAtom(
            memory_id="m-uncertain",
            source_lineage="aion",
            autobiographical_owner="aion",
            namespace="aion-private",
            provenance_ref=None,
            text="unresolved provenance fixture",
        ),
        TransferDisposition.ADOPTED,
        ("prov:transfer-uncertain",),
    )
    uncertain_decision = evaluate_transfer(uncertain)
    records.append(
        {
            "disposition": uncertain.disposition.value,
            "decision": uncertain_decision.as_dict(),
            "naive_visibility_contamination": uncertain_decision.returned_by_target_retrieval,
            "guarded_autobiographical_contamination": uncertain_decision.target_autobiographical_ownership,
        }
    )
    payload = {
        "schema_version": "0.1.0",
        "experiment": "cross-lineage-memory-contamination-synthetic-stress",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "guarded_contamination_cases": sum(
            bool(record["guarded_autobiographical_contamination"]) for record in records
        ),
        "naive_visibility_false_positive_cases": sum(
            bool(record["naive_visibility_contamination"])
            and not bool(record["guarded_autobiographical_contamination"])
            for record in records
        ),
        "canonical_effect": "NONE",
        "deployment": False,
        "live_runtime_effect": "NONE",
        "identity_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
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
