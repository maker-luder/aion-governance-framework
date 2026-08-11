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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FixtureProvenance":
        return cls(
            fixture_author=str(data["fixture_author"]),
            fixture_version=str(data["fixture_version"]),
            fixture_hash=str(data["fixture_hash"]),
            experiment_run=str(data["experiment_run"]),
            implementation_version=str(data["implementation_version"]),
            seed=int(data["seed"]),
            mode=ReplicationMode(data["mode"]),
        )


class ReplicationOutcome(str, Enum):
    CONFIRMED = "CONFIRMED"
    FAILED = "FAILED"
    MIXED = "MIXED"
    INCONCLUSIVE = "INCONCLUSIVE"


class ReplicationValidity(str, Enum):
    VALID = "VALID"
    PARTIALLY_VALID = "PARTIALLY_VALID"
    INVALID = "INVALID"
    UNRESOLVED = "UNRESOLVED"


class ReplicationInterpretation(str, Enum):
    VALID_CONTRADICTION = "VALID_CONTRADICTION"
    BOUNDARY_CONDITION_DISCOVERED = "BOUNDARY_CONDITION_DISCOVERED"
    METHOD_MISMATCH = "METHOD_MISMATCH"
    IMPLEMENTATION_MISMATCH = "IMPLEMENTATION_MISMATCH"
    EVALUATOR_DRIFT = "EVALUATOR_DRIFT"
    FIXTURE_MISMATCH = "FIXTURE_MISMATCH"
    INSUFFICIENT_POWER_OR_SAMPLE = "INSUFFICIENT_POWER_OR_SAMPLE"
    PROVENANCE_FAILURE = "PROVENANCE_FAILURE"
    UNRESOLVED = "UNRESOLVED"


def _require_nonempty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


