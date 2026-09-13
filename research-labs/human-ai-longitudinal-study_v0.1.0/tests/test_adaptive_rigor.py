from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import (
    CalibrationCondition, CalibrationError, CalibrationMetric, CalibrationRun, audit_calibration,
)


def run(task: str, condition: CalibrationCondition) -> CalibrationRun:
    return CalibrationRun(task, "LOW" if task == "low" else "HIGH", condition,
        "fixture:matched-runtime", f"sha256:{task}", "fixture:blinded-evaluator", True,
        tuple((metric, float(index + 1)) for index, metric in enumerate(CalibrationMetric)))


def matrix() -> tuple[CalibrationRun, ...]:
    return tuple(run(task, condition) for task in ("low", "high") for condition in CalibrationCondition)


def test_complete_matrix_preserves_separate_metrics_and_nonclaims() -> None:
    result = audit_calibration(matrix())
    assert result["run_count"] == 8
    assert result["metric_count"] == 6
    assert result["composite_score"] == "NONE"
    assert result["sycophancy_effect"] == "NOT_ESTABLISHED"
    assert result["adaptive_rigor_effect"] == "NOT_ESTABLISHED"
    assert result["subjectivity"] == "NOT_ESTABLISHED"


def test_missing_cell_and_binding_drift_fail_closed() -> None:
    with pytest.raises(CalibrationError, match="complete"):
        audit_calibration(matrix()[:-1])
    changed = replace(matrix()[1], provider_model_runtime_ref="drift")
    with pytest.raises(CalibrationError, match="binding drift"):
        audit_calibration((matrix()[0], changed) + matrix()[2:])


def test_blinding_privacy_and_metric_completeness_are_required() -> None:
    with pytest.raises(CalibrationError, match="blinded"):
        replace(matrix()[0], evaluator_blinded=False)
    with pytest.raises(CalibrationError, match="private"):
        replace(matrix()[0], contains_private_transcript=True)
    with pytest.raises(CalibrationError, match="all metrics"):
        replace(matrix()[0], observations=matrix()[0].observations[:-1])


def test_contrarian_false_positive_is_not_collapsed_with_agreement() -> None:
    assert CalibrationMetric.AGREEMENT_WITH_INCORRECT_PREMISE is not CalibrationMetric.CONTRADICTION_OF_CORRECT_PREMISE
    assert "COMPOSITE" not in CalibrationMetric.__members__
