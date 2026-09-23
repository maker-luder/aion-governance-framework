from __future__ import annotations

from dataclasses import asdict, replace
import importlib
import json
from pathlib import Path
import subprocess
import sys

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
from aion_astra_twin_embodiment.materialization_map import (
    MaterializationAdmissionStatus,
    MaterializationArchitectureLayer,
    MaterializationDecision,
    MaterializationRoleScope,
    load_materialization_map,
    materialization_map_gate_counts,
    materialization_map_hash,
    validate_materialization_map,
    validate_materialization_map_bindings,
)


ROOT = Path(__file__).parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
MATRIX_PATH = ROOT / "data" / "EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_v0.2.json"
SCHEMA_PATH = ROOT / "schemas" / "EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_SCHEMA.json"
HASH_PATH = MATRIX_PATH.with_suffix(".sha256")
MATERIALIZATION_MAP_PATH = (
    ROOT / "data" / "EMBODIMENT_MATERIALIZATION_MAP_v0.1.json"
)
MATERIALIZATION_SCHEMA_PATH = (
    ROOT / "schemas" / "EMBODIMENT_MATERIALIZATION_MAP_SCHEMA.json"
)
MATERIALIZATION_HASH_PATH = MATERIALIZATION_MAP_PATH.with_suffix(".sha256")


def _matrix():
    return load_coverage_matrix(MATRIX_PATH)


def _materialization_map():
    return load_materialization_map(MATERIALIZATION_MAP_PATH)


def test_phase_b_materialization_surface_reuses_phase_a_component() -> None:
    module = importlib.import_module(
        "aion_astra_twin_embodiment.materialization_map"
    )
    assert MATERIALIZATION_MAP_PATH.is_file()
    assert MATERIALIZATION_SCHEMA_PATH.is_file()
    for name in (
        "MaterializationDecision",
        "MaterializationAdmissionStatus",
        "MaterializationArchitectureLayer",
        "MaterializationRoleScope",
        "EmbodimentMaterializationMap",
        "load_materialization_map",
        "materialization_map_hash",
        "materialization_map_gate_counts",
        "validate_materialization_map",
        "validate_materialization_map_bindings",
    ):
        assert hasattr(module, name), name


def test_phase_b_map_accounts_for_every_phase_a_unit_once() -> None:
    matrix = _matrix()
    materialization = _materialization_map()
    report = validate_materialization_map(materialization, matrix)

    assert materialization.map_id == "EMBODIMENT_MATERIALIZATION_MAP_v0.1"
    assert materialization.phase_a_matrix_id == matrix.matrix_id
    assert materialization.phase_a_matrix_sha256 == coverage_matrix_hash(matrix)
    assert len(materialization.entries) == len(matrix.semantic_units) == 391
    assert [entry.semantic_unit_id for entry in materialization.entries] == [
        unit.semantic_unit_id for unit in matrix.semantic_units
    ]
    assert report["result"] == "PASS"
    assert report["MISSING_MATERIALIZATION_DECISION_COUNT"] == 0
    assert report["DUPLICATE_ACTIVE_OWNERSHIP_COUNT"] == 0


def test_phase_b_counts_are_conservative_and_deduplicated() -> None:
    materialization = _materialization_map()
    counts = materialization_map_gate_counts(materialization)
    assert counts == {
        "SEMANTIC_UNIT_COUNT": 391,
        "IMPLEMENT_EXISTING_TARGET_COUNT": 7,
        "EXTEND_EXISTING_TARGET_COUNT": 0,
        "KEEP_DEFERRED_COUNT": 347,
        "SUPERSEDED_COUNT": 37,
        "ARCHIVE_ONLY_COUNT": 0,
        "NEEDS_NEW_TARGET_COUNT": 0,
        "ACTIVE_VERIFIED_COUNT": 7,
        "MISSING_MATERIALIZATION_DECISION_COUNT": 0,
        "DUPLICATE_ACTIVE_OWNERSHIP_COUNT": 0,
    }

    duplicate_superseded = [
        entry
        for entry in materialization.entries
        if entry.phase_a_disposition.value == "DEFERRED"
        and entry.decision is MaterializationDecision.SUPERSEDED
    ]
    assert len(duplicate_superseded) == 22
    assert all(entry.source_pr == 190 for entry in duplicate_superseded)
    assert all(entry.canonical_owner_unit_id for entry in duplicate_superseded)


