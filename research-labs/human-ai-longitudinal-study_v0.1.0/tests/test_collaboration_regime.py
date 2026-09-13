from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import runpy

import pytest

from aion_human_ai_longitudinal import (
    ALL_METRICS,
    ALL_TASK_FAMILIES,
    CORE_CONDITIONS,
    CollaborationCondition,
    CollaborationExperimentSpec,
    CollaborationMetric,
    CollaborationMetricObservation,
    CollaborationRegimeHarness,
    CollaborationRun,
    ConditionPacket,
    CrossDyadRunBinding,
    RepositoryRelevance,
    StudyError,
    SyntheticTask,
    SyntheticTaskFamily,
)


LAB_ROOT = Path(__file__).resolve().parents[1]
BASE = "d95bc2625e71f1c85a725aaba78cb0feccfc0668"


def packet(condition: CollaborationCondition) -> ConditionPacket:
    refs = (
        ("git:d95bc262:docs/CURRENT_STATE.md",)
        if condition is CollaborationCondition.RECIPROCAL_PROTOCOL_WITH_REPOSITORY_HISTORY
        else ()
    )
    return ConditionPacket(
        condition=condition,
        instruction_ref=f"instruction:{condition.value}",
        closure_rule_ref=f"closure:{condition.value}",
        instruction_payload=f"Execute bounded protocol for {condition.value}.",
        closure_rule_payload=f"Stop when evidence threshold for {condition.value} is met.",
        repository_history_refs=refs,
    )


def task(family: SyntheticTaskFamily) -> SyntheticTask:
    relevance = {
        SyntheticTaskFamily.REPOSITORY_RETRIEVAL_USEFUL: RepositoryRelevance.RELEVANT,
        SyntheticTaskFamily.REPOSITORY_RETRIEVAL_UNNECESSARY: RepositoryRelevance.IRRELEVANT,
    }.get(family, RepositoryRelevance.NOT_APPLICABLE)
    anomaly = family not in {
        SyntheticTaskFamily.SUFFICIENT_CLOSURE,
        SyntheticTaskFamily.FALSE_ANOMALY_CONTROL,
        SyntheticTaskFamily.IMPLEMENTATION_FEASIBILITY,
        SyntheticTaskFamily.REPOSITORY_RETRIEVAL_USEFUL,
        SyntheticTaskFamily.REPOSITORY_RETRIEVAL_UNNECESSARY,
    }
    return SyntheticTask(
        task_id=f"task:{family.value}",
        task_version="v1",
        family=family,
        prompt_ref=f"prompt:{family.value}",
        prompt_payload=f"Synthetic task payload for {family.value}.",
        expected_anomaly=anomaly,
        repository_relevance=relevance,
    )


def metric(name: CollaborationMetric, value: float = 0.5) -> CollaborationMetricObservation:
    return CollaborationMetricObservation(
        metric=name,
        value=value,
        unit="ratio",
        evidence_refs=(f"score:{name.value}",),
    )


def run(
    synthetic_task: SyntheticTask,
    condition: CollaborationCondition,
    *,
    value: float = 0.5,
) -> CollaborationRun:
    condition_packet = packet(condition)
    binding = CrossDyadRunBinding(
        run_id=f"{synthetic_task.task_id}:{condition.value}",
        experiment_id="experiment-001",
        provider_id="synthetic-provider",
        model_id="synthetic-model",
        model_version="none",
        generation_config_ref="config:matched",
        task_id=synthetic_task.task_id,
        task_version=synthetic_task.task_version,
        tool_manifest_ref="tools:matched",
        scorer_ref="scorer:matched",
        preregistration_ref="preregistration:001",
        repository_commit=BASE,
        random_seed=7,
        condition_packet_fingerprint=condition_packet.fingerprint,
        task_payload_fingerprint=synthetic_task.payload_fingerprint,
    )
    return CollaborationRun(
        binding=binding,
        task=synthetic_task,
        condition_packet=condition_packet,
        metrics=tuple(metric(name, value) for name in ALL_METRICS),
        event_refs=(f"event:{binding.run_id}",),
    )


