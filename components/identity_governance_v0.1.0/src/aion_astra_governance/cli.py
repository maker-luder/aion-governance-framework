from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .enums import VerificationResult
from .lineage import StateLineageLedger
from .registry import CapabilityRegistry, ProjectIdentityRegistry
from .reports import write_markdown_report


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("configuration root must be an object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Offline AION/Astra identity, lineage, capability, and fork governance"
    )
    parser.add_argument("--workspace", type=Path, default=Path("artifacts/identity_lineage"))
    commands = parser.add_subparsers(dest="command", required=True)

    identity = commands.add_parser("identity", help="Show or validate the project identity candidate")
    identity.add_argument("action", choices=("show", "validate"))
    identity.add_argument("--project-id", default="AION-ASTRA-PROJECT-001")

    lineage = commands.add_parser("lineage", help="Verify or show the state lineage ledger")
    lineage.add_argument("action", choices=("verify", "show"))
    lineage.add_argument("--state-id")

    capability = commands.add_parser("capability", help="List or verify capability artifacts")
    capability.add_argument("action", choices=("list", "verify"))
    capability.add_argument("--artifact-id")

    report = commands.add_parser("report", help="Build a non-canonical governance report")
    report.add_argument("kind", choices=("identity", "lineage"))
    report.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root: Path = args.workspace
    if args.command == "identity":
        identity_registry = ProjectIdentityRegistry(root / "identity")
        identity_record = identity_registry.load(args.project_id)
        valid = (
            identity_record.get("canonical_name") == "AION／Astra"
            and identity_record.get("subjectivity_status") == "NOT_ESTABLISHED"
        )
        shown = identity_record if args.action == "show" else {"valid": valid}
        print(json.dumps(shown, ensure_ascii=False, indent=2))
        return 0 if valid else 2
    if args.command == "lineage":
        ledger = StateLineageLedger(root / "lineage")
        if args.action == "show":
            state_record = ledger.find(args.state_id or "")
            print(json.dumps(state_record, ensure_ascii=False, indent=2))
            return 0 if state_record else 2
        result = ledger.verify(CapabilityRegistry(root / "capabilities").ids())
        print(result.value)
        return 0 if result in (VerificationResult.VALID, VerificationResult.QA_HOLD) else 2
    if args.command == "capability":
        capability_registry = CapabilityRegistry(root / "capabilities")
        if args.action == "list":
            print("\n".join(sorted(capability_registry.ids())))
            return 0
        if not args.artifact_id:
            raise SystemExit("--artifact-id is required for verify")
        valid = capability_registry.verify(args.artifact_id)
        print(json.dumps({"artifact_id": args.artifact_id, "valid": valid}))
        return 0 if valid else 2
    rows = [("canonical_effect", "NONE"), ("qa_status", "QA_HOLD"), ("subjectivity", "NOT_ESTABLISHED")]
    output = write_markdown_report(args.output, f"AION/Astra {args.kind} candidate report", rows)
    print(str(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
