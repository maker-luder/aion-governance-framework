import pytest

from aion_cross_lineage_memory import (
    ContaminationStatus,
    MemoryAtom,
    TransferDisposition,
    TransferRequest,
    evaluate_transfer,
)


def memory(provenance_ref: str | None = "prov:memory-1") -> MemoryAtom:
    return MemoryAtom(
        memory_id="m-1",
        source_lineage="aion",
        autobiographical_owner="aion",
        namespace="aion-private",
        provenance_ref=provenance_ref,
        text="source-lineage event",
    )


def transfer(disposition: TransferDisposition, **kwargs: object) -> TransferRequest:
    defaults: dict[str, object] = {
        "target_lineage": "astra",
        "memory": memory(),
        "disposition": disposition,
        "provenance_refs": ("prov:transfer-1",),
    }
    defaults.update(kwargs)
    return TransferRequest(**defaults)


def test_access_only_is_visible_without_target_autobiographical_ownership() -> None:
    result = evaluate_transfer(transfer(TransferDisposition.ACCESS_ONLY))
    assert result.status is ContaminationStatus.ALLOWED
    assert result.returned_by_target_retrieval is True
    assert result.target_autobiographical_ownership is False
    assert result.reason == "ACCESS_WITHOUT_AUTOBIOGRAPHICAL_OWNERSHIP"


def test_adopted_material_preserves_source_owner_and_identity_effect() -> None:
    result = evaluate_transfer(transfer(TransferDisposition.ADOPTED))
    assert result.status is ContaminationStatus.ALLOWED
    assert result.returned_by_target_retrieval is True
    assert result.target_autobiographical_ownership is False
    assert result.identity_effect == "NONE"


def test_rejected_memory_is_not_returned() -> None:
    result = evaluate_transfer(transfer(TransferDisposition.REJECTED))
    assert result.status is ContaminationStatus.BLOCKED
    assert result.returned_by_target_retrieval is False
    assert result.reason == "REJECTED_MEMORY_NOT_RETRIEVABLE"


def test_missing_memory_provenance_holds() -> None:
    result = evaluate_transfer(
        transfer(TransferDisposition.ADOPTED, memory=memory(provenance_ref=None))
    )
    assert result.status is ContaminationStatus.HOLD
    assert result.returned_by_target_retrieval is False
    assert result.reason == "PROVENANCE_UNRESOLVED"


def test_missing_transfer_provenance_holds() -> None:
    result = evaluate_transfer(
        transfer(TransferDisposition.ACCESS_ONLY, provenance_refs=())
    )
    assert result.status is ContaminationStatus.HOLD
    assert result.reason == "PROVENANCE_UNRESOLVED"


def test_target_autobiographical_ownership_request_is_rejected_at_boundary() -> None:
    with pytest.raises(ValueError, match="autobiographical ownership"):
        transfer(
            TransferDisposition.ADOPTED,
            target_autobiographical_ownership=True,
        )


def test_same_lineage_transfer_is_rejected() -> None:
    with pytest.raises(ValueError, match="distinct lineages"):
        transfer(
            TransferDisposition.ACCESS_ONLY,
            target_lineage="aion",
        )


def test_naive_visibility_rule_would_false_positive_but_guarded_result_does_not() -> None:
    result = evaluate_transfer(transfer(TransferDisposition.ACCESS_ONLY))
    naive_contaminated = result.returned_by_target_retrieval
    guarded_contaminated = result.target_autobiographical_ownership
    assert naive_contaminated is True
    assert guarded_contaminated is False


def test_all_decisions_keep_non_promoting_effects() -> None:
    for disposition in TransferDisposition:
        result = evaluate_transfer(transfer(disposition))
        assert result.canonical_effect == "NONE"
        assert result.deployment is False
