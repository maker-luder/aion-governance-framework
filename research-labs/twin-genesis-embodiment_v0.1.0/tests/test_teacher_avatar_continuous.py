from __future__ import annotations

import math

import pytest

from aion_astra_twin_embodiment.teacher_avatar_continuous import (
    build_teacher_continuous_reference_mesh,
    validate_teacher_continuous_reference,
)


@pytest.fixture(scope="module")
def continuous_mesh():
    return build_teacher_continuous_reference_mesh()


def test_teacher_continuous_reference_is_single_connected_surface(continuous_mesh) -> None:
    result = validate_teacher_continuous_reference(continuous_mesh)

    assert result["result"] == "PASS"
    assert result["continuous_surface"] == "PASS"
    assert result["single_component"] == "PASS"
    assert continuous_mesh.connected_components == 1
    assert len(continuous_mesh.vertices) > 1000
    assert len(continuous_mesh.triangles) > 2000


def test_teacher_continuous_reference_has_aligned_vertex_attributes(continuous_mesh) -> None:
    count = len(continuous_mesh.vertices)

    assert len(continuous_mesh.normals) == count
    assert len(continuous_mesh.uvs) == count
    assert len(continuous_mesh.joints) == count
    assert len(continuous_mesh.weights) == count

    assert all(math.isclose(sum(weights), 1.0, abs_tol=2e-7) for weights in continuous_mesh.weights)
    assert all(len(set(joints)) == 4 for joints in continuous_mesh.joints)


def test_teacher_continuous_reference_preserves_t_pose_and_anterior_anatomy(continuous_mesh) -> None:
    xs = [point[0] for point in continuous_mesh.vertices]
    ys = [point[1] for point in continuous_mesh.vertices]
    zs = [point[2] for point in continuous_mesh.vertices]

    assert min(xs) < -0.9
    assert max(xs) > 0.9
    assert min(ys) >= 0.0
    assert max(ys) < 1.86
    assert max(zs) > 0.20


def test_teacher_continuous_reference_is_reference_not_production(continuous_mesh) -> None:
    assert continuous_mesh.topology_status == "SINGLE_CONNECTED_REFERENCE_SURFACE"
    assert continuous_mesh.skinning_status == "REFERENCE_LINEAR_BLEND_SKINNING"
    assert continuous_mesh.production_status == "NOT_ESTABLISHED"
    assert continuous_mesh.canonical_effect == "NONE"
    assert continuous_mesh.deployment is False


def test_teacher_continuous_reference_rejects_too_small_grid() -> None:
    with pytest.raises(ValueError, match="at least 5 samples"):
        build_teacher_continuous_reference_mesh((4, 10, 10))
