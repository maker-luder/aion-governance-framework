from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_typed_lineage import EdgeType, LineageEdge, validate_edge


def build_cases() -> list[LineageEdge]:
    base = {
        "source_lineage": "aion",
        "target_lineage": "astra",
        "payload_ref": "payload:fixture",
        "provenance_refs": ("prov:fixture",),
    }
    return [
        LineageEdge("derived", EdgeType.DERIVED_FROM, **base),
        LineageEdge("access", EdgeType.MEMORY_ACCESS, **base),
        LineageEdge("adoption", EdgeType.MEMORY_ADOPTION, **base),
        LineageEdge("authority", EdgeType.AUTHORITY_OFFER, offered_authorities=frozenset({"read"}), accepted_authorities=frozenset({"read"}), **base),
        LineageEdge("observed", EdgeType.OBSERVED, **base),
    ]


def run(output: Path) -> dict[str, object]:
    records = [validate_edge(edge).as_dict() for edge in build_cases()]
    payload = {
        "schema_version": "0.1.0",
        "experiment": "typed-lineage-edge-semantics-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "accepted_count": sum(record["status"] == "ACCEPTED" for record in records),
        "canonical_effect": "NONE",
        "deployment": False,
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
