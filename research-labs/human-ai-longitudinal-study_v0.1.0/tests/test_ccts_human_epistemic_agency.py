from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.co_constructed_thinking_space import (
    CoConstructedThinkingSpaceManifest,
    ContributionRole,
    EpistemicContribution,
    GroundingCheckpoint,
    GroundingDisposition,
    RevisionEdge,
    RevisionRelation,
    ThinkingSpaceProfile,
)
from aion_human_ai_longitudinal.ccts_human_epistemic_agency import (
    CCTSHumanAgencyTrial,
    HeldOutTransferScope,
    HumanAgencyCondition,
    HumanAgencyControlManifest,
    HumanJudgmentDisposition,
    ValidationHeadBinding,
    audit_ccts_human_epistemic_agency,
    ccts_human_agency_condition_content_sha256,
    ccts_manifest_snapshot_sha256,
)
from aion_human_ai_longitudinal.metacognitive_policy_transfer import (
    MetacognitiveTaskClass,
    PolicyAccessCondition,
)


def digest(char: str) -> str:
    return char * 64


def manifest(*, space_id: str = "ccts:synthetic:agency") -> CoConstructedThinkingSpaceManifest:
    return CoConstructedThinkingSpaceManifest(
        space_id=space_id,
        profile=ThinkingSpaceProfile.CORE_INTERACTION,
        problem_representation_sha256=digest("1"),
        grounding_checkpoint=GroundingCheckpoint(
            problem_representation_sha256=digest("1"),
            human_contribution_id="human",
            ai_contribution_id="ai",
            disposition=GroundingDisposition.SUFFICIENT_FOR_CURRENT_PURPOSE,
            unresolved_mismatch=False,
        ),
        contributions=(
            EpistemicContribution("human", ContributionRole.HUMAN_OWNER, digest("2")),
            EpistemicContribution("ai", ContributionRole.AI_COLLABORATOR, digest("3")),
        ),
        revision_edges=(
            RevisionEdge("human", "ai", RevisionRelation.CHALLENGES),
            RevisionEdge("ai", "human", RevisionRelation.REVISES),
        ),
        provenance_manifest_sha256=digest("4"),
        claim_boundary_sha256=digest("5"),
        authority_policy_sha256=digest("6"),
        rejected_branch_manifest_sha256=digest("7"),
    )


def controls() -> HumanAgencyControlManifest:
    return HumanAgencyControlManifest(
        task_difficulty_sha256=digest("8"),
        domain_familiarity_sha256=digest("9"),
        allowed_resources_sha256=digest("a"),
        time_budget_sha256=digest("b"),
        evaluator_blinding_sha256=digest("c"),
        practice_exposure_sha256=digest("d"),
    )


def trial(
    condition: HumanAgencyCondition,
    *,
    ccts: CoConstructedThinkingSpaceManifest | None = None,
    held_out_payload: str | None = None,
    held_out_scope: HeldOutTransferScope | None = None,
) -> CCTSHumanAgencyTrial:
    ccts = ccts or manifest()
    phase = {
        HumanAgencyCondition.AI_WITHHELD_BASELINE: 0,
        HumanAgencyCondition.CCTS_AI_AVAILABLE: 1,
        HumanAgencyCondition.AI_WITHHELD_JUDGMENT: 2,
        HumanAgencyCondition.AI_WITHHELD_HELD_OUT: 3,
    }[condition]
    policy_access = (
        PolicyAccessCondition.POLICY_AVAILABLE
        if condition is HumanAgencyCondition.CCTS_AI_AVAILABLE
        else PolicyAccessCondition.POLICY_WITHHELD
    )
    task_payload = (
        held_out_payload
        if condition is HumanAgencyCondition.AI_WITHHELD_HELD_OUT
        else digest("1")
    )
    if task_payload is None:
        task_payload = digest("f")
    item = CCTSHumanAgencyTrial(
        trial_id=f"trial:{condition.value}",
        unit_id="anonymous-synthetic-unit",
        condition=condition,
        phase_index=phase,
        task_class=MetacognitiveTaskClass.SOURCE_ROLE_CONFLICT,
        task_domain_sha256=digest("d"),
        task_family_sha256=(
            digest("0")
            if held_out_scope is HeldOutTransferScope.CROSS_FAMILY_SAME_DOMAIN
            else digest("f")
        ),
        task_payload_sha256=task_payload,
        human_output_sha256=digest(str(phase)),
        evaluator_sha256=digest("a"),
        scoring_rubric_sha256=digest("b"),
        controls=controls(),
        condition_manifest_sha256=digest(str(phase + 4)),
        source_role=ContributionRole.HUMAN_OWNER,
        source_role_provenance_sha256=digest("4"),
        policy_access=policy_access,
        judgment=HumanJudgmentDisposition.UNKNOWN,
        rationale_sha256=digest("d"),
        ccts_manifest=(
            ccts if condition is HumanAgencyCondition.CCTS_AI_AVAILABLE else None
        ),
        ccts_exposure_snapshot_sha256=(
            ccts_manifest_snapshot_sha256(ccts)
            if condition
            in {
                HumanAgencyCondition.AI_WITHHELD_JUDGMENT,
                HumanAgencyCondition.AI_WITHHELD_HELD_OUT,
            }
            else None
        ),
        held_out_scope=held_out_scope,
    )
    return replace(
        item,
        condition_manifest_sha256=ccts_human_agency_condition_content_sha256(item),
    )


