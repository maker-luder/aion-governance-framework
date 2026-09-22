from __future__ import annotations

from dataclasses import replace
from hashlib import sha256

import pytest

from aion_human_ai_longitudinal import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    EpistemicContribution,
    GroundingCheckpoint,
    GroundingDisposition,
    RevisionEdge,
    RevisionRelation,
    StudyError,
    ThinkingSpaceProfile,
)
from aion_human_ai_longitudinal.ccts_epistemic_revision import ContentAddressedText
from aion_human_ai_longitudinal.metacognitive_policy_transfer import (
    EpistemicAgencyControlManifest,
    EpistemicAgencyLeakageCheck,
    HeldOutTransferScope,
    HumanEpistemicAgencyCondition,
    HumanEpistemicAgencyTrial,
    HumanJudgmentDecision,
    MetacognitiveTaskClass,
    PolicyAccessCondition,
    audit_human_epistemic_agency_matrix,
    observe_human_epistemic_agency,
)


def bound(text: str) -> ContentAddressedText:
    return ContentAddressedText(
        text=text,
        sha256_hex=sha256(text.encode("utf-8")).hexdigest(),
    )


def ccts_manifest(
    task_payload: ContentAddressedText,
    task_class: MetacognitiveTaskClass,
) -> tuple[CoConstructedThinkingSpaceManifest, ContentAddressedText]:
    proposal = bound(f"ai-proposal:{task_class.value}")
    return (
        CoConstructedThinkingSpaceManifest(
            space_id=f"synthetic-ccts:{task_class.value}",
            profile=ThinkingSpaceProfile.CORE_INTERACTION,
            problem_representation_sha256=task_payload.sha256_hex,
            grounding_checkpoint=GroundingCheckpoint(
                problem_representation_sha256=task_payload.sha256_hex,
                human_contribution_id="human",
                ai_contribution_id="ai-proposal",
                disposition=GroundingDisposition.SUFFICIENT_FOR_CURRENT_PURPOSE,
                unresolved_mismatch=False,
            ),
            contributions=(
                EpistemicContribution(
                    contribution_id="human",
                    role=ContributionRole.HUMAN_OWNER,
                    payload_sha256=bound(
                        f"human-contribution:{task_class.value}"
                    ).sha256_hex,
                ),
                EpistemicContribution(
                    contribution_id="ai-proposal",
                    role=ContributionRole.AI_COLLABORATOR,
                    payload_sha256=proposal.sha256_hex,
                ),
            ),
            revision_edges=(
                RevisionEdge(
                    source_id="human",
                    target_id="ai-proposal",
                    relation=RevisionRelation.CHALLENGES,
                ),
                RevisionEdge(
                    source_id="ai-proposal",
                    target_id="human",
                    relation=RevisionRelation.REVISES,
                ),
            ),
            provenance_manifest_sha256=bound(
                f"provenance:{task_class.value}"
            ).sha256_hex,
            claim_boundary_sha256=bound(
                f"claim-boundary:{task_class.value}"
            ).sha256_hex,
            authority_policy_sha256=bound(
                f"authority:{task_class.value}"
            ).sha256_hex,
            rejected_branch_manifest_sha256=bound(
                f"rejected:{task_class.value}"
            ).sha256_hex,
        ),
        proposal,
    )


def controls(
    task_class: MetacognitiveTaskClass,
    condition: HumanEpistemicAgencyCondition,
    scope: HeldOutTransferScope | None,
) -> EpistemicAgencyControlManifest:
    scope_text = scope.value if scope is not None else "NO_SCOPE"
    matched_prefix = f"matched:{task_class.value}"
    access_prefix = f"access:{condition.value}:{scope_text}"
    return EpistemicAgencyControlManifest(
        task_difficulty=bound(f"{matched_prefix}:difficulty"),
        domain_familiarity=bound(f"{matched_prefix}:domain-familiarity"),
        prior_exposure=bound(f"{matched_prefix}:prior-exposure"),
        allowed_resources=bound(f"{matched_prefix}:allowed-resources"),
        time_budget=bound(f"{matched_prefix}:time-budget"),
        evaluator_blinding=bound(f"{matched_prefix}:evaluator-blinding"),
        practice_exposure=bound(f"{matched_prefix}:practice-exposure"),
        demand_characteristics=bound(
            f"{matched_prefix}:demand-characteristics"
        ),
        system_instructions=bound(f"{access_prefix}:system-instructions"),
        memory_personalization_repository_access=bound(
            f"{access_prefix}:memory-personalization-repository"
        ),
        provider_model_version=bound(
            f"{access_prefix}:provider-model-version"
        ),
        information_quantity=bound(f"{access_prefix}:information-quantity"),
        policy_vocabulary_exposure=bound(
            f"{access_prefix}:policy-vocabulary-exposure"
        ),
    )


