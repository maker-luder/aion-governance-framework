from __future__ import annotations

import base64
from hashlib import sha256
import json
import math
import struct
from typing import Any

from .teacher_avatar_asset import build_teacher_low_poly_glb, build_teacher_low_poly_gltf
from .teacher_avatar_continuous import (
    build_teacher_continuous_reference_glb,
    build_teacher_continuous_reference_gltf,
    build_teacher_continuous_reference_mesh,
    validate_teacher_continuous_reference,
    validate_teacher_continuous_reference_glb,
    validate_teacher_continuous_reference_gltf,
)


class TeacherAvatarAssetValidationError(ValueError):
    """Raised when the deterministic Teacher reference asset is structurally invalid."""


def _require_index(index: Any, size: int, label: str) -> int:
    if not isinstance(index, int) or isinstance(index, bool) or not 0 <= index < size:
        raise TeacherAvatarAssetValidationError(f"{label} index out of range: {index!r}")
    return index


def _embedded_buffer(payload: dict[str, Any]) -> bytes:
    buffers = payload.get("buffers")
    if not isinstance(buffers, list) or len(buffers) != 1:
        raise TeacherAvatarAssetValidationError("exactly one embedded reference buffer is required")

    buffer = buffers[0]
    if not isinstance(buffer, dict):
        raise TeacherAvatarAssetValidationError("buffer record must be an object")

    uri = buffer.get("uri")
    prefix = "data:application/octet-stream;base64,"
    if not isinstance(uri, str) or not uri.startswith(prefix):
        raise TeacherAvatarAssetValidationError("reference buffer must use an embedded base64 data URI")

    try:
        decoded = base64.b64decode(uri.removeprefix(prefix), validate=True)
    except ValueError as exc:
        raise TeacherAvatarAssetValidationError("embedded buffer is not valid base64") from exc

    if buffer.get("byteLength") != len(decoded):
        raise TeacherAvatarAssetValidationError("buffer byteLength does not match decoded bytes")
    return decoded


