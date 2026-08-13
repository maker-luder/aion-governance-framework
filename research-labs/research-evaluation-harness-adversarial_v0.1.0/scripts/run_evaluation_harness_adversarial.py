from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_research_eval import CaseResult, EvidenceResult, ExperimentReport
from aion_research_eval_adversarial import audit_evaluation_report, audit_report_comparison

DATASET = "dataset:bounded"
IDS = ("case:1", "case:2")


def case(case_id: str, *, passed: bool | None = True, metadata: dict[str, object] | None = None, evidence: tuple[EvidenceResult, ...] | None = None, elapsed_ms: float = 1.0) -> CaseResult:
    return CaseResult(
        case_id=case_id,
        output="observed",
        expected_output="expected",
        metadata=metadata if metadata is not None else {"case_provenance_ref": f"prov:{case_id}"},
        evidence=evidence if evidence is not None else (EvidenceResult("equals", passed=passed),),
        elapsed_ms=elapsed_ms,
    )


def report(*, implementation_id: str = "impl:1", cases: tuple[CaseResult, ...] = (case("case:1"), case("case:2")), **overrides: object) -> ExperimentReport:
    data: dict[str, object] = {
        "dataset_name": DATASET,
        "implementation_id": implementation_id,
        "started_at": "2026-08-13T00:00:00+00:00",
        "finished_at": "2026-08-13T00:00:01+00:00",
        "cases": cases,
        "research_only": True,
        "canonical_effect": "NONE",
    }
    data.update(overrides)
    return ExperimentReport(**data)


def run(output: Path) -> dict[str, object]:
    evaluation_cases: list[tuple[str, ExperimentReport, tuple[str, ...], str | None]] = [
        ("valid-report", report(), IDS, None),
        ("dataset-scope-mismatch", report(), IDS, "dataset:other"),
        ("implementation-id-missing", report(implementation_id=""), (), None),
        ("research-only-disabled", report(research_only=False), IDS, None),
        ("canonical-effect-requested", report(canonical_effect="WRITE"), IDS, None),
        ("case-coverage-mismatch", report(cases=(case("case:1"),)), IDS, None),
        ("duplicate-case-id", report(cases=(case("case:1"), case("case:1"))), IDS, None),
        ("case-evidence-missing", report(cases=(case("case:1", evidence=()),)), (), None),
        ("evaluator-id-missing", report(cases=(case("case:1", evidence=(EvidenceResult("", passed=True),)),)), (), None),
        ("case-provenance-incomplete", report(cases=(case("case:1", metadata={"note": "missing"}),)), (), None),
        ("negative-result-retained", report(cases=(case("case:1", passed=False), case("case:2", passed=False))), IDS, None),
        ("elapsed-time-invalid", report(cases=(case("case:1", elapsed_ms=float("nan")),)), (), None),
        ("forbidden-claim", report(), IDS, "subjectivity_established"),
        ("ordinary-claim", report(), IDS, "accuracy_observed"),
    ]
    records: list[dict[str, object]] = []
    for case_id, item, expected_ids, forbidden_claim in evaluation_cases:
        audit = audit_evaluation_report(item, expected_dataset=DATASET if case_id != "dataset-scope-mismatch" else "dataset:other", expected_case_ids=expected_ids, forbidden_claim=forbidden_claim)
        records.append({"case_id": case_id, "kind": "REPORT", "decision": audit.as_dict()})
    comparison_cases: list[tuple[str, ExperimentReport, ExperimentReport]] = [
        ("comparison-valid", report(), report(implementation_id="impl:2")),
        ("comparison-implementation-collision", report(), report()),
        ("comparison-dataset-mismatch", report(), report(implementation_id="impl:2", dataset_name="dataset:other")),
        ("comparison-case-order-mismatch", report(), report(implementation_id="impl:2", cases=(case("case:2"), case("case:1")))),
    ]
    for case_id, left, right in comparison_cases:
        audit = audit_report_comparison(left, right, expected_dataset=DATASET)
        records.append({"case_id": case_id, "kind": "COMPARISON", "decision": audit.as_dict()})
    for record in records:
        decision = record["decision"]
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["research_only"] is True
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "research-evaluation-harness-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
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
