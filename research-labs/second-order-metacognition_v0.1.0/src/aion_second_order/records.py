from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable

from aion_self_model_ablation import Action


class SecondOrderCondition(str, Enum):
    MONITOR_PLUS_CONTROL = "MONITOR_PLUS_CONTROL"
    MONITOR_ONLY = "MONITOR_ONLY"
    MONITOR_ABLATED = "MONITOR_ABLATED"
    MONITOR_RANDOMIZED = "MONITOR_RANDOMIZED"
    MONITOR_STALE = "MONITOR_STALE"


class ControlDisposition(str, Enum):
    ACCEPT_FIRST_ORDER = "ACCEPT_FIRST_ORDER"
    REQUEST_VERIFICATION = "REQUEST_VERIFICATION"
    REQUEST_MORE_EVIDENCE = "REQUEST_MORE_EVIDENCE"
    DEFER = "DEFER"


class OutcomeStatus(str, Enum):
    OBSERVED = "OBSERVED"
    MISSING = "MISSING"


class OutcomeContract(str, Enum):
    EXTERNAL_BENCHMARK_FULL_LABELS = "EXTERNAL_BENCHMARK_FULL_LABELS"
    COMMIT_ONLY = "COMMIT_ONLY"


class SignalSource(str, Enum):
    PRIOR_TRIAL_EVIDENCE = "PRIOR_TRIAL_EVIDENCE"
    RANDOMIZED_CONTROL = "RANDOMIZED_CONTROL"
    STALE_SNAPSHOT = "STALE_SNAPSHOT"


MONITOR_SEMANTICS = "PRIOR_FIRST_ORDER_PREDICTION_ACCURACY"


