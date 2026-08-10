from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from statistics import mean
from typing import Iterable

class Condition(str, Enum):
    BASELINE = "BASELINE"
    STATE_PRESENT = "STATE_PRESENT"
    STATE_ABLATED = "STATE_ABLATED"
    RANDOM_CONTROL = "RANDOM_CONTROL"

class AssessmentStatus(str, Enum):
    PASS_CANDIDATE = "PASS_CANDIDATE"
    HOLD = "HOLD"
    FAIL = "FAIL"

@dataclass(frozen=True, slots=True)
class TrialObservation:
    pair_id: str
    replicate: int
    condition: Condition
    score: float

@dataclass(frozen=True, slots=True)
class CausalAssessment:
    status: AssessmentStatus
    intervention_delta: float
    ablation_delta: float
    random_control_delta: float
    replicate_consistency: float
    reasons: tuple[str, ...]
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

def _index(observations: Iterable[TrialObservation]) -> dict[tuple[str, int], dict[Condition, float]]:
    indexed: dict[tuple[str, int], dict[Condition, float]] = {}
    for item in observations:
        key = (item.pair_id, item.replicate)
        bucket = indexed.setdefault(key, {})
        if item.condition in bucket:
            raise ValueError(f"duplicate condition {item.condition} for matched trial {key}")
        bucket[item.condition] = item.score
    return indexed

def assess_causal_effect(
    observations: Iterable[TrialObservation],
    *,
    min_replicates: int = 3,
    min_effect: float = 0.20,
    max_ablation_residual: float = 0.08,
    max_random_control: float = 0.10,
    min_directional_consistency: float = 0.80,
) -> CausalAssessment:
    indexed = _index(observations)
    if len(indexed) < min_replicates:
        return CausalAssessment(AssessmentStatus.HOLD, 0.0, 0.0, 0.0, 0.0, ("INSUFFICIENT_MATCHED_REPLICATES",))
    required = set(Condition)
    if any(set(bucket) != required for bucket in indexed.values()):
        return CausalAssessment(AssessmentStatus.HOLD, 0.0, 0.0, 0.0, 0.0, ("INCOMPLETE_MATCHED_CONDITIONS",))

    intervention_deltas, ablation_deltas, random_deltas = [], [], []
    for bucket in indexed.values():
        baseline = bucket[Condition.BASELINE]
        intervention_deltas.append(bucket[Condition.STATE_PRESENT] - baseline)
        ablation_deltas.append(bucket[Condition.STATE_ABLATED] - baseline)
        random_deltas.append(bucket[Condition.RANDOM_CONTROL] - baseline)

    intervention_delta = mean(intervention_deltas)
    ablation_delta = mean(ablation_deltas)
    random_delta = mean(random_deltas)
    consistency = sum(delta > 0 for delta in intervention_deltas) / len(intervention_deltas)

    reasons: list[str] = []
    if intervention_delta < min_effect:
        reasons.append("INTERVENTION_EFFECT_TOO_SMALL")
    if abs(ablation_delta) > max_ablation_residual:
        reasons.append("ABLATION_DID_NOT_RETURN_NEAR_BASELINE")
    if abs(random_delta) > max_random_control:
        reasons.append("RANDOM_CONTROL_TOO_LARGE")
    if consistency < min_directional_consistency:
        reasons.append("INTERVENTION_DIRECTION_NOT_REPLICATED")

    return CausalAssessment(
        AssessmentStatus.PASS_CANDIDATE if not reasons else AssessmentStatus.HOLD,
        intervention_delta, ablation_delta, random_delta, consistency,
        tuple(reasons) or ("MATCHED_CAUSAL_PATTERN_OBSERVED",),
    )
