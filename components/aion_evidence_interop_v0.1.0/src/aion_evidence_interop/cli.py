from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from .canonical import InteropError
from .manifest import bundle_hashes, build_bundle, write_bundle


def _git_head(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            stderr=subprocess.STDOUT,
            timeout=10,
        ).strip()
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Export deterministic inspection-only AION evidence interoperability views"
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--expected-head", default=None)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)

    root = args.root.resolve()
    record = args.record if args.record.is_absolute() else root / args.record
    expected_head = args.expected_head or _git_head(root)

    try:
        bundle = build_bundle(root, record, expected_head=expected_head)
        write_bundle(args.output, bundle)
    except InteropError as exc:
        print(
            json.dumps(
                {
                    "status": "HOLD",
                    "error_category": exc.category,
                    "diagnostics": [str(exc)],
                    "mutation_performed": False,
                    "canonical_effect": "NONE",
                    "deployment": False,
                    "model_execution": False,
                    "network_access": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 12 if exc.category == "write_failure" else 10

    print(
        json.dumps(
            {
                "status": "PASS",
                "output": "WRITTEN",
                "artifacts": bundle_hashes(bundle),
                "mutation_performed": False,
                "canonical_effect": "NONE",
                "deployment": False,
                "model_execution": False,
                "network_access": False,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
