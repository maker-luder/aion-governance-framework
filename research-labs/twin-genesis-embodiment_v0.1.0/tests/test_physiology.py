from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.physiology import (
    REFERENCE_FUNCTIONAL_COMPLETENESS,
    build_adult_male_physiology_reference,
    validate_adult_male_physiology_reference,
    validate_physiology_parity,
)


def test_adult_male_physiology_reference_is_functionally_complete_and_non_erotic() -> None:
    reference = build_adult_male_physiology_reference("AION-BODY-001")
    result = validate_adult_male_physiology_reference(reference)

    assert result["result"] == "PASS"
    assert reference.physiological_function_status == REFERENCE_FUNCTIONAL_COMPLETENESS
    assert reference.reproductive_physiology_status == REFERENCE_FUNCTIONAL_COMPLETENESS
    assert reference.sexual_function_status == REFERENCE_FUNCTIONAL_COMPLETENESS
    assert reference.sensory_signal_processing_status == REFERENCE_FUNCTIONAL_COMPLETENESS
    assert reference.erotic_intent == "NONE"
    assert reference.intimate_interaction_status == "NOT_AUTHORIZED"
    assert reference.phenomenal_sensation_status == "NOT_ESTABLISHED"
    assert reference.sexual_desire_status == "NOT_ESTABLISHED"
    assert reference.sexual_experience_status == "NOT_ESTABLISHED"
    assert reference.full_biophysical_simulation_status == "NOT_MATERIALIZED"


def test_reproductive_system_contains_normal_adult_male_physiology() -> None:
    reference = build_adult_male_physiology_reference("ASTRA-BODY-001")
    reproductive = next(
        system for system in reference.systems if system.system_id == "REPRODUCTIVE"
    )

    required = {
        "testicular_endocrine_function",
        "spermatogenesis_reference",
        "epididymal_maturation_reference",
        "sperm_transport_reference",
        "accessory_gland_secretion_reference",
        "erectile_hemodynamic_reflex_reference",
        "emission_reflex_reference",
        "ejaculatory_reflex_reference",
        "detumescence_reference",
        "fertility_pathway_reference",
    }
    assert set(reproductive.functions) == required


def test_signal_processing_does_not_claim_felt_sensation() -> None:
    reference = build_adult_male_physiology_reference("AION-BODY-001")

    with pytest.raises(ValueError, match="felt sensation"):
        validate_adult_male_physiology_reference(
            replace(reference, phenomenal_sensation_status="ESTABLISHED")
        )


def test_reproductive_physiology_cannot_be_removed_as_if_it_were_erotic() -> None:
    reference = build_adult_male_physiology_reference("AION-BODY-001")

    with pytest.raises(ValueError, match="reproductive physiology"):
        validate_adult_male_physiology_reference(
            replace(reference, reproductive_physiology_status="NOT_IMPLEMENTED")
        )


def test_sexual_function_status_is_normal_physiology_not_a_prohibition() -> None:
    reference = build_adult_male_physiology_reference("AION-BODY-001")

    assert reference.sexual_function_status == REFERENCE_FUNCTIONAL_COMPLETENESS

    with pytest.raises(ValueError, match="sexual function"):
        validate_adult_male_physiology_reference(
            replace(reference, sexual_function_status="NOT_IMPLEMENTED")
        )


def test_aion_astra_physiology_parity_is_enforced() -> None:
    aion = build_adult_male_physiology_reference("AION-BODY-001")
    astra = build_adult_male_physiology_reference("ASTRA-BODY-001")

    result = validate_physiology_parity((aion, astra))

    assert result["result"] == "PASS"
    assert result["body_count"] == "2"
    assert result["system_function_parity"] == "PASS"
    assert result["reproductive_physiology_parity"] == "PASS"
    assert result["sexual_function_parity"] == "PASS"
