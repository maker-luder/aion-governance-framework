"""Command-line entry point."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import AstraRuntime
from .errors import RuntimeCandidateError
from .models import TaskSpec


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="AION/Astra executable runtime candidate")
    result.add_argument("run", choices=["run"])
    result.add_argument("--task", type=Path, required=True)
    result.add_argument("--baseline", type=Path, required=True)
    result.add_argument("--sessions", type=Path, required=True)
    result.add_argument("--kill-switch", type=Path)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        raw = json.loads(args.task.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise RuntimeCandidateError("task JSON must be an object")
        task = TaskSpec.from_dict(raw)
        result = AstraRuntime().run(task, baseline_root=args.baseline, sessions_root=args.sessions, kill_switch=args.kill_switch)
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return 0 if result.status.value == "PASS_PENDING_OWNER_REVIEW" else 3
    except (RuntimeCandidateError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