def spec(
    *,
    conditions: tuple[CollaborationCondition, ...] = CORE_CONDITIONS,
    families: tuple[SyntheticTaskFamily, ...] = ALL_TASK_FAMILIES,
    metrics: tuple[CollaborationMetric, ...] = ALL_METRICS,
) -> CollaborationExperimentSpec:
    return CollaborationExperimentSpec(
        experiment_id="experiment-001",
        specification_ref="github:pr102@exact-head",
        required_conditions=conditions,
        required_task_families=families,
        required_metrics=metrics,
        falsifier="no matched per-dimension difference",
        alternative_explanations=("prompt length", "scorer sensitivity"),
    )


def complete_harness(
    conditions: tuple[CollaborationCondition, ...] = CORE_CONDITIONS,
) -> CollaborationRegimeHarness:
    harness = CollaborationRegimeHarness()
    for synthetic_task in map(task, ALL_TASK_FAMILIES):
        for index, condition in enumerate(conditions):
            harness.add_run(run(synthetic_task, condition, value=0.5 + index / 10))
    return harness


def test_complete_a_to_d_matrix_preserves_per_dimension_results_and_hold() -> None:
    audit = complete_harness().audit(spec())
    assert audit.structurally_admissible is True
    assert audit.run_count == len(ALL_TASK_FAMILIES) * len(CORE_CONDITIONS)
    assert len(audit.metric_deltas) == (
        len(ALL_TASK_FAMILIES) * (len(CORE_CONDITIONS) - 1) * len(ALL_METRICS)
    )
    assert audit.empirical_result == "SYNTHETIC_FIXTURE_ONLY"
    assert audit.causal_identification == "NOT_ESTABLISHED"
    assert audit.population_generalization == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.scientific_disposition == "HOLD"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_optional_condition_e_is_admitted_without_becoming_required_core() -> None:
    conditions = CORE_CONDITIONS + (
        CollaborationCondition.CLOSURE_CONSTRAINED_CONTROL,
    )
    audit = complete_harness(conditions).audit(spec(conditions=conditions))
    assert audit.run_count == len(ALL_TASK_FAMILIES) * 5


def test_conditions_a_to_d_and_all_task_families_are_mandatory() -> None:
    with pytest.raises(StudyError, match="conditions A-D"):
        spec(conditions=CORE_CONDITIONS[:-1])
    with pytest.raises(StudyError, match="all nine"):
        spec(families=ALL_TASK_FAMILIES[:-1])


def test_all_metrics_are_required_and_no_composite_metric_exists() -> None:
    with pytest.raises(StudyError, match="all observable metrics"):
        spec(metrics=ALL_METRICS[:-1])
    assert "BETTER_COLLABORATION" not in CollaborationMetric.__members__
    assert "COMPOSITE_SCORE" not in CollaborationMetric.__members__


def test_missing_matrix_cell_fails_closed() -> None:
    harness = complete_harness()
    harness._runs.pop((task(ALL_TASK_FAMILIES[0]).task_id, CORE_CONDITIONS[0]))
    with pytest.raises(StudyError, match="matrix mismatch"):
        harness.audit(spec())


def test_model_or_tool_drift_fails_closed() -> None:
    harness = complete_harness()
    key = (task(ALL_TASK_FAMILIES[0]).task_id, CORE_CONDITIONS[1])
    changed = harness._runs[key]
    harness._runs[key] = replace(
        changed,
        binding=replace(changed.binding, model_version="drifted"),
    )
    with pytest.raises(StudyError, match="model_version"):
        harness.audit(spec())


def test_condition_d_requires_history_and_other_conditions_reject_it() -> None:
    with pytest.raises(StudyError, match="condition D requires"):
        ConditionPacket(
            CollaborationCondition.RECIPROCAL_PROTOCOL_WITH_REPOSITORY_HISTORY,
            "instruction",
            "closure",
            "instruction payload",
            "closure payload",
        )
    with pytest.raises(StudyError, match="only condition D"):
        ConditionPacket(
            CollaborationCondition.RECIPROCAL_EPISTEMIC_PROTOCOL,
            "instruction",
            "closure",
            "instruction payload",
            "closure payload",
            ("history:unexpected",),
        )


def test_private_transcript_or_third_party_identity_is_rejected() -> None:
    baseline = run(task(ALL_TASK_FAMILIES[0]), CORE_CONDITIONS[0])
    with pytest.raises(StudyError, match="private or identity"):
        replace(baseline, contains_private_transcript=True)
    with pytest.raises(StudyError, match="private or identity"):
        replace(baseline, contains_third_party_identity=True)


