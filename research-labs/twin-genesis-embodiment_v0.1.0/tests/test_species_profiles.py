from __future__ import annotations

from dataclasses import replace

import pytest

from aion_astra_twin_embodiment import EmbodimentInstance, ValidationError
from aion_astra_twin_embodiment.species_profiles import (
    BIPEDAL_REDESIGN_REQUIRED,
    ENGINEERING_ANALOGUE,
    REFERENCE_MODEL_IMPLEMENTED,
    REFERENCE_ONLY_NOT_LIVE_BIOLOGY,
    build_aion_tiger_profile,
    build_tiger_reproductive_reference_observations,
    validate_aion_tiger_profile,
)


def aion_instance(profile_id: str) -> EmbodimentInstance:
    return EmbodimentInstance(
        embodiment_id="AION-TIGER-BODY-001",
        agent_id="AION",
        instance_id="AION-I-001",
        template_id="MALE-TEMPLATE-001",
        memory_namespace="AION_PRIVATE_EPISODIC_MEMORY",
        canonical_state_reference="AION_CANONICAL",
        species_profile_id=profile_id,
    )


def test_aion_tiger_profile_is_an_individual_anthropomorphic_adapter():
    profile = build_aion_tiger_profile()
    assert profile.agent_id == "AION"
    assert profile.reference_taxon == "Panthera tigris"
    assert profile.body_plan == "ANTHROPOMORPHIC_BIPED"
    assert profile.hybrid_integration_evidence_status == ENGINEERING_ANALOGUE
    assert profile.locomotor_translation_status == BIPEDAL_REDESIGN_REQUIRED


def test_tiger_confirmed_reproductive_anatomy_does_not_copy_human_seminal_vesicles():
    profile = build_aion_tiger_profile()
    assert "os_penis" in profile.tiger_confirmed_reproductive_anatomy
    assert "cornified_glans_papillae" in profile.tiger_confirmed_reproductive_anatomy
    assert "penile_urethra" in profile.tiger_confirmed_reproductive_anatomy
    assert "seminal_vesicles" not in profile.tiger_confirmed_reproductive_anatomy


def test_reproductive_physiology_is_implemented_as_reference_model_not_live_biology():
    profile = build_aion_tiger_profile()
    assert profile.reproductive_physiology_model_status == REFERENCE_MODEL_IMPLEMENTED
    assert profile.reproductive_runtime_status == REFERENCE_ONLY_NOT_LIVE_BIOLOGY
    assert profile.sexual_function_status == "NOT_IMPLEMENTED"
    assert profile.body_sensation == "NOT_ESTABLISHED"


def test_aion_tiger_profile_binding_validates_and_hashes():
    profile = build_aion_tiger_profile()
    result = validate_aion_tiger_profile(profile, aion_instance(profile.profile_id))
    assert result["result"] == "PASS"
    assert len(result["profile_hash"]) == 64


def test_profile_cannot_be_rebound_to_astra():
    profile = build_aion_tiger_profile()
    astra = replace(
        aion_instance(profile.profile_id),
        embodiment_id="ASTRA-BODY-001",
        agent_id="ASTRA",
        instance_id="ASTRA-I-001",
        memory_namespace="ASTRA_PRIVATE",
        canonical_state_reference="ASTRA_CANONICAL",
    )
    with pytest.raises(ValidationError):
        validate_aion_tiger_profile(profile, astra)


def test_profile_id_mismatch_is_rejected():
    profile = build_aion_tiger_profile()
    with pytest.raises(ValidationError):
        validate_aion_tiger_profile(profile, aion_instance("OTHER-PROFILE"))


def test_reproductive_measurements_keep_source_scope_and_limitations():
    observations = build_tiger_reproductive_reference_observations()
    case_report = observations[0]
    assert ("right_testis_length_cm", "4.42") in case_report.metrics
    assert ("penile_urethra_diameter_mm", "1.73") in case_report.metrics
    assert "single-specimen" in case_report.limitation