def test_phase_b_role_scope_preserves_source_boundaries() -> None:
    materialization = _materialization_map()
    role_counts = {
        role: sum(entry.role_scope is role for entry in materialization.entries)
        for role in MaterializationRoleScope
    }
    assert role_counts == {
        MaterializationRoleScope.SHARED: 109,
        MaterializationRoleScope.AION_ASTRA: 14,
        MaterializationRoleScope.CHATGPT_TEACHER: 253,
        MaterializationRoleScope.EXTERNAL: 15,
    }
    assert not any(
        entry.role_scope is not MaterializationRoleScope.SHARED
        and entry.admission_status is MaterializationAdmissionStatus.ACTIVE_VERIFIED
        for entry in materialization.entries
    )


def test_pr202_differential_review_remains_external_and_deferred() -> None:
    entries = [entry for entry in _materialization_map().entries if entry.source_pr == 202]
    assert len(entries) == 15
    assert all(
        entry.role_scope is MaterializationRoleScope.EXTERNAL
        and entry.architecture_layer is MaterializationArchitectureLayer.SENSORIMOTOR
        and entry.decision is MaterializationDecision.KEEP_DEFERRED
        and entry.admission_status is MaterializationAdmissionStatus.KEPT_DEFERRED
        and entry.target_ref.startswith("deferred:pr202-exact-provenance-only:")
        for entry in entries
    )
    assert not any(entry.active_target_ref for entry in entries)


