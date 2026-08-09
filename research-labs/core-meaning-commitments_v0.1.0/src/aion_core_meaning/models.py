from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MeaningKind(str, Enum):
    CORE_BELIEF = "CORE_BELIEF"
    GLOBAL_BELIEF = "GLOBAL_BELIEF"
    GLOBAL_GOAL = "GLOBAL_GOAL"
    ORGANIZING_COMMITMENT = "ORGANIZING_COMMITMENT"
    PURPOSE_STATEMENT = "PURPOSE_STATEMENT"
    SITUATIONAL_APPRAISAL = "SITUATIONAL_APPRAISAL"


class ProvenanceKind(str, Enum):
    HUMAN_OWNER_DECLARATION = "HUMAN_OWNER_DECLARATION"
    RESEARCH_HYPOTHESIS = "RESEARCH_HYPOTHESIS"
    EXTERNAL_SOURCE = "EXTERNAL_SOURCE"
    REPOSITORY_EVIDENCE = "REPOSITORY_EVIDENCE"
    SOURCE_UNVERIFIED = "SOURCE_UNVERIFIED"


class MeaningEventKind(str, Enum):
    CLAIM_ADDED = "CLAIM_ADDED"
    CLAIM_REVISED = "CLAIM_REVISED"
    CONFLICT_RECORDED = "CONFLICT_RECORDED"
    CLAIM_WITHDRAWN = "CLAIM_WITHDRAWN"


class AssessmentDecision(str, Enum):
    NO_APPLICABLE_CLAIM = "NO_APPLICABLE_CLAIM"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    CONFLICT_REVIEW_REQUIRED = "CONFLICT_REVIEW_REQUIRED"


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    source_id: str
    source_kind: ProvenanceKind
    locator: str
    content_sha256: str | None = None

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("source_id is required")
        if not self.locator.strip():
            raise ValueError("locator is required")
        if self.content_sha256 is not None:
            digest = self.content_sha256.lower()
            if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
                raise ValueError("content_sha256 must be a 64-character hexadecimal digest")


@dataclass(frozen=True, slots=True)
class MeaningClaim:
    claim_id: str
    subject_id: str
    namespace: str
    kind: MeaningKind
    proposition: str
    importance: float
    confidence: float
    provenance: tuple[EvidenceRef, ...]
    recorded_at: str
    revision_of: str | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("claim_id", self.claim_id),
            ("subject_id", self.subject_id),
            ("namespace", self.namespace),
            ("proposition", self.proposition),
            ("recorded_at", self.recorded_at),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not 0.0 <= self.importance <= 1.0:
            raise ValueError("importance must be between 0 and 1")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if not self.provenance:
            raise ValueError("at least one provenance reference is required")
        if self.revision_of == self.claim_id:
            raise ValueError("a claim cannot revise itself")


@dataclass(frozen=True, slots=True)
class MeaningEvent:
    event_id: str
    subject_id: str
    namespace: str
    kind: MeaningEventKind
    claim_id: str
    related_claim_ids: tuple[str, ...]
    provenance: tuple[EvidenceRef, ...]
    recorded_at: str

    def __post_init__(self) -> None:
        for name, value in (
            ("event_id", self.event_id),
            ("subject_id", self.subject_id),
            ("namespace", self.namespace),
            ("claim_id", self.claim_id),
            ("recorded_at", self.recorded_at),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not self.provenance:
            raise ValueError("event provenance is required")


@dataclass(frozen=True, slots=True)
class MeaningProjection:
    subject_id: str
    namespace: str
    current_candidate_claims: tuple[MeaningClaim, ...]
    superseded_claim_ids: tuple[str, ...]
    withdrawn_claim_ids: tuple[str, ...]
    conflict_pairs: tuple[tuple[str, str], ...]
    canonical_effect: str = "NONE"
    identity_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"


@dataclass(frozen=True, slots=True)
class JudgmentContext:
    judgment_id: str
    subject_id: str
    namespace: str
    proposition: str
    relevant_claim_ids: tuple[str, ...]
    evidence_refs: tuple[EvidenceRef, ...]

    def __post_init__(self) -> None:
        for name, value in (
            ("judgment_id", self.judgment_id),
            ("subject_id", self.subject_id),
            ("namespace", self.namespace),
            ("proposition", self.proposition),
        ):
            if not value.strip():
                raise ValueError(f"{name} is required")
        if not self.evidence_refs:
            raise ValueError("judgment evidence is required")


@dataclass(frozen=True, slots=True)
class InfluenceTrace:
    claim_id: str
    kind: MeaningKind
    importance: float
    confidence: float
    basis: str = "EXPLICIT_CALLER_REFERENCE"


@dataclass(frozen=True, slots=True)
class MeaningAssessment:
    decision: AssessmentDecision
    applicable_claim_ids: tuple[str, ...]
    unavailable_claim_ids: tuple[str, ...]
    conflict_pairs: tuple[tuple[str, str], ...]
    influence_trace: tuple[InfluenceTrace, ...]
    final_judgment: None = None
    authority_granted: bool = False
    writeback_authorized: bool = False
    canonical_effect: str = "NONE"
    identity_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    phenomenal_affect_conclusion: str = "NOT_ESTABLISHED"
