from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

GOVERNED_QA_MUTATION_PATHS = frozenset(
    {
        "qa/CURRENT_TEST_RESULTS.json",
        "qa/CURRENT_RELEASE_STATUS_LOCK.json",
        "qa/TEST_RESULTS.md",
        "qa/CURRENT_QA_RECONCILIATION.json",
        "qa/CURRENT_COVERAGE_RESULTS.json",
        "qa/CURRENT_COVERAGE_EVIDENCE.json",
        "qa/COVERAGE_REPORT.md",
        "qa/CURRENT_EVIDENCE_TRACEABILITY.json",
        "qa/IQC_REPORT.json",
    }
)


def _git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=root, text=True, stderr=subprocess.STDOUT
    ).strip()


def _paths(root: Path, *args: str) -> set[str]:
    output = _git(root, *args)
    return {line.strip() for line in output.splitlines() if line.strip()}


def inspect_source_state(root: Path, declared_head: str) -> dict[str, Any]:
    try:
        actual_head = _git(root, "rev-parse", "HEAD")
        tree_sha = _git(root, "rev-parse", "HEAD^{tree}")
        staged = _paths(root, "diff", "--cached", "--name-only")
        changed = _paths(root, "diff", "--name-only", "HEAD")
        untracked = _paths(root, "ls-files", "--others", "--exclude-standard")
    except (OSError, subprocess.CalledProcessError) as exc:
        return {
            "status": "HOLD",
            "reason": f"git source state cannot be reconstructed: {exc}",
            "declared_head": declared_head,
            "canonical_effect": "NONE",
            "mutation_performed": False,
        }

    dirty = changed | untracked
    source_dirty = sorted(path for path in dirty if path not in GOVERNED_QA_MUTATION_PATHS)
    governed_qa = sorted(dirty & GOVERNED_QA_MUTATION_PATHS)
    reasons: list[str] = []
    if declared_head == "UNSPECIFIED":
        reasons.append("declared target head is unspecified")
    elif actual_head != declared_head:
        reasons.append(f"declared head {declared_head} differs from actual Git HEAD {actual_head}")
    if staged:
        reasons.append("staged changes are present: " + ", ".join(sorted(staged)))
    if source_dirty:
        reasons.append(
            "non-QA working-tree drift is present: " + ", ".join(source_dirty)
        )

    return {
        "schema_version": "0.1.0",
        "check_id": "IQC-SRC-001",
        "status": "HOLD" if reasons else "PASS",
        "declared_head": declared_head,
        "actual_head": actual_head,
        "source_tree_sha": tree_sha,
        "staged_paths": sorted(staged),
        "source_dirty_paths": source_dirty,
        "governed_qa_mutation_paths": governed_qa,
        "reason": "; ".join(reasons) if reasons else "declared head matches actual Git HEAD and no non-QA source drift is present",
        "canonical_effect": "NONE",
        "deployment": False,
        "independent_ivv": "NOT_ACHIEVED",
        "mutation_performed": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fail-closed AION source-state binding check")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--expected-head", default="UNSPECIFIED")
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    payload = inspect_source_state(args.root.resolve(), args.expected_head)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if payload["status"] == "PASS" else 10


if __name__ == "__main__":
    raise SystemExit(main())