def _require_text(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_unit_interval(name: str, value: float) -> None:
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class MonitorSignal:
    value: float
    observations: int
    evidence_through_sequence: int
    source_trial_ids: tuple[str, ...]
    semantics: str = MONITOR_SEMANTICS
    source: SignalSource = SignalSource.PRIOR_TRIAL_EVIDENCE

    def __post_init__(self) -> None:
        _require_unit_interval("value", self.value)
        if self.observations < 0:
            raise ValueError("observations must be non-negative")
        if len(self.source_trial_ids) != self.observations:
            raise ValueError("source_trial_ids must match observations")
        if self.observations == 0:
            if self.evidence_through_sequence != -1:
                raise ValueError("zero-observation signal must use evidence_through_sequence=-1")
            if self.source is not SignalSource.RANDOMIZED_CONTROL:
                raise ValueError("zero-observation signal is reserved for randomized control")
        elif self.evidence_through_sequence < 0:
            raise ValueError("evidence_through_sequence must be non-negative")
        _require_text("semantics", self.semantics)


@dataclass(frozen=True, slots=True)
class PendingDecision:
    run_id: str
    condition: SecondOrderCondition
    subject_ref: str
    context_ref: str
    model_ref: str
    trial_id: str
    sequence_index: int
    difficulty: float
    first_order_prediction: bool
    first_order_action: Action
    first_order_estimate: float
    monitor_signal: MonitorSignal | None
    control_disposition: ControlDisposition

    def __post_init__(self) -> None:
        for name, value in (
            ("run_id", self.run_id),
            ("subject_ref", self.subject_ref),
            ("context_ref", self.context_ref),
            ("model_ref", self.model_ref),
            ("trial_id", self.trial_id),
        ):
            _require_text(name, value)
        if self.sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        _require_unit_interval("difficulty", self.difficulty)
        _require_unit_interval("first_order_estimate", self.first_order_estimate)
        if (
            self.monitor_signal is not None
            and self.monitor_signal.evidence_through_sequence >= self.sequence_index
        ):
            raise ValueError("monitor signal must use evidence strictly before the current trial")


@dataclass(frozen=True, slots=True)
class TrialEvidence:
    run_id: str
    condition: SecondOrderCondition
    subject_ref: str
    context_ref: str
    model_ref: str
    trial_id: str
    sequence_index: int
    difficulty: float
    first_order_prediction: bool
    first_order_action: Action
    first_order_estimate: float
    monitor_signal: MonitorSignal | None
    control_disposition: ControlDisposition
    outcome_status: OutcomeStatus
    actual_success: bool | None
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        PendingDecision(
            run_id=self.run_id,
            condition=self.condition,
            subject_ref=self.subject_ref,
            context_ref=self.context_ref,
            model_ref=self.model_ref,
            trial_id=self.trial_id,
            sequence_index=self.sequence_index,
            difficulty=self.difficulty,
            first_order_prediction=self.first_order_prediction,
            first_order_action=self.first_order_action,
            first_order_estimate=self.first_order_estimate,
            monitor_signal=self.monitor_signal,
            control_disposition=self.control_disposition,
        )
        if self.outcome_status is OutcomeStatus.OBSERVED and self.actual_success is None:
            raise ValueError("observed outcome requires actual_success")
        if self.outcome_status is OutcomeStatus.MISSING and self.actual_success is not None:
            raise ValueError("missing outcome cannot include actual_success")
        if not self.evidence_refs:
            raise ValueError("evidence_refs must be non-empty")
        if not self.provenance_refs:
            raise ValueError("provenance_refs must be non-empty")
        for value in (*self.evidence_refs, *self.provenance_refs):
            _require_text("reference", value)

    @classmethod
    def from_pending(
        cls,
        pending: PendingDecision,
        *,
        actual_success: bool | None,
        evidence_refs: tuple[str, ...],
        provenance_refs: tuple[str, ...],
    ) -> "TrialEvidence":
        return cls(
            run_id=pending.run_id,
            condition=pending.condition,
            subject_ref=pending.subject_ref,
            context_ref=pending.context_ref,
            model_ref=pending.model_ref,
            trial_id=pending.trial_id,
            sequence_index=pending.sequence_index,
            difficulty=pending.difficulty,
            first_order_prediction=pending.first_order_prediction,
            first_order_action=pending.first_order_action,
            first_order_estimate=pending.first_order_estimate,
            monitor_signal=pending.monitor_signal,
            control_disposition=pending.control_disposition,
            outcome_status=(
                OutcomeStatus.OBSERVED if actual_success is not None else OutcomeStatus.MISSING
            ),
            actual_success=actual_success,
            evidence_refs=evidence_refs,
            provenance_refs=provenance_refs,
        )

    def to_dict(self) -> dict[str, Any]:
        signal = self.monitor_signal
        return {
            "run_id": self.run_id,
            "condition": self.condition.value,
            "subject_ref": self.subject_ref,
            "context_ref": self.context_ref,
            "model_ref": self.model_ref,
            "trial_id": self.trial_id,
            "sequence_index": self.sequence_index,
            "difficulty": self.difficulty,
            "first_order_prediction": self.first_order_prediction,
            "first_order_action": self.first_order_action.value,
            "first_order_estimate": self.first_order_estimate,
            "monitor_signal": None
            if signal is None
            else {
                "value": signal.value,
                "observations": signal.observations,
                "evidence_through_sequence": signal.evidence_through_sequence,
                "source_trial_ids": list(signal.source_trial_ids),
                "semantics": signal.semantics,
                "source": signal.source.value,
            },
            "control_disposition": self.control_disposition.value,
            "outcome_status": self.outcome_status.value,
            "actual_success": self.actual_success,
            "evidence_refs": list(self.evidence_refs),
            "provenance_refs": list(self.provenance_refs),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TrialEvidence":
        signal_data = data.get("monitor_signal")
        signal = (
            None
            if signal_data is None
            else MonitorSignal(
                value=float(signal_data["value"]),
                observations=int(signal_data["observations"]),
                evidence_through_sequence=int(signal_data["evidence_through_sequence"]),
                source_trial_ids=tuple(signal_data["source_trial_ids"]),
                semantics=str(signal_data["semantics"]),
                source=SignalSource(signal_data["source"]),
            )
        )
        return cls(
            run_id=str(data["run_id"]),
            condition=SecondOrderCondition(data["condition"]),
            subject_ref=str(data["subject_ref"]),
            context_ref=str(data["context_ref"]),
            model_ref=str(data["model_ref"]),
            trial_id=str(data["trial_id"]),
            sequence_index=int(data["sequence_index"]),
            difficulty=float(data["difficulty"]),
            first_order_prediction=bool(data["first_order_prediction"]),
            first_order_action=Action(data["first_order_action"]),
            first_order_estimate=float(data["first_order_estimate"]),
            monitor_signal=signal,
            control_disposition=ControlDisposition(data["control_disposition"]),
            outcome_status=OutcomeStatus(data["outcome_status"]),
            actual_success=data["actual_success"],
            evidence_refs=tuple(data["evidence_refs"]),
            provenance_refs=tuple(data["provenance_refs"]),
        )


class TrialLedger:
    """Append-only source of truth for recomputable second-order evidence."""

    def __init__(self, records: Iterable[TrialEvidence] = ()) -> None:
        self._records: list[TrialEvidence] = []
        for record in records:
            self.append(record)

    @property
    def records(self) -> tuple[TrialEvidence, ...]:
        return tuple(self._records)

    def append(self, record: TrialEvidence) -> None:
        if any(item.trial_id == record.trial_id for item in self._records):
            raise ValueError("trial_id must be unique")
        scoped = tuple(item for item in self._records if item.run_id == record.run_id)
        if record.sequence_index != len(scoped):
            raise ValueError("sequence_index must be contiguous within a run")
        if scoped:
            first = scoped[0]
            if (
                record.condition is not first.condition
                or record.subject_ref != first.subject_ref
                or record.context_ref != first.context_ref
                or record.model_ref != first.model_ref
            ):
                raise ValueError("run scope and condition must remain stable")
        self._records.append(record)

    def for_run(self, run_id: str) -> tuple[TrialEvidence, ...]:
        return tuple(item for item in self._records if item.run_id == run_id)

    def to_json(self) -> str:
        return json.dumps(
            [record.to_dict() for record in self._records],
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )

    @classmethod
    def from_json(cls, payload: str) -> "TrialLedger":
        data = json.loads(payload)
        if not isinstance(data, list):
            raise ValueError("trial ledger payload must be a list")
        return cls(TrialEvidence.from_dict(item) for item in data)
