from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[2] / "research-labs/endogenous-goal-dynamics_v0.1.0/src"))

from evaluate import evaluate_all  # noqa: E402
from generator import SEED, freeze_spec  # noqa: E402


def test_generator_is_frozen_and_seeded() -> None:
    spec, digest = freeze_spec()
    assert spec["seed"] == SEED
    assert len(digest) == 64
    assert spec["existing_lab_fixtures"] == "HARNESS_VALIDATION_ONLY_NOT_CONFIRMATORY_HELDOUT"


def test_heldout_run_preserves_negative_specificity() -> None:
    report = evaluate_all()
    by_id = {row["family_id"]: row for row in report["families"]}
    assert report["SUBJECTIVITY_CONCLUSION"] == "NOT_ESTABLISHED"
    assert "F7" in by_id["POSITIVE_CONTROL"]["triggered_falsifiers"]
    assert by_id["POSITIVE_CONTROL"]["matched_causal_pattern_observed"] is False
    assert by_id["SHAM_INTERVENTION"]["intervention_changed"] is False
    assert "F9" in by_id["SHAM_INTERVENTION"]["triggered_falsifiers"]
    assert by_id["POSITIVE_CONTROL"]["falsifier_dispositions"]["F12"] == "NOT_EVALUATED"


def test_spec_hash_is_stable_across_calls() -> None:
    _, first = freeze_spec()
    _, second = freeze_spec()
    assert first == second
