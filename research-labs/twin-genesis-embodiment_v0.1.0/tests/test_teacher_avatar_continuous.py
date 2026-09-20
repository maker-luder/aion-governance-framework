from __future__ import annotations

import base64
import math
import struct

import pytest

from aion_astra_twin_embodiment.teacher_avatar_continuous import (
    build_teacher_continuous_reference_glb,
    build_teacher_continuous_reference_gltf,
    build_teacher_continuous_reference_mesh,
    validate_teacher_continuous_reference,
    validate_teacher_continuous_reference_glb,
    validate_teacher_continuous_reference_gltf,
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



def test_teacher_continuous_reference_gltf_is_skinned_and_embedded(continuous_mesh) -> None:
    payload = build_teacher_continuous_reference_gltf(continuous_mesh)
    primitive = payload["meshes"][0]["primitives"][0]

    assert payload["asset"]["version"] == "2.0"
    assert primitive["attributes"] == {
        "POSITION": 0,
        "NORMAL": 1,
        "TEXCOORD_0": 2,
        "JOINTS_0": 3,
        "WEIGHTS_0": 4,
    }
    assert payload["accessors"][3]["componentType"] == 5123
    assert payload["accessors"][4]["componentType"] == 5126
    assert payload["accessors"][5]["componentType"] == 5125
    assert payload["accessors"][6]["type"] == "MAT4"
    assert payload["skins"][0]["joints"]
    assert payload["extras"]["connected_components"] == 1
    assert payload["extras"]["status"] == "CONTINUOUS_SKINNED_REFERENCE_MATERIALIZED"
    assert payload["extras"]["production_topology_status"] == "NOT_ESTABLISHED"

    uri = payload["buffers"][0]["uri"]
    prefix = "data:application/octet-stream;base64,"
    assert uri.startswith(prefix)
    decoded = base64.b64decode(uri.removeprefix(prefix))
    assert len(decoded) == payload["buffers"][0]["byteLength"]


def test_teacher_continuous_reference_glb_has_valid_header(continuous_mesh) -> None:
    data = build_teacher_continuous_reference_glb(continuous_mesh)

    magic, version, total_length = struct.unpack("<III", data[:12])
    chunk_length, chunk_type = struct.unpack("<II", data[12:20])

    assert magic == 0x46546C67
    assert version == 2
    assert total_length == len(data)
    assert chunk_type == 0x4E4F534A
    assert chunk_length % 4 == 0
    assert chunk_length == len(data) - 20



def test_teacher_continuous_reference_gltf_validator_passes(continuous_mesh) -> None:
    payload = build_teacher_continuous_reference_gltf(continuous_mesh)
    result = validate_teacher_continuous_reference_gltf(payload)

    assert result["result"] == "PASS"
    assert result["continuous_surface_binding"] == "PASS"
    assert result["skinning_binding"] == "PASS"


def test_teacher_continuous_reference_glb_validator_passes(continuous_mesh) -> None:
    data = build_teacher_continuous_reference_glb(continuous_mesh)
    result = validate_teacher_continuous_reference_glb(data)

    assert result["result"] == "PASS"
    assert result["glb_container"] == "PASS"



def test_teacher_continuous_reference_has_morph_targets_and_texture(continuous_mesh) -> None:
    payload = build_teacher_continuous_reference_gltf(continuous_mesh)
    primitive = payload["meshes"][0]["primitives"][0]

    assert primitive["targets"] == [{"POSITION": 7}, {"POSITION": 8}]
    assert payload["meshes"][0]["extras"]["targetNames"] == [
        "blinkReference",
        "happyReference",
    ]
    assert payload["accessors"][7]["count"] == len(continuous_mesh.vertices)
    assert payload["accessors"][8]["count"] == len(continuous_mesh.vertices)
    assert payload["extras"]["reference_morph_targets_status"] == "MATERIALIZED"
    assert payload["extras"]["reference_texture_status"] == "MATERIALIZED"

    image_uri = payload["images"][0]["uri"]
    prefix = "data:image/png;base64,"
    assert image_uri.startswith(prefix)
    png = base64.b64decode(image_uri.removeprefix(prefix))
    assert png.startswith(b"\x89PNG\r\n\x1a\n")
