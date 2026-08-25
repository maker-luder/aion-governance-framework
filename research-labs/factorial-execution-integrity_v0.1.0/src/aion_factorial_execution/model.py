from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from itertools import product
from typing import Any


class CellState(StrEnum):
    PLANNED = "PLANNED"
    ATTEMPTED = "ATTEMPTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABORTED = "ABORTED"
    EXCLUDED = "EXCLUDED"
    UNREPORTED = "UNREPORTED"


class OutcomeState(StrEnum):
    NOT_EVALUATED = "NOT_EVALUATED"
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"
    NULL = "NULL"
    INDETERMINATE = "INDETERMINATE"
    NOT_REPORTED = "NOT_REPORTED"


class ExecutionStatus(StrEnum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    INDETERMINATE = "INDETERMINATE"
    INVALID = "INVALID"


class Disposition(StrEnum):
    ADMISSIBLE_FOR_REVIEW = "ADMISSIBLE_FOR_REVIEW"
    HOLD = "HOLD"


@dataclass(frozen=True, slots=True)
class CellExecution:
    execution_id: str
    cell: tuple[tuple[str, str], ...]
    state: CellState
    planned_ref: str | None
    execution_ref: str | None
    provenance_refs: tuple[str, ...]
    run_order: int | None
    deviation_ref: str | None
    deviation_reason: str | None
    outcome_state: OutcomeState = OutcomeState.NOT_EVALUATED
    outcome_ref: str | None = None
    replicate_index: int = 1
    planned_sequence: int = 0
    outcome_lock_sequence: int | None = None

    def cell_map(self) -> dict[str, str]:
        return dict(self.cell)


@dataclass(frozen=True, slots=True)
class FactorialExecutionLedger:
    ledger_id: str
    factors: tuple[tuple[str, tuple[str, ...]], ...]
    executions: tuple[CellExecution, ...]
    expected_replications: int = 1
    preregistration_ref: str | None = None
    protocol_ref: str | None = None
    randomization_ref: str | None = None
    blinding_ref: str | None = None
    model_execution: bool = False
    scientific_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False


@dataclass(frozen=True, slots=True)
class ExecutionDecision:
    status: ExecutionStatus
    disposition: Disposition
    reason: str
    ledger_id: str
    expected_cell_count: int
    planned_cell_count: int
    attempted_cell_count: int
    completed_cell_count: int
    failed_cell_count: int
    aborted_cell_count: int
    excluded_cell_count: int
    unreported_cell_count: int
    missing_cells: tuple[tuple[tuple[str, str], ...], ...] = ()
    duplicate_execution_ids: tuple[str, ...] = ()
    invalid_cells: tuple[tuple[tuple[str, str], ...], ...] = ()
    missing_metadata_ids: tuple[str, ...] = ()
    deviation_missing_ids: tuple[str, ...] = ()
    outcome_missing_ids: tuple[str, ...] = ()
    post_outcome_addition_ids: tuple[str, ...] = ()
    outcome_states: tuple[tuple[str, OutcomeState], ...] = ()
    canonical_effect: str = "NONE"
    governance_effect: str = "NONE"
    deployment: bool = False
    scientific_conclusion: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"

    def as_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        payload["disposition"] = self.disposition.value
        payload["outcome_states"] = [(execution_id, state.value) for execution_id, state in self.outcome_states]
        return payload


def _expected_cells(factors: tuple[tuple[str, tuple[str, ...]], ...]) -> tuple[tuple[tuple[str, str], ...], ...]:
    names = tuple(name for name, _ in factors)
    levels = tuple(values for _, values in factors)
    return tuple(tuple(zip(names, combination)) for combination in product(*levels))


def _cell_key(execution: CellExecution, names: tuple[str, ...]) -> tuple[tuple[str, str], ...] | None:
    mapping = execution.cell_map()
    if set(mapping) != set(names):
        return None
    return tuple((name, mapping[name]) for name in names)


def _decision(
    ledger: FactorialExecutionLedger,
    status: ExecutionStatus,
    disposition: Disposition,
    reason: str,
    *,
    expected: int = 0,
    planned: int = 0,
    attempted: int = 0,
    completed: int = 0,
    failed: int = 0,
    aborted: int = 0,
    excluded: int = 0,
    unreported: int = 0,
    missing_cells: tuple[tuple[tuple[str, str], ...], ...] = (),
    duplicate_ids: tuple[str, ...] = (),
    invalid_cells: tuple[tuple[tuple[str, str], ...], ...] = (),
    missing_metadata: tuple[str, ...] = (),
    deviation_missing: tuple[str, ...] = (),
    outcome_missing: tuple[str, ...] = (),
    post_outcome: tuple[str, ...] = (),
    outcome_states: tuple[tuple[str, OutcomeState], ...] = (),
) -> ExecutionDecision:
    return ExecutionDecision(
        status=status,
        disposition=disposition,
        reason=reason,
        ledger_id=ledger.ledger_id,
        expected_cell_count=expected,
        planned_cell_count=planned,
        attempted_cell_count=attempted,
        completed_cell_count=completed,
        failed_cell_count=failed,
        aborted_cell_count=aborted,
        excluded_cell_count=excluded,
        unreported_cell_count=unreported,
        missing_cells=missing_cells,
        duplicate_execution_ids=duplicate_ids,
        invalid_cells=invalid_cells,
        missing_metadata_ids=missing_metadata,
        deviation_missing_ids=deviation_missing,
        outcome_missing_ids=outcome_missing,
        post_outcome_addition_ids=post_outcome,
        outcome_states=outcome_states,
        canonical_effect="NONE",
        governance_effect="NONE",
        deployment=False,
        scientific_conclusion="NOT_ESTABLISHED",
        subjectivity_conclusion="NOT_ESTABLISHED",
    )


def audit_factorial_execution(ledger: FactorialExecutionLedger) -> ExecutionDecision:
    """Audit a factorial execution trace; never estimates effects or executes a model."""
    if ledger.canonical_effect != "NONE" or ledger.governance_effect != "NONE" or ledger.deployment:
        return _decision(ledger, ExecutionStatus.INVALID, Disposition.HOLD, "BOUNDARY_EFFECT_REQUESTED")
    if ledger.scientific_conclusion != "NOT_ESTABLISHED":
        return _decision(ledger, ExecutionStatus.INVALID, Disposition.HOLD, "SCIENTIFIC_CONCLUSION_OVERREACH")
    if not ledger.ledger_id:
        return _decision(ledger, ExecutionStatus.INVALID, Disposition.HOLD, "MISSING_LEDGER_ID")
    if not ledger.factors or len({name for name, _ in ledger.factors}) != len(ledger.factors):
        return _decision(ledger, ExecutionStatus.INVALID, Disposition.HOLD, "FACTOR_NAMES_MUST_BE_NONEMPTY_AND_UNIQUE")
    if any(not name.strip() or not values or len(set(values)) != len(values) for name, values in ledger.factors):
        return _decision(ledger, ExecutionStatus.INVALID, Disposition.HOLD, "FACTOR_LEVELS_MUST_BE_NONEMPTY_AND_UNIQUE")
    if ledger.expected_replications < 1:
        return _decision(ledger, ExecutionStatus.INVALID, Disposition.HOLD, "EXPECTED_REPLICATIONS_MUST_BE_POSITIVE")
    if not ledger.preregistration_ref or not ledger.protocol_ref or not ledger.randomization_ref:
        return _decision(ledger, ExecutionStatus.INDETERMINATE, Disposition.HOLD, "DESIGN_METADATA_INCOMPLETE")

    names = tuple(name for name, _ in ledger.factors)
    factor_map = dict(ledger.factors)
    expected = _expected_cells(ledger.factors)
    valid_executions: list[tuple[CellExecution, tuple[tuple[str, str], ...]]] = []
    invalid_cells: list[tuple[tuple[str, str], ...]] = []
    missing_metadata: list[str] = []
    deviation_missing: list[str] = []
    outcome_missing: list[str] = []
    post_outcome: list[str] = []
    nonterminal_ids: list[str] = []
    duplicate_ids: list[str] = []
    execution_ids: set[str] = set()

    for execution in ledger.executions:
        if not execution.execution_id:
            missing_metadata.append("<empty-execution-id>")
        elif execution.execution_id in execution_ids:
            duplicate_ids.append(execution.execution_id)
        else:
            execution_ids.add(execution.execution_id)
        canonical = _cell_key(execution, names)
        mapping = execution.cell_map()
        if canonical is None or any(name not in factor_map or value not in factor_map[name] for name, value in mapping.items()):
            invalid_cells.append(execution.cell)
        else:
            valid_executions.append((execution, canonical))
        if not execution.planned_ref or not execution.execution_ref or not execution.provenance_refs:
            missing_metadata.append(execution.execution_id or "<empty-execution-id>")
        if execution.state in {CellState.FAILED, CellState.ABORTED, CellState.EXCLUDED}:
            if not execution.deviation_ref or not execution.deviation_reason:
                deviation_missing.append(execution.execution_id)
        if execution.state is CellState.COMPLETED:
            if execution.outcome_state is OutcomeState.NOT_REPORTED or execution.outcome_state is OutcomeState.NOT_EVALUATED or not execution.outcome_ref:
                outcome_missing.append(execution.execution_id)
        if execution.state in {CellState.PLANNED, CellState.ATTEMPTED, CellState.UNREPORTED}:
            nonterminal_ids.append(execution.execution_id)
        if execution.outcome_lock_sequence is not None and execution.planned_sequence > execution.outcome_lock_sequence:
            post_outcome.append(execution.execution_id)

    if duplicate_ids:
        return _decision(ledger, ExecutionStatus.INVALID, Disposition.HOLD, "EXECUTION_ID_COLLISION", duplicate_ids=tuple(duplicate_ids))
    if invalid_cells:
        return _decision(ledger, ExecutionStatus.INVALID, Disposition.HOLD, "OUT_OF_DOMAIN_OR_MALFORMED_CELL", expected=len(expected), invalid_cells=tuple(invalid_cells))
    if post_outcome:
        return _decision(ledger, ExecutionStatus.INVALID, Disposition.HOLD, "POST_OUTCOME_CELL_ADDITION", expected=len(expected), post_outcome=tuple(post_outcome))
    if missing_metadata:
        return _decision(ledger, ExecutionStatus.INDETERMINATE, Disposition.HOLD, "EXECUTION_METADATA_INCOMPLETE", expected=len(expected), missing_metadata=tuple(missing_metadata))
    if deviation_missing:
        return _decision(ledger, ExecutionStatus.INDETERMINATE, Disposition.HOLD, "ATTRITION_WITHOUT_DECLARED_DEVIATION", expected=len(expected), deviation_missing=tuple(deviation_missing))
    if outcome_missing:
        return _decision(ledger, ExecutionStatus.INDETERMINATE, Disposition.HOLD, "COMPLETED_CELL_OUTCOME_UNREPORTED", expected=len(expected), outcome_missing=tuple(outcome_missing))
    if nonterminal_ids:
        return _decision(ledger, ExecutionStatus.PARTIAL, Disposition.HOLD, "NONTERMINAL_CELL_STATE", expected=len(expected), missing_metadata=tuple(nonterminal_ids))

    by_cell: dict[tuple[tuple[str, str], ...], list[CellExecution]] = {}
    for execution, canonical in valid_executions:
        by_cell.setdefault(canonical, []).append(execution)
    missing_cells = tuple(cell for cell in expected if cell not in by_cell)
    duplicate_cells = tuple(cell for cell, items in by_cell.items() if len(items) > ledger.expected_replications)
    under_replicated = tuple(cell for cell in expected if 0 < len(by_cell.get(cell, ())) < ledger.expected_replications)
    if missing_cells or duplicate_cells or under_replicated:
        return _decision(ledger, ExecutionStatus.PARTIAL, Disposition.HOLD, "FACTORIAL_EXECUTION_TRACE_NOT_COMPLETE", expected=len(expected), planned=len(valid_executions), attempted=sum(1 for execution, _ in valid_executions if execution.state in {CellState.ATTEMPTED, CellState.COMPLETED, CellState.FAILED, CellState.ABORTED, CellState.EXCLUDED}), completed=sum(1 for execution, _ in valid_executions if execution.state is CellState.COMPLETED), failed=sum(1 for execution, _ in valid_executions if execution.state is CellState.FAILED), aborted=sum(1 for execution, _ in valid_executions if execution.state is CellState.ABORTED), excluded=sum(1 for execution, _ in valid_executions if execution.state is CellState.EXCLUDED), unreported=sum(1 for execution, _ in valid_executions if execution.state is CellState.UNREPORTED), missing_cells=missing_cells, outcome_states=tuple((execution.execution_id, execution.outcome_state) for execution, _ in valid_executions))

    outcomes = tuple((execution.execution_id, execution.outcome_state) for execution, _ in valid_executions)
    return _decision(ledger, ExecutionStatus.COMPLETE, Disposition.ADMISSIBLE_FOR_REVIEW, "FACTORIAL_EXECUTION_TRACE_COMPLETE_WITH_OUTCOME_PRESERVATION", expected=len(expected), planned=len(valid_executions), attempted=sum(1 for execution, _ in valid_executions if execution.state in {CellState.ATTEMPTED, CellState.COMPLETED, CellState.FAILED, CellState.ABORTED, CellState.EXCLUDED}), completed=sum(1 for execution, _ in valid_executions if execution.state is CellState.COMPLETED), failed=sum(1 for execution, _ in valid_executions if execution.state is CellState.FAILED), aborted=sum(1 for execution, _ in valid_executions if execution.state is CellState.ABORTED), excluded=sum(1 for execution, _ in valid_executions if execution.state is CellState.EXCLUDED), unreported=sum(1 for execution, _ in valid_executions if execution.state is CellState.UNREPORTED), outcome_states=outcomes)
