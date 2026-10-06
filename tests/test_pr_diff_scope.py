from scripts.validate_pr_diff_scope import DiffStats, evaluate_pr_scope


POLICY = {
    "schema_version": "1.0.0",
    "main_branch": "main",
    "durable_branches": [
        "main",
        "research/ccts-human-ai-learning-lane",
        "research/embodiment-lane",
        "research/legacy-uncertainty-hold",
    ],
    "allowed_main_pr_head_prefixes": [
        "work/",
        "docs/",
        "fix/",
        "feat/",
        "governance/",
        "quality/",
        "review/",
    ],
    "large_diff_total_line_threshold": 2000,
    "large_diff_file_threshold": 30,
    "amplification_min_total_lines": 1200,
    "amplification_ratio_threshold": 4.0,
    "large_pr_ack_marker": "LARGE_PR_EXPECTED = TRUE",
    "large_pr_reason_prefix": "LARGE_PR_REASON =",
}


def stats(lines: int, files: int = 8, commits: int = 1, tip: int | None = None) -> DiffStats:
    return DiffStats(
        changed_files=files,
        additions=lines,
        deletions=0,
        commits=commits,
        tip_changes=lines if tip is None else tip,
    )


def test_small_clean_main_pr_passes() -> None:
    result = evaluate_pr_scope(
        POLICY,
        base_ref="main",
        head_ref="feat/provenance-visibility-agent",
        base_is_ancestor=True,
        body="",
        stats=stats(693),
    )
    assert result["status"] == "PASS"


def test_durable_research_lane_cannot_target_main_directly() -> None:
    result = evaluate_pr_scope(
        POLICY,
        base_ref="main",
        head_ref="research/embodiment-lane",
        base_is_ancestor=False,
        body="",
        stats=stats(4721, files=34, commits=19, tip=246),
    )
    assert result["status"] == "FAIL"
    assert any("durable research branch" in item for item in result["violations"])


def test_unexpected_thousands_of_lines_fail_closed() -> None:
    result = evaluate_pr_scope(
        POLICY,
        base_ref="main",
        head_ref="feat/accidental-cumulative-diff",
        base_is_ancestor=True,
        body="",
        stats=stats(4721, files=34, commits=19, tip=246),
    )
    assert result["status"] == "FAIL"
    assert result["large_diff"] is True
    assert result["cumulative_amplification"] is True


def test_intentional_large_pr_requires_visible_reason() -> None:
    body = "LARGE_PR_EXPECTED = TRUE\nLARGE_PR_REASON = intentional generated fixture update"
    result = evaluate_pr_scope(
        POLICY,
        base_ref="main",
        head_ref="quality/intentional-large-update",
        base_is_ancestor=True,
        body=body,
        stats=stats(2501, files=10, commits=2, tip=2000),
    )
    assert result["status"] == "PASS"
    assert result["large_pr_acknowledged"] is True


def test_main_must_be_ancestor_of_clean_promotion_head() -> None:
    result = evaluate_pr_scope(
        POLICY,
        base_ref="main",
        head_ref="feat/from-wrong-parent",
        base_is_ancestor=False,
        body="",
        stats=stats(200),
    )
    assert result["status"] == "FAIL"
    assert any("ancestor" in item for item in result["violations"])


def test_non_main_research_pr_is_not_governed_by_main_guard() -> None:
    result = evaluate_pr_scope(
        POLICY,
        base_ref="research/embodiment-lane",
        head_ref="feat/bounded-research-change",
        base_is_ancestor=True,
        body="",
        stats=stats(4000, files=40),
    )
    assert result["status"] == "NOT_APPLICABLE"
