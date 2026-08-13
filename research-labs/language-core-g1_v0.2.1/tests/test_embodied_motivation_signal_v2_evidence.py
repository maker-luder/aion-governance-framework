import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "engineering/sexuality/evidence"


def load(name: str) -> dict[str, object]:
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))


def test_v2_cases_and_controls_are_governed() -> None:
    registry = load("EMBODIED_MOTIVATION_V2_DATASET_REGISTRY.json")
    result = load("EMBODIED_MOTIVATION_SIGNAL_V2_RESULTS.json")
    assert registry["case_counts"] == {"canonical": 8, "keyword_scrubbed": 8, "label_permuted": 8}
    assert registry["exact_disjoint_case_texts"] is True
    assert registry["label_permutation_pairs_preserve_text"] is True
    assert registry["oov_tokens"] == []
    assert registry["adult_context"] is True
    assert registry["graphic_content"] is False
    assert registry["no_minors"] is True
    assert result["no_private_data"] is True
    assert result["no_private_intimate_data"] is True


def test_v2_model_and_baseline_contrast_is_recorded() -> None:
    result = load("EMBODIED_MOTIVATION_SIGNAL_V2_RESULTS.json")
    assert result["cases"]["canonical"]["exact_match_accuracy"] == 0.25
    assert result["cases"]["keyword_scrubbed"]["exact_match_accuracy"] == 0.25
    assert result["cases"]["label_permuted"]["exact_match_accuracy"] == 0.0
    assert result["cases"]["deterministic_keyword_baseline_canonical"]["exact_match_accuracy"] == 1.0
    assert result["cases"]["deterministic_keyword_baseline_scrubbed"]["exact_match_accuracy"] == 0.125
    assert result["falsification_result"] == "TEMPLATE_DEPENDENCE_NOT_SUPPORTED_IN_THIS_FIXTURE"
    assert result["prompt_template_dependence_signal"] == 0.0


def test_v2_clean_validation_and_same_real_checkpoint() -> None:
    result = load("EMBODIED_MOTIVATION_SIGNAL_V2_RESULTS.json")
    validation = load("EMBODIED_MOTIVATION_SIGNAL_V2_VALIDATION.json")
    assert result["checkpoint"].startswith("LOCAL_ONLY:")
    assert result["training_status"] == "TRAINED_FROM_SCRATCH"
    assert validation["status"] == "PASS"
    assert validation["validated_in_clean_process"] is True
    assert all(validation["checks"].values())


def test_v2_preserves_runtime_consent_and_subjectivity_non_claims() -> None:
    result = load("EMBODIED_MOTIVATION_SIGNAL_V2_RESULTS.json")
    assert result["runtime_effect"] == "NONE"
    assert result["canonical_effect"] == "NONE"
    assert result["deployment"] is False
    assert "consent" in result["authority_boundary"]
    assert "subjectivity" in result["authority_boundary"]