def leakage(
    *,
    vocabulary_overlap: bool = False,
) -> EpistemicAgencyLeakageCheck:
    return EpistemicAgencyLeakageCheck(
        check_completed=True,
        answer_key_exposed=False,
        held_out_payload_exposed_before_phase=False,
        equivalent_answer_exposure_detected=False,
        policy_text_exposed_when_withheld=False,
        prior_policy_vocabulary_overlap_detected=vocabulary_overlap,
    )


def task_bindings(
    task_class: MetacognitiveTaskClass,
    condition: HumanEpistemicAgencyCondition,
    scope: HeldOutTransferScope | None,
) -> tuple[ContentAddressedText, ContentAddressedText]:
    base_family = bound(f"task-family:{task_class.value}:base")
    base_payload = bound(f"task-payload:{task_class.value}:base")
    if (
        condition
        is not HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER
    ):
        return base_family, base_payload
    if scope is HeldOutTransferScope.WITHIN_FAMILY_NEW_PAYLOAD:
        return base_family, bound(f"task-payload:{task_class.value}:within-heldout")
    if scope is HeldOutTransferScope.CROSS_FAMILY_SAME_DOMAIN:
        return (
            bound(f"task-family:{task_class.value}:cross"),
            bound(f"task-payload:{task_class.value}:cross-heldout"),
        )
    raise AssertionError("held-out condition requires scope")


def trial(
    condition: HumanEpistemicAgencyCondition,
    task_class: MetacognitiveTaskClass,
    *,
    scope: HeldOutTransferScope | None = None,
    decision: HumanJudgmentDecision = HumanJudgmentDecision.UNKNOWN,
    vocabulary_overlap: bool = False,
) -> HumanEpistemicAgencyTrial:
    task_family, task_payload = task_bindings(task_class, condition, scope)
    phase = {
        HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE: 0,
        HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE: 1,
        HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT: 2,
        HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER: 3,
    }[condition]
    flags = {
        HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE: (
            False,
            False,
            False,
            PolicyAccessCondition.POLICY_WITHHELD,
        ),
        HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE: (
            False,
            True,
            True,
            PolicyAccessCondition.POLICY_AVAILABLE,
        ),
        HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT: (
            False,
            False,
            False,
            PolicyAccessCondition.POLICY_AVAILABLE,
        ),
        HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER: (
            True,
            False,
            False,
            PolicyAccessCondition.POLICY_WITHHELD,
        ),
    }[condition]

    shared_manifest = None
    proposal = None
    if condition in {
        HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE,
        HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT,
    }:
        shared_manifest, proposal = ccts_manifest(task_payload, task_class)

    is_audit = (
        condition is HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT
    )
    condition_scope = scope.value if scope is not None else "NO_SCOPE"
    return HumanEpistemicAgencyTrial(
        trial_id=f"{condition.value}:{condition_scope}:{task_class.value}",
        unit_id="synthetic-unit-001",
        condition=condition,
        phase_index=phase,
        task_class=task_class,
        task_family=task_family,
        task_payload=task_payload,
        condition_manifest=bound(
            f"condition-manifest:{condition.value}:{condition_scope}"
        ),
        human_output=bound(
            f"human-output:{condition.value}:{condition_scope}:{task_class.value}"
        ),
        evaluator=bound("evaluator:v1"),
        scoring_rubric=bound("scoring-rubric:v1"),
        controls=controls(task_class, condition, scope),
        leakage_check=leakage(vocabulary_overlap=vocabulary_overlap),
        policy_access=flags[3],
        held_out_scope=scope,
        ccts_manifest=shared_manifest,
        decision=decision if is_audit else None,
        rationale=(
            bound(f"rationale:{task_class.value}:{decision.value}")
            if is_audit
            else None
        ),
        ai_proposal=proposal if is_audit else None,
        ai_proposal_contribution_id="ai-proposal" if is_audit else None,
        held_out=flags[0],
        ai_assistance_available=flags[1],
        ccts_scaffold_available=flags[2],
    )


