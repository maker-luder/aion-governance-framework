from __future__ import annotations

from dataclasses import replace

from aion_factorial_completeness import (
    Disposition,
    ExecutionStatus,
    FactorialDesign,
    MatrixStatus,
    RunRecord,
    evaluate_design,
)


FACTORS = (("mode", ("baseline", "guarded")), ("memory", ("off", "on")))


def run(run_id: str, mode: str, memory: str, **changes: object) -> RunRecord:
    values: dict[str, object] = {
        "run_id": run_id,
        "cell": (("mode", mode), ("memory", memory)),
        "run_order": int(run_id.rsplit("-", 1)[-1]),
        "protocol_ref": "protocol:factorial-1",
        "execution_ref": f"execution:{run_id}",
        "provenance_refs": (f"prov:{run_id}",),
    }
    values.update(changes)
    return RunRecord(**values)


def design(runs: tuple[RunRecord, ...], **changes: object) -> FactorialDesign:
    values: dict[str, object] = {
        "design_id": "factorial-1",
        "factors": FACTORS,
        "runs": runs,
        "expected_replications": 1,
    }
    values.update(changes)
    return FactorialDesign(**values)


def complete_runs() -> tuple[RunRecord, ...]:
    return (
        run("run-1", "baseline", "off"),
        run("run-2", "baseline", "on"),
        run("run-3", "guarded", "off"),
        run("run-4", "guarded", "on"),
    )


def test_complete_cartesian_matrix_is_admissible_for_design_review() -> None:
    result = evaluate_design(design(complete_runs()))
    assert result.matrix_status is MatrixStatus.COMPLETE
    assert result.execution_status is ExecutionStatus.COMPLETE
    assert result.disposition is Disposition.ADMISSIBLE_FOR_DESIGN_REVIEW
    assert result.expected_cell_count == 4
    assert result.observed_cell_count == 4
    assert result.reason == "CARTESIAN_MATRIX_AND_EXECUTION_METADATA_COMPLETE"


def test_missing_cell_is_incomplete_and_indeterminate() -> None:
    result = evaluate_design(
        design(
            (
                run("run-1", "baseline", "off"),
                run("run-2", "baseline", "on"),
                run("run-3", "guarded", "off"),
            )
        )
    )
    assert result.matrix_status is MatrixStatus.INCOMPLETE
    assert result.disposition is Disposition.INDETERMINATE
    assert result.missing_cells == ((("mode", "guarded"), ("memory", "on")),)


def test_duplicate_cell_is_incomplete_not_silently_collapsed() -> None:
    result = evaluate_design(
        design(
            complete_runs() + (run("run-5", "baseline", "off"),)
        )
    )
    assert result.matrix_status is MatrixStatus.INCOMPLETE
    assert result.duplicate_cells == ((("mode", "baseline"), ("memory", "off")),)
    assert result.disposition is Disposition.INDETERMINATE


def test_under_replicated_cell_is_incomplete_when_two_replications_declared() -> None:
    result = evaluate_design(design(complete_runs(), expected_replications=2))
    assert result.matrix_status is MatrixStatus.INCOMPLETE
    assert len(result.under_replicated_cells) == 4
    assert result.disposition is Disposition.INDETERMINATE


def test_two_replications_per_cell_are_complete_when_declared() -> None:
    doubled = tuple(
        run(f"run-{index}", mode, memory, replication_index=replication)
        for index, (mode, memory, replication) in enumerate(
            [
                ("baseline", "off", 1),
                ("baseline", "on", 1),
                ("guarded", "off", 1),
                ("guarded", "on", 1),
                ("baseline", "off", 2),
                ("baseline", "on", 2),
                ("guarded", "off", 2),
                ("guarded", "on", 2),
            ],
            start=1,
        )
    )
    result = evaluate_design(design(doubled, expected_replications=2))
    assert result.matrix_status is MatrixStatus.COMPLETE
    assert result.execution_status is ExecutionStatus.COMPLETE
    assert result.disposition is Disposition.ADMISSIBLE_FOR_DESIGN_REVIEW


def test_out_of_domain_cell_holds() -> None:
    result = evaluate_design(
        design(complete_runs()[:-1] + (run("run-4", "unknown", "on"),))
    )
    assert result.matrix_status is MatrixStatus.INVALID
    assert result.disposition is Disposition.HOLD
    assert result.reason == "OUT_OF_DOMAIN_OR_MALFORMED_CELL"


def test_missing_execution_metadata_holds_even_when_matrix_is_complete() -> None:
    result = evaluate_design(
        design(complete_runs()[:-1] + (run("run-4", "guarded", "on", execution_ref=None),))
    )
    assert result.matrix_status is MatrixStatus.COMPLETE
    assert result.execution_status is ExecutionStatus.PARTIAL
    assert result.disposition is Disposition.HOLD
    assert result.missing_execution_runs == ("run-4",)


def test_missing_protocol_or_provenance_is_execution_incomplete() -> None:
    result = evaluate_design(
        design(complete_runs()[:-1] + (run("run-4", "guarded", "on", protocol_ref=None, provenance_refs=()),))
    )
    assert result.matrix_status is MatrixStatus.COMPLETE
    assert result.execution_status is ExecutionStatus.PARTIAL
    assert result.disposition is Disposition.HOLD


def test_duplicate_factor_names_hold() -> None:
    result = evaluate_design(
        FactorialDesign(
            design_id="bad-factors",
            factors=(("mode", ("a", "b")), ("mode", ("x", "y"))),
            runs=(),
        )
    )
    assert result.matrix_status is MatrixStatus.INVALID
    assert result.disposition is Disposition.HOLD


def test_duplicate_factor_levels_hold() -> None:
    result = evaluate_design(
        FactorialDesign(
            design_id="bad-levels",
            factors=(("mode", ("a", "a")),),
            runs=(),
        )
    )
    assert result.matrix_status is MatrixStatus.INVALID
    assert result.reason == "FACTOR_LEVELS_MUST_BE_NONEMPTY_AND_UNIQUE"


def test_zero_expected_replications_hold() -> None:
    result = evaluate_design(design(complete_runs(), expected_replications=0))
    assert result.matrix_status is MatrixStatus.INVALID
    assert result.disposition is Disposition.HOLD


def test_cell_order_is_canonicalized_to_declared_factor_order() -> None:
    reordered = tuple(
        replace(item, cell=tuple(reversed(item.cell))) for item in complete_runs()
    )
    result = evaluate_design(design(reordered))
    assert result.matrix_status is MatrixStatus.COMPLETE
    assert result.disposition is Disposition.ADMISSIBLE_FOR_DESIGN_REVIEW


def test_design_decision_serializes_enum_values_and_non_promoting_boundaries() -> None:
    payload = evaluate_design(design(complete_runs())).as_dict()
    assert payload["matrix_status"] == "COMPLETE"
    assert payload["execution_status"] == "COMPLETE"
    assert payload["disposition"] == "ADMISSIBLE_FOR_DESIGN_REVIEW"
    assert payload["canonical_effect"] == "NONE"
    assert payload["deployment"] is False
    assert payload["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert payload["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
