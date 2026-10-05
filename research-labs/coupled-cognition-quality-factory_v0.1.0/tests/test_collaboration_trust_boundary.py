"""Regression for caller-supplied READY. / 呼叫端偽造 READY 的回歸測試。"""

from dataclasses import replace

import pytest

from aion_coupled_quality import QualityError
from aion_coupled_quality.end_to_end import EndToEndDisposition
from aion_coupled_quality.human_ai_collaboration import (
    CollaborationControlDisposition,
    HumanAICollaborationQualityAssessment,
    assess_human_ai_collaboration_controls,
)
from test_extended_quality import assess, extended_controls, quality_plan, review
from test_human_ai_collaboration_controls import (
    controls,
    review as human_review,
    authority,
    bilingual,
    remediation,
    research,
    retirement,
)


def assert_rejected_at_consumer(report):
    """Run real Full-QMS; type rejection or HOLD is fail closed. / 執行真實消費端。"""
    base_review = review()
    try:
        result = assess(
            controls_value=replace(extended_controls(), human_ai_collaboration=(report,)),
            review_value=replace(base_review, input_refs=(*base_review.input_refs, report.control_id)),
        )
    except QualityError:
        return
    assert result.disposition is EndToEndDisposition.HOLD


@pytest.mark.parametrize("reasons", [(), ("SIX_CONTROLS_EVALUATED",)])
def test_full_qms_rejects_forged_ready_even_with_reason_strings(reasons):
    report = HumanAICollaborationQualityAssessment(
        control_id="forged-without-controls",
        disposition=CollaborationControlDisposition.READY_FOR_HUMAN_REVIEW,
        reasons=reasons,
    )
    assert_rejected_at_consumer(report)


def test_replace_cannot_turn_evaluated_hold_into_trusted_ready():
    held = assess_human_ai_collaboration_controls(controls(human_review=human_review(capacity_exceeded=True)))
    assert held.disposition is CollaborationControlDisposition.HOLD
    forged = replace(
        held,
        disposition=CollaborationControlDisposition.READY_FOR_HUMAN_REVIEW,
        control_id="forged-after-evaluation",
        reasons=("SIX_CONTROLS_EVALUATED",),
    )
    assert_rejected_at_consumer(forged)


@pytest.mark.parametrize(
    "changes",
    [
        {"merge_authority": "GRANTED"},
        {"branch_delete_authority": "GRANTED"},
        {"canonical_effect": "MAIN"},
        {"deployment": True},
        {"scientific_disposition": "PASS"},
    ],
)
def test_report_replace_cannot_promote_fixed_authority_or_science(changes):
    report = assess_human_ai_collaboration_controls(controls())
    with pytest.raises(QualityError):
        replace(report, **changes)


def assess_raw(raw, *, reviewed_raw=None, configured_sha=None):
    """Bind real plan and review to inputs. / 綁定真實引擎的計畫與審閱輸入。"""
    reviewed = raw if reviewed_raw is None else reviewed_raw
    bound_controls = replace(extended_controls(), human_ai_collaboration=(raw,))
    reviewed_controls = replace(extended_controls(), human_ai_collaboration=(reviewed,))
    base_review = review()
    bound_review = replace(
        base_review,
        input_refs=tuple(
            dict.fromkeys(
                (
                    *base_review.input_refs,
                    *reviewed_controls.trace_refs(),
                )
            )
        ),
    )
    plan = quality_plan()
    state_sha = raw.authority.current_state_sha if configured_sha is None else configured_sha
    plan = replace(plan, configuration_refs=(*plan.configuration_refs, f"git:{state_sha}"))
    return assess(controls_value=bound_controls, review_value=bound_review, plan_value=plan)


