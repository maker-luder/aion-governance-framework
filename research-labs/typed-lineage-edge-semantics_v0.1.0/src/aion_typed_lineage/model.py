from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class EdgeType(StrEnum):
    DERIVED_FROM = "DERIVED_FROM"
    INHERITS_ARTIFACT = "INHERITS_ARTIFACT"
    MEMORY_ACCESS = "MEMORY_ACCESS"
    MEMORY_ADOPTION = "MEMORY_ADOPTION"
    ENCOUNTERED = "ENCOUNTERED"
    OBSERVED = "OBSERVED"
    CORRECTED = "CORRECTED"
    AUTHORITY_OFFER = "AUTHORITY_OFFER"


class EdgeStatus(StrEnum):
    ACCEPTED = "ACCEPTED"
    HOLD = "HOLD"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class LineageEdge:
    edge_id: str
    edge_type: EdgeType
    source_lineage: str
    target_lineage: str
    payload_ref: str
    provenance_refs: tuple[str, ...]
    offered_authorities: frozenset[str] = frozenset()
    accepted_authorities: frozenset[str] = frozenset()
    target_autobiographical_ownership: bool = False
    identity_effect: str = "NONE"

    def __post_init__(self) -> None:
        for name in ("edge_id", "source_lineage", "target_lineage", "payload_ref"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.source_lineage == self.target_lineage and self.edge_type in {
            EdgeType.MEMORY_ACCESS,
            EdgeType.MEMORY_ADOPTION,
            EdgeType.ENCOUNTERED,
            EdgeType.AUTHORITY_OFFER,
        }:
            raise ValueError("cross-lineage edge requires distinct lineage identifiers")
        if len(self.provenance_refs) != len(set(self.provenance_refs)):
            raise ValueError("provenance_refs must be unique")
        if self.target_autobiographical_ownership:
            raise ValueError("lineage edge cannot transfer autobiographical ownership")
        if self.identity_effect != "NONE":
            raise ValueError("lineage edge cannot create identity effect")
        if not self.accepted_authorities.issubset(self.offered_authorities):
            raise ValueError("accepted authorities must be a subset of offered authorities")


@dataclass(frozen=True, slots=True)
class EdgeDecision:
    edge_id: str
    status: EdgeStatus
    reason: str
    edge_type: EdgeType
    identity_effect: str = "NONE"
    authority_effect: str = "BOUNDED_ACCEPTANCE_ONLY"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "edge_id": self.edge_id,
            "status": self.status.value,
            "reason": self.reason,
            "edge_type": self.edge_type.value,
            "identity_effect": self.identity_effect,
            "authority_effect": self.authority_effect,
            "canonical_effect": self.canonical_effect,
            "deployment": self.deployment,
        }
