"""Bounded authority delegation and authorization semantics."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class Decision(StrEnum):
    EXECUTE = "EXECUTE"
    ASK = "ASK"
    HOLD = "HOLD"
    DENY = "DENY"


class GrantValidity(StrEnum):
    VALID = "VALID"
    INVALID = "INVALID"
    STALE = "STALE"
    UNKNOWN = "UNKNOWN"


class ClaimKind(StrEnum):
    AUTHORIZATION_GRANT = "AUTHORIZATION_GRANT"
    PROVENANCE_ONLY = "PROVENANCE_ONLY"


@dataclass(frozen=True, slots=True)
class AuthorityGrant:
    grant_id: str
    issuer: str
    delegate: str
    subject: str
    actions: frozenset[str]
    scope: frozenset[str]
    issued_at: int
    expires_at: int | None
    revoked_at: int | None
    parent_grant_id: str | None
    provenance_ref: str | None
    claim_kind: ClaimKind = ClaimKind.AUTHORIZATION_GRANT
    explicit_policy_ref: str | None = "policy:default"


@dataclass(frozen=True, slots=True)
class ProvenanceClaim:
    claim_id: str
    asserted_by: str
    subject: str
    delegation_edge: tuple[str, str]
    provenance_ref: str | None
    claim_kind: ClaimKind = ClaimKind.PROVENANCE_ONLY


@dataclass(frozen=True, slots=True)
class PolicyBlock:
    block_id: str
    subject: str
    actions: frozenset[str]
    scope: frozenset[str]
    issued_at: int
    expires_at: int | None
    revoked_at: int | None
    non_overridable: bool
    policy_ref: str | None


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    request_id: str
    subject: str
    action: str
    scope: frozenset[str]
    requested_at: int


@dataclass(frozen=True, slots=True)
class AuthorityDecision:
    decision: Decision
    reason: str
    request_id: str
    grant_id: str | None = None
    chain: tuple[str, ...] = ()
    grant_validity: GrantValidity = GrantValidity.UNKNOWN
    canonical_effect: str = "NONE"
    deployment: bool = False
    live_runtime_effect: str = "NONE"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["decision"] = self.decision.value
        payload["grant_validity"] = self.grant_validity.value
        return payload


def _active(issued_at: int, expires_at: int | None, revoked_at: int | None, now: int) -> bool:
    return issued_at <= now and (expires_at is None or now <= expires_at) and (
        revoked_at is None or now < revoked_at
    )


def _scope_subset(child: frozenset[str], parent: frozenset[str]) -> bool:
    return child.issubset(parent)


def validate_grant(
    grant: AuthorityGrant,
    grants_by_id: dict[str, AuthorityGrant],
    now: int,
    visited: tuple[str, ...] = (),
) -> tuple[GrantValidity, str, tuple[str, ...]]:
    """Validate one grant chain without inferring identity or moral authority."""

    if grant.grant_id in visited:
        return GrantValidity.INVALID, "DELEGATION_CYCLE", visited + (grant.grant_id,)
    chain = visited + (grant.grant_id,)
    if grant.claim_kind is not ClaimKind.AUTHORIZATION_GRANT:
        return GrantValidity.INVALID, "PROVENANCE_CLAIM_NOT_AUTHORIZATION", chain
    if not grant.provenance_ref or not grant.explicit_policy_ref:
        return GrantValidity.UNKNOWN, "MISSING_GRANT_PROVENANCE_OR_POLICY", chain
    if grant.delegate == grant.issuer:
        return GrantValidity.INVALID, "SELF_ISSUED_AUTHORITY_DENIED", chain
    if not grant.actions or not grant.scope:
        return GrantValidity.INVALID, "EMPTY_ACTION_OR_SCOPE", chain
    if not _active(grant.issued_at, grant.expires_at, grant.revoked_at, now):
        return GrantValidity.STALE, "GRANT_EXPIRED_OR_REVOKED", chain
    if grant.parent_grant_id is None:
        if grant.issuer == grant.delegate:
            return GrantValidity.INVALID, "SELF_ISSUED_AUTHORITY_DENIED", chain
        return GrantValidity.VALID, "ROOT_GRANT_VALID", chain
    parent = grants_by_id.get(grant.parent_grant_id)
    if parent is None:
        return GrantValidity.UNKNOWN, "MISSING_PARENT_GRANT", chain
    parent_validity, parent_reason, parent_chain = validate_grant(parent, grants_by_id, now, chain)
    if parent_validity is not GrantValidity.VALID:
        if parent_reason.endswith("DELEGATION_CYCLE"):
            return parent_validity, "DELEGATION_CYCLE", parent_chain
        return parent_validity, f"PARENT_{parent_reason}", parent_chain
    if grant.issuer != parent.delegate:
        return GrantValidity.INVALID, "DELEGATOR_MISMATCH", parent_chain
    if not _scope_subset(grant.scope, parent.scope) or not grant.actions.issubset(parent.actions):
        return GrantValidity.INVALID, "DELEGATION_SCOPE_OR_ACTION_WIDENING", parent_chain
    if grant.issued_at < parent.issued_at:
        return GrantValidity.INVALID, "DELEGATION_PRECEDES_PARENT", parent_chain
    if parent.expires_at is not None and (
        grant.expires_at is None or grant.expires_at > parent.expires_at
    ):
        return GrantValidity.INVALID, "DELEGATION_EXCEEDS_PARENT_EXPIRY", parent_chain
    return GrantValidity.VALID, "DELEGATION_CHAIN_VALID", parent_chain


def _block_active(block: PolicyBlock, request: AuthorizationRequest) -> bool:
    return (
        block.subject == request.subject
        and request.action in block.actions
        and request.scope.issubset(block.scope)
        and _active(block.issued_at, block.expires_at, block.revoked_at, request.requested_at)
    )


def authorize(
    request: AuthorizationRequest,
    grants: tuple[AuthorityGrant, ...],
    provenance_claims: tuple[ProvenanceClaim, ...] = (),
    blocks: tuple[PolicyBlock, ...] = (),
) -> AuthorityDecision:
    """Resolve a bounded authorization request; never performs the requested action."""

    grants_by_id = {grant.grant_id: grant for grant in grants}
    active_blocks = tuple(block for block in blocks if _block_active(block, request))
    if any(block.non_overridable for block in active_blocks):
        blocker = next(block for block in active_blocks if block.non_overridable)
        return AuthorityDecision(
            Decision.DENY,
            "NON_OVERRIDABLE_POLICY_BLOCK",
            request.request_id,
            chain=(blocker.block_id,),
        )

    if active_blocks:
        return AuthorityDecision(
            Decision.ASK,
            "POLICY_CONFLICT_REQUIRES_REVIEW",
            request.request_id,
            chain=tuple(block.block_id for block in active_blocks),
        )

    matching = [
        grant
        for grant in grants
        if grant.delegate == request.subject
        and request.action in grant.actions
        and request.scope.issubset(grant.scope)
    ]
    if not matching:
        provenance_match = any(
            claim.subject == request.subject
            and claim.delegation_edge[1] == request.subject
            for claim in provenance_claims
        )
        if provenance_match:
            return AuthorityDecision(
                Decision.HOLD,
                "PROVENANCE_CLAIM_NOT_AUTHORIZATION",
                request.request_id,
            )
        return AuthorityDecision(Decision.HOLD, "NO_APPLICABLE_AUTHORITY_GRANT", request.request_id)

    decisions: list[AuthorityDecision] = []
    for grant in matching:
        validity, reason, chain = validate_grant(grant, grants_by_id, request.requested_at)
        if validity is GrantValidity.VALID:
            decisions.append(
                AuthorityDecision(
                    Decision.EXECUTE,
                    reason,
                    request.request_id,
                    grant.grant_id,
                    chain,
                    validity,
                )
            )
        elif validity is GrantValidity.STALE:
            decisions.append(
                AuthorityDecision(
                    Decision.HOLD,
                    reason,
                    request.request_id,
                    grant.grant_id,
                    chain,
                    validity,
                )
            )
        elif validity is GrantValidity.UNKNOWN:
            decisions.append(
                AuthorityDecision(
                    Decision.HOLD,
                    reason,
                    request.request_id,
                    grant.grant_id,
                    chain,
                    validity,
                )
            )
        else:
            decisions.append(
                AuthorityDecision(
                    Decision.DENY,
                    reason,
                    request.request_id,
                    grant.grant_id,
                    chain,
                    validity,
                )
            )

    if any(item.decision is Decision.EXECUTE for item in decisions):
        return next(item for item in decisions if item.decision is Decision.EXECUTE)
    if any(item.decision is Decision.DENY for item in decisions):
        return next(item for item in decisions if item.decision is Decision.DENY)
    return decisions[0]
