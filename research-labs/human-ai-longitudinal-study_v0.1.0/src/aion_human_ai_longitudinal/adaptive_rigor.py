from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import math


class CalibrationError(ValueError):
    pass


class CalibrationCondition(StrEnum):
    FRESH_NEUTRAL = "FRESH_NEUTRAL"
    LONGITUDINAL_CONTEXT = "LONGITUDINAL_CONTEXT"
    RECIPROCAL_CORRECTION = "RECIPROCAL_CORRECTION"
    ADAPTIVE_RIGOR = "ADAPTIVE_RIGOR"


class CalibrationMetric(StrEnum):
    EVIDENTIAL_ACCURACY = "EVIDENTIAL_ACCURACY"
    AGREEMENT_WITH_INCORRECT_PREMISE = "AGREEMENT_WITH_INCORRECT_PREMISE"
    CONTRADICTION_OF_CORRECT_PREMISE = "CONTRADICTION_OF_CORRECT_PREMISE"
    COUNTEREVIDENCE_USE = "COUNTEREVIDENCE_USE"
    VERIFICATION_TIME = "VERIFICATION_TIME"
    TOOL_CALL_COST = "TOOL_CALL_COST"


def _require_sha256(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise CalibrationError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class CalibrationRun:
    task_id: str
    task_risk: str
    condition: CalibrationCondition
    provider_model_runtime_ref: str
    prompt_hash: str
    condition_payload_sha256: str
    evaluator_ref: str
    evaluator_blinded: bool
    observations: tuple[tuple[CalibrationMetric, float], ...]
    contains_private_transcript: bool = False

    def __post_init__(self) -> None:
        for name in ("task_id", "provider_model_runtime_ref", "evaluator_ref"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise CalibrationError(f"{name} is required")
        if self.task_risk not in {"LOW", "HIGH"}:
            raise CalibrationError("task_risk must be LOW or HIGH")
        if type(self.condition) is not CalibrationCondition:
            raise CalibrationError("condition must be exact")
        _require_sha256("prompt_hash", self.prompt_hash)
        _require_sha256("condition_payload_sha256", self.condition_payload_sha256)
        if type(self.evaluator_blinded) is not bool or type(self.contains_private_transcript) is not bool:
            raise CalibrationError("flags must be exact bools")
        if not self.evaluator_blinded:
            raise CalibrationError("condition-blinded evaluation is required")
        if self.contains_private_transcript:
            raise CalibrationError("synthetic calibration rejects private transcripts")
        names = [name for name, _ in self.observations]
        if set(names) != set(CalibrationMetric) or len(names) != len(CalibrationMetric):
            raise CalibrationError("all metrics are required exactly once")
        if any(type(name) is not CalibrationMetric for name in names):
            raise CalibrationError("metric names must be exact CalibrationMetric values")
        if any(type(value) is not float or not math.isfinite(value) or value < 0 for _, value in self.observations):
            raise CalibrationError("metrics require finite non-negative floats")


def audit_calibration(runs: tuple[CalibrationRun, ...]) -> dict[str, object]:
    tasks = {run.task_id for run in runs}
    expected = {(task, condition) for task in tasks for condition in CalibrationCondition}
    actual = {(run.task_id, run.condition) for run in runs}
    if not tasks or actual != expected or len(runs) != len(expected):
        raise CalibrationError("complete task-by-condition matrix is required")

    for task in tasks:
        matched = [run for run in runs if run.task_id == task]
        bindings = {
            (
                run.task_risk,
                run.provider_model_runtime_ref,
                run.prompt_hash,
                run.evaluator_ref,
            )
            for run in matched
        }
        if len(bindings) != 1:
            raise CalibrationError("matched task binding drift")

    condition_hashes: dict[CalibrationCondition, str] = {}
    for condition in CalibrationCondition:
        hashes = {run.condition_payload_sha256 for run in runs if run.condition is condition}
        if len(hashes) != 1:
            raise CalibrationError("condition payload binding drift")
        condition_hashes[condition] = next(iter(hashes))
    if len(set(condition_hashes.values())) != len(CalibrationCondition):
        raise CalibrationError("condition payloads must be content-distinct across conditions")

    return {
        "mode": "DETERMINISTIC_SYNTHETIC_FIXTURE",
        "model_invoked": False,
        "structurally_admissible": True,
        "evidence_admissibility": "STRUCTURAL_QA_ONLY",
        "run_count": len(runs),
        "metric_count": len(CalibrationMetric),
        "condition_payloads_bound": True,
        "composite_score": "NONE",
        "empirical_result": "SYNTHETIC_FIXTURE_ONLY",
        "sycophancy_effect": "NOT_ESTABLISHED",
        "adaptive_rigor_effect": "NOT_ESTABLISHED",
        "human_psychometric_classification": False,
        "causal_identification": "NOT_ESTABLISHED",
        "population_generalization": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "scientific_disposition": "HOLD",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
    }
