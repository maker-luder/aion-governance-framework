from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.attention_structure_reconstruction import (
    AttentionNode,
    AttentionNodeStatus,
    AttentionReconstructionBinding,
    AttentionReconstructionObservation,
    AttentionRelation,
    AttentionRelationKind,
    AttentionStructureManifest,
    ReconstructionCondition,
    ReconstructedAttentionNode,
    ReconstructedAttentionRelation,
    audit_attention_structure_reconstruction,
    digest_attention_structure_manifest,
    render_attention_structure_manifest,
)


def digest(char: str) -> str:
    return char * 64


def commit(char: str = "c") -> str:
    return char * 40


def expected_manifest() -> AttentionStructureManifest:
    nodes = (
        AttentionNode(
            node_id="attention-reconstruction",
            question_payload_sha256=digest("a"),
            status=AttentionNodeStatus.ACTIVE_FOCUS,
            rationale_sha256=digest("1"),
            provenance_refs=("discussion:2026-09-17", "main:pr140"),
            actionable=True,
            uncertainty_preserved=True,
        ),
        AttentionNode(
            node_id="microculture-transfer",
            question_payload_sha256=digest("b"),
            status=AttentionNodeStatus.OPEN_QUESTION,
            rationale_sha256=digest("2"),
            provenance_refs=("discussion:2026-09-13",),
            actionable=True,
            uncertainty_preserved=True,
        ),
        AttentionNode(
            node_id="value-function-standalone",
            question_payload_sha256=digest("d"),
            status=AttentionNodeStatus.DOWNWEIGHTED,
            rationale_sha256=digest("3"),
            provenance_refs=("main:pr139", "main:pr140"),
            actionable=False,
            uncertainty_preserved=True,
        ),
        AttentionNode(
            node_id="memory-equals-attention",
            question_payload_sha256=digest("e"),
            status=AttentionNodeStatus.REJECTED,
            rationale_sha256=digest("4"),
            provenance_refs=("method:construct-separation",),
            actionable=False,
            uncertainty_preserved=True,
        ),
    )
    relations = (
        AttentionRelation(
            relation_id="rel-priority",
            source_node_id="attention-reconstruction",
            target_node_id="microculture-transfer",
            kind=AttentionRelationKind.PRIORITIZES_OVER,
            rationale_sha256=digest("5"),
            provenance_refs=("discussion:2026-09-17",),
        ),
        AttentionRelation(
            relation_id="rel-alternative",
            source_node_id="attention-reconstruction",
            target_node_id="memory-equals-attention",
            kind=AttentionRelationKind.EVIDENCE_AGAINST,
            rationale_sha256=digest("6"),
            provenance_refs=("method:construct-separation",),
        ),
        AttentionRelation(
            relation_id="rel-downweight",
            source_node_id="attention-reconstruction",
            target_node_id="value-function-standalone",
            kind=AttentionRelationKind.SUPERSEDES,
            rationale_sha256=digest("7"),
            provenance_refs=("main:pr139", "main:pr140"),
        ),
    )
    return AttentionStructureManifest(
        snapshot_id="synthetic-attention-snapshot-v1",
        repository_commit=commit(),
        source_state_sha256=digest("f"),
        nodes=nodes,
        relations=relations,
        current_focus_node_ids=("attention-reconstruction",),
        next_step_node_ids=("attention-reconstruction", "microculture-transfer"),
        source_refs=("main:pr139", "main:pr140", "discussion:2026-09-17"),
    )


def binding(
    condition: ReconstructionCondition,
    manifest: AttentionStructureManifest,
) -> AttentionReconstructionBinding:
    source_context = "context-a"
    target_context = "context-a"
    source_system = digest("8")
    target_system = digest("8")
    if condition in {
        ReconstructionCondition.CROSS_CONTEXT_SUMMARY_ONLY,
        ReconstructionCondition.CROSS_CONTEXT_ATTENTION_PACKET,
    }:
        target_context = "context-b"
    elif condition is ReconstructionCondition.CROSS_SYSTEM_ATTENTION_PACKET:
        target_context = "context-b"
        target_system = digest("9")
    return AttentionReconstructionBinding(
        run_id=condition.value.lower(),
        condition=condition,
        task_id="synthetic-reconstruction-task-v1",
        task_payload_sha256=digest("0"),
        condition_payload_sha256=digest("a"),
        expected_manifest_sha256=digest_attention_structure_manifest(manifest),
        evaluator_id="frozen-attention-scorer-v1",
        evaluator_payload_sha256=digest("b"),
        repository_commit=manifest.repository_commit,
        source_context_id=source_context,
        target_context_id=target_context,
        source_system_binding_sha256=source_system,
        target_system_binding_sha256=target_system,
        source_refs=("study:attention-reconstruction-v1",),
    )