def test_full_qms_evaluates_complete_raw_controls_and_preserves_authority_ceiling():
    result = assess_raw(controls())
    assert result.disposition is EndToEndDisposition.READY_FOR_HUMAN_REVIEW
    assert "HUMAN_AI_COLLABORATION_CONTROLS_READY_FOR_HUMAN_REVIEW" in result.reasons
    assert result.merge_authority == "NONE"
    assert result.scientific_disposition == "HOLD"
    assert result.canonical_effect == "NONE"
    assert result.deployment is False


@pytest.mark.parametrize(
    "changed",
    [
        {"human_review": human_review(capacity_exceeded=True)},
        {"remediation": remediation(retry_handoff_sha256="a" * 64)},
        {"authority": authority(presented_state_sha="1" * 40)},
        {"bilingual_review": bilingual(semantic_parity_verified=False)},
        {"research_disposition": research(scientific_claim_promoted=True)},
        {"branch_retirement": retirement(history_value_known=False)},
    ],
)
def test_each_evaluated_control_hold_propagates_to_full_qms(changed):
    result = assess_raw(controls(**changed))
    assert result.disposition is EndToEndDisposition.HOLD
    assert "HUMAN_AI_COLLABORATION_CONTROL_HOLD" in result.reasons


def test_fake_live_authority_without_verification_is_hold():
    result = assess_raw(controls(authority=authority(verification_ref="")))
    assert result.disposition is EndToEndDisposition.HOLD
    assert result.merge_authority == "NONE"


def test_live_authority_label_and_fabricated_reference_never_grant_action_authority():
    raw = controls(authority=authority(verification_ref="caller:invented-reference"))
    result = assess_raw(raw)
    report = assess_human_ai_collaboration_controls(raw)
    assert result.merge_authority == report.merge_authority == "NONE"
    assert report.branch_delete_authority == "NONE"
    assert report.canonical_effect == "NONE"
    assert result.deployment is report.deployment is False


@pytest.mark.parametrize(
    "changed",
    [
        {"control_id": "changed-id"},
        {"bilingual_review": bilingual(traditional_chinese_review_ref="docs:changed-content")},
    ],
)
def test_management_review_cannot_be_reused_after_input_or_id_changes(changed):
    original = controls()
    result = assess_raw(replace(original, **changed), reviewed_raw=original)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "MANAGEMENT_REVIEW_EXTENDED_CONTROL_INPUTS_INCOMPLETE" in result.reasons


def test_equal_declared_state_must_still_bind_quality_plan():
    raw = controls(authority=authority(current_state_sha="0" * 40, presented_state_sha="0" * 40))
    result = assess_raw(raw, configured_sha="2" * 40)
    assert result.disposition is EndToEndDisposition.HOLD
    assert "COLLABORATION_STATE_NOT_BOUND_TO_QUALITY_PLAN" in result.reasons


def test_even_legitimate_derived_ready_cannot_replace_raw_inputs():
    report = assess_human_ai_collaboration_controls(controls())
    assert report.disposition is CollaborationControlDisposition.READY_FOR_HUMAN_REVIEW
    assert_rejected_at_consumer(replace(report, control_id="changed-after-evaluation"))


def test_nested_input_mutation_is_revalidated_at_evaluation():
    raw = controls()
    object.__setattr__(raw.authority, "source", "LIVE_HUMAN_AUTHORIZATION")
    with pytest.raises(QualityError, match="source"):
        assess_human_ai_collaboration_controls(raw)


def test_whitespace_reference_cannot_stand_in_for_evidence():
    with pytest.raises(QualityError, match="verification_ref"):
        authority(verification_ref=" ")


def test_raw_inputs_cannot_use_mutable_collection():
    with pytest.raises(QualityError):
        assess(controls_value=replace(extended_controls(), human_ai_collaboration=[controls()]))


def test_optional_omission_does_not_claim_collaboration_was_evaluated():
    result = assess()
    assert result.disposition is EndToEndDisposition.READY_FOR_HUMAN_REVIEW
    assert "HUMAN_AI_COLLABORATION_CONTROLS_READY_FOR_HUMAN_REVIEW" not in result.reasons
