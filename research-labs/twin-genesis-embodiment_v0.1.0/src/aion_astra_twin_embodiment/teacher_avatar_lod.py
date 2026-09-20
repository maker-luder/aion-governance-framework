from __future__ import annotations

from dataclasses import dataclass

from .teacher_avatar_continuous import (
    ContinuousReferenceMesh,
    build_teacher_continuous_reference_mesh,
    validate_teacher_continuous_reference,
)


@dataclass(frozen=True, slots=True)
class TeacherLodReference:
    name: str
    grid: tuple[int, int, int]
    mesh: ContinuousReferenceMesh
    validation: dict[str, str]


_LOD_GRIDS = (
    ("LOD0_REFERENCE", (25, 37, 19)),
    ("LOD1_REFERENCE", (19, 29, 15)),
    ("LOD2_REFERENCE", (13, 21, 11)),
)


def build_teacher_lod_references() -> tuple[TeacherLodReference, ...]:
    levels: list[TeacherLodReference] = []
    for name, grid in _LOD_GRIDS:
        mesh = build_teacher_continuous_reference_mesh(grid)
        validation = validate_teacher_continuous_reference(mesh)
        levels.append(
            TeacherLodReference(
                name=name,
                grid=grid,
                mesh=mesh,
                validation=validation,
            )
        )
    validate_teacher_lod_references(tuple(levels))
    return tuple(levels)


def validate_teacher_lod_references(
    levels: tuple[TeacherLodReference, ...],
) -> dict[str, str]:
    if tuple(level.name for level in levels) != tuple(name for name, _ in _LOD_GRIDS):
        raise ValueError("Teacher LOD level ordering drift")
    if tuple(level.grid for level in levels) != tuple(grid for _, grid in _LOD_GRIDS):
        raise ValueError("Teacher LOD grid contract drift")

    vertex_counts = [len(level.mesh.vertices) for level in levels]
    triangle_counts = [len(level.mesh.triangles) for level in levels]
    if not all(
        vertex_counts[index] > vertex_counts[index + 1]
        for index in range(len(vertex_counts) - 1)
    ):
        raise ValueError("Teacher LOD vertex counts must decrease monotonically")
    if not all(
        triangle_counts[index] > triangle_counts[index + 1]
        for index in range(len(triangle_counts) - 1)
    ):
        raise ValueError("Teacher LOD triangle counts must decrease monotonically")

    body_ids = {level.mesh.body_id for level in levels}
    if len(body_ids) != 1:
        raise ValueError("Teacher LOD levels must refer to one body id")

    if any(level.mesh.connected_components != 1 for level in levels):
        raise ValueError("every Teacher LOD must remain one connected surface")
    if any(level.validation.get("result") != "PASS" for level in levels):
        raise ValueError("every Teacher LOD must pass continuous-reference validation")
    if any(level.mesh.production_status != "NOT_ESTABLISHED" for level in levels):
        raise ValueError("reference LOD cannot self-promote to production status")

    return {
        "result": "PASS",
        "lod_count": "3",
        "monotonic_complexity": "PASS",
        "single_connected_surface_each": "PASS",
        "reference_only_boundary": "PASS",
    }


def build_teacher_lod_manifest() -> dict[str, object]:
    levels = build_teacher_lod_references()
    validation = validate_teacher_lod_references(levels)
    return {
        "record_type": "CHATGPT_TEACHER_CONTINUOUS_REFERENCE_LOD_SET",
        "validation": validation,
        "levels": [
            {
                "name": level.name,
                "grid": list(level.grid),
                "vertices": len(level.mesh.vertices),
                "triangles": len(level.mesh.triangles),
                "connected_components": level.mesh.connected_components,
                "validation": level.validation["result"],
            }
            for level in levels
        ],
        "production_lod_status": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
    }
