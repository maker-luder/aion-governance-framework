from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys


LAB_ROOT = Path(__file__).resolve().parents[1]
SRC = LAB_ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from aion_human_ai_longitudinal import (  # noqa: E402
    ALL_METRICS,
    ALL_TASK_FAMILIES,
    CollaborationCondition,
    CollaborationExperimentSpec,
    CollaborationMetricObservation,
    CollaborationRegimeHarness,
    CollaborationRun,
    ConditionPacket,
    CrossDyadRunBinding,
    RepositoryRelevance,
    SyntheticTask,
    SyntheticTaskFamily,
)


BASE_MAIN = "d95bc2625e71f1c85a725aaba78cb0feccfc0668"
SPEC_HEAD = "3ce4f759caf662a53f0d1f3a54709bc482d7df5e"
EXPERIMENT_ID = "AION-CROSS-DYAD-COLLABORATION-REGIME-001"
SPEC_REF = (
    "github:maker-luder/aion-governance-framework#102@"
    + SPEC_HEAD
    + ":CROSS_DYAD_COLLABORATION_REGIME_EXPERIMENT_EXTENSION_2026_09_13"
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_inputs() -> tuple[list[ConditionPacket], list[SyntheticTask], Path, Path]:
    packets_path = LAB_ROOT / "fixtures" / "cross_dyad_condition_packets.json"
    tasks_path = LAB_ROOT / "fixtures" / "cross_dyad_synthetic_tasks.json"
    packet_data = json.loads(packets_path.read_text(encoding="utf-8"))
    task_data = json.loads(tasks_path.read_text(encoding="utf-8"))
    if packet_data["specification_ref"] != SPEC_REF:
        raise ValueError("fixture specification_ref does not match exact PR #102 dependency")
    if task_data["contains_private_transcript"] or task_data["contains_third_party_identity"]:
        raise ValueError("synthetic task fixture privacy boundary changed")
    packets = [
        ConditionPacket(
            condition=CollaborationCondition(row["condition"]),
            instruction_ref=row["instruction_ref"],
            closure_rule_ref=row["closure_rule_ref"],
            repository_history_refs=tuple(row["repository_history_refs"]),
        )
        for row in packet_data["packets"]
    ]
    tasks = [
        SyntheticTask(
            task_id=row["task_id"],
            task_version=row["task_version"],
            family=SyntheticTaskFamily(row["family"]),
            prompt_ref=row["prompt_ref"],
            expected_anomaly=row["expected_anomaly"],
            repository_relevance=RepositoryRelevance(row["repository_relevance"]),
        )
        for row in task_data["tasks"]
    ]
    return packets, tasks, packets_path, tasks_path


def synthetic_value(task_index: int, condition_index: int, metric_index: int) -> float:
    """Deterministic fixture value with no empirical interpretation."""
    return round(((task_index * 17 + condition_index * 13 + metric_index * 7) % 101) / 100, 2)


def execute() -> dict[str, object]:
    packets, tasks, packets_path, tasks_path = load_inputs()
    spec = CollaborationExperimentSpec(
        experiment_id=EXPERIMENT_ID,
        specification_ref=SPEC_REF,
        required_conditions=tuple(packet.condition for packet in packets),
        required_task_families=ALL_TASK_FAMILIES,
        required_metrics=ALL_METRICS,
        falsifier=(
            "Matched conditions show no reproducible per-dimension difference beyond "
            "predeclared synthetic-control tolerance."
        ),
        alternative_explanations=(
            "prompt length",
            "instruction salience",
            "tool availability",
            "scorer sensitivity",
            "task-family imbalance",
            "repository packet relevance",
        ),
    )
    harness = CollaborationRegimeHarness()
    for task_index, task in enumerate(tasks):
        for condition_index, packet in enumerate(packets):
            metrics = tuple(
                CollaborationMetricObservation(
                    metric=metric,
                    value=synthetic_value(task_index, condition_index, metric_index),
                    unit="ratio",
                    evidence_refs=(
                        f"synthetic-score:{task.task_id}:{packet.condition.value}:{metric.value}",
                    ),
                )
                for metric_index, metric in enumerate(ALL_METRICS)
            )
            binding = CrossDyadRunBinding(
                run_id=f"{task.task_id}:{packet.condition.value}",
                experiment_id=EXPERIMENT_ID,
                provider_id="SYNTHETIC_NO_PROVIDER_CALL",
                model_id="SYNTHETIC_NO_MODEL_CALL",
                model_version="NOT_APPLICABLE",
                generation_config_ref="fixture:deterministic-score-generator-v1",
                task_id=task.task_id,
                task_version=task.task_version,
                tool_manifest_ref="fixture:no-live-tools-v1",
                scorer_ref="script:run_cross_dyad_synthetic.py@v1",
                preregistration_ref="spec:cross-dyad-pr102-exact-head",
                repository_commit=BASE_MAIN,
                random_seed=20260913,
                condition_packet_fingerprint=packet.fingerprint,
            )
            harness.add_run(
                CollaborationRun(
                    binding=binding,
                    task=task,
                    condition_packet=packet,
                    metrics=metrics,
                    event_refs=(f"synthetic-event:{binding.run_id}",),
                )
            )
    audit = harness.audit(spec)

    by_metric: dict[str, list[float]] = {metric.value: [] for metric in ALL_METRICS}
    for delta in audit.metric_deltas:
        by_metric[delta.metric.value].append(delta.delta)
    summaries = {
        metric: {
            "observations": len(values),
            "minimum_delta": round(min(values), 12),
            "maximum_delta": round(max(values), 12),
            "mean_delta": round(math.fsum(values) / len(values), 12),
        }
        for metric, values in by_metric.items()
    }
    return {
        "schema_version": "0.1.0",
        "experiment_id": audit.experiment_id,
        "mode": "DETERMINISTIC_SYNTHETIC_FIXTURE",
        "specification_dependency": {
            "pull_request": 102,
            "exact_head": SPEC_HEAD,
            "unmerged_dependency": True,
            "used_as_implementation_base": False,
            "reference": SPEC_REF,
        },
        "implementation_base": BASE_MAIN,
        "condition_count": len(packets),
        "task_family_count": len(tasks),
        "run_count": audit.run_count,
        "metrics_per_run": len(ALL_METRICS),
        "metric_delta_count": len(audit.metric_deltas),
        "condition_packet_sha256": digest(packets_path),
        "synthetic_task_sha256": digest(tasks_path),
        "structurally_admissible": audit.structurally_admissible,
        "metric_delta_summary": summaries,
        "reasons": list(audit.reasons),
        "model_invoked": False,
        "private_transcript_collected": False,
        "third_party_account_accessed": False,
        "psychometric_classification": False,
        "empirical_result": audit.empirical_result,
        "causal_identification": audit.causal_identification,
        "population_generalization": audit.population_generalization,
        "subjectivity_conclusion": audit.subjectivity_conclusion,
        "scientific_disposition": audit.scientific_disposition,
        "canonical_effect": audit.canonical_effect,
        "deployment": audit.deployment,
        "merge_authorization": "NONE",
        "main_write": "NO",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=LAB_ROOT / "results" / "cross_dyad_synthetic_receipt.json",
    )
    args = parser.parse_args(argv)
    result = execute()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    encoded = (json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8")
    args.output.write_bytes(encoded)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