@dataclass(frozen=True, slots=True)
class ReplicationAttempt:
    attempt_id: str
    claim_ref: str
    fixture_ref: str
    fixture: FixtureProvenance
    protocol_ref: str
    protocol_version: str
    implementation_ref: str
    implementation_version: str
    evaluator_ref: str
    evaluator_version: str
    evaluation_contract_ref: str
    independent_group_ref: str
    seed: int
    outcome: ReplicationOutcome
    validity: ReplicationValidity
    provenance_refs: tuple[str, ...]
    executed_at: str
    observation_ref: str
    preregistered: bool = False

    def __post_init__(self) -> None:
        for name, value in (
            ("attempt_id", self.attempt_id),
            ("claim_ref", self.claim_ref),
            ("fixture_ref", self.fixture_ref),
            ("protocol_ref", self.protocol_ref),
            ("protocol_version", self.protocol_version),
            ("implementation_ref", self.implementation_ref),
            ("implementation_version", self.implementation_version),
            ("evaluator_ref", self.evaluator_ref),
            ("evaluator_version", self.evaluator_version),
            ("evaluation_contract_ref", self.evaluation_contract_ref),
            ("independent_group_ref", self.independent_group_ref),
            ("executed_at", self.executed_at),
            ("observation_ref", self.observation_ref),
        ):
            _require_nonempty(name, value)
        if self.fixture.implementation_version != self.implementation_version:
            raise ValueError("attempt implementation_version must match fixture provenance")
        if self.fixture.seed != self.seed:
            raise ValueError("attempt seed must match fixture provenance")
        if not self.provenance_refs or any(not item.strip() for item in self.provenance_refs):
            raise ValueError("replication attempt provenance_refs must be non-empty")

    @property
    def fixture_hash(self) -> str:
        return self.fixture.fixture_hash.lower()

    @property
    def is_independent_replication(self) -> bool:
        return self.fixture.mode is ReplicationMode.REPLICATION

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "claim_ref": self.claim_ref,
            "fixture_ref": self.fixture_ref,
            "fixture_hash": self.fixture_hash,
            "fixture": self.fixture.to_dict(),
            "protocol_ref": self.protocol_ref,
            "protocol_version": self.protocol_version,
            "implementation_ref": self.implementation_ref,
            "implementation_version": self.implementation_version,
            "evaluator_ref": self.evaluator_ref,
            "evaluator_version": self.evaluator_version,
            "evaluation_contract_ref": self.evaluation_contract_ref,
            "independent_group_ref": self.independent_group_ref,
            "seed": self.seed,
            "outcome": self.outcome.value,
            "validity": self.validity.value,
            "provenance_refs": list(self.provenance_refs),
            "executed_at": self.executed_at,
            "observation_ref": self.observation_ref,
            "preregistered": self.preregistered,
        }

    def to_json(self) -> str:
        return json.dumps(
            {"schema": "aion.replication-attempt.v1", "attempt": self.to_dict()},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReplicationAttempt":
        fixture = FixtureProvenance.from_dict(data["fixture"])
        if str(data["fixture_hash"]).lower() != fixture.fixture_hash.lower():
            raise ValueError("serialized fixture_hash must match fixture provenance")
        return cls(
            attempt_id=str(data["attempt_id"]),
            claim_ref=str(data["claim_ref"]),
            fixture_ref=str(data["fixture_ref"]),
            fixture=fixture,
            protocol_ref=str(data["protocol_ref"]),
            protocol_version=str(data["protocol_version"]),
            implementation_ref=str(data["implementation_ref"]),
            implementation_version=str(data["implementation_version"]),
            evaluator_ref=str(data["evaluator_ref"]),
            evaluator_version=str(data["evaluator_version"]),
            evaluation_contract_ref=str(data["evaluation_contract_ref"]),
            independent_group_ref=str(data["independent_group_ref"]),
            seed=int(data["seed"]),
            outcome=ReplicationOutcome(data["outcome"]),
            validity=ReplicationValidity(data["validity"]),
            provenance_refs=tuple(data["provenance_refs"]),
            executed_at=str(data["executed_at"]),
            observation_ref=str(data["observation_ref"]),
            preregistered=bool(data["preregistered"]),
        )

    @classmethod
    def from_json(cls, payload: str) -> "ReplicationAttempt":
        data = json.loads(payload)
        if not isinstance(data, dict) or data.get("schema") != "aion.replication-attempt.v1":
            raise ValueError("unsupported replication attempt schema")
        return cls.from_dict(data["attempt"])


@dataclass(frozen=True, slots=True)
class ReplicationAssessment:
    assessment_id: str
    attempt_ref: str
    interpretation: ReplicationInterpretation
    reason: str
    evaluator_ref: str
    evaluator_version: str
    evaluation_contract_ref: str
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name, value in (
            ("assessment_id", self.assessment_id),
            ("attempt_ref", self.attempt_ref),
            ("reason", self.reason),
            ("evaluator_ref", self.evaluator_ref),
            ("evaluator_version", self.evaluator_version),
            ("evaluation_contract_ref", self.evaluation_contract_ref),
        ):
            _require_nonempty(name, value)
        if not self.provenance_refs:
            raise ValueError("replication assessment provenance_refs must be non-empty")


@dataclass(frozen=True, slots=True)
class ReplicationRecord:
    record_id: str
    attempt_count: int
    confirmed_count: int
    failed_count: int
    mixed_count: int
    inconclusive_count: int
    independent_group_count: int
    attempt_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    automatic_evidence_level_override: str = "NONE"

    @classmethod
    def from_attempts(
        cls,
        record_id: str,
        attempts: Iterable[ReplicationAttempt],
        *,
        provenance_refs: tuple[str, ...],
    ) -> "ReplicationRecord":
        items = tuple(attempts)
        _require_nonempty("record_id", record_id)
        if not items or not provenance_refs:
            raise ValueError("replication record requires attempts and provenance")
        if len({item.attempt_id for item in items}) != len(items):
            raise ValueError("replication attempt_id must be unique")
        independent_groups = {
            item.independent_group_ref for item in items if item.is_independent_replication
        }
        return cls(
            record_id=record_id,
            attempt_count=len(items),
            confirmed_count=sum(item.outcome is ReplicationOutcome.CONFIRMED for item in items),
            failed_count=sum(item.outcome is ReplicationOutcome.FAILED for item in items),
            mixed_count=sum(item.outcome is ReplicationOutcome.MIXED for item in items),
            inconclusive_count=sum(
                item.outcome is ReplicationOutcome.INCONCLUSIVE for item in items
            ),
            independent_group_count=len(independent_groups),
            attempt_refs=tuple(item.attempt_id for item in items),
            provenance_refs=provenance_refs,
        )


class ReplicationRunner:
    """Aggregate registered raw attempts without rerunning, filtering, or promotion."""

    def __init__(self) -> None:
        self._attempts: list[ReplicationAttempt] = []

    @property
    def attempts(self) -> tuple[ReplicationAttempt, ...]:
        return tuple(self._attempts)

    def register(self, attempt: ReplicationAttempt) -> None:
        if any(item.attempt_id == attempt.attempt_id for item in self._attempts):
            raise ValueError("replication attempt_id must be unique")
        self._attempts.append(attempt)

    def record(
        self, record_id: str, *, provenance_refs: tuple[str, ...]
    ) -> ReplicationRecord:
        return ReplicationRecord.from_attempts(
            record_id, self._attempts, provenance_refs=provenance_refs
        )


def evaluator_drift_detected(
    left: ReplicationAttempt, right: ReplicationAttempt
) -> bool:
    comparable_substrate = (
        left.fixture_hash == right.fixture_hash
        and left.implementation_ref == right.implementation_ref
        and left.implementation_version == right.implementation_version
        and left.evaluation_contract_ref == right.evaluation_contract_ref
    )
    evaluator_changed = (
        left.evaluator_ref != right.evaluator_ref
        or left.evaluator_version != right.evaluator_version
    )
    return comparable_substrate and evaluator_changed and left.outcome is not right.outcome


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
