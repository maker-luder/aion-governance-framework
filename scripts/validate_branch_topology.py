"""Enforce the repository's four durable branches and governed transient PR branches.

Topology validation and closed-PR retirement assessment are read-only.
Retirement readiness never grants destructive authority. Until an independently
verified branch-deletion authority adapter exists, every retirement is HOLD.
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
    if record.get("schema_version") not in {"1.0.0", "1.1.0", "1.2.0"}:
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
    if "maximum_open_pr_branches" not in transient:
        raise BranchTopologyError("transient branch policy must declare maximum_open_pr_branches")
    maximum = transient["maximum_open_pr_branches"]
    if maximum is not None and (type(maximum) is not int or maximum < 0):
        raise BranchTopologyError(
            "transient branch cap must be null or a non-negative integer"
        )
    if transient.get("require_open_pull_request") is not True:
        raise BranchTopologyError("transient branches must require an open pull request")
    if transient.get("delete_after_pull_request_close") is not True:
        raise BranchTopologyError("closed pull requests must receive a guarded retirement assessment")
    prefixes = transient.get("allowed_prefixes")
    if not isinstance(prefixes, list) or not prefixes or any(
        not isinstance(prefix, str) or not prefix.endswith("/") for prefix in prefixes
    ):
        raise BranchTopologyError("transient prefixes must be a non-empty list of path prefixes")
    archive_prefix = record.get("archive_tag_prefix")
    if not isinstance(archive_prefix, str) or not archive_prefix.endswith("/"):
        raise BranchTopologyError("archive tag prefix must end with a slash")

    retained = record.get("retained_closed_pr_branches", [])
    if not isinstance(retained, list):
        raise BranchTopologyError("retained_closed_pr_branches must be a list")
    seen_retained: set[str] = set()
    for item in retained:
        if not isinstance(item, dict):
            raise BranchTopologyError("retained closed PR entry must be an object")
        branch = item.get("branch")
        pr = item.get("pr")
        exact_head = item.get("exact_head")
        if (
            not isinstance(branch, str)
            or not branch
            or branch in durable
            or branch in seen_retained
        ):
            raise BranchTopologyError("retained closed PR branch must be unique and non-durable")
        if type(pr) is not int or pr <= 0:
            raise BranchTopologyError("retained closed PR number must be a positive integer")
        if not isinstance(exact_head, str) or not SHA40.fullmatch(exact_head):
            raise BranchTopologyError("retained closed PR exact_head must be a lowercase SHA")
        seen_retained.add(branch)
    return record


def evaluate_topology(
    policy: dict[str, Any],
    branches: set[str],
    open_pr_heads: set[str],
    branch_heads: dict[str, str] | None = None,
) -> dict[str, Any]:
    durable = set(policy["durable_branches"])
    transient = policy["transient_branch_policy"]
    retained_entries = {
        item["branch"]: item["exact_head"]
        for item in policy.get("retained_closed_pr_branches", [])
    }
    unexpected = branches - durable
    missing = durable - branches
    prefixes = tuple(transient["allowed_prefixes"])
    associated = unexpected & open_pr_heads

    retained_present = {
        branch for branch in unexpected - open_pr_heads if branch in retained_entries
    }
    retained_head_mismatch: set[str] = set()
    if retained_present:
        if branch_heads is None:
            retained_head_mismatch = set(retained_present)
        else:
            retained_head_mismatch = {
                branch
                for branch in retained_present
                if branch_heads.get(branch) != retained_entries[branch]
            }
    retained_verified = retained_present - retained_head_mismatch

    unassociated = unexpected - open_pr_heads - retained_verified
    disallowed = {branch for branch in associated if not branch.startswith(prefixes)}
    permitted = associated - disallowed
    violations: list[str] = []

    if missing:
        violations.append("durable branches are missing")
    if retained_head_mismatch:
        violations.append("retained historical branch moved from exact reviewed head")
    if unassociated:
        violations.append("transient branches without an open pull request or exact retained exception")
    if disallowed:
        violations.append("transient branch prefix is not allowed")
    maximum = transient["maximum_open_pr_branches"]
    if maximum is not None and len(associated) > maximum:
        violations.append(f"transient branch cap exceeded: {len(associated)} > {maximum}")

    return {
        "status": "PASS" if not violations else "FAIL",
        "steady_state": branches == durable,
        "branch_count": len(branches),
        "durable_count": len(durable & branches),
        "open_pr_branch_count": len(associated),
        "maximum_open_pr_branches": maximum,
        "missing_durable": sorted(missing),
        "permitted_transient": sorted(permitted),
        "retained_historical": sorted(retained_verified),
        "retained_head_mismatch": sorted(retained_head_mismatch),
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
    if method != "GET":
        raise BranchTopologyError("branch topology transport is read-only; retirement is HOLD")
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
        if any(not isinstance(item, dict) for item in payload):
            raise BranchTopologyError("GitHub API returned a malformed list item")
        items.extend(payload)
        if len(payload) < 100:
            return items
        page += 1


def fetch_live_topology(repository: str, token: str | None) -> tuple[dict[str, str], set[str]]:
    base = f"https://api.github.com/repos/{repository}"
    branch_heads = {
        item["name"]: item["commit"]["sha"]
        for item in _paged_items(f"{base}/branches", token)
        if isinstance(item.get("name"), str)
        and isinstance(item.get("commit"), dict)
        and isinstance(item["commit"].get("sha"), str)
        and SHA40.fullmatch(item["commit"]["sha"])
    }
    pulls = _paged_items(f"{base}/pulls?state=open", token)
    heads = {
        head["ref"]
        for item in pulls
        if isinstance((head := item.get("head")), dict)
        and isinstance(head.get("ref"), str)
        and isinstance(head.get("repo"), dict)
        and head["repo"].get("full_name") == repository
    }
    return branch_heads, heads


def fetch_branch_head(repository: str, branch: str, token: str | None) -> str:
    encoded = quote(branch, safe="")
    payload, _ = _request_json(f"https://api.github.com/repos/{repository}/branches/{encoded}", token)
    try:
        head = payload["commit"]["sha"]
    except (KeyError, TypeError) as error:
        raise BranchTopologyError("GitHub branch response did not contain an exact head") from error
    if not isinstance(head, str) or not SHA40.fullmatch(head):
        raise BranchTopologyError("GitHub branch head is not an exact SHA")
    return head


def assess_retirement_evidence(
    policy: dict[str, Any], branch: str, expected_head: str, live_head: str,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """Assess preservation only. Input assertions are never deletion authority.

    This is not a receipt verifier or a replacement QMS. In particular, READY
    here is not an execution capability, even with a caller-supplied authority ref.
    """
    diagnostics: list[str] = []
    try:
        validate_deletion_request(policy, branch, expected_head, live_head)
    except (BranchTopologyError, TypeError) as error:
        diagnostics.append(str(error))
    if evidence.get("pr_disposition") not in ("MERGED", "CLOSED_UNMERGED"):
        diagnostics.append("PR disposition is unknown or not closed")
    if evidence.get("history_value_known") is not True:
        diagnostics.append("history value is unknown; retirement review required")
    for key in ("all_commits_reachable", "unique_history_present"):
        if type(evidence.get(key)) is not bool:
            diagnostics.append(f"{key} must be a verified boolean")
    if evidence.get("all_commits_reachable") is evidence.get("unique_history_present"):
        diagnostics.append("history reachability and unique-history evidence contradict")
    # Preserve an exact archive even for merged PRs (squash/rebase are not ancestry).
    archive = evidence.get("preservation_ref")
    prefix = "refs/tags/" + policy["archive_tag_prefix"]
    if not isinstance(archive, str) or not archive.startswith(prefix) or archive == prefix:
        diagnostics.append("exact archive preservation ref is missing")
    if evidence.get("preservation_exact_sha") != expected_head:
        diagnostics.append("archive ref does not match the exact reviewed head")
    if evidence.get("preservation_exact_sha_verified") is not True:
        diagnostics.append("archive exact SHA is not verified")
    for key in ("reconstruction_ref", "verification_ref"):
        value = evidence.get(key)
        if not isinstance(value, str) or not value.strip():
            diagnostics.append(f"{key} is missing")
    if evidence.get("reconstruction_verified") is not True:
        diagnostics.append("reconstruction path is not verified")
    return {
        "status": "HOLD",
        "preservation_readiness": "HOLD" if diagnostics else "READY",
        "deletion_authority": "NONE",
        "mutation_performed": False,
        "expected_head": expected_head,
        "live_head": live_head,
        "evidence": evidence,
        "diagnostics": diagnostics + [
            "separate fresh branch-deletion authority integration is unavailable; no deletion",
        ],
    }


def assess_closed_pr(
    policy: dict[str, Any], repository: str, pr_number: int,
    branch: str, expected_head: str, token: str | None,
) -> dict[str, Any]:
    """Read live disposition, durable reachability and exact archive; never write."""
    if repository != policy["repository"] or pr_number <= 0:
        raise BranchTopologyError("retirement target does not match policy")
    validate_deletion_request(policy, branch, expected_head, expected_head)
    base = f"https://api.github.com/repos/{repository}"
    pull, _ = _request_json(f"{base}/pulls/{pr_number}", token)
    try:
        if (
            pull["number"] != pr_number or pull["state"] != "closed"
            or type(pull["merged"]) is not bool
            or pull["head"]["repo"]["full_name"] != repository
            or pull["head"]["ref"] != branch or pull["head"]["sha"] != expected_head
        ):
            raise BranchTopologyError("live PR is not the exact closed same-repository target")
    except (KeyError, TypeError) as error:
        raise BranchTopologyError("malformed live PR disposition") from error
    live_head = fetch_branch_head(repository, branch, token)
    validate_deletion_request(policy, branch, expected_head, live_head)
    reachable = False
    retained: dict[str, str] = {}
    for durable in policy["durable_branches"]:
        sha = fetch_branch_head(repository, durable, token)
        if not SHA40.fullmatch(sha):
            raise BranchTopologyError("malformed durable branch SHA")
        retained[durable] = sha
        compare, _ = _request_json(f"{base}/compare/{expected_head}...{sha}", token)
        if (
            not isinstance(compare, dict)
            or compare.get("status") not in ("identical", "ahead", "behind", "diverged")
            or type(compare.get("behind_by")) is not int
            or compare["behind_by"] < 0
            or not isinstance(compare.get("base_commit"), dict)
            or not isinstance(compare.get("merge_base_commit"), dict)
        ):
            raise BranchTopologyError("malformed reachability comparison")
        if compare["status"] in ("identical", "ahead"):
            if (
                compare["behind_by"] != 0
                or compare.get("base_commit", {}).get("sha") != expected_head
                or compare.get("merge_base_commit", {}).get("sha") != expected_head
            ):
                raise BranchTopologyError("inconsistent reachability comparison")
            reachable = True
    tag = policy["archive_tag_prefix"] + f"pr-{pr_number}/{expected_head}"
    archive, _ = _request_json(f"{base}/git/ref/tags/{quote(tag, safe='/')}", token)
    try:
        verified = (
            archive["ref"] == f"refs/tags/{tag}"
            and archive["object"]["type"] == "commit"
            and archive["object"]["sha"] == expected_head
        )
    except (KeyError, TypeError) as error:
        raise BranchTopologyError("malformed archive lookup") from error
    if not verified:
        raise BranchTopologyError("archive is missing, colliding, annotated or at a different SHA")
    # A live tag is not a verified bundle or an approved history classification.
    evidence = {
        "pr_disposition": "MERGED" if pull["merged"] else "CLOSED_UNMERGED",
        "history_value_known": False,
        "all_commits_reachable": reachable,
        "unique_history_present": not reachable,
        "retained_exact_heads": retained,
        "preservation_ref": f"refs/tags/{tag}",
        "preservation_exact_sha": archive["object"]["sha"],
        "preservation_exact_sha_verified": verified,
        "reconstruction_ref": "",
        "reconstruction_verified": False,
        "verification_ref": "",
    }
    final_head = fetch_branch_head(repository, branch, token)
    validate_deletion_request(policy, branch, expected_head, final_head)
    return assess_retirement_evidence(policy, branch, expected_head, final_head, evidence)


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
    parser.add_argument("--assess-closed-pr", type=int)
    parser.add_argument("--branch")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        policy = load_policy(args.policy)
        repository = args.repository or policy["repository"]
        token = os.environ.get("GITHUB_TOKEN")
        if args.delete_closed_pr_head:
            print(json.dumps({
                "status": "HOLD", "mutation_performed": False, "deletion_authority": "NONE",
                "error": "legacy deletion path disabled; use read-only --assess-closed-pr",
            }, sort_keys=True))
            return 10
        if args.assess_closed_pr is not None:
            if not args.expected_head or not args.branch:
                raise BranchTopologyError("retirement assessment requires --branch and --expected-head")
            result = assess_closed_pr(
                policy, repository, args.assess_closed_pr, args.branch, args.expected_head, token,
            )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 10

        if args.branches_file:
            branches = _read_names(args.branches_file)
            open_pr_heads = _read_names(args.open_pr_heads_file)
            branch_heads = None
        else:
            branch_heads, open_pr_heads = fetch_live_topology(repository, token)
            branches = set(branch_heads)
        result = evaluate_topology(policy, branches, open_pr_heads, branch_heads)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["status"] == "PASS" else 1
    except (BranchTopologyError, OSError, json.JSONDecodeError, TypeError, KeyError) as error:
        retirement = bool(args.delete_closed_pr_head) or args.assess_closed_pr is not None
        print(json.dumps({
            "status": "HOLD" if retirement else "ERROR", "error": str(error),
            "mutation_performed": False,
        }, ensure_ascii=False, sort_keys=True))
        return 10 if retirement else 2


if __name__ == "__main__":
    sys.exit(main())