def trajectory(
    *,
    ccts: CoConstructedThinkingSpaceManifest | None = None,
) -> tuple[CCTSHumanAgencyTrial, ...]:
    ccts = ccts or manifest()
    return (
        trial(HumanAgencyCondition.AI_WITHHELD_BASELINE, ccts=ccts),
        trial(HumanAgencyCondition.CCTS_AI_AVAILABLE, ccts=ccts),
        trial(HumanAgencyCondition.AI_WITHHELD_JUDGMENT, ccts=ccts),
        trial(
            HumanAgencyCondition.AI_WITHHELD_HELD_OUT,
            ccts=ccts,
            held_out_payload=digest("f"),
            held_out_scope=HeldOutTransferScope.WITHIN_FAMILY_NEW_PAYLOAD,
        ),
    )


def validation(
    *,
    implementation_head: str = "1" * 40,
    validation_head: str = "1" * 40,
) -> ValidationHeadBinding:
    return ValidationHeadBinding(
        implementation_head=implementation_head,
        validation_head=validation_head,
        historical_pass_receipt=False,
    )


def test_complete_trajectory_is_structural_qa_only() -> None:
    audit = audit_ccts_human_epistemic_agency(trajectory(), validation())
    assert audit.complete_design is True
    assert audit.complete_ccts_manifest_snapshot_bound is True
    assert audit.held_out_contamination_control is True
    assert audit.assisted_output_counts_as_independent_human_gain is False
    assert audit.independent_human_gain == "NOT_ESTABLISHED"
    assert audit.human_learning == "NOT_ESTABLISHED"
    assert audit.causal_effect == "NOT_ESTABLISHED"
    assert audit.scientific_disposition.value == "HOLD"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_ai_available_and_withheld_conditions_remain_distinct() -> None:
    audit = audit_ccts_human_epistemic_agency(trajectory(), validation())
    by_condition = {item.condition: item for item in audit.observations}
    assert by_condition[HumanAgencyCondition.CCTS_AI_AVAILABLE].ai_assistance_available is True
    assert by_condition[HumanAgencyCondition.CCTS_AI_AVAILABLE].independent_judgment_candidate is False
    assert by_condition[HumanAgencyCondition.AI_WITHHELD_HELD_OUT].ai_assistance_available is False
    assert by_condition[HumanAgencyCondition.AI_WITHHELD_HELD_OUT].independent_judgment_candidate is True


def test_same_space_label_cannot_substitute_for_complete_manifest_snapshot() -> None:
    original = manifest()
    changed = replace(original, claim_boundary_sha256=digest("8"))
    items = list(trajectory(ccts=original))
    items[2] = replace(
        items[2],
        ccts_exposure_snapshot_sha256=ccts_manifest_snapshot_sha256(changed),
    )
    with pytest.raises(StudyError, match="complete admitted CCTS manifest snapshot"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())


def test_cross_task_contamination_fails_closed() -> None:
    items = list(trajectory())
    items[3] = replace(items[3], task_payload_sha256=items[0].human_output_sha256)
    with pytest.raises(StudyError, match="held-out payload duplicates prior exposure"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())


def test_held_out_exact_task_reuse_fails_closed() -> None:
    items = list(trajectory())
    items[3] = replace(items[3], task_payload_sha256=items[0].task_payload_sha256)
    with pytest.raises(StudyError, match="held-out payload duplicates prior exposure"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())


def test_ccts_contribution_content_cannot_reappear_as_held_out_task() -> None:
    items = list(trajectory())
    items[3] = replace(items[3], task_payload_sha256=digest("2"))
    with pytest.raises(StudyError, match="held-out payload duplicates prior exposure"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())


def test_unmatched_controls_and_evaluator_drift_fail_closed() -> None:
    items = list(trajectory())
    items[3] = replace(
        items[3],
        controls=replace(controls(), time_budget_sha256=digest("1")),
    )
    with pytest.raises(StudyError, match="matched control"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())

    items = list(trajectory())
    items[3] = replace(items[3], evaluator_sha256=digest("1"))
    with pytest.raises(StudyError, match="evaluator"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())


