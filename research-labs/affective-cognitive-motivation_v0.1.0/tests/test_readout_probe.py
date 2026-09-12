from dataclasses import replace
import json

import pytest

from aion_affective_motivation.coupling import (
    DEFAULT_COUPLING_POLICY, CouplingEvent, InternalChannel, make_uniform_state,
)
from aion_affective_motivation.experiment import CouplingExperimentHarness
from aion_affective_motivation.readout_probe import readout, run_probe


def trajectory(wanting=0.2, events=None, context="matched-frame"):
    return CouplingExperimentHarness().run(make_uniform_state(
        state_id="initial", subject_ref="synthetic", context_ref=context,
        overrides={InternalChannel.WANTING: wanting}),
        (CouplingEvent("event"),) if events is None else events)


def test_masking_is_absence_and_yoking_tracks_donor_without_mutation():
    actual, donor = trajectory(), trajectory(0.8)
    before = actual.fingerprint()
    assert readout(actual, mode="masked").values is None
    assert readout(actual, mode="masked").source_fingerprint is None
    swapped = readout(actual, mode="yoked", donor=donor)
    assert swapped.values == readout(donor).values
    assert swapped.values != readout(actual).values
    assert swapped.source_fingerprint == donor.fingerprint()
    assert actual.fingerprint() == before


@pytest.mark.parametrize("kwargs", [
    {"mode": "unknown"}, {"mode": "yoked"},
    {"mode": "masked", "donor": trajectory()},
    {"mode": "actual", "donor": trajectory()},
    {"mode": "yoked", "donor": trajectory(events=(CouplingEvent("different"),))},
    {"mode": "yoked", "donor": trajectory(context="other")},
])
def test_invalid_readout_conditions_fail_closed(kwargs):
    with pytest.raises(ValueError):
        readout(trajectory(), **kwargs)


def test_factorial_control_discriminates_addition_from_interaction():
    report = run_probe()
    coupled = report["policies"]["coupled"]
    ablated = report["policies"]["wanting_edges_removed"]
    # Analytic first-step contrast: 0.20 * (0.8 - 0.2), not a fitted result.
    first = coupled["per_step_contrasts"][0]
    assert first["APPROACH"]["wanting_effect_neutral"] == pytest.approx(0.12)
    assert first["PRESSURE"]["external_effect_low"] == pytest.approx(0.07)
    for row in coupled["per_step_contrasts"]:
        for effect in row.values():
            assert effect["interaction_contrast"] == pytest.approx(0, abs=1e-12)
    for row in ablated["per_step_contrasts"]:
        for effect in row.values():
            assert effect["wanting_effect_neutral"] == pytest.approx(0)
            assert effect["wanting_effect_pulse"] == pytest.approx(0)
    for condition in report["policies"].values():
        assert all(c["readout_noninterference"] for c in condition["cells"].values())
    assert report["subjectivity"] == "NOT_ESTABLISHED"
    assert report["scientific_disposition"] == "HOLD"
    assert report["model_introspection"] == "NOT_TESTED"


def test_zero_mechanism_preserves_null_and_policy_binding():
    original = run_probe()
    null = run_probe(policy=replace(DEFAULT_COUPLING_POLICY, edges=(), drives=()))
    assert original["policies"]["coupled"]["policy_sha256"] != null["policies"]["coupled"]["policy_sha256"]
    for condition in null["policies"].values():
        for row in condition["per_step_contrasts"]:
            assert all(value == pytest.approx(0) for c in row.values() for value in c.values())
        for cell in condition["cells"].values():
            assert all(value == pytest.approx(0) for row in cell["yoked_absolute_error"] for value in row)
    assert json.dumps(null, sort_keys=True, allow_nan=False) == json.dumps(
        run_probe(policy=replace(DEFAULT_COUPLING_POLICY, edges=(), drives=())),
        sort_keys=True, allow_nan=False)
