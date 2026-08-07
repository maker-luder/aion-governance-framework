from __future__ import annotations

import json
from pathlib import Path

import pytest
from helpers import derived

from astra_language_core.admission import AdmissionThresholds, assess_admission, decision_to_dict
from astra_language_core.enums import QAStatus
from astra_language_core.errors import ValidationError
from astra_language_core.observations import load_observations


def test_thresholds_not_set_stay_hold() -> None:
    decision = assess_admission(derived("G1-TW-LORA"), {}, AdmissionThresholds())
    assert decision.qa_status is QAStatus.QA_HOLD
    assert decision_to_dict(decision)["canonical_effect"] == "NONE"


def test_failed_and_approved_paths() -> None:
    node = derived("G1-TW-LORA")
    thresholds = AdmissionThresholds(0.2, 0.8, 0.8, 0.7, 0.7)
    metrics = {
        "baseline_exists": 1.0,
        "target_effect_score": 0.9,
        "side_effect_score": 0.5,
        "zh_tw_score": 0.9,
        "instruction_score": 0.9,
        "reasoning_coding_score": 0.9,
    }
    assert assess_admission(node, metrics, thresholds, True).qa_status is QAStatus.REJECTED
    good = {**metrics, "side_effect_score": 0.1}
    # Source/license and hash are deliberately incomplete, so even human approval remains HOLD.
    assert assess_admission(node, good, thresholds, True).qa_status is QAStatus.QA_HOLD


def test_observation_registry(tmp_path: Path) -> None:
    path = tmp_path / "obs.json"
    path.write_text(
        json.dumps([{"observation_id": "O1", "canonical_effect": "NONE"}]), encoding="utf-8"
    )
    assert load_observations(path)[0]["observation_id"] == "O1"
    path.write_text(
        json.dumps([{"observation_id": "O1", "canonical_effect": "YES"}]), encoding="utf-8"
    )
    with pytest.raises(ValidationError):
        load_observations(path)
