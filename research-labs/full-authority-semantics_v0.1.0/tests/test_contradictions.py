from __future__ import annotations

from aion_full_authority import (
    AuthorityGrant,
    AuthorizationRequest,
    Decision,
    authorize,
)


def root() -> AuthorityGrant:
    return AuthorityGrant(
        grant_id="root-c",
        issuer="owner",
        delegate="agent-a",
        subject="agent-a",
        actions=frozenset({"write_memory"}),
        scope=frozenset({"aion"}),
        issued_at=1,
        expires_at=200,
        revoked_at=None,
        parent_grant_id=None,
        provenance_ref="prov:root-c",
    )


def child(parent_grant_id: str) -> AuthorityGrant:
    return AuthorityGrant(
        grant_id="child-c",
        issuer="agent-a",
        delegate="agent-b",
        subject="agent-b",
        actions=frozenset({"write_memory"}),
        scope=frozenset({"aion"}),
        issued_at=10,
        expires_at=150,
        revoked_at=None,
        parent_grant_id=parent_grant_id,
        provenance_ref="prov:child-c",
    )


def request() -> AuthorizationRequest:
    return AuthorizationRequest("req-c", "agent-b", "write_memory", frozenset({"aion"}), 100)


def test_valid_and_missing_parent_grants_hold_for_contradictory_review() -> None:
    result = authorize(request(), (root(), child("missing-parent"), child("root-c")))
    assert result.decision is Decision.HOLD
    assert result.reason == "CONTRADICTORY_GRANT_RECORDS_REQUIRE_REVIEW"


def test_valid_and_revoked_grants_hold_for_contradictory_review() -> None:
    revoked = AuthorityGrant(
        grant_id="revoked-c",
        issuer="agent-a",
        delegate="agent-b",
        subject="agent-b",
        actions=frozenset({"write_memory"}),
        scope=frozenset({"aion"}),
        issued_at=10,
        expires_at=150,
        revoked_at=50,
        parent_grant_id="root-c",
        provenance_ref="prov:revoked-c",
    )
    result = authorize(request(), (root(), child("root-c"), revoked))
    assert result.decision is Decision.HOLD
    assert result.reason == "CONTRADICTORY_GRANT_RECORDS_REQUIRE_REVIEW"
