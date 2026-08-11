from __future__ import annotations

from hashlib import sha256
from typing import Iterable

from .records import (
    MONITOR_SEMANTICS,
    ControlDisposition,
    MonitorSignal,
    OutcomeStatus,
    SecondOrderCondition,
    SignalSource,
    TrialEvidence,
)


def recompute_monitor_signal(
    records: Iterable[TrialEvidence],
    *,
    min_observations: int = 2,
) -> MonitorSignal | None:
    if min_observations <= 0:
        raise ValueError("min_observations must be positive")
    observed = tuple(item for item in records if item.outcome_status is OutcomeStatus.OBSERVED)
    if len(observed) < min_observations:
        return None
    correct = sum(item.first_order_prediction is item.actual_success for item in observed)
    return MonitorSignal(
        value=round(correct / len(observed), 6),
        observations=len(observed),
        evidence_through_sequence=max(item.sequence_index for item in observed),
        source_trial_ids=tuple(item.trial_id for item in observed),
        semantics=MONITOR_SEMANTICS,
        source=SignalSource.PRIOR_TRIAL_EVIDENCE,
    )


def randomized_control_signal(*, seed: int, run_id: str, trial_id: str) -> MonitorSignal:
    if not run_id or not trial_id:
        raise ValueError("run_id and trial_id must be non-empty")
    digest = sha256(f"{seed}:{run_id}:{trial_id}".encode("utf-8")).digest()
    value = int.from_bytes(digest[:8], "big") / ((1 << 64) - 1)
    return MonitorSignal(
        value=round(value, 6),
        observations=0,
        evidence_through_sequence=-1,
        source_trial_ids=(),
        semantics="RANDOMIZED_CONTROL_SCALAR_NOT_EVIDENCE_DERIVED",
        source=SignalSource.RANDOMIZED_CONTROL,
    )


class SecondOrderMonitor:
    def __init__(
        self,
        *,
        min_observations: int = 2,
        verification_threshold: float = 0.75,
        random_seed: int = 29,
    ) -> None:
        if min_observations <= 0:
            raise ValueError("min_observations must be positive")
        if not 0.0 <= verification_threshold <= 1.0:
            raise ValueError("verification_threshold must be between 0 and 1")
        self.min_observations = min_observations
        self.verification_threshold = verification_threshold
        self.random_seed = random_seed

    def derive(
        self,
        condition: SecondOrderCondition,
        history: tuple[TrialEvidence, ...],
        *,
        run_id: str,
        trial_id: str,
        stale_snapshot: MonitorSignal | None = None,
    ) -> MonitorSignal | None:
        if condition is SecondOrderCondition.MONITOR_ABLATED:
            return None
        if condition is SecondOrderCondition.MONITOR_RANDOMIZED:
            return randomized_control_signal(seed=self.random_seed, run_id=run_id, trial_id=trial_id)
        if condition is SecondOrderCondition.MONITOR_STALE and stale_snapshot is not None:
            return stale_snapshot
        signal = recompute_monitor_signal(history, min_observations=self.min_observations)
        if signal is not None and condition is SecondOrderCondition.MONITOR_STALE:
            return MonitorSignal(
                value=signal.value,
                observations=signal.observations,
                evidence_through_sequence=signal.evidence_through_sequence,
                source_trial_ids=signal.source_trial_ids,
                semantics=signal.semantics,
                source=SignalSource.STALE_SNAPSHOT,
            )
        return signal

    def control(
        self,
        condition: SecondOrderCondition,
        signal: MonitorSignal | None,
    ) -> ControlDisposition:
        if condition in {
            SecondOrderCondition.MONITOR_ONLY,
            SecondOrderCondition.MONITOR_ABLATED,
        }:
            return ControlDisposition.ACCEPT_FIRST_ORDER
        if signal is None:
            return ControlDisposition.ACCEPT_FIRST_ORDER
        if signal.value < self.verification_threshold:
            return ControlDisposition.REQUEST_VERIFICATION
        return ControlDisposition.ACCEPT_FIRST_ORDER
