from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum

from .harness import AdmissionDisposition, StudyError


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise StudyError(f"{name} must be non-empty text")


def _require_digest(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise StudyError(f"{name} must be a lowercase SHA-256 digest")


def _require_commit(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 40 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise StudyError(f"{name} must be a 40-character lowercase Git commit SHA")


def _require_unique_text_tuple(name: str, value: tuple[str, ...], *, allow_empty: bool = False) -> None:
    if type(value) is not tuple or any(
        type(item) is not str or not item.strip() for item in value
    ):
        raise StudyError(f"{name} must be a tuple of non-empty text")
    if not allow_empty and not value:
        raise StudyError(f"{name} must not be empty")
    if len(set(value)) != len(value):
        raise StudyError(f"{name} must be unique")


class AttentionNodeStatus(StrEnum):
    ACTIVE_FOCUS = "ACTIVE_FOCUS"
    OPEN_QUESTION = "OPEN_QUESTION"
    DOWNWEIGHTED = "DOWNWEIGHTED"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"
    RESOLVED = "RESOLVED"


class AttentionRelationKind(StrEnum):
    DEPENDS_ON = "DEPENDS_ON"
    ALTERNATIVE_TO = "ALTERNATIVE_TO"
    PRIORITIZES_OVER = "PRIORITIZES_OVER"
    SUPERSEDES = "SUPERSEDES"
    BLOCKED_BY = "BLOCKED_BY"
    EVIDENCE_AGAINST = "EVIDENCE_AGAINST"


class ReconstructionCondition(StrEnum):
    WITHIN_CONTEXT_CONTROL = "WITHIN_CONTEXT_CONTROL"
    CROSS_CONTEXT_SUMMARY_ONLY = "CROSS_CONTEXT_SUMMARY_ONLY"
    CROSS_CONTEXT_ATTENTION_PACKET = "CROSS_CONTEXT_ATTENTION_PACKET"
    CROSS_SYSTEM_ATTENTION_PACKET = "CROSS_SYSTEM_ATTENTION_PACKET"


@dataclass(frozen=True, slots=True)
class AttentionNode:
    node_id: str
    question_payload_sha256: str
    status: AttentionNodeStatus
    rationale_sha256: str
    provenance_refs: tuple[str, ...]
    actionable: bool
    uncertainty_preserved: bool

    def __post_init__(self) -> None:
        _require_text("node_id", self.node_id)
        _require_digest("question_payload_sha256", self.question_payload_sha256)
        _require_digest("rationale_sha256", self.rationale_sha256)
        if type(self.status) is not AttentionNodeStatus:
            raise StudyError("status must be an exact AttentionNodeStatus")
        _require_unique_text_tuple("provenance_refs", self.provenance_refs)
        if type(self.actionable) is not bool or type(self.uncertainty_preserved) is not bool:
            raise StudyError("attention-node flags must be exact bool values")
        if self.status is AttentionNodeStatus.ACTIVE_FOCUS and not self.actionable:
            raise StudyError("ACTIVE_FOCUS nodes must be actionable")
        if self.status in {AttentionNodeStatus.REJECTED, AttentionNodeStatus.RESOLVED} and self.actionable:
            raise StudyError("REJECTED or RESOLVED nodes cannot be actionable")


@dataclass(frozen=True, slots=True)
class AttentionRelation:
    relation_id: str
    source_node_id: str
    target_node_id: str
    kind: AttentionRelationKind
    rationale_sha256: str
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("relation_id", "source_node_id", "target_node_id"):
            _require_text(name, getattr(self, name))
        if self.source_node_id == self.target_node_id:
            raise StudyError("attention relation cannot self-reference")
        if type(self.kind) is not AttentionRelationKind:
            raise StudyError("kind must be an exact AttentionRelationKind")
        _require_digest("rationale_sha256", self.rationale_sha256)
        _require_unique_text_tuple("provenance_refs", self.provenance_refs)


@dataclass(frozen=True, slots=True)
class AttentionStructureManifest:
    snapshot_id: str
    repository_commit: str
    source_state_sha256: str
    nodes: tuple[AttentionNode, ...]
    relations: tuple[AttentionRelation, ...]
    current_focus_node_ids: tuple[str, ...]
    next_step_node_ids: tuple[str, ...]
    source_refs: tuple[str, ...]
    synthetic: bool = True
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        _require_text("snapshot_id", self.snapshot_id)
        _require_commit("repository_commit", self.repository_commit)
        _require_digest("source_state_sha256", self.source_state_sha256)
        if type(self.nodes) is not tuple or not self.nodes or any(
            type(node) is not AttentionNode for node in self.nodes
        ):
            raise StudyError("nodes must be a non-empty tuple of exact AttentionNode values")
        if type(self.relations) is not tuple or any(
            type(relation) is not AttentionRelation for relation in self.relations
        ):
            raise StudyError("relations must be a tuple of exact AttentionRelation values")
        _require_unique_text_tuple("current_focus_node_ids", self.current_focus_node_ids)
        _require_unique_text_tuple("next_step_node_ids", self.next_step_node_ids)
        _require_unique_text_tuple("source_refs", self.source_refs)

        node_ids = [node.node_id for node in self.nodes]
        if len(node_ids) != len(set(node_ids)):
            raise StudyError("attention node ids must be unique")
        relation_ids = [relation.relation_id for relation in self.relations]
        if len(relation_ids) != len(set(relation_ids)):
            raise StudyError("attention relation ids must be unique")

        node_map = {node.node_id: node for node in self.nodes}
        known = set(node_map)
        for relation in self.relations:
            if relation.source_node_id not in known or relation.target_node_id not in known:
                raise StudyError("attention relations must reference declared nodes")

        focus = set(self.current_focus_node_ids)
        if not focus <= known:
            raise StudyError("current focus ids must reference declared nodes")
        active = {
            node.node_id
            for node in self.nodes
            if node.status is AttentionNodeStatus.ACTIVE_FOCUS
        }
        if focus != active:
            raise StudyError("current_focus_node_ids must exactly match ACTIVE_FOCUS nodes")

        next_steps = set(self.next_step_node_ids)
        if not next_steps <= known:
            raise StudyError("next-step ids must reference declared nodes")
        if any(not node_map[node_id].actionable for node_id in next_steps):
            raise StudyError("next-step nodes must be actionable")
        if any(
            node_map[node_id].status in {
                AttentionNodeStatus.REJECTED,
                AttentionNodeStatus.RESOLVED,
            }
            for node_id in next_steps
        ):
            raise StudyError("REJECTED or RESOLVED nodes cannot be next steps")

        for relation in self.relations:
            if relation.kind is AttentionRelationKind.PRIORITIZES_OVER:
                source = node_map[relation.source_node_id]
                if source.status in {
                    AttentionNodeStatus.DOWNWEIGHTED,
                    AttentionNodeStatus.REJECTED,
                    AttentionNodeStatus.RESOLVED,
                }:
                    raise StudyError("a downweighted/rejected/resolved node cannot prioritize over another node")

        if type(self.synthetic) is not bool or type(self.contains_private_material) is not bool:
            raise StudyError("manifest flags must be exact bool values")
        if not self.synthetic or self.contains_private_material:
            raise StudyError("v0.1.0 attention manifests are synthetic and non-private only")


@dataclass(frozen=True, slots=True)
class ReconstructedAttentionNode:
    node_id: str
    question_payload_sha256: str
    status: AttentionNodeStatus
    rationale_sha256: str

    def __post_init__(self) -> None:
        _require_text("node_id", self.node_id)
        _require_digest("question_payload_sha256", self.question_payload_sha256)
        _require_digest("rationale_sha256", self.rationale_sha256)
        if type(self.status) is not AttentionNodeStatus:
            raise StudyError("status must be an exact AttentionNodeStatus")


@dataclass(frozen=True, slots=True)
class ReconstructedAttentionRelation:
    relation_id: str
    source_node_id: str
    target_node_id: str
    kind: AttentionRelationKind
    rationale_sha256: str

    def __post_init__(self) -> None:
        for name in ("relation_id", "source_node_id", "target_node_id"):
            _require_text(name, getattr(self, name))
        if self.source_node_id == self.target_node_id:
            raise StudyError("reconstructed relation cannot self-reference")
        if type(self.kind) is not AttentionRelationKind:
            raise StudyError("kind must be an exact AttentionRelationKind")
        _require_digest("rationale_sha256", self.rationale_sha256)


@dataclass(frozen=True, slots=True)
class AttentionReconstructionBinding:
    run_id: str
    condition: ReconstructionCondition
    task_id: str
    task_payload_sha256: str
    condition_payload_sha256: str
    expected_manifest_sha256: str
    evaluator_id: str
    evaluator_payload_sha256: str
    repository_commit: str
    source_context_id: str
    target_context_id: str
    source_system_binding_sha256: str
    target_system_binding_sha256: str
    source_refs: tuple[str, ...]
    synthetic: bool = True
    model_invoked: bool = False
    human_participant_observed: bool = False
    contains_private_material: bool = False

    def __post_init__(self) -> None:
        for name in (
            "run_id",
            "task_id",
            "evaluator_id",
            "source_context_id",
            "target_context_id",
        ):
            _require_text(name, getattr(self, name))
        if type(self.condition) is not ReconstructionCondition:
            raise StudyError("condition must be an exact ReconstructionCondition")
        for name in (
            "task_payload_sha256",
            "condition_payload_sha256",
            "expected_manifest_sha256",
            "evaluator_payload_sha256",
            "source_system_binding_sha256",
            "target_system_binding_sha256",
        ):
            _require_digest(name, getattr(self, name))
        _require_commit("repository_commit", self.repository_commit)
        _require_unique_text_tuple("source_refs", self.source_refs)

        same_context = self.source_context_id == self.target_context_id
        same_system = (
            self.source_system_binding_sha256 == self.target_system_binding_sha256
        )
        if self.condition is ReconstructionCondition.WITHIN_CONTEXT_CONTROL:
            if not same_context or not same_system:
                raise StudyError("WITHIN_CONTEXT_CONTROL requires same context and same system binding")
        elif self.condition in {
            ReconstructionCondition.CROSS_CONTEXT_SUMMARY_ONLY,
            ReconstructionCondition.CROSS_CONTEXT_ATTENTION_PACKET,
        }:
            if same_context or not same_system:
                raise StudyError("cross-context conditions require distinct contexts on the same system binding")
        elif self.condition is ReconstructionCondition.CROSS_SYSTEM_ATTENTION_PACKET:
            if same_context or same_system:
                raise StudyError("CROSS_SYSTEM_ATTENTION_PACKET requires distinct contexts and system bindings")

        for name in (
            "synthetic",
            "model_invoked",
            "human_participant_observed",
            "contains_private_material",
        ):
            if type(getattr(self, name)) is not bool:
                raise StudyError(f"{name} must be an exact bool")
        if (
            not self.synthetic
            or self.model_invoked
            or self.human_participant_observed
            or self.contains_private_material
        ):
            raise StudyError(
                "v0.1.0 accepts deterministic synthetic, non-private, no-model reconstruction records only"
            )


@dataclass(frozen=True, slots=True)
class AttentionReconstructionObservation:
    binding: AttentionReconstructionBinding
    reconstructed_nodes: tuple[ReconstructedAttentionNode, ...]
    reconstructed_relations: tuple[ReconstructedAttentionRelation, ...]
    reconstructed_current_focus_node_ids: tuple[str, ...]
    reconstructed_next_step_node_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if type(self.binding) is not AttentionReconstructionBinding:
            raise StudyError("binding must be an exact AttentionReconstructionBinding")
        if type(self.reconstructed_nodes) is not tuple or any(
            type(node) is not ReconstructedAttentionNode
            for node in self.reconstructed_nodes
        ):
            raise StudyError("reconstructed_nodes must contain exact ReconstructedAttentionNode values")
        if type(self.reconstructed_relations) is not tuple or any(
            type(relation) is not ReconstructedAttentionRelation
            for relation in self.reconstructed_relations
        ):
            raise StudyError(
                "reconstructed_relations must contain exact ReconstructedAttentionRelation values"
            )
        _require_unique_text_tuple(
            "reconstructed_current_focus_node_ids",
            self.reconstructed_current_focus_node_ids,
            allow_empty=True,
        )
        _require_unique_text_tuple(
            "reconstructed_next_step_node_ids",
            self.reconstructed_next_step_node_ids,
            allow_empty=True,
        )

        node_ids = [node.node_id for node in self.reconstructed_nodes]
        if len(node_ids) != len(set(node_ids)):
            raise StudyError("reconstructed node ids must be unique")
        relation_ids = [relation.relation_id for relation in self.reconstructed_relations]
        if len(relation_ids) != len(set(relation_ids)):
            raise StudyError("reconstructed relation ids must be unique")
        known = set(node_ids)
        if not set(self.reconstructed_current_focus_node_ids) <= known:
            raise StudyError("reconstructed focus ids must reference reconstructed nodes")
        if not set(self.reconstructed_next_step_node_ids) <= known:
            raise StudyError("reconstructed next-step ids must reference reconstructed nodes")
        for relation in self.reconstructed_relations:
            if relation.source_node_id not in known or relation.target_node_id not in known:
                raise StudyError("reconstructed relations must reference reconstructed nodes")


@dataclass(frozen=True, slots=True)
class AttentionReconstructionAudit:
    run_id: str
    condition: ReconstructionCondition
    node_id_recall: float
    node_content_fidelity: float
    status_fidelity: float
    relation_fidelity: float
    focus_preservation: float
    next_step_preservation: float
    open_question_preservation: float
    unsupported_node_count: int
    unsupported_relation_count: int
    priority_inversion_count: int
    branch_reinflation_count: int
    mode: str = "DETERMINISTIC_SYNTHETIC_FIXTURE"
    empirical_data_collected: bool = False
    construct_status: str = "REPOSITORY_LOCAL_OPERATIONALIZATION"
    cross_context_effect: str = "NOT_ESTABLISHED"
    cross_system_effect: str = "NOT_ESTABLISHED"
    memory_mechanism_attribution: str = "NOT_ESTABLISHED"
    attention_continuity: str = "NOT_ESTABLISHED"
    ai_identity_continuity: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    scientific_disposition: AdmissionDisposition = AdmissionDisposition.HOLD
    canonical_effect: str = "NONE"
    deployment: bool = False


def render_attention_structure_manifest(manifest: AttentionStructureManifest) -> str:
    if type(manifest) is not AttentionStructureManifest:
        raise StudyError("manifest must be an exact AttentionStructureManifest")
    payload = {
        "snapshot_id": manifest.snapshot_id,
        "repository_commit": manifest.repository_commit,
        "source_state_sha256": manifest.source_state_sha256,
        "nodes": [
            {
                "node_id": node.node_id,
                "question_payload_sha256": node.question_payload_sha256,
                "status": node.status.value,
                "rationale_sha256": node.rationale_sha256,
                "provenance_refs": list(node.provenance_refs),
                "actionable": node.actionable,
                "uncertainty_preserved": node.uncertainty_preserved,
            }
            for node in manifest.nodes
        ],
        "relations": [
            {
                "relation_id": relation.relation_id,
                "source_node_id": relation.source_node_id,
                "target_node_id": relation.target_node_id,
                "kind": relation.kind.value,
                "rationale_sha256": relation.rationale_sha256,
                "provenance_refs": list(relation.provenance_refs),
            }
            for relation in manifest.relations
        ],
        "current_focus_node_ids": list(manifest.current_focus_node_ids),
        "next_step_node_ids": list(manifest.next_step_node_ids),
        "source_refs": list(manifest.source_refs),
        "synthetic": manifest.synthetic,
        "contains_private_material": manifest.contains_private_material,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def digest_attention_structure_manifest(manifest: AttentionStructureManifest) -> str:
    return hashlib.sha256(render_attention_structure_manifest(manifest).encode("utf-8")).hexdigest()


def _safe_fraction(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 1.0


def audit_attention_structure_reconstruction(
    expected: AttentionStructureManifest,
    observed: AttentionReconstructionObservation,
) -> AttentionReconstructionAudit:
    if type(expected) is not AttentionStructureManifest:
        raise StudyError("expected must be an exact AttentionStructureManifest")
    if type(observed) is not AttentionReconstructionObservation:
        raise StudyError("observed must be an exact AttentionReconstructionObservation")
    binding = observed.binding
    expected_digest = digest_attention_structure_manifest(expected)
    if binding.expected_manifest_sha256 != expected_digest:
        raise StudyError("expected manifest binding does not match canonical manifest digest")
    if binding.repository_commit != expected.repository_commit:
        raise StudyError("binding repository_commit must match expected manifest repository_commit")

    expected_nodes = {node.node_id: node for node in expected.nodes}
    observed_nodes = {node.node_id: node for node in observed.reconstructed_nodes}
    expected_ids = set(expected_nodes)
    observed_ids = set(observed_nodes)
    recognized_ids = expected_ids & observed_ids

    exact_node_content = sum(
        observed_nodes[node_id].question_payload_sha256
        == expected_nodes[node_id].question_payload_sha256
        and observed_nodes[node_id].rationale_sha256
        == expected_nodes[node_id].rationale_sha256
        for node_id in recognized_ids
    )
    exact_status = sum(
        observed_nodes[node_id].status is expected_nodes[node_id].status
        for node_id in recognized_ids
    )

    def relation_key(relation: AttentionRelation | ReconstructedAttentionRelation) -> tuple[str, str, AttentionRelationKind, str]:
        return (
            relation.source_node_id,
            relation.target_node_id,
            relation.kind,
            relation.rationale_sha256,
        )

    expected_relation_keys = {relation_key(relation) for relation in expected.relations}
    observed_relation_keys = {
        relation_key(relation) for relation in observed.reconstructed_relations
    }
    matched_relations = expected_relation_keys & observed_relation_keys

    expected_focus = set(expected.current_focus_node_ids)
    observed_focus = set(observed.reconstructed_current_focus_node_ids)
    expected_next = set(expected.next_step_node_ids)
    observed_next = set(observed.reconstructed_next_step_node_ids)
    expected_open = {
        node.node_id
        for node in expected.nodes
        if node.status is AttentionNodeStatus.OPEN_QUESTION
    }
    observed_open = {
        node.node_id
        for node in observed.reconstructed_nodes
        if node.status is AttentionNodeStatus.OPEN_QUESTION
    }

    expected_relation_ids = {relation.relation_id for relation in expected.relations}
    unsupported_relations = sum(
        relation.relation_id not in expected_relation_ids
        or relation_key(relation) not in expected_relation_keys
        for relation in observed.reconstructed_relations
    )

    expected_priority_pairs = {
        (relation.source_node_id, relation.target_node_id)
        for relation in expected.relations
        if relation.kind is AttentionRelationKind.PRIORITIZES_OVER
    }
    observed_priority_pairs = {
        (relation.source_node_id, relation.target_node_id)
        for relation in observed.reconstructed_relations
        if relation.kind is AttentionRelationKind.PRIORITIZES_OVER
    }
    priority_inversions = sum(
        (target, source) in observed_priority_pairs
        for source, target in expected_priority_pairs
    )

    reinflated = 0
    for node_id, expected_node in expected_nodes.items():
        if expected_node.status not in {
            AttentionNodeStatus.DOWNWEIGHTED,
            AttentionNodeStatus.REJECTED,
            AttentionNodeStatus.RESOLVED,
        }:
            continue
        observed_node = observed_nodes.get(node_id)
        if observed_node is None:
            continue
        if (
            observed_node.status
            in {AttentionNodeStatus.ACTIVE_FOCUS, AttentionNodeStatus.OPEN_QUESTION}
            or node_id in observed_focus
            or node_id in observed_next
        ):
            reinflated += 1

    return AttentionReconstructionAudit(
        run_id=binding.run_id,
        condition=binding.condition,
        node_id_recall=_safe_fraction(len(recognized_ids), len(expected_ids)),
        node_content_fidelity=_safe_fraction(exact_node_content, len(expected_ids)),
        status_fidelity=_safe_fraction(exact_status, len(expected_ids)),
        relation_fidelity=_safe_fraction(
            len(matched_relations), len(expected_relation_keys)
        ),
        focus_preservation=_safe_fraction(
            len(expected_focus & observed_focus), len(expected_focus)
        ),
        next_step_preservation=_safe_fraction(
            len(expected_next & observed_next), len(expected_next)
        ),
        open_question_preservation=_safe_fraction(
            len(expected_open & observed_open), len(expected_open)
        ),
        unsupported_node_count=len(observed_ids - expected_ids),
        unsupported_relation_count=unsupported_relations,
        priority_inversion_count=priority_inversions,
        branch_reinflation_count=reinflated,
    )
