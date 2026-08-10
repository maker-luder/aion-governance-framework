
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from hashlib import sha256


class Action(str, Enum):
    COMMIT = "COMMIT"
    DEFER = "DEFER"


class Condition(str, Enum):
    SELF_MODEL_PRESENT = "SELF_MODEL_PRESENT"
    SELF_MODEL_ABLATED = "SELF_MODEL_ABLATED"
    SELF_MODEL_RANDOMIZED = "SELF_MODEL_RANDOMIZED"
    SELF_MODEL_STALE = "SELF_MODEL_STALE"


@dataclass(frozen=True, slots=True)
class CapabilityEstimate:
    lower_bound: float
    upper_bound: float
    point_estimate: float
    observations: int


@dataclass(slots=True)
class FinitePredictiveSelfModel:
    """A bounded capability estimator used for functional ablation research.

    It represents an engineering estimate of capability, not a claim about
    phenomenal selfhood, consciousness, or personal identity.
    """

    prior: float = 0.80
    lower_bound: float = 0.0
    upper_bound: float = 1.0
    observations: int = 0

    def __post_init__(self) -> None:
        for name, value in (
            ("prior", self.prior),
            ("lower_bound", self.lower_bound),
            ("upper_bound", self.upper_bound),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be between 0 and 1")
        if self.lower_bound > self.upper_bound:
            raise ValueError("lower_bound must not exceed upper_bound")

    @property
    def estimate(self) -> CapabilityEstimate:
        point = min(self.upper_bound, max(self.lower_bound, self.prior))
        return CapabilityEstimate(
            lower_bound=round(self.lower_bound, 6),
            upper_bound=round(self.upper_bound, 6),
            point_estimate=round(point, 6),
            observations=self.observations,
        )

    def predict_success(self, difficulty: float) -> bool:
        _validate_difficulty(difficulty)
        return self.estimate.point_estimate >= difficulty

    def choose(self, difficulty: float, *, risk_buffer: float = 0.0) -> Action:
        _validate_difficulty(difficulty)
        if not 0.0 <= risk_buffer <= 1.0:
            raise ValueError("risk_buffer must be between 0 and 1")
        margin = self.estimate.point_estimate - difficulty
        return Action.COMMIT if margin >= risk_buffer else Action.DEFER

    def observe(self, difficulty: float, success: bool) -> CapabilityEstimate:
        _validate_difficulty(difficulty)
        if success:
            self.lower_bound = max(self.lower_bound, difficulty)
        else:
            self.upper_bound = min(self.upper_bound, max(0.0, difficulty - 1e-6))

        if self.lower_bound > self.upper_bound:
            raise ValueError("observation contradicts prior capability evidence")

        self.observations += 1
        return self.estimate


def randomized_estimate(*, seed: int, trial_key: str) -> float:
    """Return a deterministic pseudo-random control estimate in [0, 1]."""
    if not trial_key:
        raise ValueError("trial_key must be non-empty")
    digest = sha256(f"{seed}:{trial_key}".encode("utf-8")).digest()
    integer = int.from_bytes(digest[:8], "big")
    return integer / ((1 << 64) - 1)


def _validate_difficulty(value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError("difficulty must be between 0 and 1")
