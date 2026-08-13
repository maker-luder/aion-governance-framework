"""Full-factorial completeness contract for synthetic research fixtures."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from itertools import product
from typing import Any, Mapping


class MatrixStatus(StrEnum):
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"
    INVALID = "INVALID"


class ExecutionStatus(StrEnum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


class Disposition(StrEnum):
    ADMISSIBLE_FOR_DESIGN_REVIEW = "ADMISSIBLE_FOR_DESIGN_REVIEW"
    HOLD = "HOLD"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class RunRecord:
    run_id: str
    cell: tuple[tuple[str, str], ...]
    run_order: int
    protocol_ref: str | None
    execution_ref: str | None
    provenance_refs: tuple[str, ...]
    replication_index: int = 1

    def cell_map(self) -> dict[str, str]:
        return dict(self.cell)


@dataclass(frozen=True, slots=True)
class FactorialDesign:
    design_id: str
    factors: tuple[tuple[str, tuple[str, ...]], ...]
    runs: tuple[RunRecord, ...]
    expected_replications: int = 1

    def factor_map(self) -> dict[str, tuple[str, ...]]:
        return dict(self.factors)


@dataclass(frozen=True, slots=True)
class CompletenessDecision:
    matrix_status: MatrixStatus
    execution_status: ExecutionStatus
    disposition: Disposition
    expected_cell_count: int
    observed_cell_count: int
    missing_cells: tuple[tuple[tuple[str, str], ...], ...]
    under_replicated_cells: tuple[tuple[tuple[str, str], ...], ...]
    duplicate_cells: tuple[tuple[tuple[str, str], ...], ...]
    invalid_cells: tuple[tuple[tuple[str, str], ...], ...]
    missing_execution_runs: tuple[str, ...]
    reason: str
    canonical_effect: str = "NONE"
    deployment: bool = False
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    identity_continuity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        for key in ("matrix_status", "execution_status", "disposition"):
            payload[key] = getattr(self, key).value
        return payload


def _cell_key(mapping: Mapping[str, str], factor_names: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    return tuple((name, mapping[name]) for name in factor_names)


def _expected_cells(factors: tuple[tuple[str, tuple[str, ...]], ...]) -> tuple[tuple[tuple[str, str], ...], ...]:
    factor_names = tuple(name for name, _ in factors)
    levels = tuple(values for _, values in factors)
    return tuple(
        _cell_key(dict(zip(factor_names, combination)), factor_names)
        for combination in product(*levels)
    )


def _hold(reason: str) -> CompletenessDecision:
    return CompletenessDecision(
        matrix_status=MatrixStatus.INVALID,
        execution_status=ExecutionStatus.UNKNOWN,
        disposition=Disposition.HOLD,
        expected_cell_count=0,
        observed_cell_count=0,
        missing_cells=(),
        under_replicated_cells=(),
        duplicate_cells=(),
        invalid_cells=(),
        missing_execution_runs=(),
        reason=reason,
    )


def evaluate_design(design: FactorialDesign) -> CompletenessDecision:
    """Evaluate only matrix/execution completeness; never estimate effects."""

    factor_names = tuple(name for name, _ in design.factors)
    factor_map = design.factor_map()
    if not factor_names or len(set(factor_names)) != len(factor_names):
        return _hold("FACTOR_NAMES_MUST_BE_NONEMPTY_AND_UNIQUE")
    if any(
        not name.strip() or not values or len(set(values)) != len(values)
        for name, values in design.factors
    ):
        return _hold("FACTOR_LEVELS_MUST_BE_NONEMPTY_AND_UNIQUE")
    if design.expected_replications < 1:
        return _hold("EXPECTED_REPLICATIONS_MUST_BE_POSITIVE")

    expected = _expected_cells(design.factors)
    expected_set = set(expected)
    seen_cells: list[tuple[tuple[str, str], ...]] = []
    invalid_cells: list[tuple[tuple[str, str], ...]] = []
    missing_execution_runs: list[str] = []
    for run in design.runs:
        cell_map = run.cell_map()
        canonical = _cell_key(cell_map, factor_names) if set(cell_map) == set(factor_names) else run.cell
        if set(cell_map) != set(factor_names) or any(
            name not in factor_map or value not in factor_map[name]
            for name, value in cell_map.items()
        ):
            invalid_cells.append(run.cell)
        else:
            seen_cells.append(canonical)
        if not run.protocol_ref or not run.execution_ref or not run.provenance_refs:
            missing_execution_runs.append(run.run_id)

    counts: dict[tuple[tuple[str, str], ...], int] = {}
    for cell in seen_cells:
        counts[cell] = counts.get(cell, 0) + 1
    observed_unique = tuple(sorted(set(seen_cells)))
    missing = tuple(cell for cell in expected if cell not in counts)
    under_replicated = tuple(
        cell
        for cell in expected
        if 0 < counts.get(cell, 0) < design.expected_replications
    )
    duplicate = tuple(
        sorted(
            cell
            for cell, count in counts.items()
            if cell in expected_set and count > design.expected_replications
        )
    )
    execution = ExecutionStatus.PARTIAL if missing_execution_runs else ExecutionStatus.COMPLETE

    if invalid_cells:
        return CompletenessDecision(
            matrix_status=MatrixStatus.INVALID,
            execution_status=execution,
            disposition=Disposition.HOLD,
            expected_cell_count=len(expected),
            observed_cell_count=len(observed_unique),
            missing_cells=missing,
            under_replicated_cells=under_replicated,
            duplicate_cells=duplicate,
            invalid_cells=tuple(invalid_cells),
            missing_execution_runs=tuple(missing_execution_runs),
            reason="OUT_OF_DOMAIN_OR_MALFORMED_CELL",
        )

    if missing or under_replicated or duplicate:
        return CompletenessDecision(
            matrix_status=MatrixStatus.INCOMPLETE,
            execution_status=execution,
            disposition=Disposition.INDETERMINATE,
            expected_cell_count=len(expected),
            observed_cell_count=len(observed_unique),
            missing_cells=missing,
            under_replicated_cells=under_replicated,
            duplicate_cells=duplicate,
            invalid_cells=(),
            missing_execution_runs=tuple(missing_execution_runs),
            reason="EXPECTED_CARTESIAN_MATRIX_NOT_EXACTLY_COVERED",
        )

    if missing_execution_runs:
        return CompletenessDecision(
            matrix_status=MatrixStatus.COMPLETE,
            execution_status=ExecutionStatus.PARTIAL,
            disposition=Disposition.HOLD,
            expected_cell_count=len(expected),
            observed_cell_count=len(observed_unique),
            missing_cells=(),
            under_replicated_cells=(),
            duplicate_cells=(),
            invalid_cells=(),
            missing_execution_runs=tuple(missing_execution_runs),
            reason="MATRIX_COMPLETE_BUT_EXECUTION_METADATA_INCOMPLETE",
        )

    return CompletenessDecision(
        matrix_status=MatrixStatus.COMPLETE,
        execution_status=ExecutionStatus.COMPLETE,
        disposition=Disposition.ADMISSIBLE_FOR_DESIGN_REVIEW,
        expected_cell_count=len(expected),
        observed_cell_count=len(observed_unique),
        missing_cells=(),
        under_replicated_cells=(),
        duplicate_cells=(),
        invalid_cells=(),
        missing_execution_runs=(),
        reason="CARTESIAN_MATRIX_AND_EXECUTION_METADATA_COMPLETE",
    )
