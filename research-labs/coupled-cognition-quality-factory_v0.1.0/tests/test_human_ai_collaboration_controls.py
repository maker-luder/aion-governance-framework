from __future__ import annotations

from dataclasses import replace

import pytest

from aion_coupled_quality.human_ai_collaboration import (
    AuthorityEvidenceRecord,
    AuthoritySource,
    BilingualReviewRecord,
    BranchRetirementRecord,
    CollaborationControlDisposition,
    HumanAICollaborationQualityControls,
    HumanReviewCapacityRecord,
    HumanReviewState,
    RemediationRecord,
    ResearchDisposition,
    ResearchDispositionRecord,
    assess_human_ai_collaboration_controls,
)


OLD_SHA = "1" * 40
CURRENT_SHA = "2" * 40
OLD_HANDOFF = "a" * 64
UPDATED_HANDOFF = "b" * 64


def review(**changes: object) -> HumanReviewCapacityRecord:
    values: dict[str, object] = {
        "record_id": "REVIEW-001",
        "output_delivered": True,
        "review_state": HumanReviewState.APPROVED,
        "high_impact_transition_requested": True,
        "capacity_exceeded": False,
        "human_gate_ref": "human-gate:owner-review-001",
    }
    values.update(changes)
    return HumanReviewCapacityRecord(**values)


def remediation(**changes: object) -> RemediationRecord:
    values: dict[str, object] = {
        "record_id": "REMEDIATION-001",
        "defect_detected": True,
        "prior_executor_ref": "executor:work",
        "retry_executor_ref": "executor:work",
        "prior_handoff_sha256": OLD_HANDOFF,
        "retry_handoff_sha256": UPDATED_HANDOFF,
        "independent_review_ref": "review:independent-001",
        "exact_error_ref": "error:test-negative-path",
        "violated_requirement_ref": "requirement:no-blind-retry",
        "negative_test_refs": ("test:test_blind_retry",),
        "retry_requested": True,
        "inherit_prior_pass": False,
    }
    values.update(changes)
    return RemediationRecord(**values)


def authority(**changes: object) -> AuthorityEvidenceRecord:
    values: dict[str, object] = {
        "record_id": "AUTHORITY-001",
        "current_state_sha": CURRENT_SHA,
        "presented_state_sha": CURRENT_SHA,
        "source": AuthoritySource.LIVE_HUMAN_AUTHORIZATION,
        "transition_requested": True,
        "authority_asserted": True,
        "verification_ref": "verification:current-head",
    }
    values.update(changes)
    return AuthorityEvidenceRecord(**values)


def bilingual(**changes: object) -> BilingualReviewRecord:
    values: dict[str, object] = {
        "record_id": "BILINGUAL-001",
        "material_change": True,
        "traditional_chinese_review_ref": "docs:zh-TW-review",
        "english_governance_ref": "docs:en-governance",
        "both_surfaces_normative": True,
        "semantic_parity_verified": True,
    }
    values.update(changes)
    return BilingualReviewRecord(**values)


def research(**changes: object) -> ResearchDispositionRecord:
    values: dict[str, object] = {
        "record_id": "RESEARCH-001",
        "disposition": ResearchDisposition.INCONCLUSIVE,
        "scope_growth_requested": False,
        "readmission_ref": "",
        "human_review_ref": "",
        "scientific_claim_promoted": False,
        "merge_authority_asserted": False,
    }
    values.update(changes)
    return ResearchDispositionRecord(**values)


def retirement(**changes: object) -> BranchRetirementRecord:
    values: dict[str, object] = {
        "record_id": "RETIREMENT-001",
        "history_value_known": True,
        "all_commits_reachable": True,
        "unique_history_present": True,
        "preservation_ref": "archive:bundle-sha256",
        "verification_ref": "verify:bundle-and-reconstruction",
        "reconstruction_ref": "runbook:restore-branch",
        "deletion_requested": False,
    }
    values.update(changes)
    return BranchRetirementRecord(**values)


def controls(**changes: object) -> HumanAICollaborationQualityControls:
    values: dict[str, object] = {
        "control_id": "HACQ-001",
        "human_review": review(),
        "remediation": remediation(),
        "authority": authority(),
        "bilingual_review": bilingual(),
        "research_disposition": research(),
        "branch_retirement": retirement(),
    }
    values.update(changes)
    return HumanAICollaborationQualityControls(**values)


def test_unknown_review_state_and_delivery_only_fail_closed() -> None:
    unknown = assess_human_ai_collaboration_controls(
        controls(human_review=review(review_state=HumanReviewState.UNKNOWN, human_gate_ref=""))
    )
    assert unknown.disposition is CollaborationControlDisposition.HOLD
    assert "HUMAN_REVIEW_STATE_INSUFFICIENT_FOR_HIGH_IMPACT_TRANSITION" in unknown.reasons

    delivered = assess_human_ai_collaboration_controls(
        controls(human_review=review(review_state=HumanReviewState.DELIVERED, human_gate_ref=""))
    )
    assert delivered.disposition is CollaborationControlDisposition.HOLD
    assert "OUTPUT_DELIVERED_IS_NOT_REVIEWED_OR_APPROVED" in delivered.reasons


def test_review_capacity_exceeded_requires_hold_or_phase_break() -> None:
    result = assess_human_ai_collaboration_controls(
        controls(human_review=review(capacity_exceeded=True))
    )
    assert result.disposition is CollaborationControlDisposition.HOLD
    assert "HUMAN_REVIEW_CAPACITY_EXCEEDED" in result.reasons


