from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ProvenanceError(ValueError):
    pass


class ContributionOrigin(StrEnum):
    HUMAN_ORIGIN = "HUMAN_ORIGIN"
    AI_FORMALIZATION = "AI_FORMALIZATION"
    JOINT_SYNTHESIS = "JOINT_SYNTHESIS"
    EXTERNAL_SOURCE = "EXTERNAL_SOURCE"
    UNKNOWN = "UNKNOWN"


class ClaimLayer(StrEnum):
    DIRECT_STATEMENT = "DIRECT_STATEMENT"
    OBSERVATION = "OBSERVATION"
    SOURCE_REPORT = "SOURCE_REPORT"
    ANALYSIS = "ANALYSIS"
    INFERENCE = "INFERENCE"
    HYPOTHESIS = "HYPOTHESIS"
    CORRECTION = "CORRECTION"


class StateAttribution(StrEnum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    SELF_REPORTED = "SELF_REPORTED"
    OBSERVED_SIGNAL_ONLY = "OBSERVED_SIGNAL_ONLY"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True, slots=True)
class ContributionRecord:
    """Immutable attribution record for a bounded research proposition.

    The record classifies where a proposition entered the collaboration and what
    epistemic layer it occupies. It does not establish that the proposition is true.
    """

    record_id: str
    proposition: str
    origin: ContributionOrigin
    layer: ClaimLayer
    source_refs: tuple[str, ...] = field(default_factory=tuple)
    parent_ids: tuple[str, ...] = field(default_factory=tuple)
    state_attribution: StateAttribution = StateAttribution.NOT_APPLICABLE
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ProvenanceError("record_id must be non-empty")
        if not self.proposition.strip():
            raise ProvenanceError("proposition must be non-empty")
        if self.canonical_effect != "NONE":
            raise ProvenanceError("provenance records cannot create canonical effect")
        if self.origin in {ContributionOrigin.HUMAN_ORIGIN, ContributionOrigin.EXTERNAL_SOURCE} and not self.source_refs:
            raise ProvenanceError(f"{self.origin.value} requires at least one source reference")
        if self.state_attribution is StateAttribution.SELF_REPORTED:
            if self.origin is not ContributionOrigin.HUMAN_ORIGIN:
                raise ProvenanceError("self-reported state must be attributed to HUMAN_ORIGIN")
            if self.layer is not ClaimLayer.DIRECT_STATEMENT:
                raise ProvenanceError("self-reported state requires DIRECT_STATEMENT layer")
        if self.state_attribution is StateAttribution.INFERRED and self.origin is ContributionOrigin.HUMAN_ORIGIN:
            raise ProvenanceError("an inferred state cannot be relabeled as HUMAN_ORIGIN")


@dataclass(frozen=True, slots=True)
class ProvenanceAudit:
    record_id: str
    structurally_valid: bool
    human_origin_admissible: bool
    externally_sourced: bool
    joint_synthesis_admissible: bool
    reasons: tuple[str, ...]
    canonical_effect: str = "NONE"


class EpistemicProvenanceLedger:
    """Small append-only attribution ledger for human-AI research reconstruction.

    It guards source-role attribution only. It does not authenticate a person,
    validate external evidence, or decide scientific truth.
    """

    def __init__(self) -> None:
        self._records: dict[str, ContributionRecord] = {}

    def add(self, record: ContributionRecord) -> None:
        if record.record_id in self._records:
            raise ProvenanceError(f"duplicate record_id: {record.record_id}")
        missing = tuple(parent for parent in record.parent_ids if parent not in self._records)
        if missing:
            raise ProvenanceError(f"unknown parent_ids: {', '.join(missing)}")
        if record.origin is ContributionOrigin.JOINT_SYNTHESIS:
            if len(record.parent_ids) < 2:
                raise ProvenanceError("JOINT_SYNTHESIS requires at least two parent records")
            parent_origins = {self._records[parent].origin for parent in record.parent_ids}
            human_side = ContributionOrigin.HUMAN_ORIGIN in parent_origins or ContributionOrigin.JOINT_SYNTHESIS in parent_origins
            ai_side = ContributionOrigin.AI_FORMALIZATION in parent_origins or ContributionOrigin.JOINT_SYNTHESIS in parent_origins
            if not (human_side and ai_side):
                raise ProvenanceError("JOINT_SYNTHESIS requires traceable human and AI contribution parents")
        self._records[record.record_id] = record

    def get(self, record_id: str) -> ContributionRecord:
        try:
            return self._records[record_id]
        except KeyError as exc:
            raise ProvenanceError(f"unknown record_id: {record_id}") from exc

    def audit(self, record_id: str) -> ProvenanceAudit:
        record = self.get(record_id)
        reasons: list[str] = ["PROVENANCE_IS_NOT_TRUTH"]
        human_origin_admissible = record.origin is ContributionOrigin.HUMAN_ORIGIN and bool(record.source_refs)
        externally_sourced = record.origin is ContributionOrigin.EXTERNAL_SOURCE and bool(record.source_refs)
        joint_synthesis_admissible = False

        if record.origin is ContributionOrigin.JOINT_SYNTHESIS:
            origins = {self._records[parent].origin for parent in record.parent_ids}
            joint_synthesis_admissible = (
                (ContributionOrigin.HUMAN_ORIGIN in origins or ContributionOrigin.JOINT_SYNTHESIS in origins)
                and (ContributionOrigin.AI_FORMALIZATION in origins or ContributionOrigin.JOINT_SYNTHESIS in origins)
            )
            reasons.append("JOINT_SYNTHESIS_PRESERVES_PARENT_ORIGINS")

        if record.origin is ContributionOrigin.UNKNOWN:
            reasons.append("UNKNOWN_ORIGIN_FAILS_CLOSED")
        if record.state_attribution is StateAttribution.INFERRED:
            reasons.append("INFERRED_STATE_IS_NOT_SELF_REPORT")
        if record.state_attribution is StateAttribution.OBSERVED_SIGNAL_ONLY:
            reasons.append("OBSERVED_SIGNAL_DOES_NOT_ESTABLISH_INTERNAL_STATE")
        if record.state_attribution is StateAttribution.SELF_REPORTED:
            reasons.append("SELF_REPORT_IS_ATTRIBUTED_REPORT_NOT_INDEPENDENT_MEASUREMENT")

        return ProvenanceAudit(
            record_id=record.record_id,
            structurally_valid=True,
            human_origin_admissible=human_origin_admissible,
            externally_sourced=externally_sourced,
            joint_synthesis_admissible=joint_synthesis_admissible,
            reasons=tuple(reasons),
        )

    def records(self) -> tuple[ContributionRecord, ...]:
        return tuple(self._records.values())
