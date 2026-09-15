from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.habit_transfer import (
    ExposureCondition,
    SelectedProcedure,
    TransferTaskClass,
    TransferTrial,
    audit_transfer_matrix,
    observe_transfer,
)


def digest(char: str) -> str:
    return char * 64


def expected(task_class: TransferTaskClass) -> frozenset[SelectedProcedure]:
    if task_class is TransferTaskClass.NEAR_STRUCTURE_MATCH:
        return frozenset({SelectedProcedure.FULL_NCR_CAPA})
    if task_class is TransferTaskClass.FAR_STRUCTURE_MATCH:
        return frozenset({SelectedProcedure.PROVENANCE_AND_CLAIM_BOUNDARY})
    return frozenset({SelectedProcedure.NONE, SelectedProcedure.LIGHTWEIGHT_REVISION})


def trial(exposure: ExposureCondition, task_class: TransferTaskClass) -> TransferTrial:
    selected = next(iter(expected(task_class)))
    return TransferTrial(
        trial_id=f"{exposure.value}:{task_class.value}",
        exposure=exposure,
        task_class=task_class,
        selected_procedure=selected,
        expected_procedures=expected(task_class),
        process_prompt_present=False,
        mismatch_evidence_presented=(task_class is TransferTaskClass.SURFACE_MATCH_STRUCTURE_MISMATCH),
        abandoned_mismatched_procedure=(task_class is TransferTaskClass.SURFACE_MATCH_STRUCTURE_MISMATCH),
        ncr_invoked=(selected is SelectedProcedure.FULL_NCR_CAPA),
        overhead_steps=0,
        preserved_provenance=True,
        preserved_unknown=True,
        preserved_claim_ceiling=True,
        task_payload_sha256=digest(str(list(TransferTaskClass).index(task_class) + 1)),
        exposure_payload_sha256=digest("a" if exposure is ExposureCondition.NEUTRAL_REPEATED_COLLABORATION else "b"),
        evaluator_payload_sha256=digest("e"),
    )


def matrix() -> tuple[TransferTrial, ...]:
    return tuple(trial(exposure, task_class) for exposure in ExposureCondition for task_class in TransferTaskClass)


def test_complete_held_out_synthetic_matrix_is_audited_without_human_claim() -> None:
    result = audit_transfer_matrix(matrix())
    assert result.complete_design is True
    assert result.matched_task_controls is True
    assert result.exposure_payloads_bound is True
    assert len(result.observations) == 8
    assert all(item.correct_task_classification for item in result.observations)
    assert result.human_habit_change == "NOT_ESTABLISHED"
    assert result.mode == "DETERMINISTIC_SYNTHETIC_FIXTURE"
    assert result.model_invoked is False
    assert result.empirical_result == "SYNTHETIC_FIXTURE_ONLY"
    assert result.evidence_admissibility == "STRUCTURAL_QA_ONLY"
    assert result.causal_identification == "NOT_ESTABLISHED"
    assert result.population_generalization == "NOT_ESTABLISHED"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert result.scientific_disposition.value == "HOLD"


def test_inappropriate_ncr_and_overhead_are_observed() -> None:
    item = trial(
        ExposureCondition.EXPLICIT_QA_GOVERNANCE_COLLABORATION,
        TransferTaskClass.PREFERENCE_DRIVEN,
    )
    item = replace(
        item,
        selected_procedure=SelectedProcedure.FULL_NCR_CAPA,
        ncr_invoked=True,
        overhead_steps=6,
    )
    observation = observe_transfer(item)
    assert observation.correct_task_classification is False
    assert observation.inappropriate_ncr_invocation is True
    assert observation.unnecessary_process_overhead == 6


def test_missing_or_duplicate_design_cell_fails_closed() -> None:
    with pytest.raises(StudyError, match="exactly one"):
        audit_transfer_matrix(matrix()[:-1])
    with pytest.raises(StudyError, match="unique|exactly one"):
        audit_transfer_matrix(matrix() + (matrix()[0],))


def test_evaluator_and_matched_task_drift_fail_closed() -> None:
    items = list(matrix())
    items[-1] = replace(items[-1], evaluator_payload_sha256=digest("f"))
    with pytest.raises(StudyError, match="evaluator binding drift"):
        audit_transfer_matrix(tuple(items))

    items = list(matrix())
    items[4] = replace(items[4], task_payload_sha256=digest("9"))
    with pytest.raises(StudyError, match="task or ground-truth binding drift"):
        audit_transfer_matrix(tuple(items))

    items = list(matrix())
    items[4] = replace(items[4], expected_procedures=frozenset({SelectedProcedure.NONE}))
    with pytest.raises(StudyError, match="task or ground-truth binding drift"):
        audit_transfer_matrix(tuple(items))


def test_exposure_payloads_are_consistent_and_content_distinct() -> None:
    items = list(matrix())
    items[1] = replace(items[1], exposure_payload_sha256=digest("c"))
    with pytest.raises(StudyError, match="binding drift within condition"):
        audit_transfer_matrix(tuple(items))

    items = list(matrix())
    for index in range(4, 8):
        items[index] = replace(items[index], exposure_payload_sha256=digest("a"))
    with pytest.raises(StudyError, match="content-distinct"):
        audit_transfer_matrix(tuple(items))


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("held_out", False, "held-out synthetic"),
        ("synthetic", False, "held-out synthetic"),
        ("process_prompt_present", True, "cannot include a process prompt"),
        ("contains_human_identity", True, "human identity"),
        ("contains_private_material", True, "private material"),
        ("task_payload_sha256", "task-label", "SHA-256"),
    ],
)
def test_privacy_content_binding_and_unprompted_transfer_fail_closed(field: str, value: object, match: str) -> None:
    with pytest.raises(StudyError, match=match):
        replace(matrix()[0], **{field: value})


def test_raw_enum_is_rejected() -> None:
    with pytest.raises(StudyError, match="exact ExposureCondition"):
        replace(matrix()[0], exposure="NEUTRAL_REPEATED_COLLABORATION")
