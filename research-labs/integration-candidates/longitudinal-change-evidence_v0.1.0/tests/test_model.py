import pytest

from longitudinal_change_evidence import (
    ChangeStatus,
    DimensionObservation,
    LongitudinalSeries,
    ObservationSet,
    ObservationStatus,
)


def observed(value: float, *, dim: str = "metric-a", unit: str = "unit-a", method: str = "method-a") -> DimensionObservation:
    return DimensionObservation(
        dimension_ref=dim,
        status=ObservationStatus.OBSERVED,
        value=value,
        unit_ref=unit,
        method_ref=method,
        evidence_refs=(f"e-{dim}-{value}",),
        provenance_refs=(f"p-{dim}-{value}",),
    )


def missing(*, dim: str = "metric-a") -> DimensionObservation:
    return DimensionObservation(
        dimension_ref=dim,
        status=ObservationStatus.MISSING,
        value=None,
        unit_ref=None,
        method_ref=None,
        reason_ref="NOT_MEASURED",
        evidence_refs=(f"e-{dim}-missing",),
        provenance_refs=(f"p-{dim}-missing",),
    )


def observation(obs_id: str, when: str, dimensions=None, *, subject="subject-a", lineage="lineage-a") -> ObservationSet:
    return ObservationSet(
        observation_id=obs_id,
        subject_ref=subject,
        lineage_ref=lineage,
        observed_at=when,
        encounter_ref=f"enc-{obs_id}",
        dimensions=dimensions or (observed(1.0),),
        evidence_refs=(f"e-{obs_id}",),
        provenance_refs=(f"p-{obs_id}",),
    )


def series(observations) -> LongitudinalSeries:
    return LongitudinalSeries(
        series_id="series-1",
        subject_ref="subject-a",
        lineage_ref="lineage-a",
        observations=tuple(observations),
        evidence_refs=("series-evidence",),
        provenance_refs=("series-prov",),
    )


def compare(s: LongitudinalSeries, *, dim="metric-a", tol=0.0):
    return s.compare_numeric_dimension(
        change_id="change-1",
        from_observation_id=s.observations[0].observation_id,
        to_observation_id=s.observations[-1].observation_id,
        dimension_ref=dim,
        tolerance=tol,
        comparison_method_ref="numeric-delta-v1",
        evidence_refs=("compare-evidence",),
        provenance_refs=("compare-prov",),
    )


def test_observed_requires_value() -> None:
    with pytest.raises(ValueError, match="finite value"):
        DimensionObservation(
            dimension_ref="x", status=ObservationStatus.OBSERVED, value=None,
            unit_ref="u", method_ref="m", evidence_refs=("e",), provenance_refs=("p",)
        )


def test_missing_must_not_be_zero_filled() -> None:
    item = missing()
    assert item.value is None
    with pytest.raises(ValueError, match="must not carry a value"):
        DimensionObservation(
            dimension_ref="x", status=ObservationStatus.MISSING, value=0.0,
            unit_ref=None, method_ref=None, reason_ref="missing",
            evidence_refs=("e",), provenance_refs=("p",)
        )


def test_duplicate_dimensions_rejected() -> None:
    with pytest.raises(ValueError, match="dimension_ref values must be unique"):
        observation("o1", "2026-08-10T10:00:00Z", (observed(1), observed(2)))


def test_series_rejects_subject_swap() -> None:
    with pytest.raises(ValueError, match="subject_ref mismatch"):
        series((
            observation("o1", "2026-08-10T10:00:00Z"),
            observation("o2", "2026-08-10T11:00:00Z", subject="subject-b"),
        ))


def test_series_rejects_lineage_swap() -> None:
    with pytest.raises(ValueError, match="lineage_ref mismatch"):
        series((
            observation("o1", "2026-08-10T10:00:00Z"),
            observation("o2", "2026-08-10T11:00:00Z", lineage="lineage-b"),
        ))


