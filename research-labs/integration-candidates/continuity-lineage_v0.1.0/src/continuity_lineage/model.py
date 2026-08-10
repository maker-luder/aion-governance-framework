from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


class LineageType(str, Enum):
    """Types of continuity lineage."""

    TEMPORAL = "TEMPORAL"           # Time-based continuity
    CAUSAL = "CAUSAL"               # Cause-effect continuity
    NARRATIVE = "NARRATIVE"         # Story-based continuity
    EMBODIMENT = "EMBODIMENT"       # Body-based continuity
    MEMORY = "MEMORY"               # Memory-based continuity
    SOCIAL = "SOCIAL"               # Social recognition continuity
    FUNCTIONAL = "FUNCTIONAL"       # Functional role continuity


class LineageStatus(str, Enum):
    """Status of a lineage node."""

    ACTIVE = "ACTIVE"
    BRANCHED = "BRANCHED"
    MERGED = "MERGED"
    TERMINATED = "TERMINATED"
    SUSPENDED = "SUSPENDED"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class LineageNode:
    """A node in the continuity lineage graph."""

    node_id: str
    lineage_type: LineageType
    parent_ids: tuple[str, ...]
    timestamp: str
    continuity_strength: float
    metadata: dict[str, str] = field(default_factory=dict)
    canonical_effect: str = NONE
    identity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.node_id.strip():
            raise ValueError("node_id must be non-empty")
        if self.continuity_strength < 0.0 or self.continuity_strength > 1.0:
            raise ValueError("continuity_strength must be between 0.0 and 1.0")
        if self.canonical_effect != NONE:
            raise ValueError("node must keep canonical_effect=NONE")
        if self.identity_claim != NOT_ESTABLISHED:
            raise ValueError("identity must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class LineageConfig:
    """Configuration for continuity lineage tracking."""

    config_id: str
    agent_id: str
    tracked_types: tuple[LineageType, ...]
    max_depth: int
    strength_threshold: float
    canonical_effect: str = NONE
    personal_identity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.config_id.strip():
            raise ValueError("config_id must be non-empty")
        if not self.agent_id.strip():
            raise ValueError("agent_id must be non-empty")
        if not self.tracked_types:
            raise ValueError("at least one lineage type must be tracked")
        if self.max_depth <= 0:
            raise ValueError("max_depth must be positive")
        _require_unit_interval("strength_threshold", self.strength_threshold)
        if self.canonical_effect != NONE:
            raise ValueError("config must keep canonical_effect=NONE")
        if self.personal_identity_claim != NOT_ESTABLISHED:
            raise ValueError("personal identity must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class LineageEvent:
    """An event affecting continuity lineage."""

    event_id: str
    event_type: str
    affected_nodes: tuple[str, ...]
    continuity_delta: float
    timestamp: str
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id must be non-empty")
        if not self.event_type.strip():
            raise ValueError("event_type must be non-empty")
        if not -1.0 <= self.continuity_delta <= 1.0:
            raise ValueError("continuity_delta must be between -1.0 and 1.0")
        if self.canonical_effect != NONE:
            raise ValueError("event must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class LineageState:
    """Research state representing continuity lineage; no personal identity claim."""

    state_id: str
    config: LineageConfig
    nodes: tuple[LineageNode, ...]
    root_node_id: str | None
    current_head_ids: tuple[str, ...]
    overall_continuity: float
    branch_count: int
    events: tuple[LineageEvent, ...]
    canonical_effect: str = NONE
    personal_identity_claim: str = NOT_ESTABLISHED
    consciousness_continuity_claim: str = NOT_ESTABLISHED
    narrative_unity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        if self.overall_continuity < 0.0 or self.overall_continuity > 1.0:
            raise ValueError("overall_continuity must be between 0.0 and 1.0")
        if self.branch_count < 0:
            raise ValueError("branch_count must be non-negative")
        if self.canonical_effect != NONE:
            raise ValueError("state must keep canonical_effect=NONE")
        if self.personal_identity_claim != NOT_ESTABLISHED:
            raise ValueError("personal identity must remain NOT_ESTABLISHED")
        if self.consciousness_continuity_claim != NOT_ESTABLISHED:
            raise ValueError("consciousness continuity must remain NOT_ESTABLISHED")
        if self.narrative_unity_claim != NOT_ESTABLISHED:
            raise ValueError("narrative unity must remain NOT_ESTABLISHED")

    def get_node(self, node_id: str) -> LineageNode | None:
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def get_children(self, node_id: str) -> tuple[LineageNode, ...]:
        return tuple(n for n in self.nodes if node_id in n.parent_ids)

    def get_descendants(self, node_id: str) -> tuple[LineageNode, ...]:
        descendants = []
        children = self.get_children(node_id)
        for child in children:
            descendants.append(child)
            descendants.extend(self.get_descendants(child.node_id))
        return tuple(descendants)

    def get_nodes_by_type(self, lineage_type: LineageType) -> tuple[LineageNode, ...]:
        return tuple(n for n in self.nodes if n.lineage_type == lineage_type)