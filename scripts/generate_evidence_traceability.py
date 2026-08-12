from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


INDEX_RELATIVE = "docs/C0_ACCEPTANCE_EVIDENCE_INDEX_2026-08-08.md"
OUTPUT_RELATIVE = "qa/CURRENT_EVIDENCE_TRACEABILITY.json"
STATE_VALUES = {
    "AVAILABLE",
    "PARTIAL_AVAILABLE",
    "FUTURE_C_EVIDENCE",
    "OUT_OF_TREE_FINAL_EVIDENCE",
}
LOCAL_REF_PREFIXES = ("components/", "examples/", "research-labs/", "docs/", "qa/", "scripts/", "schemas/", ".github/")


@dataclass(frozen=True, slots=True)
class TraceabilityRecord:
    criterion: str
    requirement_source: str
    implementation_review_artifact: str
    test_review_method: str
    evidence_location_type: str
    evidence_state: str
    limitation_note: str
    local_refs: tuple[str, ...]
    missing_local_refs: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self) | {
            "local_refs": list(self.local_refs),
            "missing_local_refs": list(self.missing_local_refs),
        }


def _git_head(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return "UNSPECIFIED"


def _split_table_row(line: str) -> list[str]:
    return [part.strip() for part in line.strip().strip("|").split("|")]


def _backtick_refs(text: str) -> tuple[str, ...]:
    refs: list[str] = []
    for value in re.findall(r"`([^`]+)`", text):
        value = value.strip()
        if value and value not in refs:
            refs.append(value)
    return tuple(refs)


def _normalise_local_ref(value: str) -> str | None:
    value = value.strip().strip(".,;:()")
    value = value.split("::", 1)[0]
    value = value.split("#", 1)[0]
    if value.startswith(LOCAL_REF_PREFIXES):
        return value
    return None


def parse_index(root: Path) -> tuple[TraceabilityRecord, ...]:
    path = root / INDEX_RELATIVE
    if not path.is_file():
        return ()
    records: list[TraceabilityRecord] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `AC-"):
            continue
        cells = _split_table_row(line)
        if len(cells) != 7:
            continue
        refs = tuple(dict.fromkeys(ref for cell in cells[1:5] for ref in (_normalise_local_ref(x) for x in _backtick_refs(cell)) if ref))
        missing = tuple(sorted(ref for ref in refs if not (root / ref).exists()))
        records.append(
            TraceabilityRecord(
                criterion=cells[0].strip("`"),
                requirement_source=cells[1],
                implementation_review_artifact=cells[2],
                test_review_method=cells[3],
                evidence_location_type=cells[4],
                evidence_state=cells[5],
                limitation_note=cells[6],
                local_refs=refs,
                missing_local_refs=missing,
            )
        )
    return tuple(records)


def build_report(root: Path, *, target_head: str = "UNSPECIFIED") -> dict[str, Any]:
    records = parse_index(root)
    index_exists = (root / INDEX_RELATIVE).is_file()
    malformed = [
        record.criterion
        for record in records
        if any(part.strip() not in STATE_VALUES for part in record.evidence_state.split("+")) or not record.limitation_note
    ]
    missing = sorted({ref for record in records for ref in record.missing_local_refs})
    status = "PASS" if index_exists and records and not malformed and not missing else "HOLD"
    return {
        "schema_version": "0.1.0",
        "inspection_type": "EVIDENCE_TRACEABILITY_STRUCTURE_ONLY",
        "target_head": target_head,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_document": INDEX_RELATIVE,
        "criterion_count": len(records),
        "records": [record.as_dict() for record in records],
        "status": status,
        "acceptance_decision": "NOT_EVALUATED",
        "future_evidence_preserved": any(
            "FUTURE_C_EVIDENCE" in record.evidence_state or "OUT_OF_TREE_FINAL_EVIDENCE" in record.evidence_state
            for record in records
        ),
        "canonical_effect": "NONE",
        "deployment": False,
        "independent_ivv": "NOT_ACHIEVED",
        "mutation_performed": False,
        "diagnostics": {
            "index_exists": index_exists,
            "malformed_criteria": malformed,
            "missing_local_refs": missing,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an inspection-only evidence traceability artifact")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--target-head", default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    payload = build_report(root, target_head=args.target_head or _git_head(root))
    output = args.output or (root / OUTPUT_RELATIVE)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "PASS" else 10


if __name__ == "__main__":
    raise SystemExit(main())
