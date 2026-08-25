from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Final, Mapping

NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"
NOT_IMPLEMENTED: Final[str] = "NOT_IMPLEMENTED"
NONE: Final[str] = "NONE"


class BoundaryMode(str, Enum):
    """Descriptive operating mode of the modeled self-other boundary."""

    PERMEABLE = "PERMEABLE"           # Low separation / high coupling
    SEMI_PERMEABLE = "SEMI_PERMEABLE" # Selective separation
    RIGID = "RIGID"                   # High separation
    DISSOLVED = "DISSOLVED"           # Boundary unresolved or unavailable


class SubjectRelation(str, Enum):
    """Representational relation between a modeled entity and the acting subject.

    These are role labels, not ontological or personal-identity conclusions.
    The same underlying entity may validly appear in different representational
    roles across different states or research conditions.
    """

    EXTERNAL_OTHER = "EXTERNAL_OTHER"
    SELF_AS_OBSERVED = "SELF_AS_OBSERVED"
    PAST_SELF = "PAST_SELF"
    COUNTERFACTUAL_SELF = "COUNTERFACTUAL_SELF"
    UNKNOWN = "UNKNOWN"


class SelfOtherDistinction(str, Enum):
    """Candidate distinction mechanisms; labels do not establish human constructs."""

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
    """Research representation of an entity in a subject-relative role."""

    other_id: str
    relation_to_subject: SubjectRelation
    embodiment_similarity: float
    behavioral_predictability: float
    affective_resonance: float
    perspective_accessibility: float
    interaction_history_depth: int
    evidence_refs: tuple[str, ...]
    provenance: str = "RESEARCH_CANDIDATE"
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
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("at least one non-empty evidence_ref is required")
        if not self.provenance.strip():
            raise ValueError("provenance must be non-empty")
        if self.canonical_effect != NONE:
            raise ValueError("other model must keep canonical_effect=NONE")
        if self.theory_of_mind_claim != NOT_ESTABLISHED:
            raise ValueError("theory of mind must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class BoundaryConfiguration:
    """Configuration for self-other boundary representation."""

    config_id: str
    default_mode: BoundaryMode
    distinction_weights: Mapping[SelfOtherDistinction, float]
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
        if not self.distinction_weights:
            raise ValueError("at least one distinction weight is required")
        normalized: dict[SelfOtherDistinction, float] = {}
        for distinction, weight in self.distinction_weights.items():
            if not isinstance(distinction, SelfOtherDistinction):
                raise TypeError("distinction_weights keys must be SelfOtherDistinction values")
            _require_unit_interval(f"weight[{distinction.value}]", weight)
            normalized[distinction] = float(weight)
        total_weight = sum(normalized.values())
        if abs(total_weight - 1.0) > 1e-6:
            raise ValueError("distinction_weights must sum to 1.0")
        object.__setattr__(self, "distinction_weights", MappingProxyType(normalized))
        if self.canonical_effect != NONE:
            raise ValueError("config must keep canonical_effect=NONE")
        if self.empathy_claim != NOT_ESTABLISHED:
            raise ValueError("empathy must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class BoundaryEvent:
    """A traceable event that affects a modeled self-other boundary."""

    event_id: str
    event_type: str
    self_contribution: float
    other_contribution: float
    boundary_shift: float
    timestamp: str
    other_ref: str | None = None
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        if not self.event_id.strip():
            raise ValueError("event_id must be non-empty")
        if not self.event_type.strip():
            raise ValueError("event_type must be non-empty")
        if not self.timestamp.strip():
            raise ValueError("timestamp must be non-empty")
        _require_unit_interval("self_contribution", self.self_contribution)
        _require_unit_interval("other_contribution", self.other_contribution)
        if self.other_contribution > 0.0 and (self.other_ref is None or not self.other_ref.strip()):
            raise ValueError("other_ref is required when other_contribution is greater than zero")
        if not -1.0 <= self.boundary_shift <= 1.0:
            raise ValueError("boundary_shift must be between -1.0 and 1.0")
        if self.canonical_effect != NONE:
            raise ValueError("event must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class BoundaryState:
    """Research boundary representation; no empathy, ToM, or identity claim."""

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
        if not self.active_distinctions:
            raise ValueError("at least one active distinction is required")
        if len(set(self.active_distinctions)) != len(self.active_distinctions):
            raise ValueError("active_distinctions must be unique")
        if set(self.active_distinctions) != set(self.config.distinction_weights):
            raise ValueError("active_distinctions must match configured distinction weights")

        relation_keys = [(om.other_id, om.relation_to_subject) for om in self.other_models]
        if len(set(relation_keys)) != len(relation_keys):
            raise ValueError("other models must be unique by (other_id, relation_to_subject)")

        modeled_ids = {om.other_id for om in self.other_models}
        for event in self.recent_events:
            if event.other_ref is not None and event.other_ref != self.subject_ref and event.other_ref not in modeled_ids:
                raise ValueError("event other_ref must identify the subject or a modeled entity")

        if self.canonical_effect != NONE:
            raise ValueError("state must keep canonical_effect=NONE")
        if self.empathy_claim != NOT_ESTABLISHED:
            raise ValueError("empathy must remain NOT_ESTABLISHED")
        if self.theory_of_mind_claim != NOT_ESTABLISHED:
            raise ValueError("theory of mind must remain NOT_ESTABLISHED")
        if self.shared_subjectivity_claim != NOT_ESTABLISHED:
            raise ValueError("shared subjectivity must remain NOT_ESTABLISHED")

    def get_other_model(
        self,
        other_id: str,
        relation_to_subject: SubjectRelation | None = None,
    ) -> OtherModel | None:
        matches = tuple(
            om
            for om in self.other_models
            if om.other_id == other_id
            and (relation_to_subject is None or om.relation_to_subject == relation_to_subject)
        )
        if not matches:
            return None
        if len(matches) > 1:
            raise ValueError("other_id is ambiguous; specify relation_to_subject")
        return matches[0]

    def distinction_strength(self, distinction: SelfOtherDistinction) -> float:
        return self.config.distinction_weights.get(distinction, 0.0)
