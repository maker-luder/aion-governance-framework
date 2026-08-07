from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ParticipantKind(str, Enum):
    HUMAN = "HUMAN"
    AION_RUNTIME = "AION_RUNTIME"
    ASTRA_WORKBENCH = "ASTRA_WORKBENCH"
    EXTERNAL_SERVICE = "EXTERNAL_SERVICE"
    REVIEWER = "REVIEWER"
    SYNTHETIC_FIXTURE = "SYNTHETIC_FIXTURE"


class ApprovalAuthority(str, Enum):
    NONE = "NONE"
    PROPOSE = "PROPOSE"
    REVIEW = "REVIEW"
    APPROVE = "APPROVE"
    RELEASE = "RELEASE"


@dataclass(frozen=True, slots=True)
class ParticipantBinding:
    participant_id: str
    participant_kind: ParticipantKind
    identity_ref: str
    memory_namespace: str = "NONE"
    tool_scope: tuple[str, ...] = field(default_factory=tuple)
    read_scope: tuple[str, ...] = field(default_factory=tuple)
    write_scope: tuple[str, ...] = field(default_factory=tuple)
    approval_authority: ApprovalAuthority = ApprovalAuthority.NONE
    provenance_agent_ref: str = "UNKNOWN"

    def __post_init__(self) -> None:
        if not self.participant_id.strip():
            raise ValueError("participant_id must be non-empty")
        if not self.identity_ref.strip():
            raise ValueError("identity_ref must be non-empty")


@dataclass(frozen=True, slots=True)
class EncounterContext:
    encounter_id: str
    purpose: str
    participants: tuple[ParticipantBinding, ...]
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.encounter_id.strip():
            raise ValueError("encounter_id must be non-empty")
        if not self.purpose.strip():
            raise ValueError("purpose must be non-empty")
        if len(self.participants) < 2:
            raise ValueError("an encounter requires at least two participants")
        participant_ids = [participant.participant_id for participant in self.participants]
        if len(set(participant_ids)) != len(participant_ids):
            raise ValueError("participant_id values must be unique")
        if self.canonical_effect != "NONE":
            raise ValueError("encounter candidate must keep canonical_effect=NONE")
