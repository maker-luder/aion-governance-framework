from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment.physiology import (
    required_physiology_system_functions,
)
from aion_astra_twin_embodiment.teacher_physiology_observability import (
    DERIVED_REFERENCE,
    DIRECT_OBSERVATION_REFERENCE,
    FUNCTIONAL_REFERENCE_ONLY,
    build_teacher_physiology_observability_profile,
    validate_teacher_physiology_observability_profile,
)


def _binding(profile, system_id: str, function_id: str):
    return next(
        item
        for item in profile.bindings
        if item.system_id == system_id and item.function_id == function_id
    )


def test_declared_physiology_function_inventory_is_exhaustively_classified() -> None:
    profile = build_teacher_physiology_observability_profile()
    result = validate_teacher_physiology_observability_profile(profile)

    expected_count = sum(
        len(functions)
        for functions in required_physiology_system_functions().values()
    )
    assert len(profile.bindings) == expected_count
    assert result["result"] == "PASS"
    assert profile.declared_function_coverage_status == (
        "COMPLETE_DECLARED_FUNCTION_INVENTORY"
    )
    assert profile.observability_scope == "DECLARED_MACHINE_REFERENCE_SURFACE_ONLY"
    assert profile.direct_observation_interpretation == (
        "DIRECT_CHANNEL_BINDING_NOT_BIOLOGICAL_MEASUREMENT"
    )
    assert profile.biological_measurement_status == "NOT_ESTABLISHED"
    assert profile.full_function_observability_status == "NOT_ESTABLISHED"
    assert profile.full_biophysical_simulation_status == "NOT_MATERIALIZED"
    assert profile.phenomenal_sensation_status == "NOT_ESTABLISHED"
    assert profile.subjectivity_status == "NOT_ESTABLISHED"

    classes = {item.observability_class for item in profile.bindings}
    assert classes == {
        DIRECT_OBSERVATION_REFERENCE,
        DERIVED_REFERENCE,
        FUNCTIONAL_REFERENCE_ONLY,
    }


def test_observability_classes_preserve_direct_derived_and_functional_only_distinctions() -> None:
    profile = build_teacher_physiology_observability_profile()

    hepatic = _binding(
        profile,
        "HEPATIC",
        "detoxification_reference",
    )
    perfusion = _binding(
        profile,
        "CARDIOVASCULAR",
        "tissue_perfusion",
    )
    spermatogenesis = _binding(
        profile,
        "REPRODUCTIVE",
        "spermatogenesis_reference",
    )

    assert hepatic.observability_class == DIRECT_OBSERVATION_REFERENCE
    assert hepatic.source_channels == ("HEPATIC_DETOXIFICATION_REFERENCE",)
    assert perfusion.observability_class == DERIVED_REFERENCE
    assert set(perfusion.source_channels) == {
        "CARDIOVASCULAR_STATE",
        "OXYGENATION_STATE",
    }
    assert spermatogenesis.observability_class == FUNCTIONAL_REFERENCE_ONLY
    assert spermatogenesis.source_channels == ()


def test_observability_inventory_rejects_missing_declared_function() -> None:
    profile = build_teacher_physiology_observability_profile()
    broken = replace(
        profile,
        bindings=tuple(
            item
            for item in profile.bindings
            if not (
                item.system_id == "RENAL_URINARY"
                and item.function_id == "glomerular_filtration_reference"
            )
        ),
    )

    with pytest.raises(ValueError, match="function inventory drift"):
        validate_teacher_physiology_observability_profile(broken)


def test_observable_function_rejects_unknown_signal_source() -> None:
    profile = build_teacher_physiology_observability_profile()
    original = _binding(
        profile,
        "HEPATIC",
        "detoxification_reference",
    )
    broken_binding = replace(
        original,
        source_channels=("UNKNOWN_SIGNAL",),
    )
    broken = replace(
        profile,
        bindings=tuple(
            broken_binding
            if item == original
            else item
            for item in profile.bindings
        ),
    )

    with pytest.raises(ValueError, match="unknown signal"):
        validate_teacher_physiology_observability_profile(broken)


def test_functional_only_reference_cannot_claim_direct_source_channels() -> None:
    profile = build_teacher_physiology_observability_profile()
    original = _binding(
        profile,
        "REPRODUCTIVE",
        "spermatogenesis_reference",
    )
    broken_binding = replace(
        original,
        source_channels=("GONADAL_ENDOCRINE_REFERENCE",),
    )
    broken = replace(
        profile,
        bindings=tuple(
            broken_binding
            if item == original
            else item
            for item in profile.bindings
        ),
    )

    with pytest.raises(ValueError, match="cannot claim source channels"):
        validate_teacher_physiology_observability_profile(broken)
