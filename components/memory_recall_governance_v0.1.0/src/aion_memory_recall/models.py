from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RecallStatus(str, Enum):
    NOT_REQUIRED = "RECALL_NOT_REQUIRED"
    ALLOWED = "RECALL_ALLOWED"
    TEMPORARY_ONLY = "RECALL_ALLOWED_TEMPORARY_ONLY"
    HUMAN_APPROVAL = "RECALL_REQUIRES_HUMAN_APPROVAL"
    DENIED_ACCESS = "RECALL_DENIED_ACCESS_SCOPE"
    DENIED_IDENTITY = "RECALL_DENIED_IDENTITY_MISMATCH"
    DENIED_PROVENANCE = "RECALL_DENIED_PROVENANCE_FAILURE"
    QUARANTINED_CONFLICT = "RECALL_QUARANTINED_CONFLICT"


@dataclass(frozen=True, slots=True)
class MemoryRecord:
    memory_id: str
    namespace: str
    user_id: str
    agent_id: str
    entities: frozenset[str]
    topics: frozenset[str]
    access_scope: frozenset[str]
    provenance_verified: bool
    conflict: bool = False
    tombstoned: bool = False
    superseded: bool = False
    canonical_effect: str = "NONE"


@dataclass(frozen=True, slots=True)
class RecallRequest:
    user_id: str
    agent_id: str
    requester_scopes: frozenset[str]
    entity_cues: frozenset[str]
    topic_cues: frozenset[str]


@dataclass(frozen=True, slots=True)
class RecallDecision:
    status: RecallStatus
    memory_id: str | None
    reason: str
    writeback_allowed: bool = False
    canonical_effect: str = "NONE"
