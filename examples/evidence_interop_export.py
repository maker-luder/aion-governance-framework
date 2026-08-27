"""Print a deterministic inspection-only Evidence Interop manifest.

Install the component first as documented in docs/INSTALLATION.md. This example
reads an existing repository-local record, derives or accepts an exact Git head,
and prints decoded JSON bytes. It creates no output artifacts and performs no
network access, model execution, canonical writeback, or authority action.
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from aion_evidence_interop import build_bundle


def _git_head(root: Path) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True, encoding="utf-8"
    ).strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print an inspection-only Evidence Interop manifest")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument(
        "--record",
        type=Path,
        default=Path("components/aion_evidence_interop_v0.1.0/fixtures/valid_minimal.json"),
        help="repository-local evidence record",
    )
    parser.add_argument("--expected-head", default="", help="exact 40-hex Git head; defaults to HEAD")
    args = parser.parse_args(argv)

    root = args.root.resolve()
    record = args.record if args.record.is_absolute() else root / args.record
    expected_head = args.expected_head or _git_head(root)
    bundle = build_bundle(root, record, expected_head=expected_head)
    print(bundle["interop-manifest.json"].decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