def validate_teacher_low_poly_gltf(payload: dict[str, Any]) -> dict[str, str]:
    asset = payload.get("asset")
    if not isinstance(asset, dict) or asset.get("version") != "2.0":
        raise TeacherAvatarAssetValidationError("asset.version must be glTF 2.0")

    nodes = payload.get("nodes")
    meshes = payload.get("meshes")
    skins = payload.get("skins")
    scenes = payload.get("scenes")
    accessors = payload.get("accessors")
    views = payload.get("bufferViews")

    for name, value in (
        ("nodes", nodes),
        ("meshes", meshes),
        ("skins", skins),
        ("scenes", scenes),
        ("accessors", accessors),
        ("bufferViews", views),
    ):
        if not isinstance(value, list) or not value:
            raise TeacherAvatarAssetValidationError(f"{name} must be a non-empty array")

    scene_index = _require_index(payload.get("scene"), len(scenes), "scene")
    scene_nodes = scenes[scene_index].get("nodes")
    if not isinstance(scene_nodes, list) or not scene_nodes:
        raise TeacherAvatarAssetValidationError("default scene must contain root nodes")
    for index in scene_nodes:
        _require_index(index, len(nodes), "scene node")

    for node_index, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise TeacherAvatarAssetValidationError(f"node {node_index} must be an object")
        for child in node.get("children", []):
            _require_index(child, len(nodes), f"node {node_index} child")
        if "mesh" in node:
            _require_index(node["mesh"], len(meshes), f"node {node_index} mesh")
        if "skin" in node:
            _require_index(node["skin"], len(skins), f"node {node_index} skin")

    raw_buffer = _embedded_buffer(payload)
    for view_index, view in enumerate(views):
        if not isinstance(view, dict):
            raise TeacherAvatarAssetValidationError(f"bufferView {view_index} must be an object")
        if view.get("buffer") != 0:
            raise TeacherAvatarAssetValidationError("all reference bufferViews must use buffer 0")
        offset = view.get("byteOffset", 0)
        length = view.get("byteLength")
        if (
            not isinstance(offset, int)
            or isinstance(offset, bool)
            or not isinstance(length, int)
            or isinstance(length, bool)
            or offset < 0
            or length <= 0
            or offset + length > len(raw_buffer)
        ):
            raise TeacherAvatarAssetValidationError(
                f"bufferView {view_index} exceeds embedded buffer bounds"
            )

    for accessor_index, accessor in enumerate(accessors):
        if not isinstance(accessor, dict):
            raise TeacherAvatarAssetValidationError(f"accessor {accessor_index} must be an object")
        _require_index(accessor.get("bufferView"), len(views), f"accessor {accessor_index} bufferView")
        count = accessor.get("count")
        if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
            raise TeacherAvatarAssetValidationError(f"accessor {accessor_index} count must be positive")

    for mesh_index, mesh in enumerate(meshes):
        if not isinstance(mesh, dict):
            raise TeacherAvatarAssetValidationError(f"mesh {mesh_index} must be an object")
        primitives = mesh.get("primitives")
        if not isinstance(primitives, list) or not primitives:
            raise TeacherAvatarAssetValidationError(f"mesh {mesh_index} requires primitives")
        for primitive_index, primitive in enumerate(primitives):
            attributes = primitive.get("attributes")
            if not isinstance(attributes, dict) or "POSITION" not in attributes:
                raise TeacherAvatarAssetValidationError(
                    f"mesh {mesh_index} primitive {primitive_index} requires POSITION"
                )
            for semantic, accessor_ref in attributes.items():
                _require_index(
                    accessor_ref,
                    len(accessors),
                    f"mesh {mesh_index} primitive {primitive_index} {semantic}",
                )
            if "indices" in primitive:
                _require_index(
                    primitive["indices"],
                    len(accessors),
                    f"mesh {mesh_index} primitive {primitive_index} indices",
                )

            position_accessor = accessors[attributes["POSITION"]]
            for target_index, target in enumerate(primitive.get("targets", [])):
                if not isinstance(target, dict) or "POSITION" not in target:
                    raise TeacherAvatarAssetValidationError(
                        f"mesh {mesh_index} morph target {target_index} requires POSITION"
                    )
                target_accessor_index = _require_index(
                    target["POSITION"],
                    len(accessors),
                    f"mesh {mesh_index} morph target {target_index}",
                )
                target_accessor = accessors[target_accessor_index]
                if target_accessor.get("type") != "VEC3":
                    raise TeacherAvatarAssetValidationError("POSITION morph target must be VEC3")
                if target_accessor.get("count") != position_accessor.get("count"):
                    raise TeacherAvatarAssetValidationError(
                        "morph target vertex count must match base POSITION count"
                    )

            if "TEXCOORD_0" in attributes:
                tex_accessor = accessors[attributes["TEXCOORD_0"]]
                if tex_accessor.get("type") != "VEC2":
                    raise TeacherAvatarAssetValidationError("TEXCOORD_0 must be VEC2")
                if tex_accessor.get("count") != position_accessor.get("count"):
                    raise TeacherAvatarAssetValidationError(
                        "TEXCOORD_0 count must match base POSITION count"
                    )

            has_joints = "JOINTS_0" in attributes
            has_weights = "WEIGHTS_0" in attributes
            if has_joints != has_weights:
                raise TeacherAvatarAssetValidationError(
                    "JOINTS_0 and WEIGHTS_0 must be supplied together"
                )
            if has_joints:
                joints_accessor = accessors[attributes["JOINTS_0"]]
                weights_accessor = accessors[attributes["WEIGHTS_0"]]
                if joints_accessor.get("type") != "VEC4":
                    raise TeacherAvatarAssetValidationError("JOINTS_0 must be VEC4")
                if joints_accessor.get("componentType") not in (5121, 5123):
                    raise TeacherAvatarAssetValidationError(
                        "JOINTS_0 must use unsigned byte or unsigned short"
                    )
                if weights_accessor.get("type") != "VEC4":
                    raise TeacherAvatarAssetValidationError("WEIGHTS_0 must be VEC4")
                if weights_accessor.get("componentType") != 5126:
                    raise TeacherAvatarAssetValidationError(
                        "reference WEIGHTS_0 must use float components"
                    )
                if (
                    joints_accessor.get("count") != position_accessor.get("count")
                    or weights_accessor.get("count") != position_accessor.get("count")
                ):
                    raise TeacherAvatarAssetValidationError(
                        "skinning attribute counts must match POSITION count"
                    )

    for skin_index, skin in enumerate(skins):
        joints = skin.get("joints")
        if not isinstance(joints, list) or not joints:
            raise TeacherAvatarAssetValidationError(f"skin {skin_index} requires joints")
        for joint in joints:
            _require_index(joint, len(nodes), f"skin {skin_index} joint")
        _require_index(skin.get("skeleton"), len(nodes), f"skin {skin_index} skeleton")
        inverse_accessor_index = _require_index(
            skin.get("inverseBindMatrices"),
            len(accessors),
            f"skin {skin_index} inverseBindMatrices",
        )
        inverse_accessor = accessors[inverse_accessor_index]
        if inverse_accessor.get("type") != "MAT4" or inverse_accessor.get("componentType") != 5126:
            raise TeacherAvatarAssetValidationError(
                "inverseBindMatrices must use float MAT4 accessor"
            )
        if inverse_accessor.get("count") != len(joints):
            raise TeacherAvatarAssetValidationError(
                "inverseBindMatrices count must match skin joint count"
            )

    skinned_primitive = meshes[1]["primitives"][0]
    joint_accessor = accessors[skinned_primitive["attributes"]["JOINTS_0"]]
    weight_accessor = accessors[skinned_primitive["attributes"]["WEIGHTS_0"]]
    joint_view = views[joint_accessor["bufferView"]]
    weight_view = views[weight_accessor["bufferView"]]
    joint_offset = joint_view.get("byteOffset", 0) + joint_accessor.get("byteOffset", 0)
    weight_offset = weight_view.get("byteOffset", 0) + weight_accessor.get("byteOffset", 0)

    skin_joint_count = len(skins[0]["joints"])
    for vertex in range(joint_accessor["count"]):
        joints = struct.unpack_from("<HHHH", raw_buffer, joint_offset + vertex * 8)
        weights = struct.unpack_from("<ffff", raw_buffer, weight_offset + vertex * 16)
        if any(joint >= skin_joint_count for joint in joints):
            raise TeacherAvatarAssetValidationError("JOINTS_0 references a missing skin joint")
        if not math.isclose(sum(weights), 1.0, abs_tol=1e-6):
            raise TeacherAvatarAssetValidationError("WEIGHTS_0 must sum to 1.0 per vertex")
        if any(weight < 0.0 for weight in weights):
            raise TeacherAvatarAssetValidationError("WEIGHTS_0 cannot contain negative values")

    extras = payload.get("extras")
    if not isinstance(extras, dict):
        raise TeacherAvatarAssetValidationError("asset extras are required")
    required_boundaries = {
        "physical_body_claim": "NONE",
        "subjectivity_effect": "NONE",
        "sexual_function_status": "NOT_IMPLEMENTED",
        "intimate_interaction_status": "NOT_AUTHORIZED",
    }
    for key, expected in required_boundaries.items():
        if extras.get(key) != expected:
            raise TeacherAvatarAssetValidationError(f"boundary drift: {key}")

    return {
        "result": "PASS",
        "gltf_structure": "PASS",
        "buffer_bounds": "PASS",
        "morph_targets": "PASS",
        "reference_skinning": "PASS",
        "governance_boundaries": "PASS",
    }