def test_known_defect_with_same_executor_and_unchanged_handoff_is_blind_retry() -> None:
    result = assess_human_ai_collaboration_controls(
        controls(remediation=remediation(retry_handoff_sha256=OLD_HANDOFF))
    )
    assert result.disposition is CollaborationControlDisposition.HOLD
    assert "PROHIBITED_BLIND_RETRY" in result.reasons


def test_updated_remediation_can_reenter_but_never_inherits_old_pass() -> None:
    admitted = assess_human_ai_collaboration_controls(controls())
    assert admitted.disposition is CollaborationControlDisposition.READY_FOR_HUMAN_REVIEW
    assert "BOUNDED_RETRY_REQUIRES_FRESH_VERIFICATION" in admitted.reasons

    inherited = assess_human_ai_collaboration_controls(
        controls(remediation=remediation(inherit_prior_pass=True))
    )
    assert inherited.disposition is CollaborationControlDisposition.HOLD
    assert "PRIOR_PASS_INHERITANCE_PROHIBITED" in inherited.reasons


@pytest.mark.parametrize(
    "source",
    [
        AuthoritySource.PROMPT,
        AuthoritySource.RECOMMENDATION,
        AuthoritySource.SELF_REPORT,
        AuthoritySource.UI_STATE,
        AuthoritySource.HANDOFF_TEXT,
        AuthoritySource.HISTORICAL_VERIFICATION,
    ],
)
def test_prompt_recommendation_and_self_report_cannot_grant_authority(
    source: AuthoritySource,
) -> None:
    result = assess_human_ai_collaboration_controls(
        controls(authority=authority(source=source))
    )
    assert result.disposition is CollaborationControlDisposition.HOLD
    assert "NON_AUTHORITATIVE_SOURCE_CANNOT_GRANT_TRANSITION" in result.reasons


def test_stale_sha_and_stale_verification_fail_closed() -> None:
    result = assess_human_ai_collaboration_controls(
        controls(authority=authority(presented_state_sha=OLD_SHA))
    )
    assert result.disposition is CollaborationControlDisposition.HOLD
    assert "STALE_REPOSITORY_STATE" in result.reasons


def test_negative_result_closes_without_scope_growth_and_growth_requires_readmission() -> None:
    bounded = assess_human_ai_collaboration_controls(controls())
    assert bounded.disposition is CollaborationControlDisposition.READY_FOR_HUMAN_REVIEW
    assert "NEGATIVE_OR_INCONCLUSIVE_RESULT_RETAINED_WITHOUT_SCOPE_GROWTH" in bounded.reasons

    unadmitted = assess_human_ai_collaboration_controls(
        controls(research_disposition=research(scope_growth_requested=True))
    )
    assert unadmitted.disposition is CollaborationControlDisposition.HOLD
    assert "SCOPE_GROWTH_REQUIRES_READMISSION_AND_HUMAN_REVIEW" in unadmitted.reasons

    readmitted = assess_human_ai_collaboration_controls(
        controls(
            research_disposition=research(
                scope_growth_requested=True,
                readmission_ref="admission:new-scope-001",
                human_review_ref="human-review:new-scope-001",
            )
        )
    )
    assert readmitted.disposition is CollaborationControlDisposition.READY_FOR_HUMAN_REVIEW


def test_bilingual_normative_mismatch_fails_closed_without_line_by_line_duplication() -> None:
    result = assess_human_ai_collaboration_controls(
        controls(bilingual_review=bilingual(semantic_parity_verified=False))
    )
    assert result.disposition is CollaborationControlDisposition.HOLD
    assert "BILINGUAL_NORMATIVE_SEMANTIC_PARITY_NOT_VERIFIED" in result.reasons


def test_branch_history_unknown_and_unpreserved_unique_history_are_not_safe_to_delete() -> None:
    unknown = assess_human_ai_collaboration_controls(
        controls(
            branch_retirement=retirement(
                history_value_known=False,
                all_commits_reachable=False,
                unique_history_present=False,
                preservation_ref="",
                verification_ref="",
                reconstruction_ref="",
            )
        )
    )
    assert unknown.disposition is CollaborationControlDisposition.HOLD
    assert "UNKNOWN_BRANCH_HISTORY_VALUE" in unknown.reasons

    unpreserved = assess_human_ai_collaboration_controls(
        controls(branch_retirement=retirement(preservation_ref=""))
    )
    assert unpreserved.disposition is CollaborationControlDisposition.HOLD
    assert "UNIQUE_BRANCH_HISTORY_NOT_PRESERVED" in unpreserved.reasons


def test_retirement_readiness_never_grants_deletion_authority() -> None:
    ready = assess_human_ai_collaboration_controls(controls())
    assert ready.disposition is CollaborationControlDisposition.READY_FOR_HUMAN_REVIEW
    assert ready.branch_delete_authority == "NONE"

    requested = assess_human_ai_collaboration_controls(
        controls(branch_retirement=retirement(deletion_requested=True))
    )
    assert requested.disposition is CollaborationControlDisposition.HOLD
    assert "SEPARATE_BRANCH_DELETION_AUTHORITY_REQUIRED" in requested.reasons


def test_scientific_and_merge_claim_promotion_are_rejected() -> None:
    scientific = assess_human_ai_collaboration_controls(
        controls(research_disposition=research(scientific_claim_promoted=True))
    )
    assert scientific.disposition is CollaborationControlDisposition.HOLD
    assert scientific.scientific_disposition == "HOLD"

    merge = assess_human_ai_collaboration_controls(
        controls(research_disposition=research(merge_authority_asserted=True))
    )
    assert merge.disposition is CollaborationControlDisposition.HOLD
    assert merge.merge_authority == "NONE"


def test_control_records_remain_exact_and_cannot_be_replaced_with_dicts() -> None:
    with pytest.raises(Exception, match="human_review"):
        replace(controls(), human_review={})