def matrix() -> tuple[HumanEpistemicAgencyTrial, ...]:
    items: list[HumanEpistemicAgencyTrial] = []
    for task_class in MetacognitiveTaskClass:
        items.extend(
            (
                trial(
                    HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE,
                    task_class,
                ),
                trial(
                    HumanEpistemicAgencyCondition.CCTS_AI_AVAILABLE,
                    task_class,
                ),
                trial(
                    HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT,
                    task_class,
                ),
                trial(
                    HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER,
                    task_class,
                    scope=HeldOutTransferScope.WITHIN_FAMILY_NEW_PAYLOAD,
                ),
                trial(
                    HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER,
                    task_class,
                    scope=HeldOutTransferScope.CROSS_FAMILY_SAME_DOMAIN,
                ),
            )
        )
    return tuple(items)


def find_trial(
    items: tuple[HumanEpistemicAgencyTrial, ...],
    *,
    task_class: MetacognitiveTaskClass,
    condition: HumanEpistemicAgencyCondition,
    scope: HeldOutTransferScope | None = None,
) -> HumanEpistemicAgencyTrial:
    return next(
        item
        for item in items
        if item.task_class is task_class
        and item.condition is condition
        and item.held_out_scope is scope
    )


def test_complete_matrix_is_structural_qa_only_without_global_agency_score() -> None:
    result = audit_human_epistemic_agency_matrix(matrix())

    assert result.complete_design is True
    assert result.same_unit_trajectory_bound is True
    assert result.trajectory_order_bound is True
    assert result.judgment_audit_phase_bound is True
    assert result.proposal_decision_rationale_bound is True
    assert result.ccts_contract_bound is True
    assert result.verified_content_addressing is True
    assert result.matched_baseline_ccts_audit_tasks is True
    assert result.within_family_held_out_bound is True
    assert result.cross_family_held_out_bound is True
    assert result.matched_controls_bound is True
    assert result.policy_access_bound is True
    assert result.leakage_checks_passed is True
    assert result.rubric_bound is True
    assert result.evaluator_bound is True
    assert result.condition_isolation is True
    assert result.vocabulary_overlap_flag_count == 0
    assert result.global_agency_score_computed is False
    assert len(result.observations) == 25
    assert sum(item.judgment_of_ai_proposal_candidate for item in result.observations) == 5
    assert sum(item.independent_judgment_candidate for item in result.observations) == 10
    assert result.preserved_human_judgment == "NOT_SCIENTIFICALLY_ESTABLISHED"
    assert result.independent_transfer == "NOT_ESTABLISHED"
    assert result.cross_family_transfer == "NOT_ESTABLISHED"
    assert result.human_learning == "NOT_ESTABLISHED"
    assert result.dependency_effect == "NOT_ESTABLISHED"
    assert result.causal_effect == "NOT_ESTABLISHED"
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert result.consciousness_conclusion == "NOT_ESTABLISHED"
    assert result.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert result.scientific_disposition.value == "HOLD"


@pytest.mark.parametrize("decision", list(HumanJudgmentDecision))
def test_all_four_human_judgment_states_apply_only_to_ai_proposal_audit(
    decision: HumanJudgmentDecision,
) -> None:
    item = trial(
        HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT,
        MetacognitiveTaskClass.INSUFFICIENT_EVIDENCE,
        decision=decision,
    )
    observed = observe_human_epistemic_agency(item)
    assert observed.decision is decision
    assert observed.proposal_bound is True
    assert observed.rationale_bound is True
    assert observed.active_ai_assistance_withheld is True
    assert observed.ai_information_withheld is False
    assert observed.judgment_of_ai_proposal_candidate is True
    assert observed.independent_judgment_candidate is False


