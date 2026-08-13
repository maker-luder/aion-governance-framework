from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_factorial_completeness import FactorialDesign, RunRecord, evaluate_design

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


def complete() -> tuple[RunRecord, ...]:
    return (
        run("run-1", "baseline", "off"),
        run("run-2", "baseline", "on"),
        run("run-3", "guarded", "off"),
        run("run-4", "guarded", "on"),
    )


def build_cases() -> list[FactorialDesign]:
    base = complete()
    return [
        FactorialDesign("complete", FACTORS, base),
        FactorialDesign("missing-cell", FACTORS, base[:-1]),
        FactorialDesign("duplicate-cell", FACTORS, base + (run("run-5", "baseline", "off"),)),
        FactorialDesign("under-replicated", FACTORS, base, expected_replications=2),
        FactorialDesign(
            "invalid-cell",
            FACTORS,
            base[:-1] + (run("run-4", "unknown", "on"),),
        ),
        FactorialDesign(
            "missing-execution-metadata",
            FACTORS,
            base[:-1] + (run("run-4", "guarded", "on", execution_ref=None),),
        ),
    ]


def run_experiment(output: Path) -> dict[str, object]:
    records = []
    for design in build_cases():
        decision = evaluate_design(design)
        records.append({"design_id": design.design_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "factorial-completeness-contract-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "effect_estimation_performed": False,
        "scientific_conclusion": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "identity_continuity_conclusion": "NOT_ESTABLISHED",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run_experiment(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
