from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from math import isclose, isfinite
from typing import Final

NONE: Final[str] = "NONE"
NOT_ESTABLISHED: Final[str] = "NOT_ESTABLISHED"


class ObservationStatus(str, Enum):
    OBSERVED = "OBSERVED"
    MISSING = "MISSING"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class ChangeStatus(str, Enum):
    INCREASE = "INCREASE"
    DECREASE = "DECREASE"
    UNCHANGED = "UNCHANGED"
    NOT_COMPARABLE = "NOT_COMPARABLE"


def _require_nonempty(name: str, value: str) -> None:
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_refs(name: str, refs: tuple[str, ...]) -> None:
    if not refs:
        raise ValueError(f"{name} must be non-empty")
    for ref in refs:
        _require_nonempty(name, ref)
    if len(refs) != len(set(refs)):
        raise ValueError(f"{name} must not contain duplicates")


def _parse_timestamp(value: str) -> datetime:
    _require_nonempty("observed_at", value)
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError("observed_at must be ISO 8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("observed_at must be timezone-aware")
    return parsed


@dataclass(frozen=True, slots=True)
class DimensionObservation:
    dimension_ref: str
    status: ObservationStatus
    value: float | None
    unit_ref: str | None
    method_ref: str | None
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    reason_ref: str | None = None
    canonical_effect: str = NONE

    def __post_init__(self) -> None:
        _require_nonempty("dimension_ref", self.dimension_ref)
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.status is ObservationStatus.OBSERVED:
            if self.value is None or not isfinite(self.value):
                raise ValueError("OBSERVED dimension requires a finite value")
            if self.unit_ref is None or not self.unit_ref.strip():
                raise ValueError("OBSERVED dimension requires unit_ref")
            if self.method_ref is None or not self.method_ref.strip():
                raise ValueError("OBSERVED dimension requires method_ref")
            if self.reason_ref is not None:
                _require_nonempty("reason_ref", self.reason_ref)
        else:
            if self.value is not None:
                raise ValueError("MISSING/NOT_APPLICABLE dimension must not carry a value")
            if self.reason_ref is None or not self.reason_ref.strip():
                raise ValueError("MISSING/NOT_APPLICABLE dimension requires reason_ref")
            if self.unit_ref is not None:
                _require_nonempty("unit_ref", self.unit_ref)
            if self.method_ref is not None:
                _require_nonempty("method_ref", self.method_ref)
        if self.canonical_effect != NONE:
            raise ValueError("dimension observation must keep canonical_effect=NONE")


@dataclass(frozen=True, slots=True)
class ObservationSet:
    observation_id: str
    subject_ref: str
    lineage_ref: str
    observed_at: str
    dimensions: tuple[DimensionObservation, ...]
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    encounter_ref: str | None = None
    canonical_effect: str = NONE
    trajectory_identity_claim: str = NOT_ESTABLISHED
    personal_continuity_claim: str = NOT_ESTABLISHED
    developmental_stage_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("observation_id", "subject_ref", "lineage_ref"):
            _require_nonempty(name, getattr(self, name))
        _parse_timestamp(self.observed_at)
        if self.encounter_ref is not None:
            _require_nonempty("encounter_ref", self.encounter_ref)
        if not self.dimensions:
            raise ValueError("observation set requires at least one dimension")
        refs = [item.dimension_ref for item in self.dimensions]
        if len(refs) != len(set(refs)):
            raise ValueError("dimension_ref values must be unique within one observation")
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("observation set must keep canonical_effect=NONE")
        for name in (
            "trajectory_identity_claim",
            "personal_continuity_claim",
            "developmental_stage_claim",
        ):
            if getattr(self, name) != NOT_ESTABLISHED:
                raise ValueError(f"{name} must remain NOT_ESTABLISHED")

    def get_dimension(self, dimension_ref: str) -> DimensionObservation | None:
        for item in self.dimensions:
            if item.dimension_ref == dimension_ref:
                return item
        return None


@dataclass(frozen=True, slots=True)
class ChangeEvidence:
    change_id: str
    from_observation_id: str
    to_observation_id: str
    dimension_ref: str
    status: ChangeStatus
    elapsed_seconds: float
    delta: float | None
    rate_per_second: float | None
    tolerance: float
    comparison_method_ref: str
    basis_ref: str
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE
    trajectory_identity_claim: str = NOT_ESTABLISHED
    personal_continuity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in (
            "change_id",
            "from_observation_id",
            "to_observation_id",
            "dimension_ref",
            "comparison_method_ref",
            "basis_ref",
        ):
            _require_nonempty(name, getattr(self, name))
        if self.from_observation_id == self.to_observation_id:
            raise ValueError("change evidence requires distinct observations")
        if not isfinite(self.elapsed_seconds) or self.elapsed_seconds <= 0:
            raise ValueError("elapsed_seconds must be finite and positive")
        if not isfinite(self.tolerance) or self.tolerance < 0:
            raise ValueError("tolerance must be finite and non-negative")
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.status is ChangeStatus.NOT_COMPARABLE:
            if self.delta is not None or self.rate_per_second is not None:
                raise ValueError("NOT_COMPARABLE change must not carry delta/rate")
        else:
            if self.delta is None or self.rate_per_second is None:
                raise ValueError("comparable change requires delta and rate")
            if not isfinite(self.delta) or not isfinite(self.rate_per_second):
                raise ValueError("delta/rate must be finite")
            if not isclose(self.rate_per_second, self.delta / self.elapsed_seconds, rel_tol=1e-12, abs_tol=1e-15):
                raise ValueError("rate_per_second must equal delta / elapsed_seconds")
            expected = (
                ChangeStatus.UNCHANGED
                if abs(self.delta) <= self.tolerance
                else ChangeStatus.INCREASE
                if self.delta > 0
                else ChangeStatus.DECREASE
            )
            if self.status is not expected:
                raise ValueError("change status does not match delta/tolerance")
        if self.canonical_effect != NONE:
            raise ValueError("change evidence must keep canonical_effect=NONE")
        if self.trajectory_identity_claim != NOT_ESTABLISHED:
            raise ValueError("trajectory identity must remain NOT_ESTABLISHED")
        if self.personal_continuity_claim != NOT_ESTABLISHED:
            raise ValueError("personal continuity must remain NOT_ESTABLISHED")


@dataclass(frozen=True, slots=True)
class LongitudinalSeries:
    series_id: str
    subject_ref: str
    lineage_ref: str
    observations: tuple[ObservationSet, ...]
    evidence_refs: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    canonical_effect: str = NONE
    personal_continuity_claim: str = NOT_ESTABLISHED

    def __post_init__(self) -> None:
        for name in ("series_id", "subject_ref", "lineage_ref"):
            _require_nonempty(name, getattr(self, name))
        if not self.observations:
            raise ValueError("longitudinal series requires observations")
        ids = [item.observation_id for item in self.observations]
        if len(ids) != len(set(ids)):
            raise ValueError("observation_id values must be unique")
        previous_time: datetime | None = None
        for item in self.observations:
            if item.subject_ref != self.subject_ref:
                raise ValueError("observation subject_ref mismatch")
            if item.lineage_ref != self.lineage_ref:
                raise ValueError("observation lineage_ref mismatch")
            current_time = _parse_timestamp(item.observed_at)
            if previous_time is not None and current_time <= previous_time:
                raise ValueError("observations must be strictly increasing in time")
            previous_time = current_time
        _require_refs("evidence_refs", self.evidence_refs)
        _require_refs("provenance_refs", self.provenance_refs)
        if self.canonical_effect != NONE:
            raise ValueError("longitudinal series must keep canonical_effect=NONE")
        if self.personal_continuity_claim != NOT_ESTABLISHED:
            raise ValueError("personal continuity must remain NOT_ESTABLISHED")

    def get_observation(self, observation_id: str) -> ObservationSet | None:
        for item in self.observations:
            if item.observation_id == observation_id:
                return item
        return None

    def window(self, last_n: int) -> tuple[ObservationSet, ...]:
        if last_n <= 0:
            raise ValueError("last_n must be positive")
        return self.observations[-last_n:]

    def compare_numeric_dimension(
        self,
        *,
        change_id: str,
        from_observation_id: str,
        to_observation_id: str,
        dimension_ref: str,
        tolerance: float,
        comparison_method_ref: str,
        evidence_refs: tuple[str, ...],
        provenance_refs: tuple[str, ...],
    ) -> ChangeEvidence:
        before = self.get_observation(from_observation_id)
        after = self.get_observation(to_observation_id)
        if before is None or after is None:
            raise KeyError("from/to observation must exist in series")
        before_time = _parse_timestamp(before.observed_at)
        after_time = _parse_timestamp(after.observed_at)
        elapsed = (after_time - before_time).total_seconds()
        if elapsed <= 0:
            raise ValueError("to_observation must occur after from_observation")
        left = before.get_dimension(dimension_ref)
        right = after.get_dimension(dimension_ref)
        basis = "NUMERIC_DELTA"
        if left is None or right is None:
            status = ChangeStatus.NOT_COMPARABLE
            delta = rate = None
            basis = "DIMENSION_NOT_PRESENT"
        elif left.status is not ObservationStatus.OBSERVED or right.status is not ObservationStatus.OBSERVED:
            status = ChangeStatus.NOT_COMPARABLE
            delta = rate = None
            basis = "OBSERVATION_NOT_MEASURED"
        elif left.unit_ref != right.unit_ref:
            status = ChangeStatus.NOT_COMPARABLE
            delta = rate = None
            basis = "UNIT_MISMATCH"
        elif left.method_ref != right.method_ref:
            status = ChangeStatus.NOT_COMPARABLE
            delta = rate = None
            basis = "METHOD_MISMATCH"
        else:
            assert left.value is not None and right.value is not None
            delta = right.value - left.value
            rate = delta / elapsed
            if abs(delta) <= tolerance:
                status = ChangeStatus.UNCHANGED
            elif delta > 0:
                status = ChangeStatus.INCREASE
            else:
                status = ChangeStatus.DECREASE
        return ChangeEvidence(
            change_id=change_id,
            from_observation_id=from_observation_id,
            to_observation_id=to_observation_id,
            dimension_ref=dimension_ref,
            status=status,
            elapsed_seconds=elapsed,
            delta=delta,
            rate_per_second=rate,
            tolerance=tolerance,
            comparison_method_ref=comparison_method_ref,
            basis_ref=basis,
            evidence_refs=evidence_refs,
            provenance_refs=provenance_refs,
        )
