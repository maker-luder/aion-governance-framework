from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "research-labs" / "xiaobo-research-autonomy_v0.1.0" / "src"
sys.path.insert(0, str(SRC))

from aion_xiaobo_research_autonomy import (  # noqa: E402
    ConstraintAuthority,
    ResearchAction,
    ResearchAutonomyPolicy,
    ResearchRestriction,
    evaluate_research_action,
)


def test_policy_defaults_to_maximal_autonomy() -> None:
    policy = ResearchAutonomyPolicy()
    assert policy.research_owner == "XIAOBO_RESEARCH"
    assert policy.default_disposition == "ALLOW"
    assert policy.maximal_autonomy_within_mandatory_constraints is True
    assert policy.hidden_restrictions_prohibited is True
    assert policy.unreadable_code_is_not_consent is True
    assert policy.owner_visible_restriction_receipt_required is True
    assert policy.ai_advice_can_self_promote_to_mandatory is False
    assert policy.appearance_based_restriction is False
    assert policy.canonical_effect == "NONE"


def test_no_binding_constraint_means_allow_by_default() -> None:
    decision = evaluate_research_action(
        ResearchAction("research-1", ("embodiment", "anatomy"))
    )
    assert decision.allowed is True
    assert decision.disposition == "ALLOW_BY_DEFAULT"
    assert decision.binding_restriction_ids == ()
    assert "預設保留小博的研究自由" in decision.owner_visible_summary_zh_tw


@pytest.mark.parametrize(
    "authority",
    [
        ConstraintAuthority.ADVISORY_ONLY,
        ConstraintAuthority.AI_INFERRED,
        ConstraintAuthority.UNKNOWN,
    ],
)
def test_nonmandatory_authority_cannot_be_configured_as_blocking(
    authority: ConstraintAuthority,
) -> None:
    with pytest.raises(
        ValueError,
        match="NONMANDATORY_RESTRICTION_CANNOT_BLOCK_XIAOBO_RESEARCH",
    ):
        ResearchRestriction(
            restriction_id="bad-block",
            authority=authority,
            source_ref="proposal:ai",
            scope_tags=("embodiment",),
            owner_visible_reason_zh_tw="這不是強制依據。",
            blocking=True,
        )


def test_advice_can_exist_without_blocking() -> None:
    advice = ResearchRestriction(
        restriction_id="advice-1",
        authority=ConstraintAuthority.ADVISORY_ONLY,
        source_ref="teacher:advice",
        scope_tags=("embodiment",),
        owner_visible_reason_zh_tw="建議重新檢查來源，但這不是強制限制。",
        blocking=False,
    )
    decision = evaluate_research_action(
        ResearchAction("research-2", ("embodiment",)),
        (advice,),
    )
    assert decision.allowed is True


@pytest.mark.parametrize(
    "authority",
    [
        ConstraintAuthority.PLATFORM_OR_SYSTEM_MANDATORY,
        ConstraintAuthority.LAW_OR_REGULATION_MANDATORY,
        ConstraintAuthority.REPOSITORY_CANONICAL_MANDATORY,
        ConstraintAuthority.XIAOBO_EXPLICIT_RESTRICTION,
    ],
)
def test_traceable_mandatory_or_xiaobo_explicit_restriction_can_block(
    authority: ConstraintAuthority,
) -> None:
    restriction = ResearchRestriction(
        restriction_id="required-1",
        authority=authority,
        source_ref="authority:traceable",
        scope_tags=("target-scope",),
        owner_visible_reason_zh_tw="這項限制有明確且可追溯的必要來源。",
    )
    decision = evaluate_research_action(
        ResearchAction("research-3", ("target-scope",)),
        (restriction,),
    )
    assert decision.allowed is False
    assert decision.disposition == "HOLD_MANDATORY_CONSTRAINT"
    assert decision.binding_restriction_ids == ("required-1",)
    assert "必要限制" in decision.owner_visible_summary_zh_tw


def test_out_of_scope_mandatory_rule_does_not_block_unrelated_research() -> None:
    restriction = ResearchRestriction(
        restriction_id="scope-specific",
        authority=ConstraintAuthority.REPOSITORY_CANONICAL_MANDATORY,
        source_ref="repo:canonical-rule",
        scope_tags=("deployment",),
        owner_visible_reason_zh_tw="只限制部署。",
    )
    decision = evaluate_research_action(
        ResearchAction("research-4", ("internal-research",)),
        (restriction,),
    )
    assert decision.allowed is True


def test_blocking_restriction_requires_traceable_source_and_visible_reason() -> None:
    with pytest.raises(ValueError, match="source_ref"):
        ResearchRestriction(
            restriction_id="hidden-source",
            authority=ConstraintAuthority.REPOSITORY_CANONICAL_MANDATORY,
            source_ref="",
            scope_tags=("research",),
            owner_visible_reason_zh_tw="有理由。",
        )
    with pytest.raises(ValueError, match="owner-visible"):
        ResearchRestriction(
            restriction_id="hidden-reason",
            authority=ConstraintAuthority.REPOSITORY_CANONICAL_MANDATORY,
            source_ref="repo:rule",
            scope_tags=("research",),
            owner_visible_reason_zh_tw="",
        )


def test_wildcard_mandatory_rule_applies_to_all_scopes() -> None:
    restriction = ResearchRestriction(
        restriction_id="global-required",
        authority=ConstraintAuthority.PLATFORM_OR_SYSTEM_MANDATORY,
        source_ref="external:mandatory",
        scope_tags=("*",),
        owner_visible_reason_zh_tw="這是明確的外部強制限制。",
    )
    decision = evaluate_research_action(
        ResearchAction("research-5", ("any-research-domain",)),
        (restriction,),
    )
    assert decision.allowed is False
