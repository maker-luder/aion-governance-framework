from __future__ import annotations

import json
from pathlib import Path

import pytest

from astra_language_core.capability_governance import (
    LANGUAGE_CORE_IS_IDENTITY_CORE,
    CapabilityArtifactRecord,
    CapabilityArtifactStatus,
    ResearchProposal,
    language_core_definition,
    proposal_from_dict,
)
from astra_language_core.errors import ValidationError
from astra_language_core.json_types import JsonValue

ROOT = Path(__file__).resolve().parents[1]
PROPOSAL_ROOT = ROOT / "capability_proposals"


def load_proposal(name: str) -> tuple[dict[str, JsonValue], ResearchProposal]:
    value: JsonValue = json.loads((PROPOSAL_ROOT / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value, proposal_from_dict(value)


def test_candidate_artifact_is_not_aion_or_astra() -> None:
    record = CapabilityArtifactRecord("G1-CANDIDATE")
    assert record.artifact_status is CapabilityArtifactStatus.CANDIDATE_ARTIFACT
    assert record.may_be_called_aion_or_astra() is False


def test_approved_artifact_does_not_inherit_identity() -> None:
    record = CapabilityArtifactRecord(
        "G1-APPROVED-CANDIDATE",
        artifact_status=CapabilityArtifactStatus.APPROVED_CAPABILITY_ARTIFACT,
    )
    assert record.identity_inheritance == "DENIED"


def test_approved_artifact_does_not_write_canonical() -> None:
    with pytest.raises(ValidationError):
        CapabilityArtifactRecord("BAD", canonical_effect="WRITE")


def test_approved_artifact_requires_owner_and_gates() -> None:
    record = CapabilityArtifactRecord("G1")
    assert record.may_promote(all_gates_passed=True, owner_approved=False) is False
    assert record.may_promote(all_gates_passed=False, owner_approved=True) is False
    assert record.may_promote(all_gates_passed=True, owner_approved=True) is True


def test_language_core_is_language_component_not_identity_core() -> None:
    definition = language_core_definition()
    assert definition["classification"] == "LANGUAGE_CAPABILITY_LAYER"
    assert definition["alternate_classification"] == "LANGUAGE_PROCESSING_COMPONENT"
    assert LANGUAGE_CORE_IS_IDENTITY_CORE is False


def test_japanese_proposal_does_not_start_training() -> None:
    data, proposal = load_proposal("AION-LANGUAGE-SPECIALIZATION-JA-001.json")
    assert proposal.side_effects() == {key: False for key in proposal.side_effects()}
    assert data["dataset"] == "NOT_CREATED"
    assert data["training"] == "NOT_STARTED"


def test_japanese_preference_origin_remains_not_established() -> None:
    _, proposal = load_proposal("AION-LANGUAGE-SPECIALIZATION-JA-001.json")
    assert proposal.preference_origin == "NOT_ESTABLISHED"
    assert proposal.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_astra_scope_hold_is_owner_resource_decision() -> None:
    data, proposal = load_proposal("ASTRA-ADDITIONAL-LANGUAGE-SPECIALIZATION-HOLD-001.json")
    assert proposal.status.value == "SCOPE_HOLD"
    assert data["decision_origin"] == "OWNER_SCOPE_AND_RESOURCE_DECISION"
    assert data["astra_autonomous_refusal"] is False


def test_aion_qa_proposal_cannot_approve() -> None:
    data, _ = load_proposal("AION-QA-ADMIN-CAPABILITY-001.json")
    assert "APPROVE" in data["prohibited_authorities"]


def test_aion_qa_proposal_cannot_release_qa_hold() -> None:
    data, proposal = load_proposal("AION-QA-ADMIN-CAPABILITY-001.json")
    assert "REMOVE_QA_HOLD" in data["prohibited_authorities"]
    assert proposal.qa_status == "QA_HOLD"


def test_aion_qa_proposal_cannot_release() -> None:
    data, _ = load_proposal("AION-QA-ADMIN-CAPABILITY-001.json")
    assert "RELEASE" in data["prohibited_authorities"]


def test_aion_qa_proposal_cannot_modify_canonical() -> None:
    data, proposal = load_proposal("AION-QA-ADMIN-CAPABILITY-001.json")
    assert "CANONICAL_WRITE" in data["prohibited_authorities"]
    assert proposal.canonical_effect == "NONE"


def test_role_separation_is_only_an_architecture_proposal() -> None:
    _, proposal = load_proposal("AION-ASTRA-OWNER-ROLE-SEPARATION-001.json")
    assert proposal.status.value == "ARCHITECTURE_PROPOSAL"
    assert proposal.implementation == "NOT_STARTED"
    assert proposal.canonical_effect == "NONE"


def test_all_research_proposals_require_human_approval_and_no_effects() -> None:
    files = sorted(PROPOSAL_ROOT.glob("*.json"))
    assert len(files) == 4
    for path in files:
        value: JsonValue = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
        proposal = proposal_from_dict(value)
        assert proposal.human_approval_required is True
        assert proposal.may_promote(owner_approved=False) is False
        assert all(effect is False for effect in proposal.side_effects().values())
        assert proposal.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_invalid_proposal_side_effect_is_rejected() -> None:
    data, _ = load_proposal("AION-LANGUAGE-SPECIALIZATION-JA-001.json")
    triggers = data["execution_triggers"]
    assert isinstance(triggers, dict)
    triggers["training"] = True
    with pytest.raises(ValidationError):
        proposal_from_dict(data)


def test_invalid_proposal_without_human_approval_is_rejected() -> None:
    data, _ = load_proposal("AION-LANGUAGE-SPECIALIZATION-JA-001.json")
    data["human_approval_required"] = False
    with pytest.raises(ValidationError):
        proposal_from_dict(data)


def test_yaml_mirrors_and_schema_are_present() -> None:
    assert len(list(PROPOSAL_ROOT.glob("*.yaml"))) == 4
    schema = json.loads((ROOT / "schemas" / "research_proposal.schema.json").read_text(encoding="utf-8"))
    assert schema["title"] == "AION/Astra Research Proposal"
    assert schema["properties"]["canonical_effect"]["const"] == "NONE"