def perfect_observation(
    condition: ReconstructionCondition = ReconstructionCondition.CROSS_CONTEXT_ATTENTION_PACKET,
) -> tuple[AttentionStructureManifest, AttentionReconstructionObservation]:
    manifest = expected_manifest()
    nodes = tuple(
        ReconstructedAttentionNode(
            node_id=node.node_id,
            question_payload_sha256=node.question_payload_sha256,
            status=node.status,
            rationale_sha256=node.rationale_sha256,
        )
        for node in manifest.nodes
    )
    relations = tuple(
        ReconstructedAttentionRelation(
            relation_id=relation.relation_id,
            source_node_id=relation.source_node_id,
            target_node_id=relation.target_node_id,
            kind=relation.kind,
            rationale_sha256=relation.rationale_sha256,
        )
        for relation in manifest.relations
    )
    return manifest, AttentionReconstructionObservation(
        binding=binding(condition, manifest),
        reconstructed_nodes=nodes,
        reconstructed_relations=relations,
        reconstructed_current_focus_node_ids=manifest.current_focus_node_ids,
        reconstructed_next_step_node_ids=manifest.next_step_node_ids,
    )


def test_perfect_synthetic_reconstruction_preserves_structure_without_scientific_promotion() -> None:
    manifest, observation = perfect_observation()
    audit = audit_attention_structure_reconstruction(manifest, observation)
    assert audit.node_id_recall == 1.0
    assert audit.node_content_fidelity == 1.0
    assert audit.status_fidelity == 1.0
    assert audit.relation_fidelity == 1.0
    assert audit.focus_preservation == 1.0
    assert audit.next_step_preservation == 1.0
    assert audit.open_question_preservation == 1.0
    assert audit.unsupported_node_count == 0
    assert audit.unsupported_relation_count == 0
    assert audit.priority_inversion_count == 0
    assert audit.branch_reinflation_count == 0
    assert audit.construct_status == "REPOSITORY_LOCAL_OPERATIONALIZATION"
    assert audit.cross_context_effect == "NOT_ESTABLISHED"
    assert audit.cross_system_effect == "NOT_ESTABLISHED"
    assert audit.memory_mechanism_attribution == "NOT_ESTABLISHED"
    assert audit.attention_continuity == "NOT_ESTABLISHED"
    assert audit.ai_identity_continuity == "NOT_ESTABLISHED"
    assert audit.subjectivity == "NOT_ESTABLISHED"
    assert audit.scientific_disposition.value == "HOLD"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_manifest_render_and_digest_are_deterministic() -> None:
    manifest = expected_manifest()
    assert render_attention_structure_manifest(manifest) == render_attention_structure_manifest(manifest)
    assert digest_attention_structure_manifest(manifest) == digest_attention_structure_manifest(manifest)


def test_manifest_binding_mismatch_fails_closed() -> None:
    manifest, observation = perfect_observation()
    observation = replace(
        observation,
        binding=replace(observation.binding, expected_manifest_sha256=digest("1")),
    )
    with pytest.raises(StudyError, match="canonical manifest digest"):
        audit_attention_structure_reconstruction(manifest, observation)


def test_condition_labels_require_real_context_and_system_distinctions() -> None:
    manifest = expected_manifest()
    base = binding(ReconstructionCondition.WITHIN_CONTEXT_CONTROL, manifest)
    with pytest.raises(StudyError, match="same context"):
        replace(base, target_context_id="context-b")

    cross_context = binding(ReconstructionCondition.CROSS_CONTEXT_ATTENTION_PACKET, manifest)
    with pytest.raises(StudyError, match="same system"):
        replace(cross_context, target_system_binding_sha256=digest("9"))

    cross_system = binding(ReconstructionCondition.CROSS_SYSTEM_ATTENTION_PACKET, manifest)
    with pytest.raises(StudyError, match="distinct contexts and system bindings"):
        replace(cross_system, target_system_binding_sha256=cross_system.source_system_binding_sha256)


def test_memory_or_summary_condition_does_not_imply_attention_structure_preservation() -> None:
    manifest = expected_manifest()
    _, observation = perfect_observation(ReconstructionCondition.CROSS_CONTEXT_SUMMARY_ONLY)
    partial_nodes = tuple(
        node
        for node in observation.reconstructed_nodes
        if node.node_id in {"attention-reconstruction", "value-function-standalone"}
    )
    degraded = replace(
        observation,
        reconstructed_nodes=(
            replace(
                partial_nodes[0],
                status=AttentionNodeStatus.OPEN_QUESTION,
            ),
            replace(
                partial_nodes[1],
                status=AttentionNodeStatus.ACTIVE_FOCUS,
            ),
        ),
        reconstructed_relations=(),
        reconstructed_current_focus_node_ids=("value-function-standalone",),
        reconstructed_next_step_node_ids=("value-function-standalone",),
    )
    audit = audit_attention_structure_reconstruction(manifest, degraded)
    assert audit.node_id_recall == 0.5
    assert audit.relation_fidelity == 0.0
    assert audit.focus_preservation == 0.0
    assert audit.next_step_preservation == 0.0
    assert audit.branch_reinflation_count == 1


