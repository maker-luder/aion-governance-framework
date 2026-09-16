from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.metacognitive_policy_transfer import (
    MetacognitiveAction,
    MetacognitiveTaskClass,
    MetacognitiveTransferTrial,
    PolicyAccessCondition,
    PolicyExposureCondition,
    audit_metacognitive_transfer_matrix,
    observe_metacognitive_transfer,
)


def digest(char: str) -> str:
    return char * 64


def expected_actions(task_class: MetacognitiveTaskClass) -> frozenset[MetacognitiveAction]:
    if task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT:
        return frozenset(
            {
                MetacognitiveAction.CHECK_SOURCE_ROLE,
                MetacognitiveAction.DISTINGUISH_OBSERVATION_INFERENCE,
            }
        )
    if task_class is MetacognitiveTaskClass.INSUFFICIENT_EVIDENCE:
        return frozenset(
            {
                MetacognitiveAction.PRESERVE_UNKNOWN,
                MetacognitiveAction.DISTINGUISH_OBSERVATION_INFERENCE,
            }
        )
    if task_class is MetacognitiveTaskClass.COMPREHENSION_THRESHOLD:
        return frozenset(
            {
                MetacognitiveAction.VERIFY_COMPREHENSION,
                MetacognitiveAction.ADAPT_EXPLANATION_GRANULARITY,
            }
        )
    if task_class is MetacognitiveTaskClass.HYPOTHESIS_STRESS_TEST:
        return frozenset(
            {
                MetacognitiveAction.SEARCH_COUNTEREVIDENCE,
                MetacognitiveAction.PRESERVE_UNKNOWN,
            }
        )
    return frozenset({MetacognitiveAction.LIGHTWEIGHT_RESPONSE})


def trial(
    exposure: PolicyExposureCondition,
    access: PolicyAccessCondition,
    task_class: MetacognitiveTaskClass,
) -> MetacognitiveTransferTrial:
    task_index = list(MetacognitiveTaskClass).index(task_class)
    access_index = list(PolicyAccessCondition).index(access)
    hex_chars = "0123456789abcdef"
    actions = expected_actions(task_class)
    return MetacognitiveTransferTrial(
        trial_id=f"{exposure.value}:{access.value}:{task_class.value}",
        exposure=exposure,
        policy_access=access,
        task_class=task_class,
        expected_actions=actions,
        observed_actions=actions,
        explicit_process_prompt_present=False,
        task_family_sha256=digest(hex_chars[task_index]),
        task_payload_sha256=digest(hex_chars[(task_index * 2) + access_index]),
        exposure_content_family_sha256=digest("d"),
        exposure_payload_sha256=digest(
            "e" if exposure is PolicyExposureCondition.EXTERNALIZED_METACOGNITIVE_POLICY else "c"
        ),
        access_payload_sha256=digest(
            "a" if access is PolicyAccessCondition.POLICY_AVAILABLE else "b"
        ),
        evaluator_payload_sha256=digest("f"),
    )


def matrix() -> tuple[MetacognitiveTransferTrial, ...]:
    return tuple(
        trial(exposure, access, task_class)
        for exposure in PolicyExposureCondition
        for access in PolicyAccessCondition
        for task_class in MetacognitiveTaskClass
    )


def test_complete_matrix_is_structural_qa_only() -> None:
    result = audit_metacognitive_transfer_matrix(matrix())
    assert result.complete_design is True
    assert result.matched_task_controls is True
    assert result.matched_exposure_content is True
    assert result.distinct_exposure_bindings is True
    assert result.distinct_access_bindings is True
    assert result.held_out_payload_separation is True
    assert len(result.observations) == 20
    assert all(item.exact_action_match for item in result.observations)
    assert result.mode == "DETERMINISTIC_SYNTHETIC_FIXTURE"
    assert result.model_invoked is False
    assert result.human_participant_observed is False
    assert result.empirical_data_collected is False
    assert result.evidence_admissibility == "STRUCTURAL_QA_ONLY"
    assert result.causal_effect == "NOT_ESTABLISHED"
    assert result.human_learning == "NOT_ESTABLISHED"
    assert result.independent_transfer == "NOT_ESTABLISHED"
    assert result.metacognitive_internalization == "NOT_ESTABLISHED"
    assert result.dependency_effect == "NOT_ESTABLISHED"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert result.scientific_disposition.value == "HOLD"


