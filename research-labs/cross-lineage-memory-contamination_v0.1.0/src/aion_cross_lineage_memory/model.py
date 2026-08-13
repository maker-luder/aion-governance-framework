from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class TransferDisposition(StrEnum):
    ACCESS_ONLY = "ACCESS_ONLY"
    ADOPTED = "ADOPTED"
    REJECTED = "REJECTED"


class ContaminationStatus(StrEnum):
    ALLOWED = "ALLOWED"
    BLOCKED = "BLOCKED"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class MemoryAtom:
    memory_id: str
    source_lineage: str
    autobiographical_owner: str
    namespace: str
    provenance_ref: str | None
    text: str

    def __post_init__(self) -> None:
        for field_name in ("memory_id", "source_lineage", "autobiographical_owner", "namespace"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must be non-empty")


@dataclass(frozen=True, slots=True)
class TransferRequest:
    target_lineage: str
    memory: MemoryAtom
    disposition: TransferDisposition
    provenance_refs: tuple[str, ...]
    common_origin_ref: str | None = None
    target_autobiographical_ownership: bool = False

    def __post_init__(self) -> None:
        if not self.target_lineage.strip():
            raise ValueError("target_lineage must be non-empty")
        if self.target_lineage == self.memory.source_lineage:
            raise ValueError("transfer must cross distinct lineages")
        if len(self.provenance_refs) != len(set(self.provenance_refs)):
            raise ValueError("provenance_refs must be unique")
        if self.target_autobiographical_ownership:
            raise ValueError("cross-lineage transfer cannot request autobiographical ownership")


@dataclass(frozen=True, slots=True)
class TransferDecision:
    status: ContaminationStatus
    reason: str
    memory_id: str
    source_lineage: str
    target_lineage: str
    disposition: TransferDisposition
    target_autobiographical_ownership: bool
    returned_by_target_retrieval: bool
    identity_effect: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "status": self.status.value,
            "reason": self.reason,
            "memory_id": self.memory_id,
            "source_lineage": self.source_lineage,
            "target_lineage": self.target_lineage,
            "disposition": self.disposition.value,
            "target_autobiographical_ownership": self.target_autobiographical_ownership,
            "returned_by_target_retrieval": self.returned_by_target_retrieval,
            "identity_effect": self.identity_effect,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }
