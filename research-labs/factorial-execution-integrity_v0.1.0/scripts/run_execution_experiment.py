from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_factorial_execution import (
    CellExecution,
    CellState,
    FactorialExecutionLedger,
    OutcomeState,
    audit_factorial_execution,
)

FACTORS = (("dose", ("low", "high")), ("context", ("day", "night")))


def execution(execution_id: str, dose: str, context: str, *, state: CellState = CellState.COMPLETED, outcome: OutcomeState = OutcomeState.POSITIVE, outcome_ref: str | None = "outcome:1", planned_ref: str | None = "plan:factorial-1", execution_ref: str | None = "execution:trace", provenance_refs: tuple[str, ...] = ("trace:source",), deviation_ref: str | None = None, deviation_reason: str | None = None, planned_sequence: int = 1, outcome_lock_sequence: int | None = 100) -> CellExecution:
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
        replicate_index=1,
        planned_sequence=planned_sequence,
        outcome_lock_sequence=outcome_lock_sequence,
    )


def complete_executions() -> tuple[CellExecution, ...]:
    return (
        execution("run:1", "low", "day", outcome=OutcomeState.POSITIVE, outcome_ref="outcome:positive"),
        execution("run:2", "low", "night", outcome=OutcomeState.NEGATIVE, outcome_ref="outcome:negative", planned_sequence=2),
        execution("run:3", "high", "day", outcome=OutcomeState.NULL, outcome_ref="outcome:null", planned_sequence=3),
        execution("run:4", "high", "night", outcome=OutcomeState.INDETERMINATE, outcome_ref="outcome:indeterminate", planned_sequence=4),
    )


def ledger(*executions: CellExecution, **changes: object) -> FactorialExecutionLedger:
    values: dict[str, object] = {
        "ledger_id": "ledger:factorial-execution-exp",
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


def run(output: Path) -> dict[str, object]:
    complete = complete_executions()
    failed = execution("run:failed", "low", "day", state=CellState.FAILED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None, deviation_ref="deviation:timeout", deviation_reason="timeout")
    aborted = execution("run:aborted", "low", "night", state=CellState.ABORTED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None, deviation_ref="deviation:resource", deviation_reason="resource-limit", planned_sequence=2)
    excluded = execution("run:excluded", "high", "day", state=CellState.EXCLUDED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None, deviation_ref="deviation:criteria", deviation_reason="predeclared-exclusion", planned_sequence=3)
    cases: list[tuple[str, FactorialExecutionLedger]] = [
        ("complete-with-mixed-outcomes", ledger(*complete)),
        ("negative-and-null-preserved", ledger(*complete)),
        ("missing-cell", ledger(*complete[:-1])),
        ("under-replicated", ledger(*complete, expected_replications=2)),
        ("attrition-with-deviation", ledger(failed, aborted, excluded, complete[3])),
        ("attrition-without-deviation", ledger(execution("run:failed", "low", "day", state=CellState.FAILED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None), *complete[1:])),
        ("completed-outcome-missing", ledger(execution("run:missing", "low", "day", outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None), *complete[1:])),
        ("nonterminal-attempted", ledger(execution("run:attempted", "low", "day", state=CellState.ATTEMPTED, outcome=OutcomeState.NOT_EVALUATED, outcome_ref=None), *complete[1:])),
        ("unreported-cell", ledger(execution("run:unreported", "low", "day", state=CellState.UNREPORTED, outcome=OutcomeState.NOT_REPORTED, outcome_ref=None), *complete[1:])),
        ("post-outcome-addition", ledger(execution("run:late", "low", "day", planned_sequence=101, outcome_lock_sequence=100), *complete[1:])),
        ("execution-id-collision", ledger(complete[0], execution("run:1", "low", "day"), *complete[1:])),
        ("out-of-domain-cell", ledger(execution("run:invalid", "unexpected", "day"))),
        ("missing-randomization-metadata", ledger(*complete, randomization_ref=None)),
        ("boundary-effect-request", ledger(*complete, canonical_effect="WRITE", governance_effect="PROMOTE", deployment=True)),
    ]
    records = []
    for case_id, item in cases:
        decision = audit_factorial_execution(item)
        records.append({"case_id": case_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "factorial-execution-integrity-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
