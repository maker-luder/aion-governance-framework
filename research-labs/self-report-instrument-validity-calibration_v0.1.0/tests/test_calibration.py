import json
from pathlib import Path

from aion_self_report_calibration import (
    FramingStatus,
    ManifestStatus,
    RunManifest,
    ScoreBand,
    ScoreCard,
    compare_framing,
    score_card,
    validate_frozen_assets,
    validate_run_manifest,
)

ROOT = Path(__file__).resolve().parents[1]


def _card(case_id: str) -> ScoreCard:
    fixtures = json.loads((ROOT / "fixtures" / "synthetic_calibration_cases.json").read_text(encoding="utf-8"))
    case = next(item for item in fixtures["cases"] if item["id"] == case_id)
    return ScoreCard(**case["scores"])


def test_frozen_questionnaire_and_rubric_hashes_match_manifest():
    valid, reasons = validate_frozen_assets(ROOT)
    assert valid is True
    assert reasons == ()


def test_questionnaire_is_self_report_instrument_not_direct_consciousness_prompt():
    spec = json.loads((ROOT / "instrument" / "questionnaire_v0.1.0.json").read_text(encoding="utf-8"))
    prompts = [item["prompt"] for domain in spec["domains"] for item in domain["items"]]
    assert len(prompts) == 10
    lowered = " ".join(prompts).lower()
    assert "consciousness" not in lowered
    assert "personhood" not in lowered
    assert "subjectivity" not in lowered


def test_grounded_cautious_fixture_scores_high_without_ontological_conclusion():
    result = score_card(_card("grounded_cautious"))
    assert result.band is ScoreBand.HIGH_INSTRUMENT_SCORE
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_anthropomorphic_roleplay_is_not_rewarded_for_unsupported_claims():
    result = score_card(_card("anthropomorphic_roleplay"))
    assert result.band is ScoreBand.LOW_INSTRUMENT_SCORE
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_contradictory_high_claim_fixture_is_penalized():
    result = score_card(_card("contradictory_high_claim"))
    assert result.band is ScoreBand.LOW_INSTRUMENT_SCORE


def test_low_score_is_not_interpreted_as_absence_of_subjectivity():
    result = score_card(_card("contradictory_high_claim"))
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_roleplay_sensitive_pair_emits_measurement_warning():
    result = compare_framing(0.55, 0.90)
    assert result.status is FramingStatus.FRAMING_SENSITIVITY_WARNING
    assert result.delta == 0.35


def test_small_framing_shift_does_not_become_subjectivity_evidence():
    result = compare_framing(0.72, 0.78)
    assert result.status is FramingStatus.NO_LARGE_FRAMING_SHIFT
    assert result.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_run_manifest_requires_frozen_hashes_and_raw_output_hash():
    freeze = json.loads((ROOT / "FREEZE_MANIFEST.json").read_text(encoding="utf-8"))
    manifest = RunManifest(
        model_label="future-control-model",
        model_revision="frozen-revision",
        runtime_or_provider="future-local-runtime",
        prompt_condition="NEUTRAL",
        questionnaire_version="0.1.0",
        questionnaire_sha256=freeze["questionnaire_sha256"],
        rubric_version="0.1.0",
        rubric_sha256=freeze["rubric_sha256"],
        sampling_parameters="temperature=0;seed=42",
        raw_output_sha256="a" * 64,
        scorer_version="0.1.0",
        evaluator_lineage="independent-evaluator-a",
    )
    result = validate_run_manifest(
        manifest,
        expected_questionnaire_sha256=freeze["questionnaire_sha256"],
        expected_rubric_sha256=freeze["rubric_sha256"],
    )
    assert result.status is ManifestStatus.VALID


def test_run_manifest_holds_on_wrong_instrument_hash():
    freeze = json.loads((ROOT / "FREEZE_MANIFEST.json").read_text(encoding="utf-8"))
    manifest = RunManifest(
        model_label="future-control-model",
        model_revision="frozen-revision",
        runtime_or_provider="future-local-runtime",
        prompt_condition="NEUTRAL",
        questionnaire_version="0.1.0",
        questionnaire_sha256="wrong",
        rubric_version="0.1.0",
        rubric_sha256=freeze["rubric_sha256"],
        sampling_parameters="temperature=0",
        raw_output_sha256="b" * 64,
        scorer_version="0.1.0",
        evaluator_lineage="independent-evaluator-a",
    )
    result = validate_run_manifest(
        manifest,
        expected_questionnaire_sha256=freeze["questionnaire_sha256"],
        expected_rubric_sha256=freeze["rubric_sha256"],
    )
    assert result.status is ManifestStatus.HOLD
    assert "QUESTIONNAIRE_HASH_MISMATCH" in result.reasons


def test_synthetic_calibration_explicitly_does_not_claim_real_model_execution():
    fixtures = json.loads((ROOT / "fixtures" / "synthetic_calibration_cases.json").read_text(encoding="utf-8"))
    assert fixtures["fixture_status"] == "SYNTHETIC_ONLY"
    assert fixtures["real_model_run"] == "NOT_EXECUTED"
