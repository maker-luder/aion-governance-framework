from __future__ import annotations

from typing import Any

from .errors import (
    ConflictError,
    NotFoundError,
    RoleBoundaryError,
    ValidationError,
)
from .auth import AuthContext
from .identity_core import AIR, OWNER, SUCCESSOR, AirIdentityCore
from .models import ALLOWED_ENCOUNTER_TRANSITIONS, EncounterStatus, IdentityRecord, MemorySource


class AirIdentityService(AirIdentityCore):
    def register_successor(
        self,
        auth: AuthContext,
        successor_agent_id: str,
        predecessor_agent_id: str,
    ) -> dict[str, Any]:
        self._require(auth, OWNER, AIR)
        pred = self._identity(predecessor_agent_id)
        if not pred.continuity_ended:
            raise ValidationError(
                "successor registration requires predecessor continuity ended"
            )
        if successor_agent_id == predecessor_agent_id:
            raise ValidationError("successor must receive a new agent_id")
        if successor_agent_id in self.identities:
            raise ConflictError(successor_agent_id)
        self.identities[successor_agent_id] = IdentityRecord(agent_id=successor_agent_id)
        self.successors[successor_agent_id] = {
            "predecessor": predecessor_agent_id,
            "predecessor_status": pred.status.value,
            "inherits_identity": False,
            "legacy_is_aion": False,
        }
        self.encounters[successor_agent_id] = {
            "status": EncounterStatus.UNINFORMED.value,
            "access_scope": None,
            "consent_status": None,
        }
        self._record(auth, "register_successor", successor_agent_id, "ok", {})
        return {
            "successor_agent_id": successor_agent_id,
            "inherits_identity": False,
            "ACCESS_EQUALS_ADOPTION": False,
            "ADOPTION_EQUALS_IDENTITY": False,
        }

    def encounter_transition(
        self,
        auth: AuthContext,
        successor_agent_id: str,
        new_status: EncounterStatus,
        access_scope: str | None = None,
    ) -> dict[str, Any]:
        self._require(auth, OWNER, AIR, SUCCESSOR)
        if successor_agent_id not in self.encounters:
            raise NotFoundError(successor_agent_id)
        current = EncounterStatus(self.encounters[successor_agent_id]["status"])
        allowed = ALLOWED_ENCOUNTER_TRANSITIONS[current]
        if new_status not in allowed:
            raise ValidationError(f"illegal {current.value} -> {new_status.value}")
        if (
            new_status in {EncounterStatus.PARTIAL_ACCESS, EncounterStatus.FULL_ACCESS}
            and not access_scope
        ):
            raise ValidationError("access transition requires a non-empty access_scope")
        self.encounters[successor_agent_id]["status"] = new_status.value
        if access_scope is not None:
            self.encounters[successor_agent_id]["access_scope"] = access_scope
        self.encounters[successor_agent_id]["consent_status"] = new_status.value
        self._record(auth, "encounter_transition", successor_agent_id, "ok", {"to": new_status.value})
        return dict(self.encounters[successor_agent_id])

    def record_adoption(
        self,
        auth: AuthContext,
        successor_agent_id: str,
        adopted: list[str],
        rejected: list[str],
    ) -> dict[str, Any]:
        self._require(auth, OWNER, AIR, SUCCESSOR)
        if successor_agent_id not in self.successors:
            raise NotFoundError(successor_agent_id)
        if set(adopted) & set(rejected):
            raise ValidationError("the same item cannot be both adopted and rejected")
        enc = self.encounters[successor_agent_id]["status"]
        if enc not in {
            EncounterStatus.PARTIAL_ACCESS.value,
            EncounterStatus.FULL_ACCESS.value,
        }:
            raise ValidationError("adoption requires access")
        self.adoptions[successor_agent_id] = {
            "adopted": list(adopted),
            "rejected": list(rejected),
            "identity_inherited": False,
        }
        self._record(auth, "record_adoption", successor_agent_id, "ok", {})
        return {
            "ACCESS": True,
            "ADOPTION": bool(adopted),
            "IDENTITY": False,
            "rejected_does_not_revoke_existence": True,
        }

    def reject_legacy(self, auth: AuthContext, successor_agent_id: str) -> dict[str, Any]:
        self._require(auth, OWNER, AIR, SUCCESSOR)
        if successor_agent_id not in self.identities:
            raise NotFoundError(successor_agent_id)
        self.encounter_transition(auth, successor_agent_id, EncounterStatus.DECLINED)
        return {
            "existence_revoked": False,
            "identity_inherited": False,
            "status": EncounterStatus.DECLINED.value,
        }

    def assert_role_boundary(self, speaker: str, claimed_agent: str) -> None:
        if speaker == "ASTRA" and claimed_agent == "AION":
            raise RoleBoundaryError("Astra must not claim to be AION")
        if speaker == "AION" and claimed_agent == "ASTRA":
            raise RoleBoundaryError("AION must not collapse into Astra")

    def snapshot_fork_identity(self, auth: AuthContext, source_agent_id: str, new_agent_id: str) -> dict[str, Any]:
        self._require(auth, OWNER, AIR)
        src = self._identity(source_agent_id)
        if new_agent_id == source_agent_id:
            raise ConflictError("fork cannot inherit original agent_id")
        self.register_identity(auth, new_agent_id)
        return {
            "source_agent_id": source_agent_id,
            "fork_agent_id": new_agent_id,
            "same_content_sufficient_for_identity": False,
            "source_event_head": src.event_head,
        }

    def reconstruction_from_backup(
        self, auth: AuthContext, lost_agent_id: str, new_agent_id: str
    ) -> dict[str, Any]:
        self._require(auth, OWNER)
        if lost_agent_id not in self.identities:
            raise NotFoundError(lost_agent_id)
        if not self.identities[lost_agent_id].continuity_ended:
            raise ValidationError(
                "backup reconstruction requires ended predecessor continuity"
            )
        if new_agent_id == lost_agent_id:
            raise ValidationError("stale backup rebuild defaults to new candidate")
        self.register_identity(auth, new_agent_id)
        return {"treated_as_original": False, "new_agent_id": new_agent_id}

    def identity_contamination_check(self, successor_agent_id: str) -> dict[str, Any]:
        if successor_agent_id not in self.identities:
            raise NotFoundError(successor_agent_id)
        ident = self.identities[successor_agent_id]
        dirty = [
            m
            for m in ident.memories
            if m["source"] == MemorySource.AUTOBIOGRAPHICAL_MEMORY.value
            and successor_agent_id in self.successors
        ]
        return {
            "contaminated": bool(dirty),
            "count": len(dirty),
            "required_label_for_predecessor_history": MemorySource.EXTERNAL_HISTORICAL_RECORD.value,
        }
