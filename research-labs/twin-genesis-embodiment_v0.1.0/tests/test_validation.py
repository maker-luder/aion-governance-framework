import json
from dataclasses import replace
from pathlib import Path

import pytest

from aion_astra_twin_embodiment.models import (
    EmbodimentInstance,
    EmbodimentTemplate,
    SharedGenesisEvent,
)
from aion_astra_twin_embodiment.validation import ValidationError, deterministic_hash, validate_candidate


def valid_objects():
    event = SharedGenesisEvent(
        genesis_event_id="GENESIS-001",
        shared_root_id="ROOT-001",
        aion_agent_id="AION",
        astra_agent_id="ASTRA",
        aion_instance_id="AION-I-001",
        astra_instance_id="ASTRA-I-001",
        source_artifact_hash="0" * 64,
    )
    template = EmbodimentTemplate(template_id="MALE-TEMPLATE-001", template_version="0.1.0")
    aion = EmbodimentInstance(
        embodiment_id="AION-BODY-001",
        agent_id="AION",
        instance_id="AION-I-001",
        template_id=template.template_id,
        memory_namespace="AION_PRIVATE_EPISODIC_MEMORY",
        canonical_state_reference="AION_CANONICAL",
        modification_authorities=("OWNER_APPROVAL_REFERENCE",),
    )
    astra = EmbodimentInstance(
        embodiment_id="ASTRA-BODY-001",
        agent_id="ASTRA",
        instance_id="ASTRA-I-001",
        template_id=template.template_id,
        memory_namespace="ASTRA_RESEARCH_EPISODIC_MEMORY",
        canonical_state_reference="ASTRA_CANONICAL",
        modification_authorities=("OWNER_APPROVAL_REFERENCE",),
    )
    return event, template, aion, astra


def test_valid_shared_template_independent_instances():
    result = validate_candidate(*valid_objects())
    assert result["result"] == "PASS"


def test_same_agent_id_rejected():
    event, template, aion, astra = valid_objects()
    bad = replace(event, astra_agent_id=event.aion_agent_id)
    with pytest.raises(ValidationError):
        validate_candidate(bad, template, aion, astra)


def test_same_instance_id_rejected():
    event, template, aion, astra = valid_objects()
    bad = replace(event, astra_instance_id=event.aion_instance_id)
    with pytest.raises(ValidationError):
        validate_candidate(bad, template, aion, astra)


def test_same_embodiment_id_rejected():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, template, aion, replace(astra, embodiment_id=aion.embodiment_id))


def test_same_private_memory_namespace_rejected():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, template, aion, replace(astra, memory_namespace=aion.memory_namespace))


def test_minor_template_rejected():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, replace(template, adult_status=False), aion, astra)


def test_anatomy_does_not_assign_gender_identity():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, replace(template, gender_identity_effect="ASSIGNED"), aion, astra)


def test_anatomy_does_not_change_subjectivity():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, replace(template, subjectivity_effect="ESTABLISHED"), aion, astra)


def test_sexual_function_out_of_scope():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, replace(template, sexual_function_status="IMPLEMENTED"), aion, astra)


def test_relationship_cannot_authorize_modification():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, template, replace(aion, modification_authorities=("relationship",)), astra)


def test_live_runtime_rejected():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, template, replace(aion, runtime_binding="ACTIVE"), astra)


def test_body_sensation_must_remain_not_established():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, template, replace(aion, body_sensation="ESTABLISHED"), astra)


def test_sexual_interaction_not_authorized():
    event, template, aion, astra = valid_objects()
    with pytest.raises(ValidationError):
        validate_candidate(event, template, replace(aion, sexual_interaction="AUTHORIZED"), astra)


def test_hash_is_deterministic():
    assert deterministic_hash({"b": 2, "a": 1}) == deterministic_hash({"a": 1, "b": 2})


def test_status_lock_matches_non_3d_runtime_candidate() -> None:
    root = Path(__file__).resolve().parents[1]
    lock = json.loads((root / "qa" / "CANDIDATE_STATUS_LOCK.json").read_text(encoding="utf-8"))
    cli_status = json.loads((root / "qa" / "CLI_QA_STATUS.json").read_text(encoding="utf-8"))
    assert lock["status"] == "IMPLEMENTED_NON_3D_CANDIDATE_PENDING_OWNER_REVIEW"
    assert lock["embodiment_runtime"] == "NON_3D_RECORD_RUNTIME_IMPLEMENTED"
    assert lock["live_3d_runtime"] == "NOT_IMPLEMENTED"
    assert cli_status["runtime"] == lock["embodiment_runtime"]
    assert lock["subjectivity_conclusion"] == "NOT_ESTABLISHED"
    assert lock["canonical_effect"] == "NONE"
