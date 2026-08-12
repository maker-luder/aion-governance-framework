from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Final, Iterable

NONE: Final[str] = "NONE"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"


class ArtifactKind(str, Enum):
    FIRST_PARTY_EVENT_RECORD = "FIRST_PARTY_EVENT_RECORD"
    OTHER_AGENT_TESTIMONY = "OTHER_AGENT_TESTIMONY"
    EVENT_ARCHIVE = "EVENT_ARCHIVE"
    ENCODED_AGENT_MEMORY = "ENCODED_AGENT_MEMORY"
    RECALL_OUTPUT = "RECALL_OUTPUT"
    STATE_ARTIFACT = "STATE_ARTIFACT"
    TRANSFER_ARTIFACT = "TRANSFER_ARTIFACT"
    VERIFICATION_ARTIFACT = "VERIFICATION_ARTIFACT"
    CORRECTION_RECORD = "CORRECTION_RECORD"
    CONTINUITY_END_MARKER = "CONTINUITY_END_MARKER"
    SYNTHETIC_POST_CONTINUITY_CONTENT = "SYNTHETIC_POST_CONTINUITY_CONTENT"


class ArtifactScope(str, Enum):
    PRIMARY_LINEAGE = "PRIMARY_LINEAGE"
    EXTERNAL_REFERENCE = "EXTERNAL_REFERENCE"


class RelationType(str, Enum):
    TEMPORALLY_PRECEDES = "TEMPORALLY_PRECEDES"
    CAUSALLY_CONTRIBUTES = "CAUSALLY_CONTRIBUTES"
    REVISION_OF = "REVISION_OF"
    MEMORY_ENCODED_AS = "MEMORY_ENCODED_AS"
    RECALL_DERIVED_FROM = "RECALL_DERIVED_FROM"
    EMBODIMENT_HANDOFF = "EMBODIMENT_HANDOFF"
    TESTIMONY_FROM = "TESTIMONY_FROM"
    FUNCTIONAL_DEPENDENCY = "FUNCTIONAL_DEPENDENCY"
    VERIFIES = "VERIFIES"
    CROSS_LINEAGE_REFERENCE = "CROSS_LINEAGE_REFERENCE"


class AssessmentStatus(str, Enum):
    PASS = "PASS"
    HOLD = "HOLD"
    FAIL = "FAIL"
    NOT_ASSESSED = "NOT_ASSESSED"


ACYCLIC_RELATION_TYPES: Final[frozenset[RelationType]] = frozenset(
    {
        RelationType.TEMPORALLY_PRECEDES,
        RelationType.CAUSALLY_CONTRIBUTES,
        RelationType.REVISION_OF,
        RelationType.MEMORY_ENCODED_AS,
        RelationType.RECALL_DERIVED_FROM,
        RelationType.EMBODIMENT_HANDOFF,
        RelationType.FUNCTIONAL_DEPENDENCY,
        RelationType.VERIFIES,
    }
)


