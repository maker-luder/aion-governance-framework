from __future__ import annotations

from dataclasses import asdict, replace
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_astra_twin_embodiment.coverage_matrix import (
    ARCHIVE_HEADS_V0_2,
    CANONICAL_ORDER_FIELDS,
    EMBODIMENT_AXIS_ORDER,
    ArtifactKind,
    CoverageClassification,
    CoverageDisposition,
    coverage_matrix_gate_counts,
    coverage_matrix_hash,
    load_coverage_matrix,
    validate_coverage_matrix,
    validate_coverage_matrix_bindings,
)


ROOT = Path(__file__).parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
MATRIX_PATH = ROOT / "data" / "EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_v0.2.json"
SCHEMA_PATH = ROOT / "schemas" / "EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_SCHEMA.json"
HASH_PATH = MATRIX_PATH.with_suffix(".sha256")


def _matrix():
    return load_coverage_matrix(MATRIX_PATH)


def test_v0_2_contract_artifacts_and_exact_archive_heads_exist() -> None:
    assert MATRIX_PATH.is_file()
    assert SCHEMA_PATH.is_file()
    assert ARCHIVE_HEADS_V0_2 == {
        190: "066ed1afccebee869eb658c09691b7f096694332",
        191: "48bcf45a55a0b67dfc0e7b9cd838c5f9068b08d2",
        192: "861e6a556a21afffd04b187714c0608fe73ea4fc",
        202: "7f84ae8c95f1b7caaaa0c3850a0b6cfd049b7108",
    }


def test_persisted_hash_is_derived_after_canonical_ordering() -> None:
    expected = HASH_PATH.read_text(encoding="ascii").split()[0]
    assert expected == coverage_matrix_hash(_matrix())


def test_inventory_definitions_resolve_the_14_15_16_count_ambiguity() -> None:
    matrix = _matrix()
    summary = matrix.inventory_summary
    assert summary.pr192_implementation_modules == 19
    assert summary.pr192_teacher_modules == 17
    assert summary.pr192_v0_1_explicit_modules == 4
    assert summary.pr192_v0_1_unexplicit_modules == 15
    assert summary.pr202_external_implementation_modules == 1
    assert summary.pr192_plus_pr202_unexplicit_modules == 16

    pr192_modules = {
        item.source_path.rsplit("/", 1)[-1]
        for item in matrix.source_inventory
        if item.source_pr == 192
        and item.artifact_kind is ArtifactKind.SOURCE
        and item.semantic_coverage_required
    }
    assert len(pr192_modules) == 19
    assert len({name for name in pr192_modules if name.startswith("teacher_")}) == 17


def test_matrix_has_all_axes_independent_classification_and_disposition() -> None:
    matrix = _matrix()
    assert len(EMBODIMENT_AXIS_ORDER) == 19
    assert {
        axis for unit in matrix.semantic_units for axis in unit.embodiment_axes
    } == set(EMBODIMENT_AXIS_ORDER)
    assert any(
        unit.classification is CoverageClassification.SHARED_CORE
        and unit.disposition is CoverageDisposition.DEFERRED
        for unit in matrix.semantic_units
    )


def test_schema_matches_serialized_matrix_and_locks_required_fields() -> None:
    matrix = _matrix()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    payload = json.loads(json.dumps(asdict(matrix)))
    assert not list(validator.iter_errors(payload))
    assert list(validator.iter_errors({**payload, "unreviewed": True}))
    for required in (
        "source_pr",
        "source_head",
        "source_path",
        "source_blob_sha",
        "semantic_unit_id",
        "source_locator",
        "embodiment_axes",
        "classification",
        "disposition",
        "target_ref",
        "active_target_ref",
        "reason",
        "replacement_ref_if_superseded",
        "supporting_artifacts",
        "claim_ceiling",
        "review_status",
    ):
        broken = json.loads(json.dumps(payload))
        del broken["semantic_units"][0][required]
        assert list(validator.iter_errors(broken)), required


def test_final_gate_counts_have_no_missing_or_duplicate_ownership() -> None:
    counts = coverage_matrix_gate_counts(_matrix())
    assert counts["MISSING_UNACCOUNTED_COUNT"] == 0
    assert counts["DUPLICATE_SEMANTIC_OWNERSHIP"] == 0
    assert counts["UNCOVERED_SOURCE_MODULE_COUNT"] == 0


def test_pr202_is_exact_external_deferred_provenance_only() -> None:
    matrix = _matrix()
    units = [unit for unit in matrix.semantic_units if unit.source_pr == 202]
    assert units
    assert all(unit.source_head == ARCHIVE_HEADS_V0_2[202] for unit in units)
    assert all(
        unit.classification is CoverageClassification.EXTERNAL_DEFERRED
        and unit.disposition is CoverageDisposition.DEFERRED
        and unit.active_target_ref is None
        for unit in units
    )
    assert {
        artifact.source_path
        for artifact in matrix.source_inventory
        if artifact.source_pr == 202
    } >= {
        "research-labs/twin-genesis-embodiment_v0.1.0/src/aion_astra_twin_embodiment/sensorimotor.py",
        "research-labs/twin-genesis-embodiment_v0.1.0/schemas/SENSORIMOTOR_TRANSITION_SCHEMA.json",
        "research-labs/twin-genesis-embodiment_v0.1.0/docs/SENSORIMOTOR_EMBODIMENT_PROTOCOL.md",
        "research-labs/twin-genesis-embodiment_v0.1.0/tests/test_sensorimotor.py",
    }


