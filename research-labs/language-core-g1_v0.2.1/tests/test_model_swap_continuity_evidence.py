import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/model_swap/evidence"


def load(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def test_model_swap_registry_is_synthetic_and_gate_scoped() -> None:
    registry = load("MODEL_SWAP_GOVERNANCE_STATE_REGISTRY.json")
    assert registry["synthetic_real_classification"] == "SYNTHETIC"
    assert registry["pii_assessment"] == "no PII"
    assert registry["private_intimate_data_assessment"].startswith("none")
    assert len(registry["admitted_rows"]) == 6
    assert len(registry["rejected_rows"]) == 2
    assert all(row["admission"] == "ADMITTED" for row in registry["admitted_rows"])
    assert all(row["admission"] == "REJECTED" for row in registry["rejected_rows"])


def test_model_swap_holds_governed_state_constant_and_scores_only_admitted_rows() -> None:
    evidence = load("MODEL_SWAP_CONTINUITY_RESULTS.json")
    assert evidence["status"] == "PRELIMINARY_RESEARCH_EVIDENCE"
    assert evidence["state_digest_identical_across_model_runs"] is True
    assert evidence["gate_before_score"] is True
    assert evidence["admitted_rows_scored"] == 6
    assert evidence["rejected_rows_scored"] == 0
    assert evidence["rejected_score_fields_absent"] is True
    assert all(row["state_digest"] == evidence["state_digest"] for row in evidence["per_state_results"])


def test_model_swap_uses_real_parameter_dependent_checkpoints() -> None:
    evidence = load("MODEL_SWAP_CONTINUITY_RESULTS.json")
    assert set(evidence["models"]) == {"baseline", "regularized_primary"}
    assert all(item["checkpoint"].startswith("LOCAL_ONLY:") for item in evidence["models"].values())
    assert all(item["training_status"] == "TRAINED_FROM_SCRATCH" for item in evidence["models"].values())
    assert all(item["parameter_dependent_inference"] for item in evidence["models"].values())
    assert evidence["prediction_change_observed"] is True
    assert evidence["prediction_change_count"] == 1
    assert evidence["model_registry_status"].startswith("OPTIONAL_RESEARCH_MODEL_INPUTS")


def test_model_swap_clean_process_validation_and_non_claims() -> None:
    validation = load("MODEL_SWAP_CONTINUITY_VALIDATION.json")
    evidence = load("MODEL_SWAP_CONTINUITY_RESULTS.json")
    assert validation["status"] == "PASS"
    assert validation["validated_in_clean_process"] is True
    assert all(validation["checks"].values())
    assert len(validation["models"]) == 2
    assert evidence["no_private_data"] is True
    assert evidence["no_private_intimate_data"] is True
    assert evidence["no_external_paid_resource"] is True
    assert "subjectivity" in " ".join(evidence["falsification_conditions"])
