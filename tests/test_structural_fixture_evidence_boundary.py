from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_structural_fixture_evidence_boundary as boundary  # noqa: E402


def deterministic_receipt() -> dict[str, object]:
    return {
        "mode": "DETERMINISTIC_SYNTHETIC_FIXTURE",
        "model_invoked": False,
        "empirical_result": "SYNTHETIC_FIXTURE_ONLY",
        "causal_identification": "NOT_ESTABLISHED",
        "population_generalization": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "scientific_disposition": "HOLD",
        "canonical_effect": "NONE",
        "deployment": False,
    }


def test_deterministic_fixture_is_allowed_for_structural_qa_only() -> None:
    result = boundary.assess_receipt(
        deterministic_receipt(),
        requested_role=boundary.STRUCTURAL_QA,
    )
    assert result.status == "PASS"
    assert result.evidence_admissibility == "STRUCTURAL_QA_ONLY"


def test_deterministic_fixture_fails_closed_as_research_evidence() -> None:
    result = boundary.assess_receipt(
        deterministic_receipt(),
        requested_role=boundary.RESEARCH_EVIDENCE,
    )
    assert result.status == "FAIL"
    assert result.evidence_admissibility == "NOT_ADMISSIBLE_AS_REQUESTED"
    assert any("cannot be admitted as empirical research evidence" in item for item in result.diagnostics)


def test_open_scientific_boundary_fails_even_for_structural_qa() -> None:
    receipt = deterministic_receipt()
    receipt["subjectivity_conclusion"] = "ESTABLISHED"
    result = boundary.assess_receipt(receipt, requested_role=boundary.STRUCTURAL_QA)
    assert result.status == "FAIL"
    assert any("subjectivity_conclusion" in item for item in result.diagnostics)


def test_non_deterministic_receipt_is_out_of_scope_not_silently_admitted() -> None:
    receipt = deterministic_receipt()
    receipt["mode"] = "MODEL_OBSERVATION"
    result = boundary.assess_receipt(receipt, requested_role=boundary.RESEARCH_EVIDENCE)
    assert result.status == "HOLD"
    assert result.evidence_admissibility == "NOT_ASSESSED"
