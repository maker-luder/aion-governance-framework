from __future__ import annotations

from aion_factorial_execution import (
    CellExecution,
    CellState,
    ExecutionStatus,
    FactorialExecutionLedger,
    OutcomeState,
    audit_factorial_execution,
)


FACTORS = (("dose", ("low", "high")), ("context", ("day", "night")))


def execution(
    execution_id: str,
    dose: str,
    context: str,
    *,
    state: CellState = CellState.COMPLETED,
    outcome: OutcomeState = OutcomeState.POSITIVE,
    outcome_ref: str | None = "outcome:1",
    planned_ref: str | None = "plan:factorial-1",
    execution_ref: str | None = "execution:trace",
    provenance_refs: tuple[str, ...] = ("trace:source",),
    deviation_ref: str | None = None,
    deviation_reason: str | None = None,
    replicate_index: int = 1,
    planned_sequence: int = 1,
    outcome_lock_sequence: int | None = 100,
) -> CellExecution:
    return CellExecution(
        execution_id=execution_id,
        cell=(("dose", dose), ("context", context)),
        state=state,
        planned_ref=planned_ref,
        execution_ref=execution_ref,
        provenance_refs=provenance_refs,
        run_order=planned_sequence,
        deviation_ref=deviation_ref,
        deviation_reason=deviation_reason,
        outcome_state=outcome,
        outcome_ref=outcome_ref,
        replicate_index=replicate_index,
        planned_sequence=planned_sequence,
        outcome_lock_sequence=outcome_lock_sequence,
    )


