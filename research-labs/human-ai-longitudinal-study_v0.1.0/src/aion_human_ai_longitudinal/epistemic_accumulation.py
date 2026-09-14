from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AccumulationError(ValueError):
    pass


class ArtifactCondition(StrEnum):
    FRESH_TASK_LOCAL = "FRESH_TASK_LOCAL"
    FLAT_SUMMARY = "FLAT_SUMMARY"
    VERSIONED_ARTIFACT = "VERSIONED_ARTIFACT"
    VERSIONED_ARTIFACT_PLUS_NAVIGATION = "VERSIONED_ARTIFACT_PLUS_NAVIGATION"


class NodeType(StrEnum):
    CLAIM = "CLAIM"
    HYPOTHESIS = "HYPOTHESIS"
    SOURCE = "SOURCE"
    COUNTEREVIDENCE = "COUNTEREVIDENCE"
    PR = "PR"
    COMMIT = "COMMIT"
    BASELINE = "BASELINE"
    IMPLEMENTATION = "IMPLEMENTATION"
    TEST = "TEST"
    RECEIPT = "RECEIPT"
    AUTHORIZATION = "AUTHORIZATION"
    UNKNOWN = "UNKNOWN"


class EdgeType(StrEnum):
    DEPENDS_ON = "DEPENDS_ON"
    DERIVED_FROM = "DERIVED_FROM"
    SUPPORTED_BY = "SUPPORTED_BY"
    CONTRADICTED_BY = "CONTRADICTED_BY"
    AUTHORIZED_BY = "AUTHORIZED_BY"
    CONSTRAINED_BY = "CONSTRAINED_BY"
    IMPLEMENTED_BY = "IMPLEMENTED_BY"
    TESTED_BY = "TESTED_BY"
    SUPERSEDES = "SUPERSEDES"
    DOES_NOT_IMPLY = "DOES_NOT_IMPLY"


class SupportRelation(StrEnum):
    DIRECT = "DIRECT"
    INDIRECT = "INDIRECT"
    ANALOGY = "ANALOGY"
    BACKGROUND = "BACKGROUND"


class ReuseStatus(StrEnum):
    ALLOWED = "ALLOWED"
    RECHECK_REQUIRED = "RECHECK_REQUIRED"
    REJECTED = "REJECTED"


@dataclass(frozen=True, slots=True)
class DependencyNode:
    node_id: str
    node_type: NodeType
    version_ref: str

    def __post_init__(self) -> None:
        if not self.node_id.strip() or not self.version_ref.strip():
            raise AccumulationError("dependency node id and version ref are required")


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    source_id: str
    target_id: str
    relation: EdgeType


@dataclass(frozen=True, slots=True)
class DependencyGraph:
    baseline_id: str
    nodes: tuple[DependencyNode, ...]
    edges: tuple[DependencyEdge, ...]

    def __post_init__(self) -> None:
        ids = [node.node_id for node in self.nodes]
        if not ids or len(ids) != len(set(ids)):
            raise AccumulationError("dependency nodes must be non-empty and unique")
        known = set(ids)
        if self.baseline_id not in known:
            raise AccumulationError("baseline must reference a graph node")
        if any(edge.source_id not in known or edge.target_id not in known for edge in self.edges):
            raise AccumulationError("dependency edge references an unknown node")
        if any(edge.source_id == edge.target_id for edge in self.edges):
            raise AccumulationError("dependency self-edges are not admitted")


@dataclass(frozen=True, slots=True)
class EvidenceSupportManifest:
    claim_id: str
    source_id: str
    source_class: str
    source_version_or_date: str
    rechecked_at: str
    supported_proposition: str
    requested_proposition: str
    source_scope: str
    requested_scope: str
    support_relation: SupportRelation
    claim_ceiling: str
    known_counterevidence: tuple[str, ...]
    canonical_source: bool
    source_current: bool
    empirical_result_reused: bool
    reuse_status: ReuseStatus
    reuse_reason: str

    def __post_init__(self) -> None:
        for name in (
            "claim_id", "source_id", "source_class", "source_version_or_date", "rechecked_at",
            "supported_proposition", "requested_proposition", "source_scope", "requested_scope",
            "claim_ceiling", "reuse_reason",
        ):
            if not getattr(self, name).strip():
                raise AccumulationError(f"{name} is required")
        for name in ("canonical_source", "source_current", "empirical_result_reused"):
            if type(getattr(self, name)) is not bool:
                raise AccumulationError(f"{name} must be an exact bool")


class EvidenceReuseFirewall:
    def validate(self, manifest: EvidenceSupportManifest) -> ReuseStatus:
        mismatch = (
            manifest.supported_proposition != manifest.requested_proposition
            or manifest.source_scope != manifest.requested_scope
            or not manifest.source_current
            or not manifest.canonical_source
        )
        if manifest.empirical_result_reused:
            expected = ReuseStatus.RECHECK_REQUIRED
        elif mismatch:
            expected = ReuseStatus.RECHECK_REQUIRED
        else:
            expected = ReuseStatus.ALLOWED
        if manifest.reuse_status is not expected:
            raise AccumulationError(f"reuse status must fail closed as {expected.value}")
        return expected


@dataclass(frozen=True, slots=True)
class AccumulationConditionPacket:
    condition: ArtifactCondition
    artifact_payload: str
    provenance_present: bool
    unknown_states_present: bool
    correction_history_present: bool
    navigation_present: bool
    contains_private_transcript: bool = False

    def __post_init__(self) -> None:
        if not self.artifact_payload.strip():
            raise AccumulationError("artifact payload is required")
        if type(self.condition) is not ArtifactCondition:
            raise AccumulationError("condition must be exact")
        flags = (
            self.provenance_present, self.unknown_states_present,
            self.correction_history_present, self.navigation_present,
            self.contains_private_transcript,
        )
        if any(type(flag) is not bool for flag in flags):
            raise AccumulationError("condition flags must be exact bools")
        if self.contains_private_transcript:
            raise AccumulationError("synthetic condition cannot include private transcripts")
        if self.condition is ArtifactCondition.VERSIONED_ARTIFACT and not all(flags[:3]):
            raise AccumulationError("versioned artifact requires provenance unknowns and correction history")
        if self.condition is ArtifactCondition.VERSIONED_ARTIFACT_PLUS_NAVIGATION and not all(flags[:4]):
            raise AccumulationError("navigation condition requires all artifact controls")


def audit_accumulation_packets(packets: tuple[AccumulationConditionPacket, ...]) -> dict[str, object]:
    conditions = [packet.condition for packet in packets]
    if len(packets) != len(ArtifactCondition) or set(conditions) != set(ArtifactCondition):
        raise AccumulationError("exact A-D accumulation matrix is required")
    return {
        "mode": "DETERMINISTIC_SYNTHETIC_FIXTURE",
        "model_invoked": False,
        "structurally_admissible": True,
        "evidence_admissibility": "STRUCTURAL_QA_ONLY",
        "condition_count": len(packets),
        "empirical_result": "SYNTHETIC_FIXTURE_ONLY",
        "mutual_learning": "NOT_ESTABLISHED",
        "identity_continuity": "NOT_ESTABLISHED",
        "causal_identification": "NOT_ESTABLISHED",
        "population_generalization": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "scientific_disposition": "HOLD",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
    }
