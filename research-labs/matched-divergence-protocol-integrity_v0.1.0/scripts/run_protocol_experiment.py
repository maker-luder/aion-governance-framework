from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_matched_divergence import (
    ComparisonControls,
    ComparisonMode,
    MatchedDivergenceProtocol,
    StimulusPair,
    audit_protocol,
)


def base_protocol(**changes: object) -> MatchedDivergenceProtocol:
    pairs = (
        StimulusPair("pair-1", "sha256:stimulus-1", "sha256:context-1", "prompt:v1", 2, 2, "AB"),
        StimulusPair("pair-2", "sha256:stimulus-2", "sha256:context-2", "prompt:v1", 2, 2, "BA"),
    )
    controls = ComparisonControls("comparison:predeclared", "blind:outcome", True, "random:block", "counter:ABBA", "leakage:none", "stop:predeclared")
    values: dict[str, object] = {
        "protocol_id": "protocol-exp",
        "protocol_version": "v1",
        "question_ref": "question:exp",
        "estimand_ref": "estimand:exp",
        "system_a_ref": "system:a",
        "system_b_ref": "system:b",
        "stimulus_pairs": pairs,
        "controls": controls,
        "mode": ComparisonMode.PAIRED,
        "predeclared_outcome_ref": "outcome:exp",
        "execution_prohibition_ref": "policy:no-execution",
        "observed_result_ref": None,
    }
    values.update(changes)
    return MatchedDivergenceProtocol(**values)


def build_cases() -> list[MatchedDivergenceProtocol]:
    drift_pairs = (
        StimulusPair("pair-1", "sha256:stimulus-1", "sha256:context-1", "prompt:v1", 2, 2, "AB"),
        StimulusPair("pair-2", "sha256:stimulus-2", "sha256:context-2", "prompt:v2", 2, 2, "BA"),
    )
    return [
        base_protocol(protocol_id="complete-paired"),
        base_protocol(protocol_id="complete-blocked", mode=ComparisonMode.BLOCKED),
        base_protocol(protocol_id="stimulus-drift-metadata", stimulus_pairs=drift_pairs),
        base_protocol(protocol_id="unequal-exposure", stimulus_pairs=(StimulusPair("pair-1", "sha256:s", "sha256:c", "prompt:v1", 2, 1, "AB"),)),
        base_protocol(protocol_id="unsealed-evaluator", controls=ComparisonControls("comparison", "blind", False, "random", "counter", "leak", "stop")),
        base_protocol(protocol_id="outcome-leakage", observed_result_ref="observed:result"),
        base_protocol(protocol_id="system-collision", system_b_ref="system:a"),
        base_protocol(protocol_id="no-pairs", stimulus_pairs=()),
    ]


def run(output: Path) -> dict[str, object]:
    records = []
    for candidate in build_cases():
        decision = audit_protocol(candidate)
        records.append({"protocol_id": candidate.protocol_id, "decision": decision.as_dict()})
    payload = {
        "schema_version": "0.1.0",
        "experiment": "matched-divergence-protocol-integrity-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
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
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
