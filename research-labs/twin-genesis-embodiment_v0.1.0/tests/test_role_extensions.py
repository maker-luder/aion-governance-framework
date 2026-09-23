from __future__ import annotations

import json
from dataclasses import asdict, replace
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aion_astra_twin_embodiment.coverage_matrix import (
    CoverageClassification,
    CoverageDisposition,
    coverage_matrix_hash,
    load_coverage_matrix,
)
from aion_astra_twin_embodiment.models import EmbodimentTemplate
from aion_astra_twin_embodiment.role_extensions import (
    RoleId,
    build_teacher_extension_manifest,
    validate_role_specific_extension,
)
from aion_astra_twin_embodiment.shared_core import (
    build_shared_embodiment_core,
    shared_embodiment_core_hash,
)

SCHEMA_PATH = Path(__file__).parents[1] / "schemas" / "ROLE_SPECIFIC_EMBODIMENT_EXTENSION_SCHEMA.json"
MATRIX_PATH = (
    Path(__file__).parents[1]
    / "data"
    / "EMBODIMENT_ARCHIVE_COVERAGE_MATRIX_v0.2.json"
)


def _fixture():
    core = build_shared_embodiment_core(EmbodimentTemplate("adult-template", "v0.1"))
    matrix = load_coverage_matrix(MATRIX_PATH)
    return core, matrix, build_teacher_extension_manifest(core, matrix)


def test_teacher_manifest_binds_exact_archive_and_core_with_deferred_capabilities() -> None:
    core, matrix, ext = _fixture()
    assert ext.role is RoleId.CHATGPT_TEACHER
    assert ext.source_pr == 192
    assert ext.source_head == "861e6a556a21afffd04b187714c0608fe73ea4fc"
    assert ext.shared_core_sha256 == shared_embodiment_core_hash(core)
    assert ext.coverage_matrix_sha256 == coverage_matrix_hash(matrix)
    expected = {
        unit.semantic_unit_id
        for unit in matrix.semantic_units
        if unit.source_pr == 192
        and unit.classification is CoverageClassification.ROLE_SPECIFIC_EXTENSION
        and unit.disposition is CoverageDisposition.DEFERRED
    }
    assert {item.semantic_unit_id for item in ext.capabilities} == expected
    assert len(ext.capabilities) == len(expected)
    assert all(item.disposition is CoverageDisposition.DEFERRED for item in ext.capabilities)
    assert validate_role_specific_extension(ext, core, matrix)["result"] == "PASS"


def test_teacher_manifest_rejects_wrong_core_role_source_and_duplicate() -> None:
    core, matrix, ext = _fixture()
    for changed, match in (
        (replace(ext, shared_core_sha256="0" * 64), "shared core"),
        (replace(ext, role=RoleId.AION), "role"),
        (replace(ext, source_head="1" * 40), "archive"),
        (replace(ext, capabilities=(*ext.capabilities, ext.capabilities[0])), "duplicate"),
        (replace(ext, capabilities=(
            replace(ext.capabilities[0], semantic_unit_id="PR192.unknown.missing"),
            *ext.capabilities[1:],
        )), "semantic unit"),
    ):
        with pytest.raises(ValueError, match=match):
            validate_role_specific_extension(changed, core, matrix)


def test_teacher_manifest_rejects_unbound_adoption_and_claim_promotion() -> None:
    core, matrix, ext = _fixture()
    with pytest.raises(ValueError, match="target"):
        validate_role_specific_extension(
            replace(ext, capabilities=(
                replace(
                    ext.capabilities[0],
                    disposition=CoverageDisposition.ADOPTED,
                ),
                *ext.capabilities[1:],
            )), core, matrix,
        )
    for changed in (
        replace(ext, subjectivity_conclusion="ESTABLISHED"),
        replace(ext, phenomenal_experience_conclusion="ESTABLISHED"),
        replace(ext, canonical_effect="MERGE"),
        replace(ext, deployment=True),
    ):
        with pytest.raises(ValueError):
            validate_role_specific_extension(changed, core, matrix)


def test_extension_schema_matches_serialized_manifest_and_rejects_extra() -> None:
    _, _, ext = _fixture()
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    payload = json.loads(json.dumps(asdict(ext)))
    assert not list(validator.iter_errors(payload))
    assert list(validator.iter_errors({**payload, "unreviewed": True}))
    assert list(validator.iter_errors({**payload, "deployment": True}))
