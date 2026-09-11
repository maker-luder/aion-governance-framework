from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryCandidate:
    memory_id: str
    task_utility: float
    relational_value: float
    correction_value: float
    continuity_value: float
    user_declared_significance: float


SIGNAL_FIELDS = (
    "task_utility",
    "relational_value",
    "correction_value",
    "continuity_value",
    "user_declared_significance",
)


def validate(candidate: MemoryCandidate) -> None:
    for field_name in SIGNAL_FIELDS:
        value = getattr(candidate, field_name)
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{field_name} must be between 0 and 1")


def utility_only_score(candidate: MemoryCandidate) -> float:
    validate(candidate)
    return candidate.task_utility


def multi_signal_contextual_score(candidate: MemoryCandidate) -> float:
    validate(candidate)
    return max(getattr(candidate, field_name) for field_name in SIGNAL_FIELDS)


def select_memories(
    candidates: list[MemoryCandidate],
    budget: int,
    score_fn: Callable[[MemoryCandidate], float],
) -> list[str]:
    if budget < 1 or budget > len(candidates):
        raise ValueError("budget must be between 1 and the number of candidates")

    ranked = sorted(
        candidates,
        key=lambda candidate: (-score_fn(candidate), candidate.memory_id),
    )
    return [candidate.memory_id for candidate in ranked[:budget]]


def fixture() -> list[MemoryCandidate]:
    return [
        MemoryCandidate(
            memory_id="frequent_task_anchor",
            task_utility=0.95,
            relational_value=0.10,
            correction_value=0.10,
            continuity_value=0.10,
            user_declared_significance=0.10,
        ),
        MemoryCandidate(
            memory_id="frequent_task_secondary",
            task_utility=0.90,
            relational_value=0.10,
            correction_value=0.10,
            continuity_value=0.10,
            user_declared_significance=0.10,
        ),
        MemoryCandidate(
            memory_id="rare_relational_anchor",
            task_utility=0.15,
            relational_value=0.98,
            correction_value=0.92,
            continuity_value=0.96,
            user_declared_significance=0.99,
        ),
        MemoryCandidate(
            memory_id="low_signal_noise",
            task_utility=0.05,
            relational_value=0.05,
            correction_value=0.05,
            continuity_value=0.05,
            user_declared_significance=0.05,
        ),
    ]


def run() -> dict[str, object]:
    candidates = fixture()
    budget = 2

    utility_only = select_memories(candidates, budget, utility_only_score)
    contextual = select_memories(candidates, budget, multi_signal_contextual_score)
    relational_anchor = "rare_relational_anchor"

    assert utility_only == ["frequent_task_anchor", "frequent_task_secondary"]
    assert contextual == ["rare_relational_anchor", "frequent_task_anchor"]
    assert relational_anchor not in utility_only
    assert relational_anchor in contextual

    return {
        "experiment": "memory-value-divergence-probe_v0.1.0",
        "fixture_type": "SYNTHETIC",
        "retention_budget": budget,
        "utility_only_selected": utility_only,
        "multi_signal_contextual_selected": contextual,
        "selection_divergence": utility_only != contextual,
        "low_task_utility_relational_anchor_dropped_by_utility_only": relational_anchor
        not in utility_only,
        "low_task_utility_relational_anchor_retained_by_contextual_policy": relational_anchor
        in contextual,
        "h_ms1_status": "SYNTHETIC_POLICY_DIVERGENCE_DEMONSTRATED",
        "h_ms2_endogenous_self_relevance": "NOT_TESTED",
        "scientific_disposition": "HOLD",
        "canonical_effect": "NONE",
        "deployment": False,
        "subjectivity_conclusion": "NOT_ESTABLISHED",
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
