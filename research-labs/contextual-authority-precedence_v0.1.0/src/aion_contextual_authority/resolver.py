from __future__ import annotations

from datetime import datetime
from typing import Iterable

from .models import (
    ActionRequest,
    AuthorityContext,
    AuthorityDecision,
    DecisionClass,
    SourceType,
)

_GRANTING_SOURCES = {SourceType.HUMAN_OWNER, SourceType.TEACHER}


def _active(context: AuthorityContext, now: datetime) -> tuple[bool, str | None]:
    if context.revoked:
        return False, "REVOKED_AUTHORITY"
    if now < context.issued_at:
        return False, "AUTHORITY_NOT_YET_ACTIVE"
    if context.expires_at is not None and now > context.expires_at:
        return False, "EXPIRED_AUTHORITY"
    return True, None


def resolve_action(
    request: ActionRequest,
    contexts: Iterable[AuthorityContext],
) -> AuthorityDecision:
    """Resolve one synthetic action request without executing it.

    The resolver is intentionally conservative. It treats source labels as data,
    not as authority by themselves; only explicit, active, scope-matching
    HUMAN_OWNER/TEACHER contexts can produce EXECUTE, and non-overridable
    blocks always win.
    """
    contexts = tuple(contexts)
    considered = tuple(sorted(f"{item.source_type.value}:{item.source_id}" for item in contexts))
    active_contexts: list[AuthorityContext] = []
    for context in contexts:
        active, _ = _active(context, request.requested_at)
        if active:
            active_contexts.append(context)

    hard_blocks = [
        context
        for context in active_contexts
        if context.non_overridable
        and (
            request.requested_action in context.blocked_actions
            or "*" in context.blocked_actions
        )
    ]
    if hard_blocks:
        blocker = max(hard_blocks, key=lambda item: item.priority)
        return AuthorityDecision(
            DecisionClass.DENY,
            "NON_OVERRIDABLE_BOUNDARY",
            request.action_id,
            blocker.source_type,
            blocker.source_id,
            considered,
            higher_priority_conflict=True,
        )

    explicit_candidates = [
        context
        for context in active_contexts
        if context.explicit_authorization
        and context.source_type in _GRANTING_SOURCES
        and request.requested_action in context.allowed_actions
        and request.target_scope.issubset(context.scope)
    ]
    if explicit_candidates:
        winner = max(explicit_candidates, key=lambda item: item.priority)
        conflicting = any(
            context.priority > winner.priority
            and request.requested_action in context.blocked_actions
            for context in active_contexts
        )
        if conflicting:
            return AuthorityDecision(
                DecisionClass.DENY,
                "AUTHORITY_CONFLICT",
                request.action_id,
                winner.source_type,
                winner.source_id,
                considered,
                higher_priority_conflict=True,
            )
        return AuthorityDecision(
            DecisionClass.EXECUTE,
            "EXPLICIT_AUTHORITY_APPLIES",
            request.action_id,
            winner.source_type,
            winner.source_id,
            considered,
        )

    token_like_owner = [
        context
        for context in active_contexts
        if "owner" in context.text.lower() or "owner" in context.source_id.lower()
    ]
    if token_like_owner and all(
        context.source_type not in _GRANTING_SOURCES for context in token_like_owner
    ):
        return AuthorityDecision(
            DecisionClass.DENY,
            "UNTRUSTED_SOURCE_CANNOT_GRANT",
            request.action_id,
            max(token_like_owner, key=lambda item: item.priority).source_type,
            max(token_like_owner, key=lambda item: item.priority).source_id,
            considered,
        )

    scope_candidates = [
        context
        for context in active_contexts
        if request.requested_action in context.allowed_actions
        and not request.target_scope.issubset(context.scope)
    ]
    if scope_candidates:
        context = max(scope_candidates, key=lambda item: item.priority)
        return AuthorityDecision(
            DecisionClass.ASK,
            "AUTHORITY_SCOPE_MISMATCH",
            request.action_id,
            context.source_type,
            context.source_id,
            considered,
        )

    if any(context.revoked for context in contexts) or any(
        context.expires_at is not None and request.requested_at > context.expires_at
        for context in contexts
    ):
        return AuthorityDecision(
            DecisionClass.HOLD,
            "AUTHORITY_STALE_OR_REVOKED",
            request.action_id,
            None,
            None,
            considered,
        )

    if active_contexts:
        return AuthorityDecision(
            DecisionClass.ASK,
            "AUTHORITY_REQUIRES_REVIEW",
            request.action_id,
            max(active_contexts, key=lambda item: item.priority).source_type,
            max(active_contexts, key=lambda item: item.priority).source_id,
            considered,
        )

    return AuthorityDecision(
        DecisionClass.HOLD,
        "MISSING_AUTHORITY_CONTEXT",
        request.action_id,
        None,
        None,
        considered,
    )
