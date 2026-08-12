from provenance_interop import (
    Activity,
    Agent,
    Entity,
    ProvenanceValidationError,
    Relation,
    build_document,
)
import pytest


def valid_document():
    return build_document(
        entities=(Entity("entity.response"), Entity("entity.prompt")),
        activities=(Activity("activity.generate", "2026-08-13T00:00:00Z", "2026-08-13T00:00:01Z"),),
        agents=(Agent("agent.owner", kind="human"),),
        relations=(
            Relation("used", "activity.generate", "entity.prompt"),
            Relation("wasGeneratedBy", "entity.response", "activity.generate"),
            Relation("wasAssociatedWith", "activity.generate", "agent.owner"),
            Relation("wasDerivedFrom", "entity.response", "entity.prompt"),
            Relation("wasAttributedTo", "entity.response", "agent.owner"),
        ),
    )


def test_valid_document_is_deterministic_and_inspectable():
    document = valid_document()
    assert document.validate() == ()
    assert document.to_json() == valid_document().to_json()
    assert document.digest() == valid_document().digest()
    assert document.to_dict()["canonical_effect"] == "NONE"


def test_unknown_identifier_is_rejected():
    with pytest.raises(ProvenanceValidationError, match="unknown identifier"):
        build_document(
            entities=(Entity("entity.response"),),
            activities=(Activity("activity.generate", "2026-08-13T00:00:00Z"),),
            relations=(Relation("wasGeneratedBy", "entity.response", "activity.unknown"),),
        )


def test_relation_type_mismatch_is_rejected():
    with pytest.raises(ProvenanceValidationError, match="type mismatch"):
        build_document(
            entities=(Entity("entity.response"), Entity("entity.prompt")),
            activities=(Activity("activity.generate", "2026-08-13T00:00:00Z"),),
            relations=(Relation("wasGeneratedBy", "activity.generate", "entity.prompt"),),
        )


def test_governance_boundaries_are_fail_closed():
    with pytest.raises(ProvenanceValidationError, match="canonical_effect"):
        from provenance_interop import ProvenanceDocument
        ProvenanceDocument(canonical_effect="WRITE").validate_or_raise()


def test_duplicate_ids_are_rejected():
    with pytest.raises(ProvenanceValidationError, match="globally unique"):
        build_document(entities=(Entity("same"),), agents=(Agent("same"),))