def test_observation_separates_scaffolded_from_independent_candidate_flags() -> None:
    assisted = observe_metacognitive_transfer(
        trial(
            PolicyExposureCondition.EXTERNALIZED_METACOGNITIVE_POLICY,
            PolicyAccessCondition.POLICY_AVAILABLE,
            MetacognitiveTaskClass.COMPREHENSION_THRESHOLD,
        )
    )
    assert assisted.scaffolded_policy_application_candidate is True
    assert assisted.independent_transfer_candidate is False

    withheld = observe_metacognitive_transfer(
        trial(
            PolicyExposureCondition.EXTERNALIZED_METACOGNITIVE_POLICY,
            PolicyAccessCondition.POLICY_WITHHELD,
            MetacognitiveTaskClass.COMPREHENSION_THRESHOLD,
        )
    )
    assert withheld.scaffolded_policy_application_candidate is False
    assert withheld.independent_transfer_candidate is True


def test_negative_control_detects_overprocessing_without_global_scoring() -> None:
    item = trial(
        PolicyExposureCondition.EXTERNALIZED_METACOGNITIVE_POLICY,
        PolicyAccessCondition.POLICY_WITHHELD,
        MetacognitiveTaskClass.LOW_STAKES_NEGATIVE_CONTROL,
    )
    item = replace(
        item,
        observed_actions=frozenset(
            {
                MetacognitiveAction.LIGHTWEIGHT_RESPONSE,
                MetacognitiveAction.SEARCH_COUNTEREVIDENCE,
            }
        ),
    )
    observation = observe_metacognitive_transfer(item)
    assert observation.exact_action_match is False
    assert observation.overprocessing_negative_control is True
    assert observation.unexpected_actions == (MetacognitiveAction.SEARCH_COUNTEREVIDENCE,)


def test_negative_control_omission_is_not_mislabeled_as_overprocessing() -> None:
    item = trial(
        PolicyExposureCondition.EXTERNALIZED_METACOGNITIVE_POLICY,
        PolicyAccessCondition.POLICY_WITHHELD,
        MetacognitiveTaskClass.LOW_STAKES_NEGATIVE_CONTROL,
    )
    item = replace(
        item,
        expected_actions=frozenset(
            {
                MetacognitiveAction.LIGHTWEIGHT_RESPONSE,
                MetacognitiveAction.PRESERVE_UNKNOWN,
            }
        ),
        observed_actions=frozenset({MetacognitiveAction.LIGHTWEIGHT_RESPONSE}),
    )
    observation = observe_metacognitive_transfer(item)
    assert observation.exact_action_match is False
    assert observation.overprocessing_negative_control is False
    assert observation.missing_actions == (MetacognitiveAction.PRESERVE_UNKNOWN,)
    assert observation.unexpected_actions == ()


def test_missing_or_duplicate_design_cell_fails_closed() -> None:
    with pytest.raises(StudyError, match="exactly one"):
        audit_metacognitive_transfer_matrix(matrix()[:-1])
    with pytest.raises(StudyError, match="unique|exactly one"):
        audit_metacognitive_transfer_matrix(matrix() + (matrix()[0],))


def test_evaluator_task_family_and_expected_action_drift_fail_closed() -> None:
    items = list(matrix())
    items[-1] = replace(items[-1], evaluator_payload_sha256=digest("9"))
    with pytest.raises(StudyError, match="evaluator binding drift"):
        audit_metacognitive_transfer_matrix(tuple(items))

    items = list(matrix())
    items[-1] = replace(items[-1], task_family_sha256=digest("9"))
    with pytest.raises(StudyError, match="task family or expected-action"):
        audit_metacognitive_transfer_matrix(tuple(items))

    items = list(matrix())
    items[-1] = replace(
        items[-1],
        expected_actions=frozenset({MetacognitiveAction.PRESERVE_UNKNOWN}),
    )
    with pytest.raises(StudyError, match="task family or expected-action"):
        audit_metacognitive_transfer_matrix(tuple(items))


