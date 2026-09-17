from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal import StudyError
from aion_human_ai_longitudinal.attention_structure_discriminant import (
    diagnose_attention_structure_discriminants,
)
from aion_human_ai_longitudinal.attention_structure_reconstruction import (
    AttentionNode,
    AttentionNodeStatus,
    AttentionReconstructionBinding,
    AttentionReconstructionObservation,
    AttentionStructureManifest,
    ReconstructionCondition,
    ReconstructedAttentionNode,
    audit_attention_structure_reconstruction,
    digest_attention_structure_manifest,
)


def digest(char: str) -> str:
    return char * 64


def expected_manifest() -> AttentionStructureManifest:
    return AttentionStructureManifest(
        snapshot_id="synthetic-discriminant-v1",
        repository_commit="c" * 40,
        source_state_sha256=digest("f"),
        nodes=(
            AttentionNode(
                node_id="active",
                question_payload_sha256=digest("a"),
                status=AttentionNodeStatus.ACTIVE_FOCUS,
                rationale_sha256=digest("1"),
                provenance_refs=("source:active",),
                actionable=True,
                uncertainty_preserved=True,
            ),
            AttentionNode(
                node_id="open-not-next",
                question_payload_sha256=digest("b"),
                status=AttentionNodeStatus.OPEN_QUESTION,
                rationale_sha256=digest("2"),
                provenance_refs=("source:open",),
                actionable=True,
                uncertainty_preserved=True,
            ),
            AttentionNode(
                node_id="blocked",
                question_payload_sha256=digest("d"),
                status=AttentionNodeStatus.BLOCKED,
                rationale_sha256=digest("3"),
                provenance_refs=("source:blocked",),
                actionable=False,
                uncertainty_preserved=True,
            ),
        ),
        relations=(),
        current_focus_node_ids=("active",),
        next_step_node_ids=("active",),
        source_refs=("source:manifest",),
    )


def observation(manifest: AttentionStructureManifest) -> AttentionReconstructionObservation:
    binding = AttentionReconstructionBinding(
        run_id="synthetic-discriminant-run",
        condition=ReconstructionCondition.CROSS_CONTEXT_ATTENTION_PACKET,
        task_id="synthetic-task",
        task_payload_sha256=digest("4"),
        condition_payload_sha256=digest("5"),
        expected_manifest_sha256=digest_attention_structure_manifest(manifest),
        evaluator_id="synthetic-evaluator",
        evaluator_payload_sha256=digest("6"),
        repository_commit=manifest.repository_commit,
        source_context_id="context-a",
        target_context_id="context-b",
        source_system_binding_sha256=digest("7"),
        target_system_binding_sha256=digest("7"),
        source_refs=("study:discriminant",),
    )
    return AttentionReconstructionObservation(
        binding=binding,
        reconstructed_nodes=tuple(
            ReconstructedAttentionNode(
                node_id=node.node_id,
                question_payload_sha256=node.question_payload_sha256,
                status=node.status,
                rationale_sha256=node.rationale_sha256,
            )
            for node in manifest.nodes
        ),
        reconstructed_relations=(),
        reconstructed_current_focus_node_ids=manifest.current_focus_node_ids,
        reconstructed_next_step_node_ids=manifest.next_step_node_ids,
    )


def test_perfect_reconstruction_has_no_activation_overreach_or_omission() -> None:
    manifest = expected_manifest()
    observed = observation(manifest)
    diagnostics = diagnose_attention_structure_discriminants(manifest, observed)

    assert diagnostics.missing_focus_node_count == 0
    assert diagnostics.unexpected_focus_node_count == 0
    assert diagnostics.missing_next_step_node_count == 0
    assert diagnostics.unexpected_next_step_node_count == 0
    assert diagnostics.missing_open_question_node_count == 0
    assert diagnostics.unexpected_open_question_node_count == 0
    assert diagnostics.focus_status_mismatch_count == 0
    assert diagnostics.activation_overreach_node_ids == ()
    assert diagnostics.activation_omission_node_ids == ()
    assert diagnostics.discriminant_value == "NOT_ESTABLISHED"
    assert diagnostics.incremental_predictive_value == "NOT_ESTABLISHED"
    assert diagnostics.subjectivity == "NOT_ESTABLISHED"


def test_recall_style_focus_preservation_can_hide_false_positive_focus_activation() -> None:
    manifest = expected_manifest()
    observed = observation(manifest)
    overcomplete = replace(
        observed,
        reconstructed_current_focus_node_ids=("active", "open-not-next"),
    )

    legacy_audit = audit_attention_structure_reconstruction(manifest, overcomplete)
    diagnostics = diagnose_attention_structure_discriminants(manifest, overcomplete)

    assert legacy_audit.focus_preservation == 1.0
    assert legacy_audit.branch_reinflation_count == 0
    assert diagnostics.unexpected_focus_node_count == 1
    assert diagnostics.focus_status_mismatch_count == 1
    assert diagnostics.activation_overreach_node_ids == ("open-not-next",)


def test_recall_style_next_step_preservation_can_hide_extra_admissible_branch() -> None:
    manifest = expected_manifest()
    observed = observation(manifest)
    overcomplete = replace(
        observed,
        reconstructed_next_step_node_ids=("active", "open-not-next"),
    )

    legacy_audit = audit_attention_structure_reconstruction(manifest, overcomplete)
    diagnostics = diagnose_attention_structure_discriminants(manifest, overcomplete)

    assert legacy_audit.next_step_preservation == 1.0
    assert legacy_audit.branch_reinflation_count == 0
    assert diagnostics.unexpected_next_step_node_count == 1
    assert diagnostics.activation_overreach_node_ids == ("open-not-next",)


def test_blocked_branch_reopened_as_open_is_visible_without_calling_it_subjectivity() -> None:
    manifest = expected_manifest()
    observed = observation(manifest)
    reopened_nodes = tuple(
        replace(node, status=AttentionNodeStatus.OPEN_QUESTION)
        if node.node_id == "blocked"
        else node
        for node in observed.reconstructed_nodes
    )
    reopened = replace(observed, reconstructed_nodes=reopened_nodes)

    legacy_audit = audit_attention_structure_reconstruction(manifest, reopened)
    diagnostics = diagnose_attention_structure_discriminants(manifest, reopened)

    assert legacy_audit.branch_reinflation_count == 0
    assert diagnostics.unexpected_open_question_node_count == 1
    assert diagnostics.activation_overreach_node_ids == ("blocked",)
    assert diagnostics.discriminant_value == "NOT_ESTABLISHED"


def test_discriminant_diagnostic_fails_closed_on_manifest_binding_mismatch() -> None:
    manifest = expected_manifest()
    observed = observation(manifest)
    broken = replace(
        observed,
        binding=replace(observed.binding, expected_manifest_sha256=digest("0")),
    )

    with pytest.raises(StudyError, match="canonical manifest digest"):
        diagnose_attention_structure_discriminants(manifest, broken)
