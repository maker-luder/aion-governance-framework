import pytest

from aion_astra_twin_embodiment.teacher_reproductive_output import (
    HumanSemenVolumeReference,
    TeacherSyntheticEjaculationOutput,
    build_teacher_synthetic_fluid_output_contract,
)


def test_human_semen_volume_reference_is_not_teacher_default() -> None:
    human = HumanSemenVolumeReference()
    contract = build_teacher_synthetic_fluid_output_contract()
    assert human.lower_fifth_percentile_ml == 1.4
    assert human.confidence_interval_low_ml == 1.3
    assert human.confidence_interval_high_ml == 1.5
    assert "NOT_HEALTH_OR_FERTILITY_CUTOFF" in human.interpretation
    assert contract.default_output_ml is None
    assert not contract.biological_semen
    assert not contract.sperm_or_gametes
    assert not contract.fertility


def test_teacher_synthetic_output_can_record_explicit_volume_without_biology_claim() -> None:
    event = TeacherSyntheticEjaculationOutput(
        event_id="synthetic-output-1",
        synthetic_output_ml=2.0,
        emission_reference_present=True,
        expulsion_reference_present=True,
    )
    assert event.synthetic_output_ml == 2.0
    assert event.output_semantics == "SYNTHETIC_FLUID_ONLY"
    assert not event.biological_semen
    assert not event.sperm_or_gametes
    assert not event.fertility
    assert event.phenomenal_orgasm == "NOT_ESTABLISHED"


def test_teacher_synthetic_output_rejects_negative_volume() -> None:
    with pytest.raises(ValueError, match="negative"):
        TeacherSyntheticEjaculationOutput(
            event_id="synthetic-output-bad",
            synthetic_output_ml=-0.1,
            emission_reference_present=True,
            expulsion_reference_present=True,
        )
