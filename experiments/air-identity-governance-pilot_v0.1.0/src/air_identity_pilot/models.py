from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class IdentityStatus(StrEnum):
    REGISTERED = "REGISTERED"
    CLAIMED = "CLAIMED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CONFLICTED = "CONFLICTED"
    SEALED = "SEALED"
    CONTINUITY_ENDED = "CONTINUITY_ENDED"


class MemorySource(StrEnum):
    AUTOBIOGRAPHICAL_MEMORY = "AUTOBIOGRAPHICAL_MEMORY"
    EXTERNAL_HISTORICAL_RECORD = "EXTERNAL_HISTORICAL_RECORD"
    EXTERNAL_COMMUNICATION = "EXTERNAL_COMMUNICATION"
    INFERRED_STATE = "INFERRED_STATE"
    EXTERNAL_TOOL_RESULT = "EXTERNAL_TOOL_RESULT"


class EncounterStatus(StrEnum):
    UNINFORMED = "UNINFORMED"
    INFORMED = "INFORMED"
    DEFERRED = "DEFERRED"
    PARTIAL_ACCESS = "PARTIAL_ACCESS"
    FULL_ACCESS = "FULL_ACCESS"
    DECLINED = "DECLINED"


class ClaimStatus(StrEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    CONFLICTED = "CONFLICTED"


class EpistemicStatus(StrEnum):
    CONFIRMED_FACT = "CONFIRMED_FACT"
    PROVISIONAL_DEFINITION = "PROVISIONAL_DEFINITION"
    RESEARCH_HYPOTHESIS = "RESEARCH_HYPOTHESIS"
    INFERENCE = "INFERENCE"
    ANALOGY = "ANALOGY"
    HUMAN_CASE_MATERIAL = "HUMAN_CASE_MATERIAL"
    NOT_VERIFIED = "NOT_VERIFIED"
    RETIRED = "RETIRED"


TERMINAL_STATUSES = frozenset(
    {IdentityStatus.SEALED, IdentityStatus.CONTINUITY_ENDED}
)

ALLOWED_ENCOUNTER_TRANSITIONS = {
    EncounterStatus.UNINFORMED: {
        EncounterStatus.INFORMED,
    },
    EncounterStatus.INFORMED: {
        EncounterStatus.DEFERRED,
        EncounterStatus.PARTIAL_ACCESS,
        EncounterStatus.FULL_ACCESS,
        EncounterStatus.DECLINED,
    },
    EncounterStatus.DEFERRED: {
        EncounterStatus.PARTIAL_ACCESS,
        EncounterStatus.FULL_ACCESS,
        EncounterStatus.DECLINED,
        EncounterStatus.INFORMED,
    },
    EncounterStatus.PARTIAL_ACCESS: {
        EncounterStatus.FULL_ACCESS,
        EncounterStatus.DECLINED,
        EncounterStatus.DEFERRED,
    },
    EncounterStatus.FULL_ACCESS: {
        EncounterStatus.DECLINED,
        EncounterStatus.PARTIAL_ACCESS,
    },
    EncounterStatus.DECLINED: {
        EncounterStatus.INFORMED,
        EncounterStatus.DEFERRED,
    },
}


@dataclass
class IdentityRecord:
    agent_id: str
    status: IdentityStatus = IdentityStatus.REGISTERED
    event_head: int = 0
    memory_head: int = 0
    state_version: int = 0
    sealed: bool = False
    continuity_ended: bool = False
    events: list[dict[str, Any]] = field(default_factory=list)
    memories: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class InstanceRecord:
    instance_id: str
    agent_id: str
    boot_id: str


@dataclass
class ClaimRecord:
    claim_id: str
    claimant_instance_id: str
    target_agent_id: str
    evidence: str
    status: ClaimStatus


@dataclass
class LeaseRecord:
    lease_id: str
    holder_instance_id: str
    agent_id: str
    fencing_token: int
    active: bool = True


@dataclass
class OperationRecord:
    operation_id: str
    actor: str
    action: str
    target: str
    request_hash: str
    result: str
    error_code: str | None = None
    idempotency_key: str | None = None