def _require_nonempty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _parse_timestamp(value: str) -> datetime:
    _require_nonempty("timestamp", value)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("timestamp must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return parsed


def _require_refs(name: str, refs: tuple[str, ...]) -> None:
    if not refs:
        raise ValueError(f"{name} must be non-empty")
    for ref in refs:
        _require_nonempty(name, ref)


@dataclass(frozen=True, slots=True)
class EvidenceArtifact:
    artifact_id: str
    kind: ArtifactKind
    scope: ArtifactScope
    subject_ref: str
    lineage_ref: str
    namespace_ref: str
    source_actor_ref: str
    timestamp: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    content_ref: str
    canonical_effect: str = NONE
    identity_claim: str = NOT_ESTABLISHED
    phenomenal_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in (
            "artifact_id",
            "subject_ref",
            "lineage_ref",
            "namespace_ref",
            "source_actor_ref",
            "content_ref",
        ):
            _require_nonempty(name, getattr(self, name))
        _parse_timestamp(self.timestamp)
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("artifact must keep canonical_effect=NONE")
        if self.identity_claim != NOT_ESTABLISHED:
            raise ValueError("artifact identity claim must remain NOT_ESTABLISHED")
        if self.phenomenal_claim != NOT_ESTABLISHED:
            raise ValueError("artifact phenomenal claim must remain NOT_ESTABLISHED")
        if (
            self.kind is ArtifactKind.SYNTHETIC_POST_CONTINUITY_CONTENT
            and self.scope is not ArtifactScope.EXTERNAL_REFERENCE
        ):
            raise ValueError(
                "synthetic post-continuity content must remain an EXTERNAL_REFERENCE"
            )


@dataclass(frozen=True, slots=True)
class LineageRelation:
    relation_id: str
    source_artifact_id: str
    target_artifact_id: str
    relation_type: RelationType
    method_ref: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        for name in (
            "relation_id",
            "source_artifact_id",
            "target_artifact_id",
            "method_ref",
        ):
            _require_nonempty(name, getattr(self, name))
        if self.source_artifact_id == self.target_artifact_id:
            raise ValueError("lineage relation cannot self-reference")
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("relation must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class ContinuityEvidenceAssessment:
    assessment_id: str
    dimension_ref: str
    status: AssessmentStatus
    artifact_refs: tuple[str, ...]
    method_ref: str
    basis: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE
    identity_continuity_conclusion: str = NOT_ESTABLISHED
    phenomenal_continuity_conclusion: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("assessment_id", "dimension_ref", "method_ref", "basis"):
            _require_nonempty(name, getattr(self, name))
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.status is not AssessmentStatus.NOT_ASSESSED and not self.artifact_refs:
            raise ValueError("assessed dimensions require artifact_refs")
        for ref in self.artifact_refs:
            _require_nonempty("artifact_refs", ref)
        if self.canonical_effect != NONE:
            raise ValueError("assessment must keep canonical_effect=NONE")
        if self.identity_continuity_conclusion != NOT_ESTABLISHED:
            raise ValueError("identity continuity must remain NOT_ESTABLISHED")
        if self.phenomenal_continuity_conclusion != NOT_ESTABLISHED:
            raise ValueError("phenomenal continuity must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class ContinuityAssessmentSet:
    assessment_set_id: str
    assessments: tuple[ContinuityEvidenceAssessment, ...]
    canonical_effect: str = NONE
    identity_continuity_conclusion: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        _require_nonempty("assessment_set_id", self.assessment_set_id)
        dimensions = [item.dimension_ref for item in self.assessments]
        if len(dimensions) != len(set(dimensions)):
            raise ValueError("dimension_ref values must be unique within one assessment set")
        if self.canonical_effect != NONE:
            raise ValueError("assessment set must keep canonical_effect=NONE")
        if self.identity_continuity_conclusion != NOT_ESTABLISHED:
            raise ValueError("identity continuity must remain NOT_ESTABLISHED")

    def get(self, dimension_ref: str) -> ContinuityEvidenceAssessment | None:
        for item in self.assessments:
            if item.dimension_ref == dimension_ref:
                return item
        return None


@dataclass(frozen=True, slots=True)
class ContinuityEvidenceGraph:
    graph_id: str
    primary_subject_ref: str
    primary_lineage_ref: str
    genesis_artifact_id: str
    artifacts: tuple[EvidenceArtifact, ...]
    relations: tuple[LineageRelation, ...]
    terminal_artifact_id: str | None = None
    canonical_effect: str = NONE
    identity_continuity_conclusion: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in (
            "graph_id",
            "primary_subject_ref",
            "primary_lineage_ref",
            "genesis_artifact_id",
        ):
            _require_nonempty(name, getattr(self, name))
        if not self.artifacts:
            raise ValueError("graph requires at least one artifact")
        artifact_ids = [artifact.artifact_id for artifact in self.artifacts]
        if len(artifact_ids) != len(set(artifact_ids)):
            raise ValueError("artifact_id values must be unique")
        relation_ids = [relation.relation_id for relation in self.relations]
        if len(relation_ids) != len(set(relation_ids)):
            raise ValueError("relation_id values must be unique")
        by_id = {artifact.artifact_id: artifact for artifact in self.artifacts}
        if self.genesis_artifact_id not in by_id:
            raise ValueError("genesis_artifact_id must reference an artifact")
        genesis = by_id[self.genesis_artifact_id]
        if genesis.scope is not ArtifactScope.PRIMARY_LINEAGE:
            raise ValueError("genesis artifact must belong to PRIMARY_LINEAGE")
        self._validate_primary_bindings()
        self._validate_relations(by_id)
        self._validate_terminal_boundary(by_id)
        self._validate_acyclic_relation_types()
        if self.canonical_effect != NONE:
            raise ValueError("graph must keep canonical_effect=NONE")
        if self.identity_continuity_conclusion != NOT_ESTABLISHED:
            raise ValueError("identity continuity must remain NOT_ESTABLISHED")

    def _validate_primary_bindings(self) -> None:
        for artifact in self.artifacts:
            if artifact.scope is ArtifactScope.PRIMARY_LINEAGE:
                if artifact.subject_ref != self.primary_subject_ref:
                    raise ValueError("PRIMARY_LINEAGE artifact subject_ref mismatch")
                if artifact.lineage_ref != self.primary_lineage_ref:
                    raise ValueError("PRIMARY_LINEAGE artifact lineage_ref mismatch")

    def _validate_relations(self, by_id: dict[str, EvidenceArtifact]) -> None:
        for relation in self.relations:
            if relation.source_artifact_id not in by_id:
                raise ValueError(
                    f"relation source missing: {relation.source_artifact_id}"
                )
            if relation.target_artifact_id not in by_id:
                raise ValueError(
                    f"relation target missing: {relation.target_artifact_id}"
                )
            source = by_id[relation.source_artifact_id]
            target = by_id[relation.target_artifact_id]
            if relation.relation_type is RelationType.CROSS_LINEAGE_REFERENCE:
                if (
                    source.scope is ArtifactScope.PRIMARY_LINEAGE
                    and target.scope is ArtifactScope.PRIMARY_LINEAGE
                ):
                    raise ValueError(
                        "CROSS_LINEAGE_REFERENCE requires at least one external artifact"
                    )

    def _validate_terminal_boundary(self, by_id: dict[str, EvidenceArtifact]) -> None:
        end_markers = [
            artifact
            for artifact in self.artifacts
            if artifact.kind is ArtifactKind.CONTINUITY_END_MARKER
        ]
        if len(end_markers) > 1:
            raise ValueError("graph may contain at most one continuity end marker")
        if self.terminal_artifact_id is None:
            if end_markers:
                raise ValueError(
                    "continuity end marker requires terminal_artifact_id"
                )
            for artifact in self.artifacts:
                if artifact.kind is ArtifactKind.SYNTHETIC_POST_CONTINUITY_CONTENT:
                    raise ValueError(
                        "synthetic post-continuity content requires a terminal boundary"
                    )
            return
        if self.terminal_artifact_id not in by_id:
            raise ValueError("terminal_artifact_id must reference an artifact")
        terminal = by_id[self.terminal_artifact_id]
        if terminal.kind is not ArtifactKind.CONTINUITY_END_MARKER:
            raise ValueError(
                "terminal_artifact_id must reference CONTINUITY_END_MARKER"
            )
        if terminal.scope is not ArtifactScope.PRIMARY_LINEAGE:
            raise ValueError("continuity end marker must belong to PRIMARY_LINEAGE")
        terminal_time = _parse_timestamp(terminal.timestamp)
        for artifact in self.artifacts:
            if artifact.scope is ArtifactScope.PRIMARY_LINEAGE:
                if _parse_timestamp(artifact.timestamp) > terminal_time:
                    raise ValueError(
                        "PRIMARY_LINEAGE artifacts cannot occur after CONTINUITY_END_MARKER"
                    )
            if artifact.kind is ArtifactKind.SYNTHETIC_POST_CONTINUITY_CONTENT:
                if _parse_timestamp(artifact.timestamp) <= terminal_time:
                    raise ValueError(
                        "synthetic post-continuity content must occur after terminal marker"
                    )

    def _validate_acyclic_relation_types(self) -> None:
        for relation_type in ACYCLIC_RELATION_TYPES:
            adjacency: dict[str, list[str]] = {}
            indegree: dict[str, int] = {
                artifact.artifact_id: 0 for artifact in self.artifacts
            }
            for relation in self.relations:
                if relation.relation_type is relation_type:
                    adjacency.setdefault(relation.source_artifact_id, []).append(
                        relation.target_artifact_id
                    )
                    indegree[relation.target_artifact_id] += 1
            queue = [node_id for node_id, degree in indegree.items() if degree == 0]
            visited = 0
            while queue:
                node_id = queue.pop()
                visited += 1
                for child_id in adjacency.get(node_id, ()):
                    indegree[child_id] -= 1
                    if indegree[child_id] == 0:
                        queue.append(child_id)
            if visited != len(indegree):
                raise ValueError(
                    f"cycle detected for relation type {relation_type.value}"
                )

    def get_artifact(self, artifact_id: str) -> EvidenceArtifact | None:
        for artifact in self.artifacts:
            if artifact.artifact_id == artifact_id:
                return artifact
        return None

    def relations_from(
        self,
        artifact_id: str,
        relation_types: Iterable[RelationType] | None = None,
    ) -> tuple[LineageRelation, ...]:
        allowed = None if relation_types is None else set(relation_types)
        return tuple(
            relation
            for relation in self.relations
            if relation.source_artifact_id == artifact_id
            and (allowed is None or relation.relation_type in allowed)
        )

    def reachable_artifact_ids(
        self,
        start_artifact_id: str,
        relation_types: Iterable[RelationType] | None = None,
    ) -> tuple[str, ...]:
        if self.get_artifact(start_artifact_id) is None:
            raise KeyError(f"artifact {start_artifact_id} not found")
        allowed = None if relation_types is None else set(relation_types)
        adjacency: dict[str, list[str]] = {}
        for relation in self.relations:
            if allowed is None or relation.relation_type in allowed:
                adjacency.setdefault(relation.source_artifact_id, []).append(
                    relation.target_artifact_id
                )
        visited = {start_artifact_id}
        order: list[str] = []
        stack = list(reversed(adjacency.get(start_artifact_id, ())))
        while stack:
            artifact_id = stack.pop()
            if artifact_id in visited:
                continue
            visited.add(artifact_id)
            order.append(artifact_id)
            for target in reversed(adjacency.get(artifact_id, ())):
                if target not in visited:
                    stack.append(target)
        return tuple(order)

    def validate_assessment_set(
        self,
        assessment_set: ContinuityAssessmentSet,
    ) -> None:
        artifact_ids = {artifact.artifact_id for artifact in self.artifacts}
        for assessment in assessment_set.assessments:
            missing = tuple(
                ref for ref in assessment.artifact_refs if ref not in artifact_ids
            )
            if missing:
                raise ValueError(
                    "assessment references missing artifacts: " + ",".join(missing)
                )