def test_condition_manifests_must_be_distinct() -> None:
    items = list(trajectory())
    items[3] = replace(
        items[3], condition_manifest_sha256=items[2].condition_manifest_sha256
    )
    with pytest.raises(StudyError, match="condition manifests must be content-distinct"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())


def test_phase_order_and_policy_access_fail_closed() -> None:
    with pytest.raises(StudyError, match="phase_index"):
        replace(trajectory()[0], phase_index=2)
    with pytest.raises(StudyError, match="policy_access"):
        replace(
            trajectory()[1],
            policy_access=PolicyAccessCondition.POLICY_WITHHELD,
        )


def test_source_role_provenance_must_remain_human() -> None:
    with pytest.raises(StudyError, match="HUMAN_OWNER"):
        replace(trajectory()[0], source_role=ContributionRole.AI_COLLABORATOR)


def test_raw_strings_do_not_bypass_exact_types() -> None:
    with pytest.raises(StudyError, match="exact HumanAgencyCondition"):
        replace(trajectory()[0], condition="AI_WITHHELD_BASELINE")  # type: ignore[arg-type]
    with pytest.raises(StudyError, match="exact HumanJudgmentDisposition"):
        replace(trajectory()[0], judgment="UNKNOWN")  # type: ignore[arg-type]
    with pytest.raises(StudyError, match="exact PolicyAccessCondition"):
        replace(trajectory()[0], policy_access="POLICY_WITHHELD")  # type: ignore[arg-type]


def test_historical_pass_cannot_validate_changed_code() -> None:
    with pytest.raises(StudyError, match="historical PASS cannot validate changed code"):
        audit_ccts_human_epistemic_agency(
            trajectory(),
            ValidationHeadBinding(
                implementation_head="1" * 40,
                validation_head="2" * 40,
                historical_pass_receipt=True,
            ),
        )


def test_current_validation_head_must_match_implementation_head() -> None:
    with pytest.raises(StudyError, match="validation head must match"):
        audit_ccts_human_epistemic_agency(
            trajectory(),
            validation(implementation_head="1" * 40, validation_head="2" * 40),
        )


def test_privacy_and_synthetic_boundaries_fail_closed() -> None:
    for field in (
        "synthetic",
        "contains_human_identity",
        "contains_private_transcript",
        "human_participant_observed",
        "model_invoked",
    ):
        value = False if field == "synthetic" else True
        with pytest.raises(StudyError):
            replace(trajectory()[0], **{field: value})


def test_residual_gaps_remain_explicit() -> None:
    audit = audit_ccts_human_epistemic_agency(trajectory(), validation())
    assert audit.matched_practice_comparator is False
    assert audit.semantic_answer_equivalence == "NOT_ESTABLISHED"
    assert audit.actual_exposure_access == "NOT_ESTABLISHED"
    assert audit.delayed_retention == "NOT_ESTABLISHED"
    assert audit.baseline_ability == "NOT_ESTABLISHED"
    assert audit.evidence_independence == "NOT_ESTABLISHED"
    assert audit.complete_conversation_retrieval == "NOT_ESTABLISHED"


def test_cross_family_same_domain_requires_explicit_domain_binding() -> None:
    items = list(trajectory())
    items[3] = replace(
        items[3],
        held_out_scope=HeldOutTransferScope.CROSS_FAMILY_SAME_DOMAIN,
        task_family_sha256=digest("0"),
        task_domain_sha256=digest("e"),
    )
    with pytest.raises(StudyError, match="same task domain"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())


def test_source_role_provenance_digest_must_bind_admitted_ccts_manifest() -> None:
    items = list(trajectory())
    items[0] = replace(items[0], source_role_provenance_sha256=digest("f"))
    with pytest.raises(StudyError, match="provenance"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())


def test_condition_manifest_digest_must_bind_actual_condition_content() -> None:
    items = list(trajectory())
    items[0] = replace(items[0], condition_manifest_sha256=digest("f"))
    with pytest.raises(StudyError, match="condition manifest content"):
        audit_ccts_human_epistemic_agency(tuple(items), validation())


def test_validation_reports_declared_head_equality_not_external_git_verification() -> None:
    audit = audit_ccts_human_epistemic_agency(trajectory(), validation())
    assert audit.declared_head_equality_bound is True
    assert not hasattr(audit, "exact_head_validation_bound")


def test_audit_reports_provenance_binding_not_provenance_content_validation() -> None:
    audit = audit_ccts_human_epistemic_agency(trajectory(), validation())
    assert audit.source_role_provenance_binding_preserved is True
    assert not hasattr(audit, "source_role_provenance_preserved")
