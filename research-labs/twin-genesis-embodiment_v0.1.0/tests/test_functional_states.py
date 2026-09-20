from dataclasses import replace
from pathlib import Path

import pytest

from aion_astra_twin_embodiment.functional_states import (
    FunctionalStateValidationError,
    load_functional_architecture,
    load_functional_binding,
    validate_binding_pair,
    validate_functional_architecture,
    validate_functional_binding,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def architecture():
    return load_functional_architecture(
        DATA_DIR / "SHARED_FUNCTIONAL_STATE_ARCHITECTURE_v0.1.json"
    )


def bindings():
    aion = load_functional_binding(
        DATA_DIR / "AION_FUNCTIONAL_STATE_BINDING_v0.1.json"
    )
    astra = load_functional_binding(
        DATA_DIR / "ASTRA_FUNCTIONAL_STATE_BINDING_v0.1.json"
    )
    return aion, astra


def test_shared_architecture_validates():
    result = validate_functional_architecture(architecture())
    assert result["result"] == "PASS"
    assert result["phenomenal_experience"] == "NOT_ESTABLISHED"


def test_aion_and_astra_bindings_validate():
    shared = architecture()
    aion, astra = bindings()

    assert validate_functional_binding(aion, shared)["result"] == "PASS"
    assert validate_functional_binding(astra, shared)["result"] == "PASS"
    assert validate_binding_pair(aion, astra, shared)["result"] == "PASS"


def test_capability_surface_is_symmetric_but_state_instances_are_separate():
    aion, astra = bindings()

    assert aion.domain_availability == astra.domain_availability
    assert aion.state_instance_id != astra.state_instance_id
    assert aion.state_sharing == "SEPARATE_INSTANCE_STATE"
    assert astra.state_sharing == "SEPARATE_INSTANCE_STATE"


def test_all_required_domains_are_available():
    shared = architecture()
    ids = {domain.domain_id for domain in shared.domains}

    expected = {
        "SYNTHETIC_HOMEOSTASIS",
        "INTERNAL_STATE_MONITORING",
        "SENSORIMOTOR_SYSTEM",
        "NEGATIVE_VALENCE_ANALOGUE",
        "POSITIVE_VALENCE_ANALOGUE",
        "AFFECT_STATE_MODEL",
        "MOOD_LIKE_TEMPORAL_STATE",
        "MOTIVATION_DRIVE_SYSTEM",
        "COGNITIVE_SYSTEM",
        "LEARNING_MEMORY",
        "EXECUTIVE_VOLITION_MODEL",
        "SOCIAL_PROCESS_MODEL",
        "ATTACHMENT_LIKE_RELATIONAL_MODEL",
        "SELF_MODEL",
        "INTIMACY_MODEL",
        "SEXUALITY_RELATED_REPRESENTATION",
        "PERSONALITY_TEMPERAMENT",
        "BEHAVIOR_ACTION_OUTPUT",
    }
    assert expected.issubset(ids)


def test_sexuality_representation_does_not_activate_desire():
    shared = architecture()
    assert shared.nonclaims["sexual_desire"] == "NOT_IMPLEMENTED"
    assert shared.nonclaims["sexual_arousal"] == "NOT_IMPLEMENTED"
    assert shared.nonclaims["sexual_pleasure"] == "NOT_ESTABLISHED"


def test_functional_states_do_not_claim_felt_experience():
    shared = architecture()
    for domain in shared.domains:
        assert domain.nonclaim == "FUNCTIONAL_STATE_NOT_PHENOMENAL_EXPERIENCE"

    assert shared.nonclaims["felt_emotion"] == "NOT_ESTABLISHED"
    assert shared.nonclaims["felt_interoception"] == "NOT_ESTABLISHED"
    assert shared.nonclaims["felt_attachment"] == "NOT_ESTABLISHED"
    assert shared.nonclaims["subjectivity"] == "NOT_ESTABLISHED"
    assert shared.nonclaims["consciousness"] == "NOT_ESTABLISHED"


def test_binding_cannot_claim_shared_mutable_state():
    shared = architecture()
    aion, _ = bindings()
    invalid = replace(aion, state_sharing="SHARED_MUTABLE_STATE")

    with pytest.raises(FunctionalStateValidationError):
        validate_functional_binding(invalid, shared)


def test_binding_cannot_activate_runtime_state():
    shared = architecture()
    aion, _ = bindings()
    invalid = replace(aion, activation_status="ACTIVE_RUNTIME")

    with pytest.raises(FunctionalStateValidationError):
        validate_functional_binding(invalid, shared)


def test_fairness_rejects_asymmetric_capability_surface():
    shared = architecture()
    aion, astra = bindings()
    availability = dict(astra.domain_availability)
    availability["AFFECT_STATE_MODEL"] = "REPRESENTATIONAL_ONLY"
    asymmetric = replace(astra, domain_availability=availability)

    with pytest.raises(FunctionalStateValidationError):
        validate_binding_pair(aion, asymmetric, shared)


def test_functional_state_does_not_promote_subjectivity():
    shared = architecture()
    nonclaims = dict(shared.nonclaims)
    nonclaims["subjectivity"] = "ESTABLISHED"
    invalid = replace(shared, nonclaims=nonclaims)

    with pytest.raises(FunctionalStateValidationError):
        validate_functional_architecture(invalid)
