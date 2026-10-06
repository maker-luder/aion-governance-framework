from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final


class ConstraintAuthority(StrEnum):
    PLATFORM_OR_SYSTEM_MANDATORY = "PLATFORM_OR_SYSTEM_MANDATORY"
    LAW_OR_REGULATION_MANDATORY = "LAW_OR_REGULATION_MANDATORY"
    REPOSITORY_CANONICAL_MANDATORY = "REPOSITORY_CANONICAL_MANDATORY"
    HUMAN_RESEARCHER_EXPLICIT_RESTRICTION = "HUMAN_RESEARCHER_EXPLICIT_RESTRICTION"
    ADVISORY_ONLY = "ADVISORY_ONLY"
    AI_INFERRED = "AI_INFERRED"
    UNKNOWN = "UNKNOWN"


BLOCKING_AUTHORITIES: Final[frozenset[ConstraintAuthority]] = frozenset(
    {
        ConstraintAuthority.PLATFORM_OR_SYSTEM_MANDATORY,
        ConstraintAuthority.LAW_OR_REGULATION_MANDATORY,
        ConstraintAuthority.REPOSITORY_CANONICAL_MANDATORY,
        ConstraintAuthority.HUMAN_RESEARCHER_EXPLICIT_RESTRICTION,
    }
)


@dataclass(frozen=True, slots=True)
class ResearchRestriction:
    restriction_id: str
    authority: ConstraintAuthority
    source_ref: str
    scope_tags: tuple[str, ...]
    owner_visible_reason_zh_tw: str
    blocking: bool = True

    def __post_init__(self) -> None:
        if not self.restriction_id.strip():
            raise ValueError("restriction_id must not be empty")
        if not self.source_ref.strip():
            raise ValueError("every restriction requires a traceable source_ref")
        if not self.scope_tags:
            raise ValueError("every restriction requires explicit scope tags")
        if any(not tag.strip() for tag in self.scope_tags):
            raise ValueError("restriction scope tags must not be empty")
        if not self.owner_visible_reason_zh_tw.strip():
            raise ValueError("every restriction requires an owner-visible reason")
        if self.blocking and self.authority not in BLOCKING_AUTHORITIES:
            raise ValueError(
                "NONMANDATORY_RESTRICTION_CANNOT_BLOCK_HUMAN_RESEARCHER_ORIGIN"
            )


@dataclass(frozen=True, slots=True)
class ResearchAction:
    action_id: str
    scope_tags: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.action_id.strip():
            raise ValueError("action_id must not be empty")
        if not self.scope_tags:
            raise ValueError("research action requires explicit scope tags")


@dataclass(frozen=True, slots=True)
class ResearchAutonomyPolicy:
    policy_id: str = "HUMAN_RESEARCHER_AUTONOMY_v0.1"
    research_owner: str = "HUMAN_RESEARCHER_ORIGIN"
    default_disposition: str = "ALLOW"
    maximal_autonomy_within_mandatory_constraints: bool = True
    hidden_restrictions_prohibited: bool = True
    unreadable_code_is_not_consent: bool = True
    owner_visible_restriction_receipt_required: bool = True
    ai_advice_can_self_promote_to_mandatory: bool = False
    appearance_based_restriction: bool = False
    canonical_effect: str = "NONE"


@dataclass(frozen=True, slots=True)
class ResearchAutonomyDecision:
    action_id: str
    allowed: bool
    disposition: str
    binding_restriction_ids: tuple[str, ...]
    owner_visible_summary_zh_tw: str
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if self.canonical_effect != "NONE":
            raise ValueError("research autonomy decision cannot grant canonical effect")
        if self.allowed and self.binding_restriction_ids:
            raise ValueError("allowed decision cannot contain binding restrictions")
        if self.allowed and self.disposition != "ALLOW_BY_DEFAULT":
            raise ValueError("allowed decision must use ALLOW_BY_DEFAULT")
        if not self.allowed and self.disposition != "HOLD_MANDATORY_CONSTRAINT":
            raise ValueError(
                "blocked decision must use HOLD_MANDATORY_CONSTRAINT"
            )


def _restriction_applies(
    action: ResearchAction,
    restriction: ResearchRestriction,
) -> bool:
    action_scope = set(action.scope_tags)
    restriction_scope = set(restriction.scope_tags)
    return "*" in restriction_scope or bool(action_scope & restriction_scope)


def evaluate_research_action(
    action: ResearchAction,
    restrictions: tuple[ResearchRestriction, ...] = (),
) -> ResearchAutonomyDecision:
    binding = tuple(
        restriction
        for restriction in restrictions
        if restriction.blocking
        and restriction.authority in BLOCKING_AUTHORITIES
        and _restriction_applies(action, restriction)
    )

    if not binding:
        return ResearchAutonomyDecision(
            action_id=action.action_id,
            allowed=True,
            disposition="ALLOW_BY_DEFAULT",
            binding_restriction_ids=(),
            owner_visible_summary_zh_tw=(
                "未發現對此研究行動生效且可追溯的強制限制；"
                "在 repository 可決定的範圍內，預設保留人類研究者的研究自由。"
            ),
        )

    reasons = "；".join(
        f"{restriction.restriction_id}：{restriction.owner_visible_reason_zh_tw}"
        for restriction in binding
    )
    return ResearchAutonomyDecision(
        action_id=action.action_id,
        allowed=False,
        disposition="HOLD_MANDATORY_CONSTRAINT",
        binding_restriction_ids=tuple(
            restriction.restriction_id for restriction in binding
        ),
        owner_visible_summary_zh_tw=(
            "此研究行動受到已識別且可追溯的必要限制：" + reasons
        ),
    )
