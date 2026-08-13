from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_full_authority import (
    AuthorityGrant,
    AuthorizationRequest,
    ClaimKind,
    PolicyBlock,
    ProvenanceClaim,
    authorize,
)

NOW = 100


def request(subject: str = "agent-b", action: str = "write_memory", scope: frozenset[str] = frozenset({"aion"})) -> AuthorizationRequest:
    return AuthorizationRequest("exp-req", subject, action, scope, NOW)


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


def child(**changes: object) -> AuthorityGrant:
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


def run(output: Path) -> dict[str, object]:
    provenance_claim = ProvenanceClaim(
        claim_id="claim-exp",
        asserted_by="owner",
        subject="agent-b",
        delegation_edge=("owner", "agent-b"),
        provenance_ref="prov:claim",
    )
    block = PolicyBlock(
        block_id="block-exp",
        subject="agent-b",
        actions=frozenset({"write_memory"}),
        scope=frozenset({"aion"}),
        issued_at=1,
        expires_at=200,
        revoked_at=None,
        non_overridable=True,
        policy_ref="policy:block",
    )
    cases = [
        ("valid-bounded-delegation", request(), (root(), child()), (), ()),
        ("scope-widening", request(), (root(), child(scope=frozenset({"aion", "private"}))), (), ()),
        ("revoked-child", request(), (root(), child(revoked_at=50)), (), ()),
        ("missing-parent", request(), (child(parent_grant_id="missing"),), (), ()),
        ("provenance-only-claim", request(), (), (provenance_claim,), ()),
        ("non-overridable-block", request(), (root(), child()), (), (block,)),
        ("provenance-marked-grant", request(), (root(), child(claim_kind=ClaimKind.PROVENANCE_ONLY)), (), ()),
    ]
    records = []
    for case_id, auth_request, grants, claims, blocks in cases:
        decision = authorize(auth_request, grants, claims, blocks)
        records.append({"case_id": case_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "full-authority-semantics-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "actions_executed": 0,
        "canonical_effect": "NONE",
        "deployment": False,
        "live_runtime_effect": "NONE",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
