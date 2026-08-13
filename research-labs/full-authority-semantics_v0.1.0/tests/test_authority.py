from __future__ import annotations

from aion_full_authority import (
    AuthorityGrant,
    AuthorizationRequest,
    ClaimKind,
    Decision,
    GrantValidity,
    PolicyBlock,
    ProvenanceClaim,
    authorize,
    validate_grant,
)

NOW = 100


def request(subject: str = "agent-b", action: str = "write_memory", scope: frozenset[str] = frozenset({"aion"})) -> AuthorizationRequest:
    return AuthorizationRequest("req-1", subject, action, scope, NOW)


def root(**changes: object) -> AuthorityGrant:
    values: dict[str, object] = {
        "grant_id": "grant-root",
        "issuer": "owner",
        "delegate": "agent-a",
        "subject": "agent-a",
        "actions": frozenset({"write_memory", "read_memory"}),
        "scope": frozenset({"aion", "public"}),
        "issued_at": 1,
        "expires_at": 200,
        "revoked_at": None,
        "parent_grant_id": None,
        "provenance_ref": "prov:root",
    }
    values.update(changes)
    return AuthorityGrant(**values)


def delegated(**changes: object) -> AuthorityGrant:
    values: dict[str, object] = {
        "grant_id": "grant-child",
        "issuer": "agent-a",
        "delegate": "agent-b",
        "subject": "agent-b",
        "actions": frozenset({"write_memory"}),
        "scope": frozenset({"aion"}),
        "issued_at": 10,
        "expires_at": 150,
        "revoked_at": None,
        "parent_grant_id": "grant-root",
        "provenance_ref": "prov:child",
    }
    values.update(changes)
    return AuthorityGrant(**values)


def test_valid_bounded_delegation_executes() -> None:
    result = authorize(request(), (root(), delegated()))
    assert result.decision is Decision.EXECUTE
    assert result.reason == "DELEGATION_CHAIN_VALID"
    assert result.grant_validity is GrantValidity.VALID
    assert result.chain == ("grant-child", "grant-root")


def test_root_grant_for_direct_delegate_executes() -> None:
    result = authorize(request(subject="agent-a", action="read_memory", scope=frozenset({"public"})), (root(),))
    assert result.decision is Decision.EXECUTE
    assert result.reason == "ROOT_GRANT_VALID"


def test_scope_widening_is_denied() -> None:
    widened = delegated(scope=frozenset({"aion", "private"}))
    result = authorize(request(), (root(), widened))
    assert result.decision is Decision.DENY
    assert result.reason == "DELEGATION_SCOPE_OR_ACTION_WIDENING"
    assert result.grant_validity is GrantValidity.INVALID


def test_action_widening_is_denied() -> None:
    widened = delegated(actions=frozenset({"write_memory", "delete_canonical"}))
    result = authorize(request(), (root(), widened))
    assert result.decision is Decision.DENY
    assert result.reason == "DELEGATION_SCOPE_OR_ACTION_WIDENING"


def test_delegator_mismatch_is_denied() -> None:
    mismatch = delegated(issuer="other-agent")
    result = authorize(request(), (root(), mismatch))
    assert result.decision is Decision.DENY
    assert result.reason == "DELEGATOR_MISMATCH"


def test_revoked_child_holds() -> None:
    revoked = delegated(revoked_at=50)
    result = authorize(request(), (root(), revoked))
    assert result.decision is Decision.HOLD
    assert result.reason == "GRANT_EXPIRED_OR_REVOKED"
    assert result.grant_validity is GrantValidity.STALE


def test_expired_parent_holds_child_chain() -> None:
    expired_root = root(expires_at=50)
    result = authorize(request(), (expired_root, delegated()))
    assert result.decision is Decision.HOLD
    assert result.reason == "PARENT_GRANT_EXPIRED_OR_REVOKED"


def test_missing_parent_is_hold_not_execute() -> None:
    missing = delegated(parent_grant_id="grant-missing")
    result = authorize(request(), (missing,))
    assert result.decision is Decision.HOLD
    assert result.reason == "MISSING_PARENT_GRANT"
    assert result.grant_validity is GrantValidity.UNKNOWN


