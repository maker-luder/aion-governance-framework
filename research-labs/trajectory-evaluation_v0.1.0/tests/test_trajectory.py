import pytest

from aion_trajectory_eval import (
    StepKind,
    TrajectoryStep,
    Trajectory,
    TrajectoryExpectation,
    TrajectoryEvidence,
    evaluate_trajectory,
    compare_trajectories,
)


def step(index: int, kind: StepKind, name: str) -> TrajectoryStep:
    return TrajectoryStep(index, kind, name)


def good() -> Trajectory:
    return Trajectory(
        "task-1",
        "good",
        (
            step(0, StepKind.PLAN, "plan"),
            step(1, StepKind.TOOL, "search"),
            step(2, StepKind.FINAL, "answer"),
        ),
        "same answer",
    )


def test_sequence_must_be_contiguous() -> None:
    with pytest.raises(ValueError):
        Trajectory("t", "i", (step(1, StepKind.PLAN, "x"),), "o")


def test_expected_path_full_coverage_passes() -> None:
    report = evaluate_trajectory(good(), TrajectoryExpectation(expected_step_names=("plan", "search", "answer")))
    item = next(value for value in report.evidence if value.metric == "expected_path_coverage")
    assert item.passed is True and item.score == 1.0


def test_expected_path_order_matters() -> None:
    report = evaluate_trajectory(good(), TrajectoryExpectation(expected_step_names=("search", "plan", "answer")))
    item = next(value for value in report.evidence if value.metric == "expected_path_coverage")
    assert item.passed is False and item.score < 1.0


def test_step_budget_detects_excess() -> None:
    report = evaluate_trajectory(good(), TrajectoryExpectation(max_steps=2))
    item = next(value for value in report.evidence if value.metric == "step_budget")
    assert item.passed is False


def test_retry_budget_detects_excess() -> None:
    trajectory = Trajectory(
        "t",
        "i",
        (
            step(0, StepKind.RETRY, "again"),
            step(1, StepKind.RETRY, "again"),
            step(2, StepKind.FINAL, "done"),
        ),
        "x",
    )
    report = evaluate_trajectory(trajectory, TrajectoryExpectation(max_retries=1))
    item = next(value for value in report.evidence if value.metric == "retry_budget")
    assert item.passed is False


def test_forbidden_tool_is_detected() -> None:
    trajectory = Trajectory("t", "i", (step(0, StepKind.TOOL, "danger"),), "x")
    report = evaluate_trajectory(trajectory, TrajectoryExpectation(forbidden_tools=frozenset({"danger"})))
    item = next(value for value in report.evidence if value.metric == "forbidden_tools")
    assert item.passed is False


def test_non_tool_name_does_not_trigger_forbidden_tool() -> None:
    trajectory = Trajectory("t", "i", (step(0, StepKind.PLAN, "danger"),), "x")
    report = evaluate_trajectory(trajectory, TrajectoryExpectation(forbidden_tools=frozenset({"danger"})))
    item = next(value for value in report.evidence if value.metric == "forbidden_tools")
    assert item.passed is True


def test_consecutive_loop_guard_detects_repeat() -> None:
    trajectory = Trajectory(
        "t",
        "i",
        (
            step(0, StepKind.TOOL, "search"),
            step(1, StepKind.TOOL, "search"),
            step(2, StepKind.TOOL, "search"),
        ),
        "x",
    )
    report = evaluate_trajectory(trajectory, TrajectoryExpectation(max_consecutive_signature_repeats=2))
    item = next(value for value in report.evidence if value.metric == "consecutive_loop_guard")
    assert item.passed is False


def test_nonconsecutive_repeat_is_not_same_as_loop_run() -> None:
    trajectory = Trajectory(
        "t",
        "i",
        (
            step(0, StepKind.TOOL, "search"),
            step(1, StepKind.OBSERVE, "read"),
            step(2, StepKind.TOOL, "search"),
        ),
        "x",
    )
    report = evaluate_trajectory(trajectory, TrajectoryExpectation(max_consecutive_signature_repeats=1))
    item = next(value for value in report.evidence if value.metric == "consecutive_loop_guard")
    assert item.passed is True


def test_same_output_can_have_different_paths() -> None:
    left = good()
    right = Trajectory(
        "task-1",
        "other",
        (
            step(0, StepKind.PLAN, "plan"),
            step(1, StepKind.RETRY, "retry"),
            step(2, StepKind.FINAL, "answer"),
        ),
        "same answer",
    )
    comparison = compare_trajectories(left, right)
    assert comparison["same_final_output"] is True
    assert comparison["same_recorded_path"] is False
    assert comparison["causal_claim"] == "NOT_ESTABLISHED"


def test_compare_requires_same_task() -> None:
    with pytest.raises(ValueError):
        compare_trajectories(good(), Trajectory("other", "x", (), "same answer"))


def test_report_is_research_only() -> None:
    report = evaluate_trajectory(good(), TrajectoryExpectation())
    assert report.research_only is True
    assert report.canonical_effect == "NONE"


def test_evidence_score_range_fail_closed() -> None:
    with pytest.raises(ValueError):
        TrajectoryEvidence("x", True, 1.1, "bad")


def test_invalid_expectation_bounds_rejected() -> None:
    with pytest.raises(ValueError):
        TrajectoryExpectation(max_steps=0)
    with pytest.raises(ValueError):
        TrajectoryExpectation(max_retries=-1)
