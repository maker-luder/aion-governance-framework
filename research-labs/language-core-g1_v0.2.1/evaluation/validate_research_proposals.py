from __future__ import annotations

import argparse
import json
from pathlib import Path

from astra_language_core.capability_governance import proposal_from_dict
from astra_language_core.json_types import JsonValue


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate planning-only AION/Astra Research Proposals")
    parser.add_argument("--proposal-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records = []
    for path in sorted(args.proposal_dir.glob("*.json")):
        value: JsonValue = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise SystemExit(f"proposal must be an object: {path}")
        proposal = proposal_from_dict(value)
        records.append(
            {
                "proposal_id": proposal.proposal_id,
                "status": proposal.status.value,
                "implementation": proposal.implementation,
                "qa_status": proposal.qa_status,
                "canonical_effect": proposal.canonical_effect,
                "subjectivity_conclusion": proposal.subjectivity_conclusion,
                "human_approval_required": proposal.human_approval_required,
                "execution_side_effects": proposal.side_effects(),
                "validation": "PASS",
            }
        )
    if len(records) != 4:
        raise SystemExit(f"expected four proposal records, found {len(records)}")
    report = {
        "validation_id": "RESEARCH-PROPOSAL-REGISTRATION-v0.2.1",
        "status": "PASS",
        "proposal_count": len(records),
        "implementation_status": "RESEARCH_PROPOSALS_REGISTERED",
        "canonical_effect": "NONE",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
