import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/temporal/evidence"


def load(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def test_temporal_registry_has_fixed_admitted_state_and_zero_overlap_case() -> None:
    registry = load("TEMPORAL_CONTINUITY_FALSIFICATION_DATASET_REGISTRY.json")
    assert registry["synthetic_real_classification"] == "SYNTHETIC"
    assert registry["state_metadata"]["admission"] == "ADMITTED"
    assert registry["case_admission"] == {"lexical_replay": "ADMITTED", "zero_overlap_reexpression": "ADMITTED"}
    assert registry["tokenizer_scope"] == "V3 train-only vocabulary"


def test_temporal_falsification_holds_state_constant_and_measures_the_contrast() -> None:
    evidence = load("TEMPORAL_CONTINUITY_LEXICAL_FALSIFICATION_RESULTS.json")
    assert evidence["status"] == "PRELIMINARY_RESEARCH_EVIDENCE"
    assert evidence["state_metadata_constant"] is True
    assert evidence["lexical_overlap_jaccard"]["lexical_replay"] == 0.6
    assert evidence["lexical_overlap_jaccard"]["zero_overlap_reexpression"] == 0.0
    assert evidence["falsification_result"] == "LEXICAL_CARRYOVER_EXPLANATION_NOT_SUPPORTED_IN_THIS_FIXTURE"
    assert evidence["lexical_carryover_signal_observed"] is False
    assert evidence["mean_carryover_gap"] < 0.0
    assert all(case["state_digest"] == evidence["state_digest"] for model in evidence["models"].values() for case in model["cases"].values())


def test_temporal_uses_real_parameter_dependent_models() -> None:
    evidence = load("TEMPORAL_CONTINUITY_LEXICAL_FALSIFICATION_RESULTS.json")
    assert set(evidence["models"]) == {"baseline", "regularized_primary"}
    assert all(model["checkpoint"].startswith("LOCAL_ONLY:") for model in evidence["models"].values())
    assert all(model["training_status"] == "TRAINED_FROM_SCRATCH" for model in evidence["models"].values())
    assert all(model["parameter_dependent_inference"] for model in evidence["models"].values())
    assert all(case["previous_logits_finite"] and case["current_logits_finite"] for model in evidence["models"].values() for case in model["cases"].values())


def test_temporal_clean_validation_and_non_claims() -> None:
    validation = load("TEMPORAL_CONTINUITY_LEXICAL_FALSIFICATION_VALIDATION.json")
    evidence = load("TEMPORAL_CONTINUITY_LEXICAL_FALSIFICATION_RESULTS.json")
    assert validation["status"] == "PASS"
    assert validation["validated_in_clean_process"] is True
    assert all(validation["checks"].values())
    assert len(validation["models"]) == 2
    assert evidence["no_private_data"] is True
    assert evidence["no_private_intimate_data"] is True
    assert evidence["no_external_paid_resource"] is True
    assert "phenomenal continuity" in " ".join(evidence["falsification_conditions"])
