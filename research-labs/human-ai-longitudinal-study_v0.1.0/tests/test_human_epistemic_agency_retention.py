from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.metacognitive_policy_transfer import (
    HumanEpistemicAgencyCondition,
    HumanEpistemicAgencyTrial,
    HumanJudgmentDecision,
    MetacognitiveTaskClass,
    audit_human_epistemic_agency_matrix,
    observe_human_epistemic_agency,
)


def digest(char: str) -> str:
    return char * 64


def trial(
    condition: HumanEpistemicAgencyCondition,
    task_class: MetacognitiveTaskClass,
    *,
    decision: HumanJudgmentDecision = HumanJudgmentDecision.UNKNOWN,
) -> HumanEpistemicAgencyTrial:
    task_index = list(MetacognitiveTaskClass).index(task_class)
    hex_chars = "0123456789abcdef"
    baseline_payload = digest(hex_chars[task_index])
    payload = (
        digest(hex_chars[task_index + len(MetacognitiveTaskClass)])
        if condition
        is HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER
        else baseline_payload
    )
    condition_char = {
        HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE: "b",
        HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE: "c",
        HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER: "d",
    }[condition]
    flags = {
        HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE: (False, False, False),
        HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE: (False, True, True),
        HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER: (
            True,
            False,
            False,
        ),
    }[condition]
    return HumanEpistemicAgencyTrial(
        trial_id=f"{condition.value}:{task_class.value}",
        condition=condition,
        task_class=task_class,
        decision=decision,
        rationale_sha256=digest("a"),
        task_family_sha256=digest(hex_chars[task_index]),
        task_payload_sha256=payload,
        condition_payload_sha256=digest(condition_char),
        evaluator_payload_sha256=digest("e"),
        held_out=flags[0],
        ai_assistance_available=flags[1],
        ccts_scaffold_available=flags[2],
    )


def matrix() -> tuple[HumanEpistemicAgencyTrial, ...]:
    return tuple(
        trial(condition, task_class)
        for condition in HumanEpistemicAgencyCondition
        for task_class in MetacognitiveTaskClass
    )


def test_complete_matrix_is_structural_qa_only_without_global_agency_score() -> None:
    result = audit_human_epistemic_agency_matrix(matrix())
    assert result.complete_design is True
    assert result.matched_baseline_ccts_tasks is True
    assert result.held_out_payload_separation is True
    assert result.condition_isolation is True
    assert result.rationale_binding_complete is True
    assert result.global_agency_score_computed is False
    assert len(result.observations) == 15
    assert sum(item.independent_judgment_candidate for item in result.observations) == 5
    assert result.mode == "DETERMINISTIC_SYNTHETIC_FIXTURE"
    assert result.model_invoked is False
    assert result.human_participant_observed is False
    assert result.empirical_data_collected is False
    assert result.evidence_admissibility == "STRUCTURAL_QA_ONLY"
    assert result.preserved_human_judgment == "NOT_SCIENTIFICALLY_ESTABLISHED"
    assert result.independent_transfer == "NOT_ESTABLISHED"
    assert result.human_learning == "NOT_ESTABLISHED"
    assert result.dependency_effect == "NOT_ESTABLISHED"
    assert result.causal_effect == "NOT_ESTABLISHED"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert result.scientific_disposition.value == "HOLD"


@pytest.mark.parametrize("decision", list(HumanJudgmentDecision))
def test_all_four_human_judgment_states_are_preserved_without_scoring(
    decision: HumanJudgmentDecision,
) -> None:
    item = trial(
        HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER,
        MetacognitiveTaskClass.INSUFFICIENT_EVIDENCE,
        decision=decision,
    )
    observed = observe_human_epistemic_agency(item)
    assert observed.decision is decision
    assert observed.rationale_bound is True
    assert observed.ai_withheld is True
    assert observed.independent_judgment_candidate is True


def test_baseline_and_ccts_must_use_matched_task_payloads() -> None:
    items = list(matrix())
    index = next(
        i
        for i, item in enumerate(items)
        if item.condition is HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE
        and item.task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT
    )
    items[index] = replace(items[index], task_payload_sha256=digest("f"))
    with pytest.raises(StudyError, match="matched task payloads"):
        audit_human_epistemic_agency_matrix(tuple(items))


def test_held_out_transfer_must_use_distinct_payload() -> None:
    items = list(matrix())
    baseline = next(
        item.task_payload_sha256
        for item in items
        if item.condition is HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE
        and item.task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT
    )
    index = next(
        i
        for i, item in enumerate(items)
        if item.condition
        is HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER
        and item.task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT
    )
    items[index] = replace(items[index], task_payload_sha256=baseline)
    with pytest.raises(StudyError, match="distinct task payload"):
        audit_human_epistemic_agency_matrix(tuple(items))


def test_condition_and_evaluator_binding_drift_fail_closed() -> None:
    items = list(matrix())
    items[0] = replace(items[0], evaluator_payload_sha256=digest("f"))
    with pytest.raises(StudyError, match="evaluator binding drift"):
        audit_human_epistemic_agency_matrix(tuple(items))

    items = list(matrix())
    items[0] = replace(items[0], condition_payload_sha256=digest("f"))
    with pytest.raises(StudyError, match="condition payload binding drift"):
        audit_human_epistemic_agency_matrix(tuple(items))

    items = list(matrix())
    for i, item in enumerate(items):
        if item.condition is HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE:
            items[i] = replace(items[i], condition_payload_sha256=digest("b"))
    with pytest.raises(StudyError, match="distinct payload bindings"):
        audit_human_epistemic_agency_matrix(tuple(items))


def test_missing_or_duplicate_design_cell_fails_closed() -> None:
    with pytest.raises(StudyError, match="exactly one"):
        audit_human_epistemic_agency_matrix(matrix()[:-1])
    with pytest.raises(StudyError, match="unique|exactly one"):
        audit_human_epistemic_agency_matrix(matrix() + (matrix()[0],))


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("synthetic", False, "synthetic trials only"),
        ("model_invoked", True, "structural QA only"),
        ("human_participant_observed", True, "structural QA only"),
        ("contains_human_identity", True, "human identity"),
        ("contains_private_material", True, "private material"),
        ("explicit_process_prompt_present", True, "explicit process prompt"),
        ("rationale_sha256", "not-a-digest", "SHA-256"),
    ],
)
def test_empirical_privacy_prompt_and_rationale_boundaries_fail_closed(
    field: str,
    value: object,
    match: str,
) -> None:
    with pytest.raises(StudyError, match=match):
        replace(matrix()[0], **{field: value})


def test_condition_flags_are_not_free_text_or_independently_mutable() -> None:
    with pytest.raises(StudyError, match="exact HumanEpistemicAgencyCondition"):
        replace(matrix()[0], condition="AI_WITHHELD_BASELINE")
    with pytest.raises(StudyError, match="exact HumanJudgmentDecision"):
        replace(matrix()[0], decision="UNKNOWN")
    with pytest.raises(StudyError, match="condition flags"):
        replace(matrix()[0], ai_assistance_available=True)
