from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .models import TaskBudget, TaskUsage, ToolAction
from .trajectory import evaluate_trajectory


def _object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON root must be an object")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline trajectory and upstream-agent incident governance candidate")
    command = parser.add_subparsers(dest="command", required=True)
    policy = command.add_parser("validate-policy", help="Validate candidate policy status and fail-closed defaults")
    policy.add_argument("--path", type=Path, required=True)
    trajectory = command.add_parser("evaluate-trajectory", help="Evaluate a local JSON trajectory without execution")
    trajectory.add_argument("--path", type=Path, required=True)
    trajectory.add_argument("--output", type=Path)
    return parser


def _evaluate(path: Path) -> dict[str, object]:
    raw = _object(path)
    budget_raw = raw.get("budget")
    usage_raw = raw.get("usage")
    actions_raw = raw.get("actions")
    if not isinstance(budget_raw, dict) or not isinstance(usage_raw, dict) or not isinstance(actions_raw, list):
        raise ValueError("trajectory requires budget, usage, and actions")
    budget = TaskBudget(**budget_raw)
    usage = TaskUsage(**usage_raw)
    actions = tuple(ToolAction(**item) for item in actions_raw if isinstance(item, dict))
    decision = evaluate_trajectory(actions, budget, usage)
    return {
        "decision": decision.decision.value,
        "reasons": decision.reasons,
        "triggering_sequences": decision.triggering_sequences,
        "qa_status": decision.qa_status.value,
        "canonical_effect": decision.canonical_effect,
    }


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate-policy":
        policy = _object(args.path)
        valid = (
            policy.get("policy_id") == "POL-UPSTREAM-AGENT-INCIDENT-001"
            and policy.get("status") == "PROPOSED"
            and policy.get("qa_status") == "QA_HOLD"
            and policy.get("canonical_effect") == "NONE"
        )
        print(json.dumps({"valid": valid}, indent=2))
        return 0 if valid else 2
    result = _evaluate(args.path)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        if args.output.exists():
            raise FileExistsError(f"output already exists: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(str(args.output))
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
