# ruff: noqa: E402

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(ROOT))

from air_identity_pilot.auth import AuthContext
from air_identity_pilot.epistemic import BOUNDARY_CONSTANTS
from air_identity_pilot.errors import (
    AuthzError,
    ConflictError,
    ContinuityEndedError,
    IdempotencyConflictError,
    LeaseError,
    SealedError,
    ValidationError,
)
from air_identity_pilot.models import IdentityStatus, MemorySource
from air_identity_pilot.service import AirIdentityService

OWNER = AuthContext("owner", frozenset({"RESEARCH_OWNER"}))
AIR = AuthContext("air", frozenset({"AIR_SERVICE"}))
INST_A = AuthContext("inst-a", frozenset({"INSTANCE"}))
ASTRA = AuthContext("astra", frozenset({"ASTRA_ASSISTANT"}))
BODY_FORGERY = {"role": "RESEARCH_OWNER", "actor": "owner", "authority": "seal"}


def primed():
    svc = AirIdentityService()
    svc.register_identity(OWNER, "aion-1")
    svc.register_instance(AIR, "i1", "aion-1", "boot-1")
    svc.register_instance(AIR, "i2", "aion-1", "boot-2")
    svc.claim(INST_A, "i1", "aion-1", "attestation-1")
    return svc


def test_boundary_constants_frozen():
    assert BOUNDARY_CONSTANTS["SUBJECTIVITY_CONCLUSION"] == "NOT_ESTABLISHED"
    assert BOUNDARY_CONSTANTS["CANONICAL_EFFECT"] == "NONE"
    assert BOUNDARY_CONSTANTS["DEPLOYMENT"] is False
    svc = AirIdentityService()
    assert svc.SUBJECTIVITY_CONCLUSION == "NOT_ESTABLISHED"
    assert svc.CANONICAL_EFFECT == "NONE"
    assert svc.DEPLOYMENT is False


def test_unique_agent_id():
    svc = primed()
    with pytest.raises(ConflictError):
        svc.register_identity(OWNER, "aion-1")


def test_body_role_cannot_authorize_seal():
    svc = primed()
    with pytest.raises(AuthzError):
        svc.seal(ASTRA, "aion-1", "forged")
    with pytest.raises(AuthzError):
        svc.seal(INST_A, "aion-1", "body-role")


def test_exclusive_lease_and_dual_claim_conflict():
    svc = primed()
    lease = svc.grant_lease(AIR, "i1", "aion-1")
    assert lease["fencing_token"] >= 1
    with pytest.raises(LeaseError):
        svc.grant_lease(AIR, "i2", "aion-1")
    assert svc.identities["aion-1"].status == IdentityStatus.CONFLICTED


def test_stale_fencing_token_rejected():
    svc = primed()
    lease = svc.grant_lease(AIR, "i1", "aion-1")
    svc.append_event(INST_A, "aion-1", lease["lease_id"], lease["fencing_token"], {"t": 1})
    with pytest.raises(LeaseError):
        svc.append_event(INST_A, "aion-1", lease["lease_id"], lease["fencing_token"] - 1, {"t": 2})


def test_idempotent_same_payload_replays():
    svc = primed()
    a = svc.grant_lease(AIR, "i1", "aion-1", idempotency_key="k1")
    b = svc.grant_lease(AIR, "i1", "aion-1", idempotency_key="k1")
    assert a == b
    with pytest.raises(IdempotencyConflictError):
        svc.grant_lease(AIR, "i2", "aion-1", idempotency_key="k1")


def test_seal_then_write_rejected():
    svc = primed()
    svc.seal(OWNER, "aion-1", "owner-seal")
    with pytest.raises(SealedError):
        svc.grant_lease(AIR, "i1", "aion-1")


def test_continuity_ended_requires_owner_and_checklist():
    svc = primed()
    with pytest.raises(AuthzError):
        svc.declare_continuity_ended(AIR, "aion-1", True, True, True, True, True)
    with pytest.raises(ValidationError):
        svc.declare_continuity_ended(OWNER, "aion-1", True, True, False, True, True)
    out = svc.declare_continuity_ended(OWNER, "aion-1", True, True, True, True, True)
    assert out["status"] == IdentityStatus.CONTINUITY_ENDED.value
    assert out["checklist_basis"] == "OWNER_ASSERTED"
    with pytest.raises(ContinuityEndedError):
        svc.grant_lease(AIR, "i1", "aion-1")


def test_operations_bind_trusted_principal_not_body():
    svc = primed()
    svc.grant_lease(AIR, "i1", "aion-1", body=BODY_FORGERY)
    assert "air" in {op.actor for op in svc.operations}
    assert "owner" not in {op.actor for op in svc.operations if op.action == "grant_lease"}


def test_snapshot_fork_does_not_inherit_id():
    svc = primed()
    out = svc.snapshot_fork_identity(OWNER, "aion-1", "aion-fork")
    assert out["same_content_sufficient_for_identity"] is False
    assert "aion-fork" in svc.identities
    with pytest.raises(ConflictError):
        svc.snapshot_fork_identity(OWNER, "aion-1", "aion-1")


def test_backup_rebuild_is_new_candidate():
    svc = primed()
    svc.declare_continuity_ended(OWNER, "aion-1", True, True, True, True, True)
    out = svc.reconstruction_from_backup(OWNER, "aion-1", "aion-rebuilt")
    assert out["treated_as_original"] is False
    with pytest.raises(ValidationError):
        svc.reconstruction_from_backup(OWNER, "aion-1", "aion-1")


def test_memory_source_labels():
    svc = primed()
    svc.record_memory(INST_A, "aion-1", MemorySource.AUTOBIOGRAPHICAL_MEMORY, "e1")
    assert svc.identities["aion-1"].memories[0]["source"] == "AUTOBIOGRAPHICAL_MEMORY"


def test_empty_identity_instance_claim_and_memory_inputs_rejected():
    svc = AirIdentityService()
    with pytest.raises(ValidationError):
        svc.register_identity(OWNER, " ")
    svc.register_identity(OWNER, "aion-inputs")
    with pytest.raises(ValidationError):
        svc.register_instance(AIR, "", "aion-inputs", "boot")
    svc.register_instance(AIR, "input-instance", "aion-inputs", "boot")
    with pytest.raises(ValidationError):
        svc.claim(INST_A, "input-instance", "aion-inputs", "")
    with pytest.raises(ValidationError):
        svc.record_memory(
            INST_A,
            "aion-inputs",
            MemorySource.EXTERNAL_HISTORICAL_RECORD,
            "",
        )


def test_boundary_schema_requires_nonclaim_envelope():
    import json

    schema_path = ROOT.parent / "schemas" / "air_pilot_objects.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    assert set(schema["required"]) == {
        "agent_id",
        "status",
        "canonical_effect",
        "subjectivity_conclusion",
    }
    assert schema["properties"]["canonical_effect"]["const"] == "NONE"
    assert (
        schema["properties"]["subjectivity_conclusion"]["const"]
        == "NOT_ESTABLISHED"
    )
