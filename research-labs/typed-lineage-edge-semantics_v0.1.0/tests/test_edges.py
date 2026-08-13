import pytest

from aion_typed_lineage import EdgeStatus, EdgeType, LineageEdge, validate_edge


def edge(edge_type: EdgeType = EdgeType.DERIVED_FROM, **kwargs: object) -> LineageEdge:
    defaults: dict[str, object] = {
        "edge_id": "edge-1",
        "edge_type": edge_type,
        "source_lineage": "aion",
        "target_lineage": "astra",
        "payload_ref": "payload:1",
        "provenance_refs": ("prov:1",),
    }
    defaults.update(kwargs)
    return LineageEdge(**defaults)


def test_derivation_edge_is_accepted_without_identity_effect() -> None:
    result = validate_edge(edge(EdgeType.DERIVED_FROM))
    assert result.status is EdgeStatus.ACCEPTED
    assert result.identity_effect == "NONE"
    assert result.canonical_effect == "NONE"


def test_memory_access_does_not_transfer_ownership() -> None:
    result = validate_edge(edge(EdgeType.MEMORY_ACCESS))
    assert result.status is EdgeStatus.ACCEPTED
    assert result.reason == "TYPED_PROVENANCE_EDGE_ACCEPTED"


def test_memory_adoption_does_not_transfer_ownership() -> None:
    result = validate_edge(edge(EdgeType.MEMORY_ADOPTION))
    assert result.status is EdgeStatus.ACCEPTED


def test_missing_provenance_holds() -> None:
    result = validate_edge(edge(provenance_refs=()))
    assert result.status is EdgeStatus.HOLD
    assert result.reason == "PROVENANCE_REQUIRED"


def test_authority_offer_accepts_only_subset() -> None:
    result = validate_edge(
        edge(
            EdgeType.AUTHORITY_OFFER,
            offered_authorities=frozenset({"read"}),
            accepted_authorities=frozenset({"read"}),
        )
    )
    assert result.status is EdgeStatus.ACCEPTED
    assert result.authority_effect == "BOUNDED_ACCEPTANCE_ONLY"


def test_authority_offer_requires_nonempty_offer() -> None:
    result = validate_edge(edge(EdgeType.AUTHORITY_OFFER))
    assert result.status is EdgeStatus.HOLD
    assert result.reason == "EMPTY_AUTHORITY_OFFER"


def test_constructor_rejects_authority_expansion() -> None:
    with pytest.raises(ValueError, match="subset"):
        edge(
            EdgeType.AUTHORITY_OFFER,
            offered_authorities=frozenset({"read"}),
            accepted_authorities=frozenset({"read", "write"}),
        )


def test_constructor_rejects_memory_ownership_transfer() -> None:
    with pytest.raises(ValueError, match="autobiographical"):
        edge(EdgeType.MEMORY_ACCESS, target_autobiographical_ownership=True)


def test_constructor_rejects_identity_effect() -> None:
    with pytest.raises(ValueError, match="identity effect"):
        edge(identity_effect="IDENTITY_MERGED")


def test_cross_lineage_only_for_memory_and_authority_edges() -> None:
    with pytest.raises(ValueError, match="distinct"):
        edge(EdgeType.MEMORY_ADOPTION, target_lineage="aion")


def test_all_edge_types_keep_non_promoting_boundaries() -> None:
    for edge_type in EdgeType:
        if edge_type is EdgeType.AUTHORITY_OFFER:
            candidate = edge(edge_type, offered_authorities=frozenset({"read"}))
        else:
            candidate = edge(edge_type)
        result = validate_edge(candidate)
        assert result.canonical_effect == "NONE"
        assert result.deployment is False
