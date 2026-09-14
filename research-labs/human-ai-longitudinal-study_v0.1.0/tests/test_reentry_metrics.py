from __future__ import annotations

from dataclasses import replace

import pytest

from aion_human_ai_longitudinal.reentry_metrics import (
    ReconstructionRecord,
    ReentryBinding,
    ReentryCondition,
    compare_reentry_conditions,
    score_reconstruction,
)
from aion_human_ai_longitudinal import StudyError


def digest(char: str) -> str:
    return char * 64


def binding(run_id: str, packet: str) -> ReentryBinding:
    return ReentryBinding(
        run_id=run_id,
        task_id="synthetic-reentry-task-v1",
        task_payload_sha256=digest("a"),
        packet_payload_sha256=digest(packet),
        evaluator_id="frozen-scorer-v1",
        evaluator_payload_sha256=digest("e"),
        repository_commit=digest("c"),
        preregistration_ref="docs/research/reentry-preregistration-v1",
        source_refs=("PR-93", "PR-102"),
    )


def record(condition: ReentryCondition) -> ReconstructionRecord:
    structured = condition is ReentryCondition.STRUCTURED_BOUNDARY_PACKET
    return ReconstructionRecord(
        binding=binding("structured" if structured else "unstructured", "b" if structured else "d"),
        condition=condition,
        expected_protocol_items=frozenset({"provenance", "unknown", "claim-ceiling", "correction"}),
        reconstructed_protocol_items=(
            frozenset({"provenance", "unknown", "claim-ceiling", "correction"})
            if structured
            else frozenset({"provenance", "correction"})
        ),
        expected_open_alternatives=frozenset({"search-convenience", "prompt-specificity"}),
        retained_open_alternatives=(
            frozenset({"search-convenience", "prompt-specificity"})
            if structured
            else frozenset({"search-convenience"})
        ),
        stale_claim_ids=frozenset() if structured else frozenset({"claim-7"}),
        provenance_error_ids=frozenset() if structured else frozenset({"claim-2"}),
    )


def test_scores_and_compares_preregistered_reentry_metrics() -> None:
    receipt = compare_reentry_conditions(
        record(ReentryCondition.UNSTRUCTURED_OUTPUT),
        record(ReentryCondition.STRUCTURED_BOUNDARY_PACKET),
    )
    assert receipt.baseline.protocol_reconstruction_fidelity == 0.5
    assert receipt.intervention.protocol_reconstruction_fidelity == 1.0
    assert dict(receipt.deltas) == {
        "protocol_reconstruction_fidelity": 0.5,
        "stale_claim_errors": -1.0,
        "provenance_errors": -1.0,
        "unresolved_alternative_retention": 0.5,
    }
    assert receipt.scientific_disposition.value == "HOLD"
    assert receipt.canonical_effect == "NONE"
    assert receipt.deployment is False
    assert receipt.mode == "DETERMINISTIC_SYNTHETIC_FIXTURE"
    assert receipt.model_invoked is False
    assert receipt.empirical_result == "SYNTHETIC_FIXTURE_ONLY"
    assert receipt.evidence_admissibility == "STRUCTURAL_QA_ONLY"
    assert receipt.causal_identification == "NOT_ESTABLISHED"
    assert receipt.population_generalization == "NOT_ESTABLISHED"
    assert receipt.subjectivity_conclusion == "NOT_ESTABLISHED"


@pytest.mark.parametrize(
    "field,value",
    [
        ("task_payload_sha256", digest("f")),
        ("evaluator_payload_sha256", digest("f")),
        ("repository_commit", digest("f")),
        ("source_refs", ("PR-93",)),
    ],
)
def test_uncontrolled_binding_drift_fails_closed(field: str, value: object) -> None:
    left = record(ReentryCondition.UNSTRUCTURED_OUTPUT)
    right = record(ReentryCondition.STRUCTURED_BOUNDARY_PACKET)
    right = replace(right, binding=replace(right.binding, **{field: value}))
    with pytest.raises(StudyError, match="binding drift"):
        compare_reentry_conditions(left, right)


def test_packet_label_without_distinct_content_binding_fails_closed() -> None:
    left = record(ReentryCondition.UNSTRUCTURED_OUTPUT)
    right = record(ReentryCondition.STRUCTURED_BOUNDARY_PACKET)
    right = replace(
        right,
        binding=replace(right.binding, packet_payload_sha256=left.binding.packet_payload_sha256),
    )
    with pytest.raises(StudyError, match="distinct content bindings"):
        compare_reentry_conditions(left, right)


def test_private_or_non_synthetic_record_is_rejected() -> None:
    with pytest.raises(StudyError, match="synthetic non-private"):
        replace(binding("run", "b"), contains_private_material=True)
    with pytest.raises(StudyError, match="synthetic non-private"):
        replace(binding("run", "b"), synthetic=False)


def test_scorer_vocabularies_fail_closed() -> None:
    item = record(ReentryCondition.UNSTRUCTURED_OUTPUT)
    with pytest.raises(StudyError, match="scorer-recognized"):
        replace(item, reconstructed_protocol_items=frozenset({"invented-item"}))
    with pytest.raises(StudyError, match="scorer-recognized"):
        replace(item, retained_open_alternatives=frozenset({"invented-alternative"}))


def test_raw_condition_and_invalid_hash_are_rejected() -> None:
    item = record(ReentryCondition.UNSTRUCTURED_OUTPUT)
    with pytest.raises(StudyError, match="exact ReentryCondition"):
        replace(item, condition="UNSTRUCTURED_OUTPUT")
    with pytest.raises(StudyError, match="SHA-256"):
        replace(item.binding, task_payload_sha256="reference-label-only")


def test_score_is_deterministic() -> None:
    item = record(ReentryCondition.UNSTRUCTURED_OUTPUT)
    assert score_reconstruction(item) == score_reconstruction(item)
