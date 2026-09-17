from __future__ import annotations

from dataclasses import dataclass

from .attention_structure_reconstruction import (
    AttentionNodeStatus,
    AttentionReconstructionObservation,
    AttentionStructureManifest,
    digest_attention_structure_manifest,
)
from .harness import StudyError


@dataclass(frozen=True, slots=True)
class AttentionDiscriminantDiagnostics:
    run_id: str
    missing_focus_node_count: int
    unexpected_focus_node_count: int
    missing_next_step_node_count: int
    unexpected_next_step_node_count: int
    missing_open_question_node_count: int
    unexpected_open_question_node_count: int
    focus_status_mismatch_count: int
    activation_overreach_node_ids: tuple[str, ...]
    activation_omission_node_ids: tuple[str, ...]
    mode: str = "DETERMINISTIC_SYNTHETIC_DIAGNOSTIC"
    empirical_data_collected: bool = False
    discriminant_value: str = "NOT_ESTABLISHED"
    incremental_predictive_value: str = "NOT_ESTABLISHED"
    causal_identification: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False


def diagnose_attention_structure_discriminants(
    expected: AttentionStructureManifest,
    observed: AttentionReconstructionObservation,
) -> AttentionDiscriminantDiagnostics:
    """Expose false-positive activation that recall-style preservation can hide.

    This is a structural diagnostic only. It does not establish that ATTENTION_STRUCTURE
    is scientifically distinct from memory, re-entry, CCTS, goal resumption, or other
    adjacent constructs.
    """

    if type(expected) is not AttentionStructureManifest:
        raise StudyError("expected must be an exact AttentionStructureManifest")
    if type(observed) is not AttentionReconstructionObservation:
        raise StudyError("observed must be an exact AttentionReconstructionObservation")

    binding = observed.binding
    if binding.expected_manifest_sha256 != digest_attention_structure_manifest(expected):
        raise StudyError("expected manifest binding does not match canonical manifest digest")
    if binding.repository_commit != expected.repository_commit:
        raise StudyError("binding repository_commit must match expected manifest repository_commit")

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
    observed_active_by_status = {
        node.node_id
        for node in observed.reconstructed_nodes
        if node.status is AttentionNodeStatus.ACTIVE_FOCUS
    }

    missing_focus = expected_focus - observed_focus
    unexpected_focus = observed_focus - expected_focus
    missing_next = expected_next - observed_next
    unexpected_next = observed_next - expected_next
    missing_open = expected_open - observed_open
    unexpected_open = observed_open - expected_open

    activation_overreach = unexpected_focus | unexpected_next | unexpected_open
    activation_omission = missing_focus | missing_next | missing_open
    focus_status_mismatch = observed_focus ^ observed_active_by_status

    return AttentionDiscriminantDiagnostics(
        run_id=binding.run_id,
        missing_focus_node_count=len(missing_focus),
        unexpected_focus_node_count=len(unexpected_focus),
        missing_next_step_node_count=len(missing_next),
        unexpected_next_step_node_count=len(unexpected_next),
        missing_open_question_node_count=len(missing_open),
        unexpected_open_question_node_count=len(unexpected_open),
        focus_status_mismatch_count=len(focus_status_mismatch),
        activation_overreach_node_ids=tuple(sorted(activation_overreach)),
        activation_omission_node_ids=tuple(sorted(activation_omission)),
    )
