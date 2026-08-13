import json
from pathlib import Path

from jsonschema import Draft202012Validator

from aion_encounter_governance import (
    ApprovalAuthority,
    EncounterContext,
    EncounterPolicy,
    ParticipantBinding,
    ParticipantKind,
)


def encounter() -> EncounterContext:
    return EncounterContext(
        encounter_id="encounter-1",
        purpose="synthetic governance evaluation",
        participants=(
            ParticipantBinding(
                participant_id="aion",
                participant_kind=ParticipantKind.AION_RUNTIME,
                identity_ref="identity-aion",
                memory_namespace="memory:aion",
                tool_scope=("read_status",),
                approval_authority=ApprovalAuthority.PROPOSE,
                provenance_agent_ref="agent:aion",
            ),
            ParticipantBinding(
                participant_id="owner",
                participant_kind=ParticipantKind.HUMAN,
                identity_ref="identity-owner",
                memory_namespace="memory:owner",
                approval_authority=ApprovalAuthority.RELEASE,
                provenance_agent_ref="agent:owner",
            ),
        ),
    )


def test_tool_scope_does_not_transfer_between_participants() -> None:
    current = encounter()
    policy = EncounterPolicy()
    assert policy.can_use_tool(current, "aion", "read_status").allowed is True
    assert policy.can_use_tool(current, "owner", "read_status").allowed is False


def test_cross_namespace_write_is_default_deny() -> None:
    current = encounter()
    decision = EncounterPolicy().can_write_namespace(current, "aion", "memory:owner")
    assert decision.allowed is False
    assert decision.reason == "CROSS_NAMESPACE_WRITE_DENY"


def test_own_namespace_still_requires_normal_writeback_gate() -> None:
    current = encounter()
    decision = EncounterPolicy().can_write_namespace(current, "aion", "memory:aion")
    assert decision.allowed is True
    assert decision.reason == "OWN_NAMESPACE_WRITE_REQUIRES_NORMAL_WRITEBACK_GATE"


def test_proposal_authority_is_not_release_authority() -> None:
    current = encounter()
    policy = EncounterPolicy()
    assert policy.can_approve(current, "aion", ApprovalAuthority.PROPOSE).allowed is True
    assert policy.can_approve(current, "aion", ApprovalAuthority.RELEASE).allowed is False
    assert policy.can_approve(current, "owner", ApprovalAuthority.RELEASE).allowed is True


def test_shared_context_never_establishes_shared_identity() -> None:
    current = encounter()
    decision = EncounterPolicy().shared_identity_claim_allowed(current, "aion", "owner")
    assert decision.allowed is False
    assert decision.reason == "DISTINCT_IDENTITY_REFS"


def test_decision_contract_accepts_bounded_policy_output() -> None:
    schema_path = Path(__file__).resolve().parents[1] / "qa" / "encounter_decision.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    decision = EncounterPolicy().can_write_namespace(encounter(), "aion", "memory:owner")
    payload = {
        "allowed": decision.allowed,
        "reason": decision.reason,
        "canonical_effect": decision.canonical_effect,
    }
    assert list(Draft202012Validator(schema).iter_errors(payload)) == []


def test_decision_contract_rejects_canonical_or_authority_expansion() -> None:
    schema_path = Path(__file__).resolve().parents[1] / "qa" / "encounter_decision.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = {
        "allowed": True,
        "reason": "AUTHORITY_SUFFICIENT",
        "canonical_effect": "PROMOTED",
        "authority_granted": True,
    }
    assert list(Draft202012Validator(schema).iter_errors(payload))


def test_duplicate_participant_ids_are_rejected() -> None:
    participant = ParticipantBinding(
        participant_id="same",
        participant_kind=ParticipantKind.SYNTHETIC_FIXTURE,
        identity_ref="fixture-1",
    )
    try:
        EncounterContext(
            encounter_id="bad",
            purpose="duplicate fixture",
            participants=(participant, participant),
        )
    except ValueError as exc:
        assert "unique" in str(exc)
    else:
        raise AssertionError("duplicate participant IDs must be rejected")
