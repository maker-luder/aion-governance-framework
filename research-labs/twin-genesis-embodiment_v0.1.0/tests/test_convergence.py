from __future__ import annotations

from dataclasses import replace
import importlib.util
import json
from pathlib import Path

import pytest

import aion_astra_twin_embodiment.convergence as convergence
from aion_astra_twin_embodiment.convergence import (
    AdoptionStatus,
    ConvergenceClassification,
    convergence_ledger_hash,
    load_convergence_ledger,
    validate_convergence_ledger,
)


ROOT = Path(__file__).parents[1]
LEDGER_PATH = ROOT / "data" / "EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_v0.1.json"
SCHEMA_PATH = (
    ROOT / "schemas" / "EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_SCHEMA.json"
)

EXPECTED_HEADS = {
    190: "066ed1afccebee869eb658c09691b7f096694332",
    191: "48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2",
    192: "861e6a556a21afffd04b187714c0608fe73ea4fc",
}


def test_convergence_module_exists_for_archive_classification_contract() -> None:
    assert (
        importlib.util.find_spec("aion_astra_twin_embodiment.convergence")
        is not None
    ), "convergence module must exist before archive classifications can be loaded"


@pytest.mark.parametrize(
    "name",
    (
        "ConvergenceClassification",
        "AdoptionStatus",
        "ArchiveDisposition",
        "ConvergenceLedger",
        "load_convergence_ledger",
        "convergence_ledger_hash",
        "validate_convergence_ledger",
    ),
)
def test_convergence_public_contract_surface_exists(name: str) -> None:
    assert hasattr(convergence, name), f"missing convergence contract surface: {name}"


@pytest.mark.parametrize(
    "relative_path",
    (
        "data/EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_v0.1.json",
        "schemas/EMBODIMENT_ARCHIVE_CONVERGENCE_LEDGER_SCHEMA.json",
    ),
)
def test_convergence_contract_artifacts_exist(relative_path: str) -> None:
    assert (ROOT / relative_path).is_file(), f"missing convergence artifact: {relative_path}"


def test_archive_ledger_loads_typed_entries_and_exact_source_heads() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    assert ledger.entries
    assert {entry.source_pr for entry in ledger.entries} == {190, 191, 192}
    assert all(
        entry.source_head == EXPECTED_HEADS[entry.source_pr]
        for entry in ledger.entries
    )
    assert all(
        isinstance(entry.classification, ConvergenceClassification)
        for entry in ledger.entries
    )
    assert all(isinstance(entry.adoption_status, AdoptionStatus) for entry in ledger.entries)
    assert {
        entry.classification for entry in ledger.entries
    } == set(ConvergenceClassification)
    assert {
        entry.adoption_status for entry in ledger.entries
    } == set(AdoptionStatus)


def test_archive_ledger_validates_exact_frozen_source_heads() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    result = validate_convergence_ledger(ledger)
    assert result["result"] == "PASS"
    assert result["source_heads"] == "PASS"
    assert result["classification_partition"] == "PASS"
    assert result["boundary_lock"] == "PASS"


def test_archive_ledger_rejects_source_head_drift() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    entries = list(ledger.entries)
    entries[0] = replace(entries[0], source_head="0" * 40)
    with pytest.raises(ValueError, match="exact archive head"):
        validate_convergence_ledger(replace(ledger, entries=tuple(entries)))


def test_archive_ledger_rejects_duplicate_semantic_unit() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    duplicate = (*ledger.entries, ledger.entries[0])
    with pytest.raises(ValueError, match="duplicate"):
        validate_convergence_ledger(replace(ledger, entries=duplicate))


def test_superseded_entry_requires_replacement_reference() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    index = next(
        i
        for i, item in enumerate(ledger.entries)
        if item.classification is ConvergenceClassification.SUPERSEDED
    )
    entries = list(ledger.entries)
    entries[index] = replace(entries[index], replacement_ref_if_superseded=None)
    with pytest.raises(ValueError, match="replacement"):
        validate_convergence_ledger(replace(ledger, entries=tuple(entries)))


