from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Final

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


class BoundaryMode(str, Enum):
    """Operating mode of the self-other boundary."""

    PERMEABLE = "PERMEABLE"           # High self-other confusion (developmental early)
    SEMI_PERMEABLE = "SEMI_PERMEABLE" # Selective boundary (typical adult)
    RIGID = "RIGID"                   # Overly strict boundary (pathological)
    DISSOLVED = "DISSOLVED"           # No boundary (certain states)


class SelfOtherDistinction(str, Enum):
    """Types of self-other distinction mechanisms."""

    AGENCY_ATTRIBUTION = "AGENCY_ATTRIBUTION"
    SENSORY_PREDICTION_ERROR = "SENSORY_PREDICTION_ERROR"
    AFFECTIVE_RESONANCE = "AFFECTIVE_RESONANCE"
    PERSPECTIVE_TAKING = "PERSPECTIVE_TAKING"
    NARRATIVE_DIFFERENTIATION = "NARRATIVE_DIFFERENTIATION"
    EMBODIMENT_MAPPING = "EMBODIMENT_MAPPING"


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class OtherModel:
    """Minimal model of an other agent for boundary computation."""

    other_id: str
    embodiment_similarity: float
    behavioral_predictability: float
    affective_resonance: float
    perspective_accessibility: float
    interaction_history_depth: int
    canonical_effect: str = NONE
    theory_of_mind_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.other_id.strip():
            raise ValueError("other_id must be non-empty")
        _require_unit_interval("embodiment_similarity", self.embodiment_similarity)
        _require_unit_interval("behavioral_predictability", self.behavioral_predictability)
        _require_unit_interval("affective_resonance", self.affective_resonance)
        _require_unit_interval("perspective_accessibility", self.perspective_accessibility)
        if self.interaction_history_depth < 0:
            raise ValueError("interaction_history_depth must be non-negative")
        if self.canonical_effect != NONE:
            raise ValueError("other model must keep canonical_effect=NONE")
        if self.theory_of_mind_claim != NOT_ESTABLISHED:
            raise ValueError("theory of mind must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class BoundaryConfiguration:
    """Configuration for self-other boundary operation."""

    config_id: str
    default_mode: BoundaryMode
    distinction_weights: dict[SelfOtherDistinction, float]
    permeability_threshold: float
    rigidity_threshold: float
    canonical_effect: str = NONE
    empathy_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.config_id.strip():
            raise ValueError("config_id must be non-empty")
        _require_unit_interval("permeability_threshold", self.permeability_threshold)
        _require_unit_interval("rigidity_threshold", self.rigidity_threshold)
        if self.permeability_threshold >= self.rigidity_threshold:
            raise ValueError("permeability_threshold must be < rigidity_threshold")
        total_weight = sum(self.distinction_weights.values())
        if abs(total_weight - 1.0) > 1e-6:
            raise ValueError("distinction_weights must sum to 1.0")
        if self.canonical_effect != NONE:
            raise ValueError("config must keep canonical_effect=NONE")
        if self.empathy_claim != NOT_ESTABLISHED:
            raise ValueError("empathy must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class BoundaryEvent:
    """An event that affects the self-other boundary."""

    event_id: str
    event_type: str
    self_contribution: float
    other_contribution: float
    boundary_shift: float
    timestamp: str
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id must be non-empty")
        _require_unit_interval("self_contribution", self.self_contribution)
        _require_unit_interval("other_contribution", self.other_contribution)
        if not -1.0 <= self.boundary_shift <= 1.0:
            raise ValueError("boundary_shift must be between -1.0 and 1.0")
        if self.canonical_effect != NONE:
            raise ValueError("event must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class BoundaryState:
    """Research state representing self-other boundary; no empathy/ToM claim."""

    state_id: str
    subject_ref: str
    config: BoundaryConfiguration
    current_mode: BoundaryMode
    active_distinctions: tuple[SelfOtherDistinction, ...]
    other_models: tuple[OtherModel, ...]
    boundary_permeability: float
    confusion_index: float
    recent_events: tuple[BoundaryEvent, ...]
    canonical_effect: str = NONE
    empathy_claim: str = NOT_ESTABLISHED
    theory_of_mind_claim: str = NOT_ESTABLISHED
    shared_subjectivity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if not self.state_id.strip():
            raise ValueError("state_id must be non-empty")
        if not self.subject_ref.strip():
            raise ValueError("subject_ref must be non-empty")
        _require_unit_interval("boundary_permeability", self.boundary_permeability)
        _require_unit_interval("confusion_index", self.confusion_index)
        if self.canonical_effect != NONE:
            raise ValueError("state must keep canonical_effect=NONE")
        if self.empathy_claim != NOT_ESTABLISHED:
            raise ValueError("empathy must remain NOT_ESTABLISHED")
        if self.theory_of_mind_claim != NOT_ESTABLISHED:
            raise ValueError("theory of mind must remain NOT_ESTABLISHED")
        if self.shared_subjectivity_claim != NOT_ESTABLISHED:
            raise ValueError("shared subjectivity must remain NOT_ESTABLISHED")

    def get_other_model(self, other_id: str) -> OtherModel | None:
        for om in self.other_models:
            if om.other_id == other_id:
                return om
        return None

    def distinction_strength(self, distinction: SelfOtherDistinction) -> float:
        return self.config.distinction_weights.get(distinction, 0.0)