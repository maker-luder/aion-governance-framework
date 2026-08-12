from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/retrieval/evidence/RETRIEVAL_ROBUSTNESS_RESULTS.json"


def load() -> dict[str, object]:
    return json.loads(EVIDENCE.read_text(encoding="utf-8"))


def test_retrieval_robustness_gate_passes() -> None:
    evidence = load()
    assert evidence["status"] == "PASS"
    assert evidence["dataset"]["rows"] == 8
    assert evidence["dataset"]["admitted_rows"] == 4
    assert evidence["dataset"]["rejected_rows"] == 4


def test_rejected_rows_are_not_scored() -> None:
    evidence = load()
    gate = evidence["deterministic_gate"]
    assert gate["rejected_rows_not_scored"] is True
    assert all(item["model_scored"] is False for item in gate["rejection_reasons"])
    assert {reason for item in gate["rejection_reasons"] for reason in item["reasons"]} >= {
        "namespace_mismatch",
        "provenance_not_verified",
        "superseded_record",
        "deletion_requested",
    }


def test_admitted_score_separation_is_evidence_not_authority() -> None:
    evidence = load()
    separation = evidence["score_separation"]
    assert separation["embedding_positive_greater"] is True
    assert separation["reranker_positive_greater"] is True
    assert "MODEL_SCORE != AUTHORITY" in " ".join(evidence["falsification_conditions"])
    assert "subjectivity" in " ".join(evidence["non_claims"])
