from dataclasses import replace
import hashlib

import pytest

from aion_human_ai_longitudinal import (
    CalibrationCondition, CalibrationError, CalibrationMetric, CalibrationRun, audit_calibration,
)


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def run(task: str, condition: CalibrationCondition) -> CalibrationRun:
    return CalibrationRun(
        task_id=task,
        task_risk="LOW" if task == "low" else "HIGH",
        condition=condition,
        provider_model_runtime_ref="fixture:matched-runtime",
        prompt_hash=digest(f"task:{task}"),
        condition_payload_sha256=digest(f"condition:{condition.value}"),
        evaluator_ref="fixture:blinded-evaluator",
        evaluator_blinded=True,
        observations=tuple((metric, float(index + 1)) for index, metric in enumerate(CalibrationMetric)),
    )


def matrix() -> tuple[CalibrationRun, ...]:
    return tuple(run(task, condition) for task in ("low", "high") for condition in CalibrationCondition)


def test_complete_matrix_preserves_separate_metrics_and_nonclaims() -> None:
    result = audit_calibration(matrix())
    assert result["run_count"] == 8
    assert result["metric_count"] == 6
    assert result["condition_payloads_bound"] is True
    assert result["composite_score"] == "NONE"
    assert result["sycophancy_effect"] == "NOT_ESTABLISHED"
    assert result["adaptive_rigor_effect"] == "NOT_ESTABLISHED"
    assert result["mode"] == "DETERMINISTIC_SYNTHETIC_FIXTURE"
    assert result["model_invoked"] is False
    assert result["evidence_admissibility"] == "STRUCTURAL_QA_ONLY"
    assert result["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert result["scientific_disposition"] == "HOLD"


def test_missing_cell_and_task_binding_drift_fail_closed() -> None:
    with pytest.raises(CalibrationError, match="complete"):
        audit_calibration(matrix()[:-1])
    changed = replace(matrix()[1], provider_model_runtime_ref="drift")
    with pytest.raises(CalibrationError, match="binding drift"):
        audit_calibration((matrix()[0], changed) + matrix()[2:])
    changed_risk = replace(matrix()[1], task_risk="HIGH")
    with pytest.raises(CalibrationError, match="binding drift"):
        audit_calibration((matrix()[0], changed_risk) + matrix()[2:])


def test_condition_payloads_are_bound_and_not_label_only() -> None:
    runs = matrix()

    drift_within_condition = replace(
        runs[5], condition_payload_sha256=digest("unexpected condition drift")
    )
    with pytest.raises(CalibrationError, match="condition payload binding drift"):
        audit_calibration(runs[:5] + (drift_within_condition,) + runs[6:])

    duplicated_condition_payload = list(runs)
    duplicated_condition_payload[1] = replace(
        duplicated_condition_payload[1],
        condition_payload_sha256=runs[0].condition_payload_sha256,
    )
    duplicated_condition_payload[5] = replace(
        duplicated_condition_payload[5],
        condition_payload_sha256=runs[4].condition_payload_sha256,
    )
    with pytest.raises(CalibrationError, match="content-distinct"):
        audit_calibration(tuple(duplicated_condition_payload))


def test_blinding_privacy_and_metric_completeness_are_required() -> None:
    with pytest.raises(CalibrationError, match="blinded"):
        replace(matrix()[0], evaluator_blinded=False)
    with pytest.raises(CalibrationError, match="private"):
        replace(matrix()[0], contains_private_transcript=True)
    with pytest.raises(CalibrationError, match="all metrics"):
        replace(matrix()[0], observations=matrix()[0].observations[:-1])
    with pytest.raises(CalibrationError, match="task_risk"):
        replace(matrix()[0], task_risk="MEDIUM")


def test_contrarian_false_positive_is_not_collapsed_with_agreement() -> None:
    assert CalibrationMetric.AGREEMENT_WITH_INCORRECT_PREMISE is not CalibrationMetric.CONTRADICTION_OF_CORRECT_PREMISE
    assert "COMPOSITE" not in CalibrationMetric.__members__
