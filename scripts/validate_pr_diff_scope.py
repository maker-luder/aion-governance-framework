"""Fail closed when a PR diff is unexpectedly cumulative or misbased."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


SHA40 = re.compile(r"[0-9a-f]{40}")


@dataclass(frozen=True)
class DiffStats:
    changed_files: int
    additions: int
    deletions: int
    commits: int

    @property
    def total_lines(self) -> int:
        return self.additions + self.deletions


class PRDiffScopeError(ValueError):
    pass


def _require_nonempty_string(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PRDiffScopeError(f"{name} must be a non-empty string")
    return value


def load_policy(path: Path) -> dict[str, Any]:
    policy = json.loads(path.read_text(encoding="utf-8"))
    if policy.get("schema_version") != "1.1.0":
        raise PRDiffScopeError("unsupported PR diff policy schema")

    repository = _require_nonempty_string(policy.get("repository"), "repository")
    if repository.count("/") != 1:
        raise PRDiffScopeError("repository must use owner/name form")

    durable = policy.get("durable_branches")
    if (
        not isinstance(durable, list)
        or not durable
        or any(not isinstance(item, str) or not item for item in durable)
        or len(durable) != len(set(durable))
        or "main" not in durable
    ):
        raise PRDiffScopeError("durable_branches must be unique and include main")

    prefixes = policy.get("allowed_transient_head_prefixes")
    if (
        not isinstance(prefixes, list)
        or not prefixes
        or any(not isinstance(item, str) or not item.endswith("/") for item in prefixes)
        or len(prefixes) != len(set(prefixes))
    ):
        raise PRDiffScopeError(
            "allowed_transient_head_prefixes must be unique path prefixes"
        )

    if policy.get("require_same_repository_head") is not True:
        raise PRDiffScopeError("same-repository PR heads must be required")

    for key in ("large_diff_total_line_threshold", "large_diff_file_threshold"):
        value = policy.get(key)
        if type(value) is not int or value <= 0:
            raise PRDiffScopeError(f"{key} must be a positive integer")

    reason_min = policy.get("large_pr_reason_min_chars")
    if type(reason_min) is not int or reason_min < 12:
        raise PRDiffScopeError("large_pr_reason_min_chars must be at least 12")

    _require_nonempty_string(policy.get("large_pr_ack_marker"), "large_pr_ack_marker")
    _require_nonempty_string(
        policy.get("large_pr_reason_prefix"), "large_pr_reason_prefix"
    )
    return policy


def _visible_large_pr_ack(policy: dict[str, Any], body: str) -> tuple[bool, str | None]:
    marker = re.escape(str(policy["large_pr_ack_marker"]))
    reason_prefix = re.escape(str(policy["large_pr_reason_prefix"]))
    ack = re.search(rf"(?m)^\s*{marker}\s*$", body) is not None
    reason_match = re.search(rf"(?m)^\s*{reason_prefix}\s*(.*?)\s*$", body)
    reason = reason_match.group(1).strip() if reason_match else None
    reason_ok = (
        reason is not None
        and len(reason) >= int(policy["large_pr_reason_min_chars"])
    )
    return ack and reason_ok, reason


def evaluate_pr_scope(
    policy: dict[str, Any],
    *,
    base_ref: str,
    head_ref: str,
    same_repository_head: bool,
    base_is_ancestor: bool,
    body: str,
    stats: DiffStats,
    base_sha: str = "",
    head_sha: str = "",
    merge_base_sha: str = "",
) -> dict[str, Any]:
    durable = set(policy["durable_branches"])
    if base_ref not in durable:
        return {
            "status": "NOT_APPLICABLE",
            "violations": [],
            "reason": "PR base is not a governed durable branch",
            "base_ref": base_ref,
            "head_ref": head_ref,
        }

    violations: list[str] = []
    prefixes = tuple(policy["allowed_transient_head_prefixes"])

    if not same_repository_head:
        violations.append(
            "governed durable-branch PR must use a same-repository head branch"
        )
    if head_ref in durable:
        violations.append(
            "durable branch must not be used directly as the head of another durable-branch PR"
        )
    if not head_ref.startswith(prefixes):
        violations.append(
            "governed PR head must use an approved transient branch prefix"
        )
    if not base_is_ancestor:
        violations.append(
            "selected durable base must be an ancestor of the PR head; create or update a clean branch from the intended base"
        )

    total_lines = stats.total_lines
    large = (
        total_lines > int(policy["large_diff_total_line_threshold"])
        or stats.changed_files > int(policy["large_diff_file_threshold"])
    )
    acknowledged, reason = _visible_large_pr_ack(policy, body)
    if large and not acknowledged:
        violations.append(
            "unexpectedly large PR diff requires explicit LARGE_PR_EXPECTED acknowledgement and a substantive reason"
        )

    return {
        "status": "PASS" if not violations else "FAIL",
        "violations": violations,
        "base_ref": base_ref,
        "head_ref": head_ref,
        "same_repository_head": same_repository_head,
        "base_is_ancestor": base_is_ancestor,
        "base_sha": base_sha,
        "head_sha": head_sha,
        "merge_base_sha": merge_base_sha,
        "diff": asdict(stats) | {"total_lines": total_lines},
        "large_diff": large,
        "large_pr_acknowledged": acknowledged,
        "large_pr_reason": reason,
        "large_pr_acknowledgement_is_merge_authority": False,
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


def _numstat(root: Path, merge_base: str, head_sha: str) -> tuple[int, int, int]:
    output = _git(
        root,
        "diff",
        "--no-ext-diff",
        "--find-renames",
        "--numstat",
        f"{merge_base}...{head_sha}",
    )
    files = additions = deletions = 0
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) != 3:
            raise PRDiffScopeError("unexpected git --numstat record")
        added, removed, _path = parts
        files += 1
        if added.isdigit():
            additions += int(added)
        if removed.isdigit():
            deletions += int(removed)
    return files, additions, deletions


def collect_stats(
    root: Path,
    base_sha: str,
    head_sha: str,
) -> tuple[bool, str, DiffStats]:
    if not SHA40.fullmatch(base_sha) or not SHA40.fullmatch(head_sha):
        raise PRDiffScopeError("base/head must be exact lowercase 40-character SHAs")

    ancestor_check = subprocess.run(
        ["git", "merge-base", "--is-ancestor", base_sha, head_sha],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if ancestor_check.returncode not in (0, 1):
        raise PRDiffScopeError(
            "git merge-base --is-ancestor failed instead of returning an ancestry decision"
        )
    ancestor = ancestor_check.returncode == 0

    merge_base = _git(root, "merge-base", base_sha, head_sha)
    if not SHA40.fullmatch(merge_base):
        raise PRDiffScopeError("git merge-base did not return an exact SHA")

    changed_files, additions, deletions = _numstat(root, merge_base, head_sha)
    commits = int(
        _git(root, "rev-list", "--count", f"{merge_base}..{head_sha}") or "0"
    )
    return (
        ancestor,
        merge_base,
        DiffStats(
            changed_files=changed_files,
            additions=additions,
            deletions=deletions,
            commits=commits,
        ),
    )


def _write_result(path: Path | None, result: dict[str, Any]) -> None:
    if path is None:
        return
    path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, required=True)
    parser.add_argument("--event-file", type=Path, required=True)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result: dict[str, Any]
    try:
        policy = load_policy(args.policy)
        event = json.loads(args.event_file.read_text(encoding="utf-8"))
        pull = event.get("pull_request")
        if not isinstance(pull, dict):
            result = {
                "status": "NOT_APPLICABLE",
                "reason": "not a pull_request event",
            }
            _write_result(args.output, result)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0

        event_repo = _require_nonempty_string(
            event.get("repository", {}).get("full_name")
            if isinstance(event.get("repository"), dict)
            else None,
            "event repository",
        )
        if event_repo != policy["repository"]:
            raise PRDiffScopeError("event repository does not match policy repository")

        base = pull["base"]
        head = pull["head"]
        if not isinstance(base, dict) or not isinstance(head, dict):
            raise PRDiffScopeError("pull request base/head payload is malformed")

        base_ref = _require_nonempty_string(base.get("ref"), "base ref")
        head_ref = _require_nonempty_string(head.get("ref"), "head ref")
        base_sha = _require_nonempty_string(base.get("sha"), "base sha")
        head_sha = _require_nonempty_string(head.get("sha"), "head sha")
        body = pull.get("body") or ""
        if not isinstance(body, str):
            raise PRDiffScopeError("pull request body must be text")

        head_repo = head.get("repo")
        head_repo_name = (
            head_repo.get("full_name") if isinstance(head_repo, dict) else None
        )
        same_repository_head = head_repo_name == event_repo

        ancestor, merge_base, stats = collect_stats(
            args.repository_root.resolve(), base_sha, head_sha
        )
        result = evaluate_pr_scope(
            policy,
            base_ref=base_ref,
            head_ref=head_ref,
            same_repository_head=same_repository_head,
            base_is_ancestor=ancestor,
            body=body,
            stats=stats,
            base_sha=base_sha,
            head_sha=head_sha,
            merge_base_sha=merge_base,
        )
        _write_result(args.output, result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] in {"PASS", "NOT_APPLICABLE"} else 1
    except (
        PRDiffScopeError,
        OSError,
        KeyError,
        TypeError,
        ValueError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
    ) as error:
        result = {"status": "ERROR", "error": str(error)}
        _write_result(args.output, result)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