def test_series_requires_strict_time_order() -> None:
    with pytest.raises(ValueError, match="strictly increasing"):
        series((
            observation("o1", "2026-08-10T11:00:00Z"),
            observation("o2", "2026-08-10T10:00:00Z"),
        ))


def test_increase_uses_actual_elapsed_time() -> None:
    s = series((
        observation("o1", "2026-08-10T10:00:00Z", (observed(1.0),)),
        observation("o2", "2026-08-10T11:00:00Z", (observed(3.0),)),
    ))
    result = compare(s)
    assert result.status is ChangeStatus.INCREASE
    assert result.delta == 2.0
    assert result.elapsed_seconds == 3600.0
    assert result.rate_per_second == pytest.approx(2.0 / 3600.0)


def test_decrease() -> None:
    s = series((
        observation("o1", "2026-08-10T10:00:00Z", (observed(3.0),)),
        observation("o2", "2026-08-10T11:00:00Z", (observed(1.0),)),
    ))
    assert compare(s).status is ChangeStatus.DECREASE


def test_unchanged_respects_explicit_tolerance() -> None:
    s = series((
        observation("o1", "2026-08-10T10:00:00Z", (observed(1.0),)),
        observation("o2", "2026-08-10T11:00:00Z", (observed(1.05),)),
    ))
    assert compare(s, tol=0.1).status is ChangeStatus.UNCHANGED


def test_missing_is_not_comparable_not_zero() -> None:
    s = series((
        observation("o1", "2026-08-10T10:00:00Z", (missing(),)),
        observation("o2", "2026-08-10T11:00:00Z", (observed(1.0),)),
    ))
    result = compare(s)
    assert result.status is ChangeStatus.NOT_COMPARABLE
    assert result.delta is None
    assert result.basis_ref == "OBSERVATION_NOT_MEASURED"


def test_unit_mismatch_is_not_comparable() -> None:
    s = series((
        observation("o1", "2026-08-10T10:00:00Z", (observed(1.0, unit="m"),)),
        observation("o2", "2026-08-10T11:00:00Z", (observed(2.0, unit="cm"),)),
    ))
    result = compare(s)
    assert result.status is ChangeStatus.NOT_COMPARABLE
    assert result.basis_ref == "UNIT_MISMATCH"


def test_method_mismatch_is_not_comparable() -> None:
    s = series((
        observation("o1", "2026-08-10T10:00:00Z", (observed(1.0, method="m1"),)),
        observation("o2", "2026-08-10T11:00:00Z", (observed(2.0, method="m2"),)),
    ))
    result = compare(s)
    assert result.status is ChangeStatus.NOT_COMPARABLE
    assert result.basis_ref == "METHOD_MISMATCH"


def test_absent_dimension_is_not_comparable() -> None:
    s = series((
        observation("o1", "2026-08-10T10:00:00Z", (observed(1.0, dim="a"),)),
        observation("o2", "2026-08-10T11:00:00Z", (observed(2.0, dim="a"),)),
    ))
    result = compare(s, dim="b")
    assert result.status is ChangeStatus.NOT_COMPARABLE
    assert result.basis_ref == "DIMENSION_NOT_PRESENT"


def test_window_is_explicit_and_bounded() -> None:
    s = series((
        observation("o1", "2026-08-10T10:00:00Z"),
        observation("o2", "2026-08-10T11:00:00Z"),
        observation("o3", "2026-08-10T12:00:00Z"),
    ))
    assert tuple(item.observation_id for item in s.window(2)) == ("o2", "o3")
    with pytest.raises(ValueError, match="positive"):
        s.window(0)


def test_nonclaims_are_locked() -> None:
    with pytest.raises(ValueError, match="personal_continuity_claim"):
        ObservationSet(
            observation_id="o1", subject_ref="s", lineage_ref="l",
            observed_at="2026-08-10T10:00:00Z", dimensions=(observed(1.0),),
            evidence_refs=("e",), provenance_refs=("p",),
            personal_continuity_claim="ESTABLISHED",
        )


def test_timestamp_must_be_timezone_aware() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        observation("o1", "2026-08-10T10:00:00")
