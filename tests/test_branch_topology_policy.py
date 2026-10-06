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
        "schema_version": "1.2.0",
        "repository": "maker-luder/aion-governance-framework",
        "steady_state_branch_count": 4,
        "durable_branches": sorted(DURABLE),
        "transient_branch_policy": {
            "maximum_open_pr_branches": None,
            "require_open_pull_request": True,
            "delete_after_pull_request_close": True,
            "allowed_prefixes": ["work/", "docs/", "fix/", "feat/", "governance/", "quality/", "review/"],
        },
        "archive_tag_prefix": "archive/branch-heads/",
        "retained_closed_pr_branches": [
            {
                "branch": "feat/provenance-heuristic-reveal-20261006",
                "pr": 281,
                "exact_head": "5ce1909b7d1d21525bb6f3b4cc4bb69c94775db9",
                "reason": "explicit Human Owner retention",
            },
            {
                "branch": "feat/text-provenance-visibility-v0.2-20261006",
                "pr": 282,
                "exact_head": "bde86b008a90bb6eb0818c29498845ef2baab47b",
                "reason": "explicit Human Owner retention",
            },
        ],
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


def test_multiple_open_pr_branches_are_allowed_without_hard_cap() -> None:
    transients = {"work/one", "fix/two", "review/three"}
    result = evaluate_topology(policy(), DURABLE | transients, transients)

    assert result["status"] == "PASS"
    assert result["open_pr_branch_count"] == 3
    assert result["maximum_open_pr_branches"] is None
    assert result["permitted_transient"] == sorted(transients)
    assert result["violations"] == []


def test_configured_finite_open_pr_branch_cap_still_fails_closed() -> None:
    bounded = policy()
    transient = bounded["transient_branch_policy"]
    assert isinstance(transient, dict)
    transient["maximum_open_pr_branches"] = 1
    transients = {"work/one", "fix/two"}

    result = evaluate_topology(bounded, DURABLE | transients, transients)

    assert result["status"] == "FAIL"
    assert "transient branch cap exceeded: 2 > 1" in result["violations"]


def test_policy_loader_accepts_explicit_unbounded_open_pr_branch_limit(tmp_path) -> None:
    path = tmp_path / "policy.json"
    path.write_text(__import__("json").dumps(policy()), encoding="utf-8")

    loaded = load_policy(path)

    transient = loaded["transient_branch_policy"]
    assert isinstance(transient, dict)
    assert transient["maximum_open_pr_branches"] is None


def test_exact_retained_closed_branch_is_allowed_but_not_steady_state() -> None:
    branch = "feat/provenance-heuristic-reveal-20261006"
    head = "5ce1909b7d1d21525bb6f3b4cc4bb69c94775db9"
    result = evaluate_topology(
        policy(),
        DURABLE | {branch},
        set(),
        {**{name: "a" * 40 for name in DURABLE}, branch: head},
    )

    assert result["status"] == "PASS"
    assert result["steady_state"] is False
    assert result["retained_historical"] == [branch]


def test_moved_retained_closed_branch_fails_closed() -> None:
    branch = "feat/provenance-heuristic-reveal-20261006"
    result = evaluate_topology(
        policy(),
        DURABLE | {branch},
        set(),
        {**{name: "a" * 40 for name in DURABLE}, branch: "b" * 40},
    )

    assert result["status"] == "FAIL"
    assert result["retained_head_mismatch"] == [branch]


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
