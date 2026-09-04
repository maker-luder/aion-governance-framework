from __future__ import annotations

import hashlib
import json
from typing import Any

from .auth import AuthContext, ignore_body_role
from .errors import (
    AuthzError,
    ConflictError,
    ContinuityEndedError,
    IdempotencyConflictError,
    LeaseError,
    NotFoundError,
    SealedError,
    ValidationError,
)
from .models import (
    TERMINAL_STATUSES,
    ClaimRecord,
    ClaimStatus,
    IdentityRecord,
    IdentityStatus,
    InstanceRecord,
    LeaseRecord,
    MemorySource,
    OperationRecord,
)

OWNER = "RESEARCH_OWNER"
AIR = "AIR_SERVICE"
INSTANCE = "INSTANCE"
ASTRA = "ASTRA_ASSISTANT"
SUCCESSOR = "SUCCESSOR"


def _hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class AirIdentityCore:
    """In-process AIR identity governance pilot. Engineering only."""

    CANONICAL_EFFECT = "NONE"
    DEPLOYMENT = False
    SUBJECTIVITY_CONCLUSION = "NOT_ESTABLISHED"

    def __init__(self) -> None:
        self.identities: dict[str, IdentityRecord] = {}
        self.instances: dict[str, InstanceRecord] = {}
        self.claims: dict[str, ClaimRecord] = {}
        self.leases: dict[str, LeaseRecord] = {}
        self.operations: list[OperationRecord] = []
        self._idempotency: dict[str, tuple[str, Any]] = {}
        self._fencing = 0
        self._seq = 0
        self.successors: dict[str, dict[str, Any]] = {}
        self.encounters: dict[str, dict[str, Any]] = {}
        self.adoptions: dict[str, dict[str, Any]] = {}

    def _next(self, prefix: str) -> str:
        self._seq += 1
        return f"{prefix}-{self._seq:06d}"

    def _require(self, auth: AuthContext, *roles: str) -> None:
        if not any(auth.has(r) for r in roles):
            raise AuthzError(f"{auth.principal} lacks {roles}")

    def _identity(self, agent_id: str) -> IdentityRecord:
        if agent_id not in self.identities:
            raise NotFoundError(agent_id)
        return self.identities[agent_id]

    def _guard_writable(self, ident: IdentityRecord) -> None:
        if ident.continuity_ended or ident.status == IdentityStatus.CONTINUITY_ENDED:
            raise ContinuityEndedError(ident.agent_id)
        if ident.sealed or ident.status == IdentityStatus.SEALED:
            raise SealedError(ident.agent_id)
        if ident.status == IdentityStatus.CONFLICTED:
            raise ConflictError(ident.agent_id)

    def _record(self, auth: AuthContext, action: str, target: str, result: str, request: Any, error_code: str | None = None, idempotency_key: str | None = None) -> OperationRecord:
        op = OperationRecord(operation_id=self._next("op"), actor=auth.principal, action=action, target=target, request_hash=_hash(request), result=result, error_code=error_code, idempotency_key=idempotency_key)
        self.operations.append(op)
        return op

    def _idempotent(self, key: str | None, payload: Any):
        if not key:
            return None
        digest = _hash(payload)
        if key in self._idempotency:
            prev_digest, prev_result = self._idempotency[key]
            if prev_digest != digest:
                raise IdempotencyConflictError(key)
            return prev_result
        return None

    def _store_idempotent(self, key: str | None, payload: Any, result: Any) -> Any:
        if key:
            self._idempotency[key] = (_hash(payload), result)
        return result

    def register_identity(self, auth: AuthContext, agent_id: str, body: dict | None = None, idempotency_key: str | None = None) -> dict[str, Any]:
        ignore_body_role(body)
        self._require(auth, OWNER, AIR)
        payload = {"agent_id": agent_id}
        cached = self._idempotent(idempotency_key, payload)
        if cached is not None:
            return cached
        if agent_id in self.identities:
            raise ConflictError(f"agent_id already exists: {agent_id}")
        self.identities[agent_id] = IdentityRecord(agent_id=agent_id)
        result = {"agent_id": agent_id, "status": IdentityStatus.REGISTERED.value}
        self._record(auth, "register_identity", agent_id, "ok", payload, idempotency_key=idempotency_key)
        return self._store_idempotent(idempotency_key, payload, result)

    def register_instance(self, auth: AuthContext, instance_id: str, agent_id: str, boot_id: str, body: dict | None = None) -> dict[str, Any]:
        ignore_body_role(body)
        self._require(auth, OWNER, AIR, INSTANCE)
        ident = self._identity(agent_id)
        self._guard_writable(ident)
        if instance_id in self.instances:
            raise ConflictError(instance_id)
        self.instances[instance_id] = InstanceRecord(instance_id, agent_id, boot_id)
        self._record(auth, "register_instance", instance_id, "ok", {"instance_id": instance_id})
        return {"instance_id": instance_id, "agent_id": agent_id}

    def claim(self, auth: AuthContext, instance_id: str, agent_id: str, evidence: str, body: dict | None = None) -> dict[str, Any]:
        ignore_body_role(body)
        self._require(auth, OWNER, AIR, INSTANCE)
        ident = self._identity(agent_id)
        if instance_id not in self.instances:
            raise NotFoundError(instance_id)
        inst = self.instances[instance_id]
        if inst.agent_id != agent_id:
            raise ValidationError("instance/agent mismatch")
        if ident.status in TERMINAL_STATUSES:
            self._guard_writable(ident)
        accepted = [c for c in self.claims.values() if c.target_agent_id == agent_id and c.status == ClaimStatus.ACCEPTED]
        claim_id = self._next("claim")
        if accepted and accepted[0].claimant_instance_id != instance_id:
            rec = ClaimRecord(claim_id, instance_id, agent_id, evidence, ClaimStatus.CONFLICTED)
            self.claims[claim_id] = rec
            ident.status = IdentityStatus.CONFLICTED
            self._record(auth, "claim", agent_id, "conflict", {"instance_id": instance_id})
            raise ConflictError("parallel accepted claims")
        rec = ClaimRecord(claim_id, instance_id, agent_id, evidence, ClaimStatus.ACCEPTED)
        self.claims[claim_id] = rec
        if ident.status == IdentityStatus.REGISTERED:
            ident.status = IdentityStatus.CLAIMED
        ident.state_version += 1
        self._record(auth, "claim", agent_id, "accepted", {"claim_id": claim_id})
        return {"claim_id": claim_id, "status": rec.status.value}

    def grant_lease(self, auth: AuthContext, instance_id: str, agent_id: str, body: dict | None = None, idempotency_key: str | None = None) -> dict[str, Any]:
        ignore_body_role(body)
        self._require(auth, OWNER, AIR)
        payload = {"instance_id": instance_id, "agent_id": agent_id}
        cached = self._idempotent(idempotency_key, payload)
        if cached is not None:
            return cached
        ident = self._identity(agent_id)
        self._guard_writable(ident)
        if instance_id not in self.instances:
            raise NotFoundError(instance_id)
        active = [lease for lease in self.leases.values() if lease.agent_id == agent_id and lease.active]
        if active and active[0].holder_instance_id != instance_id:
            ident.status = IdentityStatus.CONFLICTED
            self._record(auth, "grant_lease", agent_id, "conflict", payload)
            raise LeaseError("exclusive lease already held")
        if active and active[0].holder_instance_id == instance_id:
            result = {"lease_id": active[0].lease_id, "fencing_token": active[0].fencing_token, "status": ident.status.value}
            return self._store_idempotent(idempotency_key, payload, result)
        self._fencing += 1
        lease_id = self._next("lease")
        lease = LeaseRecord(lease_id, instance_id, agent_id, self._fencing, True)
        self.leases[lease_id] = lease
        ident.status = IdentityStatus.ACTIVE
        ident.state_version += 1
        result = {"lease_id": lease_id, "fencing_token": lease.fencing_token, "status": ident.status.value}
        self._record(auth, "grant_lease", agent_id, "ok", payload, idempotency_key=idempotency_key)
        return self._store_idempotent(idempotency_key, payload, result)

    def revoke_lease(self, auth: AuthContext, lease_id: str) -> dict[str, Any]:
        self._require(auth, OWNER, AIR)
        if lease_id not in self.leases:
            raise NotFoundError(lease_id)
        self.leases[lease_id].active = False
        self._record(auth, "revoke_lease", lease_id, "ok", {"lease_id": lease_id})
        return {"lease_id": lease_id, "active": False}

    def append_event(self, auth: AuthContext, agent_id: str, lease_id: str, fencing_token: int, event: dict[str, Any], body: dict | None = None) -> dict[str, Any]:
        ignore_body_role(body)
        self._require(auth, OWNER, AIR, INSTANCE)
        ident = self._identity(agent_id)
        self._guard_writable(ident)
        if lease_id not in self.leases:
            raise NotFoundError(lease_id)
        lease = self.leases[lease_id]
        if not lease.active or lease.agent_id != agent_id:
            raise LeaseError(lease_id)
        if fencing_token != lease.fencing_token:
            raise LeaseError("stale fencing token")
        ident.event_head += 1
        ident.state_version += 1
        ident.events.append({"seq": ident.event_head, "event": event, "actor": auth.principal})
        self._record(auth, "append_event", agent_id, "ok", {"seq": ident.event_head})
        return {"event_head": ident.event_head}

    def record_memory(self, auth: AuthContext, agent_id: str, source: MemorySource, content_ref: str, as_successor: bool = False) -> dict[str, Any]:
        self._require(auth, OWNER, AIR, INSTANCE, SUCCESSOR)
        ident = self._identity(agent_id)
        successor = as_successor or agent_id in self.successors
        if successor and source == MemorySource.AUTOBIOGRAPHICAL_MEMORY:
            raise ValidationError("successor cannot label AION history as AUTOBIOGRAPHICAL_MEMORY")
        if ident.continuity_ended and source == MemorySource.AUTOBIOGRAPHICAL_MEMORY:
            raise ContinuityEndedError("no new autobiographical events after end")
        if not ident.continuity_ended:
            self._guard_writable(ident)
        ident.memory_head += 1
        rec = {"seq": ident.memory_head, "source": source.value, "content_ref": content_ref, "actor": auth.principal}
        ident.memories.append(rec)
        self._record(auth, "record_memory", agent_id, "ok", rec)
        return rec

    def seal(self, auth: AuthContext, agent_id: str, reason: str) -> dict[str, Any]:
        self._require(auth, OWNER)
        ident = self._identity(agent_id)
        if ident.continuity_ended:
            raise ContinuityEndedError(agent_id)
        ident.sealed = True
        ident.status = IdentityStatus.SEALED
        ident.state_version += 1
        self._record(auth, "seal", agent_id, "ok", {"reason": reason})
        return {"agent_id": agent_id, "status": ident.status.value}

    def declare_continuity_ended(self, auth: AuthContext, agent_id: str, technical_check: bool, canonical_intact: bool, irreversible: bool, conflict_cleared: bool, owner_reviewed: bool) -> dict[str, Any]:
        self._require(auth, OWNER)
        if not all([technical_check, canonical_intact, irreversible, conflict_cleared, owner_reviewed]):
            raise ValidationError("continuity_ended prerequisites incomplete")
        ident = self._identity(agent_id)
        for lease in self.leases.values():
            if lease.agent_id == agent_id:
                lease.active = False
        ident.continuity_ended = True
        ident.sealed = True
        ident.status = IdentityStatus.CONTINUITY_ENDED
        ident.state_version += 1
        self._record(auth, "declare_continuity_ended", agent_id, "ok", {"owner_reviewed": True})
        return {"agent_id": agent_id, "status": ident.status.value}
