import pytest

from scripts.validate_branch_topology import (
    BranchTopologyError,
    evaluate_topology,
    load_policy,
    validate_deletion_request,
)


DURABLE = {
    "main",
    "research/ccts-human-ai-learning-lane",
    "research/embodiment-lane",
    "research/legacy-uncertainty-hold",
}


def policy() -> dict[str, object]:
    return {
        "schema_version": "1.0.0",
        "repository": "maker-luder/aion-governance-framework",
        "steady_state_branch_count": 4,
        "durable_branches": sorted(DURABLE),
        "transient_branch_policy": {
            "maximum_open_pr_branches": 1,
            "require_open_pull_request": True,
            "delete_after_pull_request_close": True,
            "allowed_prefixes": ["work/", "docs/", "fix/", "feat/", "governance/", "quality/", "review/"],
        },
        "archive_tag_prefix": "archive/branch-heads/",
    }


def test_exact_four_durable_branches_is_steady_state() -> None:
    result = evaluate_topology(policy(), DURABLE, set())

    assert result["status"] == "PASS"
    assert result["steady_state"] is True
    assert result["branch_count"] == 4
    assert result["violations"] == []


def test_missing_durable_branch_fails_closed() -> None:
    result = evaluate_topology(policy(), DURABLE - {"research/embodiment-lane"}, set())

    assert result["status"] == "FAIL"
    assert result["missing_durable"] == ["research/embodiment-lane"]


def test_unassociated_fifth_branch_fails_closed() -> None:
    result = evaluate_topology(policy(), DURABLE | {"work/unreviewed"}, set())

    assert result["status"] == "FAIL"
    assert result["unassociated_transient"] == ["work/unreviewed"]


def test_one_open_pr_branch_is_bounded_transient_not_steady_state() -> None:
    branches = DURABLE | {"docs/pr264-governance"}
    result = evaluate_topology(policy(), branches, {"docs/pr264-governance"})

    assert result["status"] == "PASS"
    assert result["steady_state"] is False
    assert result["permitted_transient"] == ["docs/pr264-governance"]


def test_more_than_one_open_pr_branch_fails_hard_cap() -> None:
    transients = {"work/one", "fix/two"}
    result = evaluate_topology(policy(), DURABLE | transients, transients)

    assert result["status"] == "FAIL"
    assert "transient branch cap exceeded: 2 > 1" in result["violations"]


def test_disallowed_transient_prefix_fails_even_with_open_pr() -> None:
    result = evaluate_topology(policy(), DURABLE | {"research/new-lane"}, {"research/new-lane"})

    assert result["status"] == "FAIL"
    assert result["disallowed_transient"] == ["research/new-lane"]


def test_policy_rejects_duplicate_or_mismatched_durable_contract(tmp_path) -> None:
    path = tmp_path / "policy.json"
    bad = policy()
    bad["durable_branches"] = ["main", "main"]
    path.write_text(__import__("json").dumps(bad), encoding="utf-8")

    with pytest.raises(BranchTopologyError, match="durable branch list"):
        load_policy(path)


def test_cleanup_never_deletes_durable_branch() -> None:
    with pytest.raises(BranchTopologyError, match="durable"):
        validate_deletion_request(policy(), "main", "a" * 40, "a" * 40)


def test_cleanup_requires_exact_unchanged_head() -> None:
    with pytest.raises(BranchTopologyError, match="moved"):
        validate_deletion_request(policy(), "work/pr-264", "a" * 40, "b" * 40)


def test_cleanup_accepts_bounded_transient_at_exact_head() -> None:
    assert validate_deletion_request(policy(), "work/pr-264", "a" * 40, "a" * 40) is None
