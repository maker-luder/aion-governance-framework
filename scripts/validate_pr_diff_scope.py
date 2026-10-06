"""Fail closed when a PR diff is unexpectedly cumulative or misbased."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


@dataclass(frozen=True)
class DiffStats:
    changed_files: int
    additions: int
    deletions: int
    commits: int
    tip_changes: int

    @property
    def total_lines(self) -> int:
        return self.additions + self.deletions


class PRDiffScopeError(ValueError):
    pass


def load_policy(path: Path) -> dict[str, Any]:
    policy = json.loads(path.read_text(encoding="utf-8"))
    if policy.get("schema_version") != "1.0.0":
        raise PRDiffScopeError("unsupported PR diff policy schema")
    required = (
        "main_branch",
        "durable_branches",
        "allowed_main_pr_head_prefixes",
        "large_diff_total_line_threshold",
        "large_diff_file_threshold",
        "amplification_min_total_lines",
        "amplification_ratio_threshold",
        "large_pr_ack_marker",
        "large_pr_reason_prefix",
    )
    missing = [key for key in required if key not in policy]
    if missing:
        raise PRDiffScopeError(f"policy keys missing: {missing}")
    return policy


def evaluate_pr_scope(
    policy: dict[str, Any],
    *,
    base_ref: str,
    head_ref: str,
    base_is_ancestor: bool,
    body: str,
    stats: DiffStats,
) -> dict[str, Any]:
    if base_ref != policy["main_branch"]:
        return {
            "status": "NOT_APPLICABLE",
            "violations": [],
            "reason": "PR does not target main",
        }

    violations: list[str] = []
    durable = set(policy["durable_branches"])
    prefixes = tuple(policy["allowed_main_pr_head_prefixes"])

    if head_ref in durable and head_ref != policy["main_branch"]:
        violations.append(
            "durable research branch must not be used directly as a PR head into main"
        )
    if not head_ref.startswith(prefixes):
        violations.append("main PR head must use an approved transient branch prefix")
    if not base_is_ancestor:
        violations.append(
            "current main base must be an ancestor of the PR head; create/update a clean promotion branch"
        )

    total_lines = stats.total_lines
    large = (
        total_lines > int(policy["large_diff_total_line_threshold"])
        or stats.changed_files > int(policy["large_diff_file_threshold"])
    )
    amplified = (
        stats.commits > 1
        and total_lines >= int(policy["amplification_min_total_lines"])
        and stats.tip_changes > 0
        and total_lines / stats.tip_changes
        >= float(policy["amplification_ratio_threshold"])
    )

    ack = str(policy["large_pr_ack_marker"]) in body
    reason_prefix = re.escape(str(policy["large_pr_reason_prefix"]))
    reason_match = re.search(rf"(?m)^\s*{reason_prefix}\s*(\S.+?)\s*$", body)
    reason_present = reason_match is not None

    if (large or amplified) and not (ack and reason_present):
        violations.append(
            "unexpectedly large/cumulative PR diff requires explicit LARGE_PR_EXPECTED acknowledgement and reason"
        )

    return {
        "status": "PASS" if not violations else "FAIL",
        "violations": violations,
        "base_ref": base_ref,
        "head_ref": head_ref,
        "base_is_ancestor": base_is_ancestor,
        "changed_files": stats.changed_files,
        "additions": stats.additions,
        "deletions": stats.deletions,
        "total_lines": total_lines,
        "commits": stats.commits,
        "tip_changes": stats.tip_changes,
        "large_diff": large,
        "cumulative_amplification": amplified,
        "large_pr_acknowledged": ack and reason_present,
    }


def _git(root: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def _numstat(root: Path, revspec: str) -> tuple[int, int, int]:
    output = _git(root, "diff", "--numstat", revspec)
    files = additions = deletions = 0
    for line in output.splitlines():
        if not line.strip():
            continue
        added, removed, _path = line.split("\t", 2)
        files += 1
        if added.isdigit():
            additions += int(added)
        if removed.isdigit():
            deletions += int(removed)
    return files, additions, deletions


def collect_stats(root: Path, base_sha: str, head_sha: str) -> tuple[bool, DiffStats]:
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", base_sha, head_sha],
        cwd=root,
        check=False,
    ).returncode == 0
    merge_base = _git(root, "merge-base", base_sha, head_sha)
    changed_files, additions, deletions = _numstat(
        root, f"{merge_base}...{head_sha}"
    )
    commits = int(_git(root, "rev-list", "--count", f"{merge_base}..{head_sha}") or "0")
    tip_output = _git(root, "show", "--numstat", "--format=", head_sha)
    tip_changes = 0
    for line in tip_output.splitlines():
        if not line.strip():
            continue
        added, removed, _path = line.split("\t", 2)
        if added.isdigit():
            tip_changes += int(added)
        if removed.isdigit():
            tip_changes += int(removed)
    return ancestor, DiffStats(
        changed_files=changed_files,
        additions=additions,
        deletions=deletions,
        commits=commits,
        tip_changes=tip_changes,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--event-file", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        policy = load_policy(args.policy)
        event = json.loads(args.event_file.read_text(encoding="utf-8"))
        pull = event.get("pull_request")
        if not isinstance(pull, dict):
            print(json.dumps({"status": "NOT_APPLICABLE", "reason": "not a pull_request event"}))
            return 0
        base = pull["base"]
        head = pull["head"]
        body = pull.get("body") or ""
        base_ref = str(base["ref"])
        head_ref = str(head["ref"])
        base_sha = str(base["sha"])
        head_sha = str(head["sha"])
        ancestor, stats = collect_stats(
            args.repository_root.resolve(), base_sha, head_sha
        )
        result = evaluate_pr_scope(
            policy,
            base_ref=base_ref,
            head_ref=head_ref,
            base_is_ancestor=ancestor,
            body=body,
            stats=stats,
        )
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] in {"PASS", "NOT_APPLICABLE"} else 1
    except (PRDiffScopeError, OSError, KeyError, TypeError, ValueError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