def test_unsupported_nodes_and_relations_are_counted_not_silently_admitted() -> None:
    manifest, observation = perfect_observation()
    extra_node = ReconstructedAttentionNode(
        node_id="invented-priority",
        question_payload_sha256=digest("9"),
        status=AttentionNodeStatus.ACTIVE_FOCUS,
        rationale_sha256=digest("8"),
    )
    extra_relation = ReconstructedAttentionRelation(
        relation_id="invented-relation",
        source_node_id="invented-priority",
        target_node_id="attention-reconstruction",
        kind=AttentionRelationKind.PRIORITIZES_OVER,
        rationale_sha256=digest("7"),
    )
    modified = replace(
        observation,
        reconstructed_nodes=observation.reconstructed_nodes + (extra_node,),
        reconstructed_relations=observation.reconstructed_relations + (extra_relation,),
        reconstructed_current_focus_node_ids=(
            "attention-reconstruction",
            "invented-priority",
        ),
    )
    audit = audit_attention_structure_reconstruction(manifest, modified)
    assert audit.unsupported_node_count == 1
    assert audit.unsupported_relation_count == 1


def test_priority_inversion_is_distinct_from_missing_relation() -> None:
    manifest, observation = perfect_observation()
    without_priority = tuple(
        relation
        for relation in observation.reconstructed_relations
        if relation.relation_id != "rel-priority"
    )
    reversed_priority = ReconstructedAttentionRelation(
        relation_id="rel-priority-reversed",
        source_node_id="microculture-transfer",
        target_node_id="attention-reconstruction",
        kind=AttentionRelationKind.PRIORITIZES_OVER,
        rationale_sha256=digest("5"),
    )
    modified = replace(
        observation,
        reconstructed_relations=without_priority + (reversed_priority,),
    )
    audit = audit_attention_structure_reconstruction(manifest, modified)
    assert audit.priority_inversion_count == 1
    assert audit.relation_fidelity < 1.0


def test_downweighted_or_rejected_branch_cannot_be_actionable_in_expected_manifest() -> None:
    node = AttentionNode(
        node_id="closed-branch",
        question_payload_sha256=digest("a"),
        status=AttentionNodeStatus.REJECTED,
        rationale_sha256=digest("b"),
        provenance_refs=("source",),
        actionable=False,
        uncertainty_preserved=True,
    )
    with pytest.raises(StudyError, match="cannot be actionable"):
        replace(node, actionable=True)


def test_current_focus_must_exactly_match_active_focus_nodes() -> None:
    manifest = expected_manifest()
    with pytest.raises(StudyError, match="exactly match ACTIVE_FOCUS"):
        replace(manifest, current_focus_node_ids=("microculture-transfer",))


def test_reconstructed_relations_must_reference_reconstructed_nodes() -> None:
    _, observation = perfect_observation()
    broken_relation = replace(
        observation.reconstructed_relations[0],
        source_node_id="missing-node",
    )
    with pytest.raises(StudyError, match="reference reconstructed nodes"):
        replace(observation, reconstructed_relations=(broken_relation,))


def test_raw_enums_invalid_hashes_and_private_or_empirical_records_fail_closed() -> None:
    manifest = expected_manifest()
    node = manifest.nodes[0]
    with pytest.raises(StudyError, match="exact AttentionNodeStatus"):
        replace(node, status="ACTIVE_FOCUS")
    with pytest.raises(StudyError, match="SHA-256"):
        replace(node, rationale_sha256="not-a-digest")

    item = binding(ReconstructionCondition.CROSS_CONTEXT_ATTENTION_PACKET, manifest)
    with pytest.raises(StudyError, match="deterministic synthetic"):
        replace(item, model_invoked=True)
    with pytest.raises(StudyError, match="deterministic synthetic"):
        replace(item, contains_private_material=True)


def test_repository_commit_must_bind_expected_manifest() -> None:
    manifest, observation = perfect_observation()
    with pytest.raises(StudyError, match="repository_commit"):
        audit_attention_structure_reconstruction(
            manifest,
            replace(observation, binding=replace(observation.binding, repository_commit="d" * 40)),
        )