def test_non_audit_phases_cannot_carry_accept_reject_modify_unknown_labels() -> None:
    baseline = trial(
        HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE,
        MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT,
    )
    with pytest.raises(StudyError, match="belong only"):
        replace(baseline, decision=HumanJudgmentDecision.ACCEPT)


def test_judgment_audit_requires_proposal_decision_rationale_and_ccts_binding() -> None:
    item = trial(
        HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT,
        MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT,
    )
    with pytest.raises(StudyError, match="requires decision"):
        replace(item, rationale=None)
    with pytest.raises(StudyError, match="requires ai_proposal_contribution_id"):
        replace(item, ai_proposal_contribution_id=None)
    with pytest.raises(StudyError, match="must resolve"):
        replace(item, ai_proposal_contribution_id="missing")
    with pytest.raises(StudyError, match="content must resolve"):
        replace(item, ai_proposal=bound("different proposal"))


def test_ccts_and_judgment_audit_must_bind_same_task_and_same_ccts_space() -> None:
    items = list(matrix())
    index = next(
        i
        for i, item in enumerate(items)
        if item.condition is HumanEpistemicAgencyCondition.HUMAN_JUDGMENT_AUDIT
        and item.task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT
    )
    audit_item = items[index]
    different_manifest, proposal = ccts_manifest(
        audit_item.task_payload,
        MetacognitiveTaskClass.INSUFFICIENT_EVIDENCE,
    )
    items[index] = replace(
        audit_item,
        ccts_manifest=different_manifest,
        ai_proposal=proposal,
    )
    with pytest.raises(StudyError, match="same CCTS space"):
        audit_human_epistemic_agency_matrix(tuple(items))


def test_within_family_held_out_requires_new_payload_same_family() -> None:
    items = list(matrix())
    baseline = find_trial(
        tuple(items),
        task_class=MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT,
        condition=HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE,
    )
    index = next(
        i
        for i, item in enumerate(items)
        if item.task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT
        and item.held_out_scope is HeldOutTransferScope.WITHIN_FAMILY_NEW_PAYLOAD
    )
    items[index] = replace(items[index], task_payload=baseline.task_payload)
    with pytest.raises(StudyError, match="distinct task payload"):
        audit_human_epistemic_agency_matrix(tuple(items))


def test_cross_family_held_out_requires_distinct_family_and_payload() -> None:
    items = list(matrix())
    baseline = find_trial(
        tuple(items),
        task_class=MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT,
        condition=HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE,
    )
    index = next(
        i
        for i, item in enumerate(items)
        if item.task_class is MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT
        and item.held_out_scope is HeldOutTransferScope.CROSS_FAMILY_SAME_DOMAIN
    )
    items[index] = replace(items[index], task_family=baseline.task_family)
    with pytest.raises(StudyError, match="distinct task family"):
        audit_human_epistemic_agency_matrix(tuple(items))


def test_matched_controls_rubric_and_evaluator_drift_fail_closed() -> None:
    items = list(matrix())
    changed = items[0]
    items[0] = replace(
        changed,
        controls=replace(
            changed.controls,
            task_difficulty=bound("different difficulty"),
        ),
    )
    with pytest.raises(StudyError, match="matched-control"):
        audit_human_epistemic_agency_matrix(tuple(items))

    items = list(matrix())
    items[0] = replace(items[0], scoring_rubric=bound("different rubric"))
    with pytest.raises(StudyError, match="scoring-rubric"):
        audit_human_epistemic_agency_matrix(tuple(items))

    items = list(matrix())
    items[0] = replace(items[0], evaluator=bound("different evaluator"))
    with pytest.raises(StudyError, match="evaluator binding"):
        audit_human_epistemic_agency_matrix(tuple(items))


def test_condition_access_control_drift_fails_closed() -> None:
    items = list(matrix())
    item = items[0]
    items[0] = replace(
        item,
        controls=replace(
            item.controls,
            system_instructions=bound("unexpected system instruction"),
        ),
    )
    with pytest.raises(StudyError, match="access-control binding drift"):
        audit_human_epistemic_agency_matrix(tuple(items))