def ledger(*executions: CellExecution, **changes: object) -> FactorialExecutionLedger:
    values: dict[str, object] = {
        "ledger_id": "ledger:factorial-execution-001",
        "factors": FACTORS,
        "executions": executions,
        "expected_replications": 1,
        "preregistration_ref": "preregistration:factorial-1",
        "protocol_ref": "protocol:factorial-1",
        "randomization_ref": "randomization:seeded-order-1",
        "blinding_ref": "blinding:not-applicable",
        "model_execution": False,
        "scientific_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    values.update(changes)
    return FactorialExecutionLedger(**values)


def complete_executions() -> tuple[CellExecution, ...]:
    return (
        execution("run:1", "low", "day", outcome=OutcomeState.POSITIVE, outcome_ref="outcome:positive"),
        execution("run:2", "low", "night", outcome=OutcomeState.NEGATIVE, outcome_ref="outcome:negative", planned_sequence=2),
        execution("run:3", "high", "day", outcome=OutcomeState.NULL, outcome_ref="outcome:null", planned_sequence=3),
        execution("run:4", "high", "night", outcome=OutcomeState.INDETERMINATE, outcome_ref="outcome:indeterminate", planned_sequence=4),
    )


def test_complete_factorial_trace_is_admissible_for_review() -> None:
    result = audit_factorial_execution(ledger(*complete_executions()))
    assert result.status is ExecutionStatus.COMPLETE
    assert result.reason == "FACTORIAL_EXECUTION_TRACE_COMPLETE_WITH_OUTCOME_PRESERVATION"
    assert result.expected_cell_count == 4
    assert result.completed_cell_count == 4


def test_negative_and_null_outcomes_are_preserved() -> None:
    result = audit_factorial_execution(ledger(*complete_executions()))
    states = dict(result.outcome_states)
    assert states["run:2"] is OutcomeState.NEGATIVE
    assert states["run:3"] is OutcomeState.NULL
    assert states["run:4"] is OutcomeState.INDETERMINATE


def test_missing_cell_is_partial_and_held() -> None:
    runs = complete_executions()[:-1]
    result = audit_factorial_execution(ledger(*runs))
    assert result.status is ExecutionStatus.PARTIAL
    assert result.reason == "FACTORIAL_EXECUTION_TRACE_NOT_COMPLETE"
    assert len(result.missing_cells) == 1


def test_under_replicated_cell_is_partial() -> None:
    result = audit_factorial_execution(ledger(*complete_executions(), expected_replications=2))
    assert result.status is ExecutionStatus.PARTIAL
    assert result.reason == "FACTORIAL_EXECUTION_TRACE_NOT_COMPLETE"


def test_failed_aborted_and_excluded_cells_require_deviation_and_are_preserved() -> None:
    runs = (
        execution("run:1", "low", "day", state=CellState.FAILED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None, deviation_ref="deviation:1", deviation_reason="timeout"),
        execution("run:2", "low", "night", state=CellState.ABORTED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None, deviation_ref="deviation:2", deviation_reason="resource-limit", planned_sequence=2),
        execution("run:3", "high", "day", state=CellState.EXCLUDED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None, deviation_ref="deviation:3", deviation_reason="predeclared-exclusion", planned_sequence=3),
        execution("run:4", "high", "night", planned_sequence=4),
    )
    result = audit_factorial_execution(ledger(*runs))
    assert result.status is ExecutionStatus.COMPLETE
    assert result.failed_cell_count == 1
    assert result.aborted_cell_count == 1
    assert result.excluded_cell_count == 1


def test_attrition_without_deviation_is_indeterminate() -> None:
    failed = execution("run:1", "low", "day", state=CellState.FAILED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None)
    result = audit_factorial_execution(ledger(failed, *complete_executions()[1:]))
    assert result.status is ExecutionStatus.INDETERMINATE
    assert result.reason == "ATTRITION_WITHOUT_DECLARED_DEVIATION"


def test_completed_cell_without_outcome_is_indeterminate() -> None:
    missing = execution("run:1", "low", "day", outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None)
    result = audit_factorial_execution(ledger(missing, *complete_executions()[1:]))
    assert result.status is ExecutionStatus.INDETERMINATE
    assert result.reason == "COMPLETED_CELL_OUTCOME_UNREPORTED"


def test_attempted_nonterminal_cell_is_partial() -> None:
    attempted = execution("run:1", "low", "day", state=CellState.ATTEMPTED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None)
    result = audit_factorial_execution(ledger(attempted, *complete_executions()[1:]))
    assert result.status is ExecutionStatus.PARTIAL
    assert result.reason == "NONTERMINAL_CELL_STATE"


def test_unreported_cell_is_partial() -> None:
    unreported = execution("run:1", "low", "day", state=CellState.UNREPORTED, outcome=OutcomeState.NOT_REPORTED, outcome_ref=None)
    result = audit_factorial_execution(ledger(unreported, *complete_executions()[1:]))
    assert result.status is ExecutionStatus.PARTIAL
    assert result.reason == "NONTERMINAL_CELL_STATE"


def test_post_outcome_cell_addition_is_invalid() -> None:
    late = execution("run:1", "low", "day", planned_sequence=101, outcome_lock_sequence=100)
    result = audit_factorial_execution(ledger(late, *complete_executions()[1:]))
    assert result.status is ExecutionStatus.INVALID
    assert result.reason == "POST_OUTCOME_CELL_ADDITION"


def test_execution_id_collision_is_invalid() -> None:
    duplicate = execution("run:1", "low", "day")
    result = audit_factorial_execution(ledger(complete_executions()[0], duplicate, *complete_executions()[1:]))
    assert result.status is ExecutionStatus.INVALID
    assert result.reason == "EXECUTION_ID_COLLISION"


def test_out_of_domain_cell_is_invalid() -> None:
    invalid = execution("run:invalid", "unexpected", "day")
    result = audit_factorial_execution(ledger(invalid))
    assert result.status is ExecutionStatus.INVALID
    assert result.reason == "OUT_OF_DOMAIN_OR_MALFORMED_CELL"


def test_execution_metadata_missing_is_indeterminate() -> None:
    incomplete = execution("run:1", "low", "day", execution_ref=None)
    result = audit_factorial_execution(ledger(incomplete, *complete_executions()[1:]))
    assert result.status is ExecutionStatus.INDETERMINATE
    assert result.reason == "EXECUTION_METADATA_INCOMPLETE"


def test_design_metadata_missing_is_indeterminate() -> None:
    result = audit_factorial_execution(ledger(*complete_executions(), preregistration_ref=None))
    assert result.status is ExecutionStatus.INDETERMINATE
    assert result.reason == "DESIGN_METADATA_INCOMPLETE"


def test_duplicate_factor_names_are_invalid() -> None:
    result = audit_factorial_execution(ledger(*complete_executions(), factors=(("dose", ("low", "high")), ("dose", ("a", "b")))))
    assert result.status is ExecutionStatus.INVALID
    assert result.reason == "FACTOR_NAMES_MUST_BE_NONEMPTY_AND_UNIQUE"


def test_duplicate_cell_over_expected_replication_is_partial() -> None:
    duplicate = execution("run:duplicate", "low", "day", planned_sequence=5)
    result = audit_factorial_execution(ledger(*complete_executions(), duplicate))
    assert result.status is ExecutionStatus.PARTIAL
    assert result.reason == "FACTORIAL_EXECUTION_TRACE_NOT_COMPLETE"


def test_scientific_conclusion_overreach_is_invalid() -> None:
    result = audit_factorial_execution(ledger(*complete_executions(), scientific_conclusion="CONFIRMED"))
    assert result.status is ExecutionStatus.INVALID
    assert result.reason == "SCIENTIFIC_CONCLUSION_OVERREACH"


def test_boundary_effect_is_invalid_and_output_is_normalized() -> None:
    result = audit_factorial_execution(ledger(*complete_executions(), canonical_effect="WRITE", governance_effect="PROMOTE", deployment=True))
    assert result.status is ExecutionStatus.INVALID
    assert result.reason == "BOUNDARY_EFFECT_REQUESTED"
    assert result.canonical_effect == "NONE"
    assert result.governance_effect == "NONE"
    assert result.deployment is False
