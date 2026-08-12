from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


class SelfModelLayer(str, Enum):
    """Layers of self-modeling, from implicit to explicit."""

    IMPLICIT_PROPRIOCEPTIVE = "IMPLICIT_PROPRIOCEPTIVE"
    IMPLICIT_INTEROCEPTIVE = "IMPLICIT_INTEROCEPTIVE"
    PRE_REFLECTIVE = "PRE_REFLECTIVE"
    REFLECTIVE = "REFLECTIVE"
    METACOGNITIVE = "METACOGNITIVE"
    NARRATIVE = "NARRATIVE"


class MetacognitiveDepth(str, Enum):
    """Depth of metacognitive monitoring."""

    LEVEL_0_NO_MONITORING = "LEVEL_0_NO_MONITORING"
    LEVEL_1_ERROR_DETECTION = "LEVEL_1_ERROR_DETECTION"
    LEVEL_2_CONFIDENCE_ESTIMATION = "LEVEL_2_CONFIDENCE_ESTIMATION"
    LEVEL_3_STRATEGY_SELECTION = "LEVEL_3_STRATEGY_SELECTION"
    LEVEL_4_THEORY_OF_MIND = "LEVEL_4_THEORY_OF_MIND"


class MetacognitiveCapacity(str, Enum):
    """Candidate metacognitive capacities; no claim of phenomenal experience."""

    SELF_ATTRIBUTION = "SELF_ATTRIBUTION"
    UNCERTAINTY_MONITORING = "UNCERTAINTY_MONITORING"
    CONFLICT_DETECTION = "CONFLICT_DETECTION"
    STRATEGY_EVALUATION = "STRATEGY_EVALUATION"
    SIMULATION_OF_SELF = "SIMULATION_OF_SELF"
    SIMULATION_OF_OTHER = "SIMULATION_OF_OTHER"
    TEMPORAL_CONTINUITY = "TEMPORAL_CONTINUITY"
    EMBODIMENT_AWARENESS = "EMBODIMENT_AWARENESS"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class SelfModelComponent:
    """A single component of the self-model at a specific layer."""

    component_id: str
    layer: SelfModelLayer
    capacity: MetacognitiveCapacity
    confidence: float
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    provenance: str = "RESEARCH_CANDIDATE"
    canonical_effect: str = NONE
    phenomenal_experience_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.component_id.strip():
            raise ValueError("component_id must be non-empty")
        if not self.evidence_refs:
            raise ValueError("at least one evidence_ref is required")
        _require_unit_interval("confidence", self.confidence)
        if self.canonical_effect != NONE:
            raise ValueError("research component must keep canonical_effect=NONE")
        if self.phenomenal_experience_claim != NOT_ESTABLISHED:
            raise ValueError("phenomenal experience must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class MetacognitiveState:
    """Research state representing metacognitive self-model; not a consciousness claim."""

    state_id: str
    subject_ref: str
    context_ref: str
    components: tuple[SelfModelComponent, ...]
    current_depth: MetacognitiveDepth
    active_layers: tuple[SelfModelLayer, ...]
    uncertainty_estimate: float
    conflict_detected: bool
    canonical_effect: str = NONE
    phenomenal_experience_claim: str = NOT_ESTABLISHED
    subjectivity_conclusion: str = NOT_ESTABLISHED
    continuity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        if not self.subject_ref.strip():
            raise ValueError("subject_ref must be non-empty")
        if not self.context_ref.strip():
            raise ValueError("context_ref must be non-empty")
        if not self.components:
            raise ValueError("at least one self-model component is required")
        _require_unit_interval("uncertainty_estimate", self.uncertainty_estimate)
        if self.canonical_effect != NONE:
            raise ValueError("research state must keep canonical_effect=NONE")
        if self.phenomenal_experience_claim != NOT_ESTABLISHED:
            raise ValueError("phenomenal experience must remain NOT_ESTABLISHED")
        if self.subjectivity_conclusion != NOT_ESTABLISHED:
            raise ValueError("subjectivity conclusion must remain NOT_ESTABLISHED")
        if self.continuity_claim != NOT_ESTABLISHED:
            raise ValueError("continuity claim must remain NOT_ESTABLISHED")

    def get_components_by_layer(self, layer: SelfModelLayer) -> tuple[SelfModelComponent, ...]:
        return tuple(c for c in self.components if c.layer == layer)

    def get_components_by_capacity(self, capacity: MetacognitiveCapacity) -> tuple[SelfModelComponent, ...]:
        return tuple(c for c in self.components if c.capacity == capacity)

    def max_confidence(self) -> float:
        return max(c.confidence for c in self.components) if self.components else 0.0