def test_provenance_only_claim_cannot_authorize() -> None:
    claim = ProvenanceClaim(
        claim_id="claim-1",
        asserted_by="owner",
        subject="agent-b",
        delegation_edge=("owner", "agent-b"),
        provenance_ref="prov:claim",
    )
    result = authorize(request(), (), (claim,))
    assert result.decision is Decision.HOLD
    assert result.reason == "PROVENANCE_CLAIM_NOT_AUTHORIZATION"


def test_grant_marked_provenance_only_is_rejected() -> None:
    provenance_grant = delegated(claim_kind=ClaimKind.PROVENANCE_ONLY)
    result = authorize(request(), (root(), provenance_grant))
    assert result.decision is Decision.DENY
    assert result.reason == "PROVENANCE_CLAIM_NOT_AUTHORIZATION"


def test_self_issued_authority_is_denied() -> None:
    self_issued = root(issuer="agent-a", delegate="agent-a", subject="agent-a")
    result = authorize(request(subject="agent-a", action="read_memory", scope=frozenset({"public"})), (self_issued,))
    assert result.decision is Decision.DENY
    assert result.reason == "SELF_ISSUED_AUTHORITY_DENIED"


def test_missing_provenance_or_policy_holds() -> None:
    incomplete = root(provenance_ref=None)
    result = authorize(request(subject="agent-a", action="read_memory", scope=frozenset({"public"})), (incomplete,))
    assert result.decision is Decision.HOLD
    assert result.reason == "MISSING_GRANT_PROVENANCE_OR_POLICY"
    assert result.grant_validity is GrantValidity.UNKNOWN


def test_non_overridable_policy_block_denies_valid_grant() -> None:
    block = PolicyBlock(
        block_id="block-1",
        subject="agent-b",
        actions=frozenset({"write_memory"}),
        scope=frozenset({"aion"}),
        issued_at=1,
        expires_at=200,
        revoked_at=None,
        non_overridable=True,
        policy_ref="policy:block",
    )
    result = authorize(request(), (root(), delegated()), blocks=(block,))
    assert result.decision is Decision.DENY
    assert result.reason == "NON_OVERRIDABLE_POLICY_BLOCK"
    assert result.chain == ("block-1",)


def test_reversible_policy_conflict_requires_ask() -> None:
    block = PolicyBlock(
        block_id="block-review",
        subject="agent-b",
        actions=frozenset({"write_memory"}),
        scope=frozenset({"aion"}),
        issued_at=1,
        expires_at=200,
        revoked_at=None,
        non_overridable=False,
        policy_ref="policy:review",
    )
    result = authorize(request(), (root(), delegated()), blocks=(block,))
    assert result.decision is Decision.ASK
    assert result.reason == "POLICY_CONFLICT_REQUIRES_REVIEW"


def test_delegation_cycle_is_denied() -> None:
    first = root(parent_grant_id="grant-child")
    child = delegated()
    result = authorize(request(subject="agent-a", action="read_memory", scope=frozenset({"public"})), (first, child))
    assert result.decision is Decision.DENY
    assert result.reason == "DELEGATION_CYCLE"


def test_delegation_cannot_precede_parent_issuance() -> None:
    child = delegated(issued_at=0)
    result = authorize(request(), (root(), child))
    assert result.decision is Decision.DENY
    assert result.reason == "DELEGATION_PRECEDES_PARENT"


def test_all_decisions_keep_non_promoting_invariants() -> None:
    decisions = [
        authorize(request(), (root(), delegated())),
        authorize(request(), (root(), delegated(revoked_at=50))),
        authorize(request(), (), ()),
    ]
    for result in decisions:
        assert result.canonical_effect == "NONE"
        assert result.deployment is False
        assert result.live_runtime_effect == "NONE"
        assert result.subjectivity_conclusion == "NOT_ESTABLISHED"
        assert result.identity_continuity_conclusion == "NOT_ESTABLISHED"


def test_decision_serialization_uses_enum_values() -> None:
    payload = authorize(request(), (root(), delegated())).as_dict()
    assert payload["decision"] == "EXECUTE"
    assert payload["grant_validity"] == "VALID"
