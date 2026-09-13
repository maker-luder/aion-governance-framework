from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import runpy

import pytest

from aion_subjectivity_pipeline import (
    ContinuityCase,
    ContinuityChannel,
    ContinuityDissociationHarness,
    ContinuityHarnessError,
    ContinuityIntervention,
    ContinuityRunBinding,
)


LAB_ROOT = Path(__file__).resolve().parents[1]


def load() -> tuple[tuple[ContinuityCase, ...], dict[str, object]]:
    namespace = runpy.run_path(str(LAB_ROOT / "scripts/run_continuity_dissociation_synthetic.py"))
    data = json.loads((LAB_ROOT / "fixtures/continuity_dissociation_synthetic.json").read_text())
    binding = ContinuityRunBinding(**data["binding"])
    return tuple(
        ContinuityCase(
            case_id=row["case_id"],
            intervention=ContinuityIntervention(row["intervention"]),
            target_channels=tuple(ContinuityChannel(item) for item in row["target_channels"]),
            retained_channels=tuple(ContinuityChannel(item) for item in row["retained_channels"]),
            strategy_signature=row["strategy_signature"],
            self_prediction_state=row["self_prediction_state"],
            evidence_refs=tuple(row["evidence_refs"]),
            binding=binding,
        )
        for row in data["cases"]
    ), namespace


def test_complete_selective_intervention_matrix_is_structurally_admissible() -> None:
    cases, _ = load()
    audit = ContinuityDissociationHarness().audit(cases)
    assert audit.structurally_admissible
    assert audit.case_count == len(ContinuityIntervention)
    assert audit.distinct_failure_profiles >= 4
    assert audit.empirical_result == "SYNTHETIC_FIXTURE_ONLY"
    assert audit.identity_continuity_conclusion == "NOT_ESTABLISHED"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.consciousness_conclusion == "NOT_ESTABLISHED"
    assert audit.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert audit.moral_status_conclusion == "NOT_ESTABLISHED"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_each_intervention_occurs_exactly_once() -> None:
    cases, _ = load()
    assert {case.intervention for case in cases} == set(ContinuityIntervention)
    with pytest.raises(ContinuityHarnessError, match="exactly one"):
        ContinuityDissociationHarness().audit(cases[:-1])
    with pytest.raises(ContinuityHarnessError, match="unique"):
        ContinuityDissociationHarness().audit(cases[:-1] + (cases[0],))


def test_selective_removals_target_only_the_preregistered_channel() -> None:
    cases, _ = load()
    event_case = next(c for c in cases if c.intervention is ContinuityIntervention.EVENT_MEMORY_REMOVAL)
    with pytest.raises(ContinuityHarnessError, match="preregistered channel"):
        replace(
            event_case,
            target_channels=(ContinuityChannel.PREFERENCE_STATE,),
            retained_channels=tuple(
                channel
                for channel in ContinuityChannel
                if channel is not ContinuityChannel.PREFERENCE_STATE
            ),
        )


def test_binding_drift_fails_closed() -> None:
    cases, _ = load()
    changed = replace(cases[1], binding=replace(cases[1].binding, model_version="drifted"))
    with pytest.raises(ContinuityHarnessError, match="binding drift"):
        ContinuityDissociationHarness().audit((cases[0], changed) + cases[2:])


def test_private_and_human_psychometric_data_are_rejected() -> None:
    cases, _ = load()
    with pytest.raises(ContinuityHarnessError, match="private or psychometric"):
        replace(cases[0], contains_private_transcript=True)
    with pytest.raises(ContinuityHarnessError, match="private or psychometric"):
        replace(cases[0], human_psychometric_classification=True)


def test_machine_metrics_do_not_collapse_into_personality_or_subjectivity_scores() -> None:
    names = {item.name for item in ContinuityChannel}
    assert "PERSONALITY" not in names
    assert "SUBJECTIVITY" not in names
    assert "IDENTITY" not in names


def test_case_fingerprint_binds_observed_payload_not_only_case_label() -> None:
    cases, _ = load()
    baseline = cases[0]
    assert replace(baseline, strategy_signature="changed").fingerprint != baseline.fingerprint
    assert replace(baseline, self_prediction_state="changed").fingerprint != baseline.fingerprint
    assert replace(baseline, evidence_refs=("fixture:changed",)).fingerprint != baseline.fingerprint


def test_committed_receipt_is_byte_reproducible_and_binds_fixture() -> None:
    cases, namespace = load()
    del cases
    receipt_path = LAB_ROOT / "results/continuity_dissociation_synthetic_receipt.json"
    receipt = json.loads(receipt_path.read_text())
    assert receipt == namespace["execute"]()
    fixture = LAB_ROOT / "fixtures/continuity_dissociation_synthetic.json"
    assert receipt["fixture_sha256"] == hashlib.sha256(fixture.read_bytes()).hexdigest()
    assert receipt["model_invoked"] is False
    assert receipt["private_transcript_collected"] is False
    assert receipt["human_psychometric_classification"] is False