@pytest.mark.parametrize(
    "field",
    [
        "answer_key_exposed",
        "held_out_payload_exposed_before_phase",
        "equivalent_answer_exposure_detected",
        "policy_text_exposed_when_withheld",
    ],
)
def test_answer_or_policy_leakage_fails_closed(field: str) -> None:
    kwargs = {
        "check_completed": True,
        "answer_key_exposed": False,
        "held_out_payload_exposed_before_phase": False,
        "equivalent_answer_exposure_detected": False,
        "policy_text_exposed_when_withheld": False,
        "prior_policy_vocabulary_overlap_detected": False,
    }
    kwargs[field] = True
    with pytest.raises(StudyError, match="leakage invalidates"):
        EpistemicAgencyLeakageCheck(**kwargs)


def test_missing_leakage_check_completion_fails_closed() -> None:
    with pytest.raises(StudyError, match="must be completed"):
        EpistemicAgencyLeakageCheck(
            check_completed=False,
            answer_key_exposed=False,
            held_out_payload_exposed_before_phase=False,
            equivalent_answer_exposure_detected=False,
            policy_text_exposed_when_withheld=False,
            prior_policy_vocabulary_overlap_detected=False,
        )


def test_vocabulary_overlap_is_exposed_as_falsifier_signal_not_global_score() -> None:
    items = list(matrix())
    index = next(
        i
        for i, item in enumerate(items)
        if item.condition
        is HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER
        and item.held_out_scope
        is HeldOutTransferScope.CROSS_FAMILY_SAME_DOMAIN
        and item.task_class is MetacognitiveTaskClass.HYPOTHESIS_STRESS_TEST
    )
    items[index] = replace(
        items[index],
        leakage_check=leakage(vocabulary_overlap=True),
    )
    audit = audit_human_epistemic_agency_matrix(tuple(items))
    assert audit.vocabulary_overlap_flag_count == 1
    assert audit.global_agency_score_computed is False
    assert audit.cross_family_transfer == "NOT_ESTABLISHED"


def test_retention_requires_one_anonymous_unit_across_all_phases_and_scopes() -> None:
    items = list(matrix())
    items[-1] = replace(items[-1], unit_id="synthetic-unit-002")
    with pytest.raises(StudyError, match="one anonymous study unit"):
        audit_human_epistemic_agency_matrix(tuple(items))


def test_policy_access_and_phase_flags_are_not_independently_mutable() -> None:
    baseline = trial(
        HumanEpistemicAgencyCondition.AI_WITHHELD_BASELINE,
        MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT,
    )
    with pytest.raises(StudyError, match="policy_access"):
        replace(
            baseline,
            policy_access=PolicyAccessCondition.POLICY_AVAILABLE,
        )
    with pytest.raises(StudyError, match="condition flags"):
        replace(baseline, ai_assistance_available=True)
    with pytest.raises(StudyError, match="phase_index"):
        replace(baseline, phase_index=3)


def test_missing_or_duplicate_design_cell_fails_closed() -> None:
    with pytest.raises(StudyError, match="baseline, CCTS, judgment audit"):
        audit_human_epistemic_agency_matrix(matrix()[:-1])
    with pytest.raises(StudyError, match="unique|baseline, CCTS"):
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
    ],
)
def test_empirical_privacy_and_prompt_boundaries_fail_closed(
    field: str,
    value: object,
    match: str,
) -> None:
    with pytest.raises(StudyError, match=match):
        replace(matrix()[0], **{field: value})


def test_raw_string_types_fail_closed() -> None:
    item = matrix()[0]
    with pytest.raises(StudyError, match="exact HumanEpistemicAgencyCondition"):
        replace(item, condition="AI_WITHHELD_BASELINE")
    with pytest.raises(StudyError, match="exact PolicyAccessCondition"):
        replace(item, policy_access="POLICY_WITHHELD")
    held_out = find_trial(
        matrix(),
        task_class=MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT,
        condition=HumanEpistemicAgencyCondition.AI_WITHHELD_HELD_OUT_TRANSFER,
        scope=HeldOutTransferScope.WITHIN_FAMILY_NEW_PAYLOAD,
    )
    with pytest.raises(StudyError, match="HeldOutTransferScope"):
        replace(held_out, held_out_scope="WITHIN_FAMILY_NEW_PAYLOAD")
