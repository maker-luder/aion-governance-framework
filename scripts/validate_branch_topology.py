"""Enforce the repository's four durable branches and one bounded PR branch.

Read-only validation is the default. Deletion is available only for a closed
same-repository pull-request head and requires an unchanged exact SHA.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_POLICY = ROOT / ".github" / "branch-topology-policy.json"
SHA40 = re.compile(r"[0-9a-f]{40}")


class BranchTopologyError(ValueError):
    """Raised when the topology contract or a destructive request is invalid."""


def load_policy(path: Path) -> dict[str, Any]:
    record = json.loads(path.read_text(encoding="utf-8"))
    if record.get("schema_version") != "1.0.0":
        raise BranchTopologyError("unknown branch topology policy schema")
    repository = record.get("repository")
    if not isinstance(repository, str) or repository.count("/") != 1:
        raise BranchTopologyError("repository must use owner/name form")
    durable = record.get("durable_branches")
    if not isinstance(durable, list) or not durable or any(not isinstance(item, str) or not item for item in durable):
        raise BranchTopologyError("durable branch list must contain non-empty strings")
    if len(durable) != len(set(durable)):
        raise BranchTopologyError("durable branch list contains duplicates")
    if record.get("steady_state_branch_count") != len(durable):
        raise BranchTopologyError("steady-state count must equal the durable branch list")
    if "main" not in durable:
        raise BranchTopologyError("durable branch list must include main")

    transient = record.get("transient_branch_policy")
    if not isinstance(transient, dict):
        raise BranchTopologyError("missing transient branch policy")
    maximum = transient.get("maximum_open_pr_branches")
    if type(maximum) is not int or maximum < 0:
        raise BranchTopologyError("transient branch cap must be a non-negative integer")
    if transient.get("require_open_pull_request") is not True:
        raise BranchTopologyError("transient branches must require an open pull request")
    if transient.get("delete_after_pull_request_close") is not True:
        raise BranchTopologyError("closed pull-request branches must be deleted")
    prefixes = transient.get("allowed_prefixes")
    if not isinstance(prefixes, list) or not prefixes or any(
        not isinstance(prefix, str) or not prefix.endswith("/") for prefix in prefixes
    ):
        raise BranchTopologyError("transient prefixes must be a non-empty list of path prefixes")
    archive_prefix = record.get("archive_tag_prefix")
    if not isinstance(archive_prefix, str) or not archive_prefix.endswith("/"):
        raise BranchTopologyError("archive tag prefix must end with a slash")
    return record


def evaluate_topology(
    policy: dict[str, Any],
    branches: set[str],
    open_pr_heads: set[str],
) -> dict[str, Any]:
    durable = set(policy["durable_branches"])
    transient = policy["transient_branch_policy"]
    unexpected = branches - durable
    missing = durable - branches
    prefixes = tuple(transient["allowed_prefixes"])
    associated = unexpected & open_pr_heads
    unassociated = unexpected - open_pr_heads
    disallowed = {branch for branch in associated if not branch.startswith(prefixes)}
    permitted = associated - disallowed
    violations: list[str] = []

    if missing:
        violations.append("durable branches are missing")
    if unassociated:
        violations.append("transient branches without an open pull request")
    if disallowed:
        violations.append("transient branch prefix is not allowed")
    maximum = transient["maximum_open_pr_branches"]
    if len(associated) > maximum:
        violations.append(f"transient branch cap exceeded: {len(associated)} > {maximum}")

    return {
        "status": "PASS" if not violations else "FAIL",
        "steady_state": branches == durable,
        "branch_count": len(branches),
        "durable_count": len(durable & branches),
        "missing_durable": sorted(missing),
        "permitted_transient": sorted(permitted),
        "unassociated_transient": sorted(unassociated),
        "disallowed_transient": sorted(disallowed),
        "violations": violations,
    }


def validate_deletion_request(
    policy: dict[str, Any],
    branch: str,
    expected_head: str,
    live_head: str,
) -> None:
    if branch in set(policy["durable_branches"]):
        raise BranchTopologyError("durable branches must never be deleted")
    if not SHA40.fullmatch(expected_head) or not SHA40.fullmatch(live_head):
        raise BranchTopologyError("deletion requires exact lowercase 40-character SHAs")
    if live_head != expected_head:
        raise BranchTopologyError("branch moved after review; deletion stopped")


def _request_json(url: str, token: str | None, method: str = "GET") -> tuple[Any, dict[str, str]]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "aion-branch-topology-governance",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers, method=method)
    try:
        with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed GitHub API origin
            data = response.read()
            payload = json.loads(data) if data else None
            return payload, dict(response.headers.items())
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise BranchTopologyError(f"GitHub API {method} failed ({error.code}): {detail}") from error


def _paged_items(url: str, token: str | None) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    page = 1
    while True:
        separator = "&" if "?" in url else "?"
        payload, _ = _request_json(f"{url}{separator}per_page=100&page={page}", token)
        if not isinstance(payload, list):
            raise BranchTopologyError("GitHub API returned a non-list page")
        items.extend(item for item in payload if isinstance(item, dict))
        if len(payload) < 100:
            return items
        page += 1


def fetch_live_topology(repository: str, token: str | None) -> tuple[set[str], set[str]]:
    base = f"https://api.github.com/repos/{repository}"
    branches = {item["name"] for item in _paged_items(f"{base}/branches", token) if isinstance(item.get("name"), str)}
    pulls = _paged_items(f"{base}/pulls?state=open", token)
    heads = {
        head["ref"]
        for item in pulls
        if isinstance((head := item.get("head")), dict)
        and isinstance(head.get("ref"), str)
        and isinstance(head.get("repo"), dict)
        and head["repo"].get("full_name") == repository
    }
    return branches, heads


def fetch_branch_head(repository: str, branch: str, token: str) -> str:
    encoded = quote(branch, safe="")
    payload, _ = _request_json(f"https://api.github.com/repos/{repository}/branches/{encoded}", token)
    try:
        head = payload["commit"]["sha"]
    except (KeyError, TypeError) as error:
        raise BranchTopologyError("GitHub branch response did not contain an exact head") from error
    if not isinstance(head, str):
        raise BranchTopologyError("GitHub branch head is not a string")
    return head


def delete_branch(repository: str, branch: str, token: str) -> None:
    encoded = quote(f"heads/{branch}", safe="/")
    _request_json(f"https://api.github.com/repos/{repository}/git/refs/{encoded}", token, method="DELETE")


def _read_names(path: Path | None) -> set[str]:
    if path is None:
        return set()
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=DEFAULT_POLICY)
    parser.add_argument("--repository")
    parser.add_argument("--branches-file", type=Path)
    parser.add_argument("--open-pr-heads-file", type=Path)
    parser.add_argument("--delete-closed-pr-head")
    parser.add_argument("--expected-head")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        policy = load_policy(args.policy)
        repository = args.repository or policy["repository"]
        token = os.environ.get("GITHUB_TOKEN")
        if args.delete_closed_pr_head:
            if not args.expected_head:
                raise BranchTopologyError("deletion requires --expected-head")
            if not token:
                raise BranchTopologyError("deletion requires GITHUB_TOKEN")
            live_head = fetch_branch_head(repository, args.delete_closed_pr_head, token)
            validate_deletion_request(policy, args.delete_closed_pr_head, args.expected_head, live_head)
            delete_branch(repository, args.delete_closed_pr_head, token)

        if args.branches_file:
            branches = _read_names(args.branches_file)
            open_pr_heads = _read_names(args.open_pr_heads_file)
        else:
            branches, open_pr_heads = fetch_live_topology(repository, token)
        result = evaluate_topology(policy, branches, open_pr_heads)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "PASS" else 1
    except (BranchTopologyError, OSError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "ERROR", "error": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