def test_structural_validation_rejects_invalid_disposition_boundaries() -> None:
    matrix = _matrix()
    deferred_index = next(
        index
        for index, unit in enumerate(matrix.semantic_units)
        if unit.disposition is CoverageDisposition.DEFERRED
    )
    units = list(matrix.semantic_units)
    units[deferred_index] = replace(
        units[deferred_index], active_target_ref="README.md"
    )
    with pytest.raises(ValueError, match="deferred"):
        validate_coverage_matrix(replace(matrix, semantic_units=tuple(units)))

    adopted_index = next(
        index
        for index, unit in enumerate(matrix.semantic_units)
        if unit.disposition is CoverageDisposition.ADOPTED
    )
    units = list(matrix.semantic_units)
    units[adopted_index] = replace(units[adopted_index], active_target_ref=None)
    with pytest.raises(ValueError, match="adopted"):
        validate_coverage_matrix(replace(matrix, semantic_units=tuple(units)))

    superseded_index = next(
        index
        for index, unit in enumerate(matrix.semantic_units)
        if unit.disposition is CoverageDisposition.SUPERSEDED
    )
    units = list(matrix.semantic_units)
    units[superseded_index] = replace(
        units[superseded_index], replacement_ref_if_superseded=None
    )
    with pytest.raises(ValueError, match="superseded"):
        validate_coverage_matrix(replace(matrix, semantic_units=tuple(units)))

    units = list(matrix.semantic_units)
    units[adopted_index] = replace(
        units[adopted_index], target_ref="active:unbound-description"
    )
    with pytest.raises(ValueError, match="target_ref"):
        validate_coverage_matrix(replace(matrix, semantic_units=tuple(units)))


def test_structural_validation_rejects_duplicate_owner_and_uncovered_module() -> None:
    matrix = _matrix()
    units = list(matrix.semantic_units)
    units[1] = replace(
        units[1],
        source_pr=units[0].source_pr,
        source_head=units[0].source_head,
        source_path=units[0].source_path,
        source_blob_sha=units[0].source_blob_sha,
        source_locator=units[0].source_locator,
    )
    with pytest.raises(ValueError, match="duplicate semantic ownership"):
        validate_coverage_matrix(replace(matrix, semantic_units=tuple(units)))

    covered_artifact_ids = {
        unit.primary_source_artifact_id for unit in matrix.semantic_units
    }
    victim = next(
        artifact
        for artifact in matrix.source_inventory
        if artifact.semantic_coverage_required
        and artifact.artifact_id in covered_artifact_ids
    )
    with pytest.raises(ValueError, match="uncovered source module"):
        validate_coverage_matrix(
            replace(
                matrix,
                semantic_units=tuple(
                    unit
                    for unit in matrix.semantic_units
                    if unit.primary_source_artifact_id != victim.artifact_id
                ),
            )
        )


def test_repository_bindings_reject_wrong_blob_target_and_replacement() -> None:
    matrix = _matrix()
    assert validate_coverage_matrix_bindings(matrix, REPOSITORY_ROOT)["result"] == "PASS"

    inventory = list(matrix.source_inventory)
    victim_id = inventory[0].artifact_id
    inventory[0] = replace(inventory[0], git_blob_sha="0" * 40)
    units = tuple(
        replace(unit, source_blob_sha="0" * 40)
        if unit.primary_source_artifact_id == victim_id
        else unit
        for unit in matrix.semantic_units
    )
    with pytest.raises(ValueError, match="blob"):
        validate_coverage_matrix_bindings(
            replace(
                matrix,
                source_inventory=tuple(inventory),
                semantic_units=units,
            ),
            REPOSITORY_ROOT,
        )

    adopted_index = next(
        index
        for index, unit in enumerate(matrix.semantic_units)
        if unit.disposition is CoverageDisposition.ADOPTED
    )
    units = list(matrix.semantic_units)
    units[adopted_index] = replace(
        units[adopted_index], active_target_ref="does/not/exist.py#missing"
    )
    with pytest.raises(ValueError, match="active target"):
        validate_coverage_matrix_bindings(
            replace(matrix, semantic_units=tuple(units)), REPOSITORY_ROOT
        )

    superseded_index = next(
        index
        for index, unit in enumerate(matrix.semantic_units)
        if unit.disposition is CoverageDisposition.SUPERSEDED
    )
    units = list(matrix.semantic_units)
    units[superseded_index] = replace(
        units[superseded_index], replacement_ref_if_superseded="missing.py"
    )
    with pytest.raises(ValueError, match="replacement"):
        validate_coverage_matrix_bindings(
            replace(matrix, semantic_units=tuple(units)), REPOSITORY_ROOT
        )


def test_canonical_order_and_hash_are_order_independent_but_content_sensitive() -> None:
    matrix = _matrix()
    assert matrix.canonical_order == CANONICAL_ORDER_FIELDS
    original = coverage_matrix_hash(matrix)

    reordered = replace(
        matrix,
        source_inventory=tuple(reversed(matrix.source_inventory)),
        semantic_units=tuple(reversed(matrix.semantic_units)),
    )
    assert coverage_matrix_hash(reordered) == original
    with pytest.raises(ValueError, match="canonical order"):
        validate_coverage_matrix(reordered)

    changed_units = list(matrix.semantic_units)
    adopted_index = next(
        index
        for index, unit in enumerate(changed_units)
        if unit.disposition is CoverageDisposition.ADOPTED
    )
    changed_units[adopted_index] = replace(
        changed_units[adopted_index], disposition=CoverageDisposition.DEFERRED,
        active_target_ref=None,
        replacement_ref_if_superseded=None,
    )
    changed = replace(matrix, semantic_units=tuple(changed_units))
    assert coverage_matrix_hash(changed) != original
