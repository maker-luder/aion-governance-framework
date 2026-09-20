from __future__ import annotations

from aion_astra_twin_embodiment.teacher_avatar_lod import (
    build_teacher_lod_manifest,
    build_teacher_lod_references,
    validate_teacher_lod_references,
)


def test_teacher_lod_reference_set_has_three_monotonic_levels() -> None:
    levels = build_teacher_lod_references()
    result = validate_teacher_lod_references(levels)

    assert result["result"] == "PASS"
    assert len(levels) == 3
    vertices = [len(level.mesh.vertices) for level in levels]
    triangles = [len(level.mesh.triangles) for level in levels]
    assert vertices[0] > vertices[1] > vertices[2]
    assert triangles[0] > triangles[1] > triangles[2]
    assert all(level.mesh.connected_components == 1 for level in levels)


def test_teacher_lod_manifest_preserves_reference_boundary() -> None:
    manifest = build_teacher_lod_manifest()

    assert len(manifest["levels"]) == 3
    assert manifest["production_lod_status"] == "NOT_ESTABLISHED"
    assert manifest["canonical_effect"] == "NONE"
    assert manifest["deployment"] is False