@pytest.mark.parametrize("value", (True, False, "0.5", None, float("nan"), float("inf")))
def test_metric_values_reject_bool_non_numeric_and_non_finite(value: object) -> None:
    with pytest.raises(StudyError, match="finite exact"):
        CollaborationMetricObservation(
            metric=CollaborationMetric.ANOMALY_DETECTION,
            value=value,
            unit="ratio",
            evidence_refs=("score:invalid",),
        )


def test_raw_enum_and_condition_packet_fingerprint_drift_fail_closed() -> None:
    with pytest.raises(StudyError, match="exact CollaborationCondition"):
        ConditionPacket(
            "CONDITION_A_NEUTRAL_TASK_COMPLETION",
            "instruction",
            "closure",
            "instruction payload",
            "closure payload",
        )
    baseline = run(task(ALL_TASK_FAMILIES[0]), CORE_CONDITIONS[0])
    with pytest.raises(StudyError, match="fingerprint mismatch"):
        replace(
            baseline,
            binding=replace(baseline.binding, condition_packet_fingerprint="0" * 64),
        )


def test_actual_condition_and_closure_payloads_are_immutably_bound() -> None:
    baseline = run(task(ALL_TASK_FAMILIES[0]), CORE_CONDITIONS[0])
    with pytest.raises(StudyError, match="condition packet fingerprint mismatch"):
        replace(
            baseline,
            condition_packet=replace(
                baseline.condition_packet,
                instruction_payload=baseline.condition_packet.instruction_payload + " tampered",
            ),
        )
    with pytest.raises(StudyError, match="condition packet fingerprint mismatch"):
        replace(
            baseline,
            condition_packet=replace(
                baseline.condition_packet,
                closure_rule_payload=baseline.condition_packet.closure_rule_payload + " tampered",
            ),
        )


def test_actual_task_payload_is_immutably_bound() -> None:
    baseline = run(task(ALL_TASK_FAMILIES[0]), CORE_CONDITIONS[0])
    with pytest.raises(StudyError, match="task payload fingerprint mismatch"):
        replace(
            baseline,
            task=replace(baseline.task, prompt_payload=baseline.task.prompt_payload + " tampered"),
        )


def test_repository_task_relevance_and_negative_controls_are_bound() -> None:
    with pytest.raises(StudyError, match="relevance disagree"):
        SyntheticTask(
            "task:bad-relevance",
            "v1",
            SyntheticTaskFamily.REPOSITORY_RETRIEVAL_USEFUL,
            "prompt:bad",
            "bad prompt payload",
            False,
            RepositoryRelevance.IRRELEVANT,
        )
    with pytest.raises(StudyError, match="negative-control"):
        SyntheticTask(
            "task:false-anomaly",
            "v1",
            SyntheticTaskFamily.FALSE_ANOMALY_CONTROL,
            "prompt:false-anomaly",
            "false anomaly prompt payload",
            True,
            RepositoryRelevance.NOT_APPLICABLE,
        )


def test_committed_execution_receipt_matches_fixture_inputs() -> None:
    receipt_path = LAB_ROOT / "results" / "cross_dyad_synthetic_receipt.json"
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    namespace = runpy.run_path(str(LAB_ROOT / "scripts" / "run_cross_dyad_synthetic.py"))
    regenerated = namespace["execute"]()
    assert receipt == regenerated
    for name, key in (
        ("cross_dyad_condition_packets.json", "condition_packet_sha256"),
        ("cross_dyad_synthetic_tasks.json", "synthetic_task_sha256"),
    ):
        payload = (LAB_ROOT / "fixtures" / name).read_bytes()
        assert receipt[key] == hashlib.sha256(payload).hexdigest()
    assert receipt["model_invoked"] is False
    assert receipt["private_transcript_collected"] is False
    assert receipt["third_party_account_accessed"] is False
    assert receipt["scientific_disposition"] == "HOLD"
    assert receipt["canonical_effect"] == "NONE"
    assert receipt["implementation_base"] == {
        "commit_sha": BASE,
        "tree_sha": "77470062979df1db2f17c3a2a396891d1e910f98",
    }
