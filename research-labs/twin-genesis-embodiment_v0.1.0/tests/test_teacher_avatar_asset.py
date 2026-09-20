from __future__ import annotations

import base64
import struct

from aion_astra_twin_embodiment.teacher_avatar_asset import (
    build_teacher_low_poly_glb,
    build_teacher_low_poly_gltf,
)


def test_teacher_low_poly_asset_is_renderable_gltf_reference() -> None:
    payload = build_teacher_low_poly_gltf()

    assert payload["asset"]["version"] == "2.0"
    assert payload["scene"] == 0
    assert payload["meshes"][0]["primitives"][0]["mode"] == 4
    assert payload["accessors"][0]["type"] == "VEC3"
    assert payload["accessors"][1]["type"] == "SCALAR"
    assert payload["extras"]["renderable_mesh_status"] == "LOW_POLY_REFERENCE_MATERIALIZED"
    assert payload["extras"]["continuous_production_mesh_status"] == "NOT_MATERIALIZED"
    assert payload["extras"]["production_asset_status"] == "NOT_ESTABLISHED"

    uri = payload["buffers"][0]["uri"]
    prefix = "data:application/octet-stream;base64,"
    assert uri.startswith(prefix)
    decoded = base64.b64decode(uri.removeprefix(prefix))
    assert len(decoded) == payload["buffers"][0]["byteLength"]


def test_teacher_low_poly_asset_contains_reference_uvs_and_morph_data() -> None:
    payload = build_teacher_low_poly_gltf()
    primitive = payload["meshes"][0]["primitives"][0]

    assert primitive["attributes"]["TEXCOORD_0"] == 2
    assert primitive["targets"] == [{"POSITION": 3}, {"POSITION": 4}]
    assert payload["meshes"][0]["extras"]["targetNames"] == [
        "blinkReference",
        "happyReference",
    ]
    assert payload["accessors"][3]["min"] == [0.0, -0.08, 0.0]
    assert payload["accessors"][3]["max"] == [0.0, 0.0, 0.0]
    assert payload["accessors"][4]["min"] == [-0.04, 0.0, 0.0]
    assert payload["accessors"][4]["max"] == [0.04, 0.03, 0.0]
    assert payload["extras"]["reference_uv_status"] == "MATERIALIZED"
    assert payload["extras"]["reference_morph_target_vertex_data_status"] == "MATERIALIZED"
    assert payload["extras"]["production_morph_target_vertex_data_status"] == "NOT_MATERIALIZED"


def test_teacher_low_poly_asset_contains_reference_skinning_data() -> None:
    payload = build_teacher_low_poly_gltf()
    skinned = payload["meshes"][1]["primitives"][0]

    assert skinned["attributes"]["JOINTS_0"] == 5
    assert skinned["attributes"]["WEIGHTS_0"] == 6
    assert payload["skins"][0]["inverseBindMatrices"] == 7
    assert payload["skins"][0]["joints"]
    assert payload["accessors"][5]["componentType"] == 5123
    assert payload["accessors"][5]["type"] == "VEC4"
    assert payload["accessors"][6]["componentType"] == 5126
    assert payload["accessors"][6]["type"] == "VEC4"
    assert payload["accessors"][7]["type"] == "MAT4"
    assert payload["extras"]["reference_skin_weights_status"] == "MATERIALIZED"
    assert payload["extras"]["reference_inverse_bind_matrices_status"] == "MATERIALIZED"
    assert payload["extras"]["linear_blend_skin_weights_status"] == "NOT_MATERIALIZED"


def test_teacher_low_poly_asset_contains_full_external_reference_regions() -> None:
    payload = build_teacher_low_poly_gltf()
    names = {node["name"] for node in payload["nodes"]}

    assert "GEO_head" in names
    assert "GEO_leftHand" in names
    assert "GEO_rightHand" in names
    assert "GEO_leftFoot" in names
    assert "GEO_rightFoot" in names
    assert "GEO_PENIS" in names
    assert "GEO_SCROTUM" in names
    assert "GEO_PERINEUM_REFERENCE" in names


def test_teacher_low_poly_glb_has_valid_container_header() -> None:
    payload = build_teacher_low_poly_glb()

    magic, version, total_length = struct.unpack("<III", payload[:12])
    chunk_length, chunk_type = struct.unpack("<II", payload[12:20])

    assert magic == 0x46546C67
    assert version == 2
    assert total_length == len(payload)
    assert chunk_type == 0x4E4F534A
    assert chunk_length == len(payload) - 20
    assert chunk_length % 4 == 0


def test_teacher_low_poly_asset_preserves_nonclaim_boundaries() -> None:
    payload = build_teacher_low_poly_gltf()
    extras = payload["extras"]

    assert extras["physical_body_claim"] == "NONE"
    assert extras["subjectivity_effect"] == "NONE"
    assert extras["physiology_profile_id"] == "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1"
    assert (
        extras["reproductive_physiology_status"]
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert (
        extras["sexual_function_status"]
        == "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED"
    )
    assert extras["phenomenal_sensation_status"] == "NOT_ESTABLISHED"
    assert extras["erotic_intent"] == "NONE"
    assert extras["intimate_interaction_status"] == "NOT_AUTHORIZED"
