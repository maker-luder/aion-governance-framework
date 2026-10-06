from scripts.validate_pr_diff_scope import DiffStats, evaluate_pr_scope


POLICY = {
    "schema_version": "1.2.0",
    "repository": "maker-luder/aion-governance-framework",
    "durable_branches": [
        "main",
        "research/ccts-human-ai-learning-lane",
        "research/embodiment-lane",
        "research/legacy-uncertainty-hold",
    ],
    "allowed_transient_head_prefixes": [
        "work/",
        "docs/",
        "fix/",
        "feat/",
        "governance/",
        "quality/",
        "review/",
    ],
    "enforce_transient_head_prefixes": False,
    "require_same_repository_head": True,
    "large_diff_total_line_threshold": 2000,
    "large_diff_file_threshold": 30,
    "large_pr_ack_marker": "LARGE_PR_EXPECTED = TRUE",
    "large_pr_reason_prefix": "LARGE_PR_REASON =",
    "large_pr_reason_min_chars": 24,
}


def stats(lines: int, files: int = 8, commits: int = 1) -> DiffStats:
    return DiffStats(
        changed_files=files,
        additions=lines,
        deletions=0,
        commits=commits,
    )


def evaluate(
    *,
    base: str = "main",
    head: str = "feat/bounded-change",
    same_repo: bool = True,
    ancestor: bool = True,
    body: str = "",
    diff: DiffStats | None = None,
) -> dict[str, object]:
    return evaluate_pr_scope(
        POLICY,
        base_ref=base,
        head_ref=head,
        same_repository_head=same_repo,
        base_is_ancestor=ancestor,
        body=body,
        stats=diff or stats(200),
        base_sha="a" * 40,
        head_sha="b" * 40,
        merge_base_sha="a" * 40,
    )


def test_small_clean_main_pr_passes() -> None:
    result = evaluate(head="feat/provenance-visibility-agent", diff=stats(693))
    assert result["status"] == "PASS"


def test_bounded_research_lane_pr_is_also_guarded_and_can_pass() -> None:
    result = evaluate(
        base="research/embodiment-lane",
        head="feat/bounded-embodiment-change",
        diff=stats(700),
    )
    assert result["status"] == "PASS"


def test_durable_research_lane_cannot_be_used_as_head() -> None:
    result = evaluate(
        head="research/embodiment-lane",
        ancestor=False,
        diff=stats(4721, files=34, commits=19),
    )
    assert result["status"] == "FAIL"
    assert any("durable branch" in item for item in result["violations"])


def test_github_default_patch_branch_name_is_advisory_not_failure() -> None:
    result = evaluate(head="maker-luder-patch-1", diff=stats(50))

    assert result["status"] == "PASS"
    assert result["head_prefix_preferred"] is False
    assert result["head_prefix_enforced"] is False
    assert any("nonpreferred" in item for item in result["advisories"])


def test_strict_prefix_mode_can_still_fail_nonpreferred_head() -> None:
    strict = dict(POLICY)
    strict["enforce_transient_head_prefixes"] = True
    result = evaluate_pr_scope(
        strict,
        base_ref="main",
        head_ref="maker-luder-patch-1",
        same_repository_head=True,
        base_is_ancestor=True,
        body="",
        stats=stats(50),
        base_sha="a" * 40,
        head_sha="b" * 40,
        merge_base_sha="a" * 40,
    )

    assert result["status"] == "FAIL"
    assert any("approved transient branch prefix" in item for item in result["violations"])


def test_wrong_parent_fails_even_when_diff_is_small() -> None:
    result = evaluate(head="feat/from-wrong-parent", ancestor=False, diff=stats(50))
    assert result["status"] == "FAIL"
    assert any("ancestor" in item for item in result["violations"])


def test_fork_or_other_repository_head_fails_for_durable_base() -> None:
    result = evaluate(same_repo=False)
    assert result["status"] == "FAIL"
    assert any("same-repository" in item for item in result["violations"])


def test_unexpected_thousands_of_lines_fail_closed() -> None:
    result = evaluate(
        head="feat/accidental-cumulative-diff",
        diff=stats(4721, files=34, commits=19),
    )
    assert result["status"] == "FAIL"
    assert result["large_diff"] is True


def test_intentional_large_pr_requires_substantive_visible_reason() -> None:
    body = (
        "LARGE_PR_EXPECTED = TRUE\n"
        "LARGE_PR_REASON = intentional generated fixture migration with reviewed scope"
    )
    result = evaluate(
        head="quality/intentional-large-update",
        body=body,
        diff=stats(2501, files=10, commits=2),
    )
    assert result["status"] == "PASS"
    assert result["large_pr_acknowledged"] is True
    assert result["large_pr_acknowledgement_is_merge_authority"] is False


def test_short_large_pr_reason_does_not_bypass_guard() -> None:
    body = "LARGE_PR_EXPECTED = TRUE\nLARGE_PR_REASON = big update"
    result = evaluate(body=body, diff=stats(2501))
    assert result["status"] == "FAIL"


def test_large_pr_ack_does_not_override_wrong_ancestry() -> None:
    body = (
        "LARGE_PR_EXPECTED = TRUE\n"
        "LARGE_PR_REASON = intentionally large migration with bounded reviewed scope"
    )
    result = evaluate(body=body, ancestor=False, diff=stats(2501))
    assert result["status"] == "FAIL"
    assert any("ancestor" in item for item in result["violations"])


def test_transient_to_transient_pr_is_outside_durable_guard() -> None:
    result = evaluate(base="feat/stack-parent", head="feat/stack-child")
    assert result["status"] == "NOT_APPLICABLE"