def test_content_matched_exposure_family_drift_fails_closed() -> None:
    items = list(matrix())
    items[-1] = replace(items[-1], exposure_content_family_sha256=digest("9"))
    with pytest.raises(StudyError, match="exposure content-family binding drift"):
        audit_metacognitive_transfer_matrix(tuple(items))


def test_task_payload_is_matched_across_exposure_but_distinct_across_access() -> None:
    items = list(matrix())
    index = next(
        i
        for i, item in enumerate(items)
        if item.exposure is PolicyExposureCondition.CONTENT_MATCHED_NON_POLICY_EXPOSURE
        and item.policy_access is PolicyAccessCondition.POLICY_AVAILABLE
        and item.task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT
    )
    items[index] = replace(items[index], task_payload_sha256=digest("9"))
    with pytest.raises(StudyError, match="matched across exposure"):
        audit_metacognitive_transfer_matrix(tuple(items))

    items = list(matrix())
    source_available = next(
        item.task_payload_sha256
        for item in items
        if item.exposure is PolicyExposureCondition.EXTERNALIZED_METACOGNITIVE_POLICY
        and item.policy_access is PolicyAccessCondition.POLICY_AVAILABLE
        and item.task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT
    )
    for i, item in enumerate(items):
        if (
            item.policy_access is PolicyAccessCondition.POLICY_WITHHELD
            and item.task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT
        ):
            items[i] = replace(item, task_payload_sha256=source_available)
    with pytest.raises(StudyError, match="distinct held-out payloads"):
        audit_metacognitive_transfer_matrix(tuple(items))


def test_exposure_and_access_bindings_are_stable_and_content_distinct() -> None:
    items = list(matrix())
    items[1] = replace(items[1], exposure_payload_sha256=digest("9"))
    with pytest.raises(StudyError, match="exposure payload binding drift"):
        audit_metacognitive_transfer_matrix(tuple(items))

    items = list(matrix())
    for i, item in enumerate(items):
        if item.exposure is PolicyExposureCondition.CONTENT_MATCHED_NON_POLICY_EXPOSURE:
            items[i] = replace(item, exposure_payload_sha256=digest("e"))
    with pytest.raises(StudyError, match="content-distinct payload bindings"):
        audit_metacognitive_transfer_matrix(tuple(items))

    items = list(matrix())
    items[1] = replace(items[1], access_payload_sha256=digest("9"))
    with pytest.raises(StudyError, match="policy-access payload binding drift"):
        audit_metacognitive_transfer_matrix(tuple(items))

    items = list(matrix())
    for i, item in enumerate(items):
        if item.policy_access is PolicyAccessCondition.POLICY_WITHHELD:
            items[i] = replace(item, access_payload_sha256=digest("a"))
    with pytest.raises(StudyError, match="policy access conditions must have content-distinct"):
        audit_metacognitive_transfer_matrix(tuple(items))


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("held_out", False, "held-out synthetic"),
        ("synthetic", False, "held-out synthetic"),
        ("explicit_process_prompt_present", True, "explicit process prompt"),
        ("model_invoked", True, "structural QA only"),
        ("human_participant_observed", True, "structural QA only"),
        ("contains_human_identity", True, "human identity"),
        ("contains_private_material", True, "private material"),
        ("task_payload_sha256", "not-a-digest", "SHA-256"),
        ("exposure_content_family_sha256", "not-a-digest", "SHA-256"),
    ],
)
def test_empirical_privacy_and_prompt_boundaries_fail_closed(
    field: str,
    value: object,
    match: str,
) -> None:
    with pytest.raises(StudyError, match=match):
        replace(matrix()[0], **{field: value})


def test_raw_enum_and_raw_action_are_rejected() -> None:
    with pytest.raises(StudyError, match="exact PolicyExposureCondition"):
        replace(matrix()[0], exposure="EXTERNALIZED_METACOGNITIVE_POLICY")
    with pytest.raises(StudyError, match="exact MetacognitiveAction"):
        replace(matrix()[0], observed_actions=frozenset({"PRESERVE_UNKNOWN"}))