def validate_teacher_low_poly_glb(data: bytes) -> dict[str, str]:
    if len(data) < 20:
        raise TeacherAvatarAssetValidationError("GLB payload is too short")

    magic, version, total_length = struct.unpack("<III", data[:12])
    if magic != 0x46546C67 or version != 2 or total_length != len(data):
        raise TeacherAvatarAssetValidationError("invalid GLB 2.0 header")

    chunk_length, chunk_type = struct.unpack("<II", data[12:20])
    if chunk_type != 0x4E4F534A or chunk_length % 4 != 0:
        raise TeacherAvatarAssetValidationError("first GLB chunk must be aligned JSON")
    if 20 + chunk_length != len(data):
        raise TeacherAvatarAssetValidationError("GLB JSON chunk length mismatch")

    try:
        payload = json.loads(data[20:].decode("utf-8").rstrip(" "))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TeacherAvatarAssetValidationError("GLB JSON chunk is invalid") from exc

    validate_teacher_low_poly_gltf(payload)
    return {
        "result": "PASS",
        "glb_container": "PASS",
        "embedded_gltf": "PASS",
    }


def build_teacher_asset_manifest() -> dict[str, Any]:
    low_poly_gltf = build_teacher_low_poly_gltf()
    low_poly_gltf_validation = validate_teacher_low_poly_gltf(low_poly_gltf)
    low_poly_gltf_bytes = json.dumps(
        low_poly_gltf,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")

    low_poly_glb_bytes = build_teacher_low_poly_glb()
    low_poly_glb_validation = validate_teacher_low_poly_glb(low_poly_glb_bytes)

    continuous_mesh = build_teacher_continuous_reference_mesh()
    continuous_mesh_validation = validate_teacher_continuous_reference(continuous_mesh)
    continuous_gltf = build_teacher_continuous_reference_gltf(continuous_mesh)
    continuous_gltf_validation = validate_teacher_continuous_reference_gltf(continuous_gltf)
    continuous_gltf_bytes = json.dumps(
        continuous_gltf,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")

    continuous_glb_bytes = build_teacher_continuous_reference_glb(continuous_mesh)
    continuous_glb_validation = validate_teacher_continuous_reference_glb(
        continuous_glb_bytes
    )

    return {
        "schema_version": "0.2.0",
        "record_type": "CHATGPT_TEACHER_3D_REFERENCE_ASSET_MANIFEST",
        "body_id": low_poly_gltf["extras"]["body_id"],
        "artifacts": [
            {
                "kind": "LOW_POLY_GLTF_REFERENCE",
                "media_type": "model/gltf+json",
                "bytes": len(low_poly_gltf_bytes),
                "sha256": sha256(low_poly_gltf_bytes).hexdigest(),
                "validation": low_poly_gltf_validation["result"],
            },
            {
                "kind": "LOW_POLY_GLB_REFERENCE",
                "media_type": "model/gltf-binary",
                "bytes": len(low_poly_glb_bytes),
                "sha256": sha256(low_poly_glb_bytes).hexdigest(),
                "validation": low_poly_glb_validation["result"],
            },
            {
                "kind": "CONTINUOUS_SKINNED_GLTF_REFERENCE",
                "media_type": "model/gltf+json",
                "bytes": len(continuous_gltf_bytes),
                "sha256": sha256(continuous_gltf_bytes).hexdigest(),
                "validation": continuous_gltf_validation["result"],
                "mesh_validation": continuous_mesh_validation["result"],
                "vertices": len(continuous_mesh.vertices),
                "triangles": len(continuous_mesh.triangles),
                "connected_components": continuous_mesh.connected_components,
            },
            {
                "kind": "CONTINUOUS_SKINNED_GLB_REFERENCE",
                "media_type": "model/gltf-binary",
                "bytes": len(continuous_glb_bytes),
                "sha256": sha256(continuous_glb_bytes).hexdigest(),
                "validation": continuous_glb_validation["result"],
                "mesh_validation": continuous_mesh_validation["result"],
                "vertices": len(continuous_mesh.vertices),
                "triangles": len(continuous_mesh.triangles),
                "connected_components": continuous_mesh.connected_components,
            },
        ],
        "reference_continuous_surface_status": "MATERIALIZED",
        "reference_continuous_skinning_status": "MATERIALIZED",
        "production_asset_status": "NOT_ESTABLISHED",
        "physical_body_claim": "NONE",
        "subjectivity_effect": "NONE",
        "canonical_effect": "NONE",
        "deployment": False,
    }
