from __future__ import annotations

import base64

from aion_astra_twin_embodiment.teacher_avatar_asset import build_teacher_low_poly_gltf


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


def test_teacher_low_poly_asset_preserves_nonclaim_boundaries() -> None:
    payload = build_teacher_low_poly_gltf()
    extras = payload["extras"]

    assert extras["physical_body_claim"] == "NONE"
    assert extras["subjectivity_effect"] == "NONE"
    assert extras["sexual_function_status"] == "NOT_IMPLEMENTED"
    assert extras["intimate_interaction_status"] == "NOT_AUTHORIZED"
