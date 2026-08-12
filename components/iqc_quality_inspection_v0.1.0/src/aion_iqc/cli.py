from __future__ import annotations

import argparse
import json
from pathlib import Path

from .inspector import CheckStatus, InspectionPolicy, inspect_repository


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspection-only AION IQC quality report")
    parser.add_argument("--root", type=Path, default=None, help="repository root; defaults to the main repository root")
    parser.add_argument("--target-head", default="UNSPECIFIED")
    parser.add_argument("--inspection-id", default="IQC-AION-001")
    parser.add_argument("--expected-targets", type=int, default=None)
    parser.add_argument("--output", type=Path, default=None, help="optional JSON output path; no output file is written by default")
    parser.add_argument("--require-traceability", action="store_true", help="require current evidence traceability artifact to pass")
    parser.add_argument("--require-component-contracts", action="store_true", help="require every tested target to have README.md and pyproject.toml")
    parser.add_argument("--require-qa-reconciliation", action="store_true", help="require current QA reconciliation to match test results and status lock")
    parser.add_argument("--require-source-state-binding", action="store_true", help="require declared target head to match actual Git HEAD with no non-QA source drift")
    args = parser.parse_args(argv)
    root = args.root.resolve() if args.root else Path(__file__).resolve().parents[4]
    report = inspect_repository(
        root,
        inspection_id=args.inspection_id,
        target_head=args.target_head,
        policy=InspectionPolicy(
            required_test_target_count=args.expected_targets,
            require_traceability=args.require_traceability,
            require_component_contracts=args.require_component_contracts,
            require_qa_reconciliation=args.require_qa_reconciliation,
            require_source_state_binding=args.require_source_state_binding,
        ),
    )
    payload = json.dumps(report.as_dict(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")
    if report.verdict is CheckStatus.FAIL:
        return 2
    if report.verdict is CheckStatus.HOLD:
        return 10
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