def test_archive_only_requires_historical_only_status() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    index = next(
        i
        for i, item in enumerate(ledger.entries)
        if item.classification is ConvergenceClassification.ARCHIVE_ONLY
    )
    entries = list(ledger.entries)
    entries[index] = replace(entries[index], adoption_status=AdoptionStatus.ADOPTED)
    with pytest.raises(ValueError, match="ARCHIVE_ONLY"):
        validate_convergence_ledger(replace(ledger, entries=tuple(entries)))


def test_shared_core_adoption_requires_shared_core_target_owner() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    index = next(
        i
        for i, item in enumerate(ledger.entries)
        if item.classification is ConvergenceClassification.SHARED_CORE
        and item.adoption_status is AdoptionStatus.ADOPTED
    )
    entries = list(ledger.entries)
    entries[index] = replace(entries[index], target_owner="role_extension:teacher")
    with pytest.raises(ValueError, match="shared_core:"):
        validate_convergence_ledger(replace(ledger, entries=tuple(entries)))


def test_role_extension_requires_role_extension_target_owner() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    index = next(
        i
        for i, item in enumerate(ledger.entries)
        if item.classification is ConvergenceClassification.ROLE_SPECIFIC_EXTENSION
    )
    entries = list(ledger.entries)
    entries[index] = replace(entries[index], target_owner="shared_core:body")
    with pytest.raises(ValueError, match="role_extension:"):
        validate_convergence_ledger(replace(ledger, entries=tuple(entries)))


@pytest.mark.parametrize(
    ("field", "bad_value", "message"),
    (
        ("claim_ceiling", "ESTABLISHED", "claim ceiling"),
        ("review_status", "", "review status"),
    ),
)
def test_archive_ledger_rejects_entry_boundary_drift(
    field: str,
    bad_value: str,
    message: str,
) -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    entries = list(ledger.entries)
    entries[0] = replace(entries[0], **{field: bad_value})
    with pytest.raises(ValueError, match=message):
        validate_convergence_ledger(replace(ledger, entries=tuple(entries)))


@pytest.mark.parametrize(
    ("field", "bad_value", "message"),
    (
        ("scientific_disposition", "PASS", "scientific disposition"),
        ("canonical_effect", "CANONICAL", "canonical effect"),
        ("deployment", True, "deployment"),
    ),
)
def test_archive_ledger_rejects_top_level_boundary_drift(
    field: str,
    bad_value: object,
    message: str,
) -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    with pytest.raises(ValueError, match=message):
        validate_convergence_ledger(replace(ledger, **{field: bad_value}))


def test_convergence_ledger_hash_is_deterministic_and_content_addressed() -> None:
    ledger = load_convergence_ledger(LEDGER_PATH)
    first = convergence_ledger_hash(ledger)
    second = convergence_ledger_hash(ledger)
    assert first == second
    assert len(first) == 64
    assert all(ch in "0123456789abcdef" for ch in first)

    changed = replace(
        ledger,
        ledger_id=ledger.ledger_id + "-changed",
    )
    assert convergence_ledger_hash(changed) != first


def test_convergence_schema_locks_shape_enums_heads_and_superseded_condition() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert schema["additionalProperties"] is False

    entry = schema["$defs"]["archiveDisposition"]
    assert entry["additionalProperties"] is False
    assert entry["properties"]["source_head"]["pattern"] == "^[0-9a-f]{40}$"
    assert set(entry["properties"]["classification"]["enum"]) == {
        item.value for item in ConvergenceClassification
    }
    assert set(entry["properties"]["adoption_status"]["enum"]) == {
        item.value for item in AdoptionStatus
    }

    serialized = json.dumps(entry["allOf"], sort_keys=True)
    assert "SUPERSEDED" in serialized
    assert "replacement_ref_if_superseded" in serialized
