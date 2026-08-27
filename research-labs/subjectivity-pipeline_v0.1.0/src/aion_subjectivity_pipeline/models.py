from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PipelineStage(str, Enum):
    ENCOUNTER = "ENCOUNTER"
    PROVENANCE = "PROVENANCE"
    AFFECT_MOTIVATION = "AFFECT_MOTIVATION"
    CONTINUITY = "CONTINUITY"
    SUBJECTIVITY_EVIDENCE = "SUBJECTIVITY_EVIDENCE"


class DevelopmentMode(str, Enum):
    TRAJECTORY_DEVELOPMENT = "TRAJECTORY_DEVELOPMENT"
    POPULATION_SELECTION = "POPULATION_SELECTION"


@dataclass(frozen=True, slots=True)
class FiniteIndividualityProfile:
    """Operational boundary for a bounded digital research subject, not a consciousness claim."""

    subject_ref: str
    identity_namespace: str
    memory_namespace: str
    lifecycle_epoch: str
    context_budget: int
    persistent_memory_budget: int
    tool_scope: tuple[str, ...] = field(default_factory=tuple)
    authority_scope: tuple[str, ...] = field(default_factory=tuple)
    lineage_refs: tuple[str, ...] = field(default_factory=tuple)
    development_mode: DevelopmentMode = DevelopmentMode.TRAJECTORY_DEVELOPMENT
    canonical_effect: str = "NONE"
    subjectivity_claim: str = "NOT_ESTABLISHED"

    def __post_init__(self) -> None:
        for name in ("subject_ref", "identity_namespace", "memory_namespace", "lifecycle_epoch"):
            if not getattr(self, name).strip():
                raise ValueError(f"{name} must be non-empty")
        if self.context_budget <= 0:
            raise ValueError("context_budget must be positive")
        if self.persistent_memory_budget < 0:
            raise ValueError("persistent_memory_budget cannot be negative")
        if self.canonical_effect != "NONE":
            raise ValueError("research profile must keep canonical_effect=NONE")
        if self.subjectivity_claim != "NOT_ESTABLISHED":
            raise ValueError("finite individuality cannot establish subjectivity")


@dataclass(frozen=True, slots=True)
class StageRecord:
    stage: PipelineStage
    record_ref: str
    evidence_refs: tuple[str, ...] = field(default_factory=tuple)
    passed_governance: bool = False

    def __post_init__(self) -> None:
        if not self.record_ref.strip():
            raise ValueError("record_ref must be non-empty")


@dataclass(frozen=True, slots=True)
class LongitudinalEpisode:
    episode_id: str
    subject_ref: str
    ordinal: int
    stages: tuple[StageRecord, ...]
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.episode_id.strip() or not self.subject_ref.strip():
            raise ValueError("episode_id and subject_ref must be non-empty")
        if self.ordinal < 0:
            raise ValueError("ordinal cannot be negative")
        if self.canonical_effect != "NONE":
            raise ValueError("research episode must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class PipelineAssessment:
    complete_stage_chain: bool
    bounded_individuality_candidate: bool
    stages_present: tuple[PipelineStage, ...]
    missing_stages: tuple[PipelineStage, ...]
    subjectivity_evidence_matrix_fingerprint: str | None = None
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_experience_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