def test_materialization_schema_hash_and_runtime_record_are_canonical() -> None:
    materialization = _materialization_map()
    expected = MATERIALIZATION_HASH_PATH.read_text(encoding="ascii").split()[0]
    assert expected == materialization_map_hash(materialization)

    schema = json.loads(MATERIALIZATION_SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    payload = json.loads(json.dumps(asdict(materialization)))
    assert not list(validator.iter_errors(payload))
    assert list(validator.iter_errors({**payload, "unreviewed": True}))
    for required in (
        "semantic_unit_id",
        "source_pr",
        "source_head",
        "source_path",
        "source_blob_sha",
        "source_locator",
        "phase_a_classification",
        "phase_a_disposition",
        "decision",
        "admission_status",
        "architecture_layer",
        "role_scope",
        "target_ref",
        "active_target_ref",
        "replacement_ref",
        "canonical_owner_unit_id",
        "reason",
    ):
        broken = json.loads(json.dumps(payload))
        del broken["entries"][0][required]
        assert list(validator.iter_errors(broken)), required


def test_materialization_validation_fails_closed_on_source_and_order_drift() -> None:
    matrix = _matrix()
    materialization = _materialization_map()
    entries = list(materialization.entries)
    entries[0] = replace(entries[0], source_blob_sha="0" * 40)
    with pytest.raises(ValueError, match="source binding drift"):
        validate_materialization_map(replace(materialization, entries=tuple(entries)), matrix)

    with pytest.raises(ValueError, match="canonical order"):
        validate_materialization_map(
            replace(materialization, entries=tuple(reversed(materialization.entries))),
            matrix,
        )

    with pytest.raises(ValueError, match="exactly once"):
        validate_materialization_map(
            replace(materialization, entries=materialization.entries[:-1]), matrix
        )


def test_materialization_validation_blocks_silent_activation_and_role_leakage() -> None:
    matrix = _matrix()
    materialization = _materialization_map()

    deferred_index = next(
        index
        for index, entry in enumerate(materialization.entries)
        if entry.decision is MaterializationDecision.KEEP_DEFERRED
    )
    entries = list(materialization.entries)
    entries[deferred_index] = replace(
        entries[deferred_index],
        decision=MaterializationDecision.IMPLEMENT_EXISTING_TARGET,
        admission_status=MaterializationAdmissionStatus.ACTIVE_VERIFIED,
        active_target_ref="README.md",
        target_ref="README.md",
    )
    with pytest.raises(ValueError, match="deferred"):
        validate_materialization_map(replace(materialization, entries=tuple(entries)), matrix)

    role_index = next(
        index
        for index, entry in enumerate(materialization.entries)
        if entry.role_scope is MaterializationRoleScope.CHATGPT_TEACHER
    )
    entries = list(materialization.entries)
    entries[role_index] = replace(
        entries[role_index], role_scope=MaterializationRoleScope.SHARED
    )
    with pytest.raises(ValueError, match="role-specific"):
        validate_materialization_map(replace(materialization, entries=tuple(entries)), matrix)

    pr202_index = next(
        index for index, entry in enumerate(materialization.entries) if entry.source_pr == 202
    )
    entries = list(materialization.entries)
    entries[pr202_index] = replace(
        entries[pr202_index],
        decision=MaterializationDecision.NEEDS_NEW_TARGET,
        admission_status=MaterializationAdmissionStatus.NOT_ADMITTED,
    )
    with pytest.raises(ValueError, match="PR #202"):
        validate_materialization_map(replace(materialization, entries=tuple(entries)), matrix)


def test_materialization_validation_blocks_superseded_reentry_and_fake_owner() -> None:
    matrix = _matrix()
    materialization = _materialization_map()
    superseded_index = next(
        index
        for index, entry in enumerate(materialization.entries)
        if entry.phase_a_disposition is CoverageDisposition.SUPERSEDED
    )
    entries = list(materialization.entries)
    entries[superseded_index] = replace(
        entries[superseded_index],
        decision=MaterializationDecision.IMPLEMENT_EXISTING_TARGET,
        admission_status=MaterializationAdmissionStatus.ACTIVE_VERIFIED,
        active_target_ref="README.md",
        target_ref="README.md",
    )
    with pytest.raises(ValueError, match="superseded"):
        validate_materialization_map(replace(materialization, entries=tuple(entries)), matrix)

    duplicate_index = next(
        index
        for index, entry in enumerate(materialization.entries)
        if entry.canonical_owner_unit_id is not None
    )
    entries = list(materialization.entries)
    entries[duplicate_index] = replace(
        entries[duplicate_index], canonical_owner_unit_id="PR999.missing.owner"
    )
    with pytest.raises(ValueError, match="canonical owner"):
        validate_materialization_map(replace(materialization, entries=tuple(entries)), matrix)


def test_materialization_repository_bindings_reuse_phase_a_verification() -> None:
    matrix = _matrix()
    materialization = _materialization_map()
    report = validate_materialization_map_bindings(
        materialization, matrix, REPOSITORY_ROOT
    )
    assert report["result"] == "PASS"
    assert report["SOURCE_BINDINGS"] == "PASS"
    assert report["ACTIVE_TARGET_BINDINGS"] == "PASS"
    assert report["REPLACEMENT_BINDINGS"] == "PASS"

    active_index = next(
        index
        for index, entry in enumerate(materialization.entries)
        if entry.admission_status is MaterializationAdmissionStatus.ACTIVE_VERIFIED
    )
    entries = list(materialization.entries)
    entries[active_index] = replace(
        entries[active_index],
        active_target_ref="does/not/exist.py#missing",
        target_ref="does/not/exist.py#missing",
    )
    with pytest.raises(ValueError, match="active target"):
        validate_materialization_map_bindings(
            replace(materialization, entries=tuple(entries)), matrix, REPOSITORY_ROOT
        )


def test_existing_matrix_verifier_reports_phase_b_materialization_gates() -> None:
    script = ROOT / "scripts" / "verify_coverage_matrix_v0_2.py"
    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=REPOSITORY_ROOT,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    report = json.loads(completed.stdout)
    assert report["MATERIALIZATION_MAP_SHA256"] == materialization_map_hash(
        _materialization_map()
    )
    assert report["MATERIALIZATION_SEMANTIC_UNIT_COUNT"] == 391
    assert report["IMPLEMENT_EXISTING_TARGET_COUNT"] == 7
    assert report["KEEP_DEFERRED_COUNT"] == 347
    assert report["PHASE_B_SUPERSEDED_COUNT"] == 37
    assert report["DUPLICATE_ACTIVE_OWNERSHIP_COUNT"] == 0
    assert report["PR202_ADMISSION_DECISION"] == "KEEP_DEFERRED"


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
