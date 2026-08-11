from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable

from aion_self_model_ablation import Task, default_benchmark_tasks

from .intervention import InterventionConditionResult, run_intervention_condition
from .records import OutcomeContract
from .verification import (
    InterventionPolicy,
    ProviderReliabilityProfile,
    VerificationInterventionCondition,
)


class ReplicationMode(str, Enum):
    REPRODUCTION = "REPRODUCTION"
    REPLICATION = "REPLICATION"


@dataclass(frozen=True, slots=True)
class FixtureProvenance:
    fixture_author: str
    fixture_version: str
    fixture_hash: str
    experiment_run: str
    implementation_version: str
    seed: int
    mode: ReplicationMode

    def __post_init__(self) -> None:
        for name, value in (
            ("fixture_author", self.fixture_author),
            ("fixture_version", self.fixture_version),
            ("experiment_run", self.experiment_run),
            ("implementation_version", self.implementation_version),
        ):
            if not value.strip():
                raise ValueError(f"{name} must be non-empty")
        digest = self.fixture_hash.lower()
        if len(digest) != 64 or any(char not in "0123456789abcdef" for char in digest):
            raise ValueError("fixture_hash must be a SHA-256 hex digest")

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_author": self.fixture_author,
            "fixture_version": self.fixture_version,
            "fixture_hash": self.fixture_hash.lower(),
            "experiment_run": self.experiment_run,
            "implementation_version": self.implementation_version,
            "seed": self.seed,
            "mode": self.mode.value,
        }


@dataclass(frozen=True, slots=True)
class FactorialCell:
    threshold: float
    intervention_condition: VerificationInterventionCondition
    result: InterventionConditionResult


@dataclass(frozen=True, slots=True)
class ThresholdInterventionFactorial:
    cells: tuple[FactorialCell, ...]
    thresholds: tuple[float, ...]
    conditions: tuple[VerificationInterventionCondition, ...]
    same_task_stream: bool
    same_first_order_model: bool
    same_latent_capability: bool
    same_base_task_difficulty: bool
    same_outcome_contract: bool
    same_provider_reliability_profile: bool
    same_random_seed_policy: bool
    status: str = "SUBSTRATE_IMPLEMENTED_FULL_STUDY_DEFERRED_TO_EXPERIMENT"
    optimization: str = "NONE"
    winner: str = "NONE"

    def raw_matrix(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            {
                "threshold": cell.threshold,
                "condition": cell.intervention_condition.value,
                "verification_requests": cell.result.verification_diagnostics.verification_requests,
                "interventions_applied": cell.result.intervention_diagnostics.interventions_applied,
                "prevented_failed_commit": cell.result.intervention_diagnostics.prevented_failed_commit,
                "unnecessary_defer": cell.result.intervention_diagnostics.unnecessary_defer,
                "verification_cost_units": cell.result.intervention_diagnostics.verification_cost_units,
                "intervention_cost_units": cell.result.intervention_diagnostics.intervention_cost_units,
                "synthetic_latency_steps": cell.result.intervention_diagnostics.synthetic_latency_steps,
            }
            for cell in self.cells
        )

    def to_json(self) -> str:
        return json.dumps(
            {
                "schema": "aion.threshold-intervention-factorial.v1",
                "status": self.status,
                "optimization": self.optimization,
                "winner": self.winner,
                "thresholds": list(self.thresholds),
                "conditions": [item.value for item in self.conditions],
                "invariants": {
                    "same_task_stream": self.same_task_stream,
                    "same_first_order_model": self.same_first_order_model,
                    "same_latent_capability": self.same_latent_capability,
                    "same_base_task_difficulty": self.same_base_task_difficulty,
                    "same_outcome_contract": self.same_outcome_contract,
                    "same_provider_reliability_profile": self.same_provider_reliability_profile,
                    "same_random_seed_policy": self.same_random_seed_policy,
                },
                "raw_matrix": self.raw_matrix(),
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )


def build_threshold_intervention_factorial(
    *,
    thresholds: Iterable[float] = (0.50, 0.60, 0.70, 0.75, 0.80, 0.90),
    conditions: Iterable[VerificationInterventionCondition] = tuple(
        VerificationInterventionCondition
    ),
    tasks: Iterable[Task] | None = None,
    latent_capability: float = 0.62,
    outcome_contract: OutcomeContract = OutcomeContract.EXTERNAL_BENCHMARK_FULL_LABELS,
    provider_profile: ProviderReliabilityProfile | None = None,
    provider_sampling_seed: int = 101,
    intervention_seed: int = 41,
    policy: InterventionPolicy | None = None,
) -> ThresholdInterventionFactorial:
    threshold_grid = tuple(float(item) for item in thresholds)
    condition_grid = tuple(conditions)
    if not threshold_grid or any(not 0.0 <= item <= 1.0 for item in threshold_grid):
        raise ValueError("threshold grid must contain values within [0,1]")
    if not condition_grid:
        raise ValueError("condition grid must be non-empty")
    task_stream = tuple(default_benchmark_tasks() if tasks is None else tasks)
    cells = tuple(
        FactorialCell(
            threshold,
            condition,
            run_intervention_condition(
                condition,
                task_stream,
                latent_capability=latent_capability,
                verification_threshold=threshold,
                random_seed=intervention_seed,
                outcome_contract=outcome_contract,
                provider_profile=provider_profile,
                provider_sampling_seed=provider_sampling_seed,
                policy=policy,
            ),
        )
        for threshold in threshold_grid
        for condition in condition_grid
    )
    task_ids = {
        tuple(record.trial_id for record in cell.result.records) for cell in cells
    }
    first_order_models = {
        tuple(record.model_ref for record in cell.result.records) for cell in cells
    }
    difficulties = {
        tuple(record.difficulty for record in cell.result.records) for cell in cells
    }
    profiles = {cell.result.provider_profile_ref for cell in cells}
    return ThresholdInterventionFactorial(
        cells=cells,
        thresholds=threshold_grid,
        conditions=condition_grid,
        same_task_stream=len(task_ids) == 1,
        same_first_order_model=len(first_order_models) == 1,
        same_latent_capability=True,
        same_base_task_difficulty=len(difficulties) == 1,
        same_outcome_contract=True,
        same_provider_reliability_profile=len(profiles) == 1,
        same_random_seed_policy=True,
    )
