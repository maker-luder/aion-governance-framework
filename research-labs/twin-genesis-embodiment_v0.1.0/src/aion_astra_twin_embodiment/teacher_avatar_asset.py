from __future__ import annotations

import base64
import json
import struct
from typing import Any

from .teacher_avatar import build_teacher_avatar_contract, validate_teacher_avatar_contract


_CUBE_POSITIONS: tuple[tuple[float, float, float], ...] = (
    (-0.5, -0.5, -0.5),
    (0.5, -0.5, -0.5),
    (0.5, 0.5, -0.5),
    (-0.5, 0.5, -0.5),
    (-0.5, -0.5, 0.5),
    (0.5, -0.5, 0.5),
    (0.5, 0.5, 0.5),
    (-0.5, 0.5, 0.5),
)

_CUBE_INDICES: tuple[int, ...] = (
    0, 1, 2, 2, 3, 0,
    4, 6, 5, 6, 4, 7,
    0, 4, 5, 5, 1, 0,
    3, 2, 6, 6, 7, 3,
    1, 5, 6, 6, 2, 1,
    0, 3, 7, 7, 4, 0,
)

_CUBE_UVS: tuple[tuple[float, float], ...] = (
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0),
    (0.0, 0.0),
    (1.0, 0.0),
    (1.0, 1.0),
    (0.0, 1.0),
)

_BLINK_REFERENCE_DELTAS: tuple[tuple[float, float, float], ...] = tuple(
    (0.0, -0.08 if position[1] > 0 else 0.0, 0.0)
    for position in _CUBE_POSITIONS
)

_HAPPY_REFERENCE_DELTAS: tuple[tuple[float, float, float], ...] = tuple(
    (
        0.04 if position[0] > 0 else -0.04,
        0.03 if position[1] < 0 and position[2] > 0 else 0.0,
        0.0,
    )
    for position in _CUBE_POSITIONS
)


def _reference_buffer() -> tuple[bytes, dict[str, tuple[int, int]]]:
    chunks: list[bytes] = []
    layout: dict[str, tuple[int, int]] = {}
    offset = 0

    def add(name: str, payload: bytes) -> None:
        nonlocal offset
        if offset % 4:
            padding = 4 - (offset % 4)
            chunks.append(b"\x00" * padding)
            offset += padding
        layout[name] = (offset, len(payload))
        chunks.append(payload)
        offset += len(payload)

    add(
        "positions",
        b"".join(struct.pack("<fff", *position) for position in _CUBE_POSITIONS),
    )
    add("indices", struct.pack("<" + "H" * len(_CUBE_INDICES), *_CUBE_INDICES))
    add("uvs", b"".join(struct.pack("<ff", *uv) for uv in _CUBE_UVS))
    add(
        "blink",
        b"".join(struct.pack("<fff", *delta) for delta in _BLINK_REFERENCE_DELTAS),
    )
    add(
        "happy",
        b"".join(struct.pack("<fff", *delta) for delta in _HAPPY_REFERENCE_DELTAS),
    )
    return b"".join(chunks), layout


def _bone_translation(name: str) -> list[float]:
    direct: dict[str, tuple[float, float, float]] = {
        "hips": (0.0, 0.96, 0.0),
        "spine": (0.0, 0.20, 0.0),
        "chest": (0.0, 0.23, 0.0),
        "upperChest": (0.0, 0.20, 0.0),
        "neck": (0.0, 0.13, 0.0),
        "head": (0.0, 0.14, 0.0),
        "leftEye": (0.035, 0.035, 0.09),
        "rightEye": (-0.035, 0.035, 0.09),
        "jaw": (0.0, -0.08, 0.04),
        "leftShoulder": (0.16, 0.08, 0.0),
        "rightShoulder": (-0.16, 0.08, 0.0),
        "leftUpperArm": (0.22, 0.0, 0.0),
        "rightUpperArm": (-0.22, 0.0, 0.0),
        "leftLowerArm": (0.30, 0.0, 0.0),
        "rightLowerArm": (-0.30, 0.0, 0.0),
        "leftHand": (0.25, 0.0, 0.0),
        "rightHand": (-0.25, 0.0, 0.0),
        "leftUpperLeg": (0.11, -0.11, 0.0),
        "rightUpperLeg": (-0.11, -0.11, 0.0),
        "leftLowerLeg": (0.0, -0.45, 0.0),
        "rightLowerLeg": (0.0, -0.45, 0.0),
        "leftFoot": (0.0, -0.43, 0.07),
        "rightFoot": (0.0, -0.43, 0.07),
        "leftToes": (0.0, 0.0, 0.15),
        "rightToes": (0.0, 0.0, 0.15),
    }
    if name in direct:
        return list(direct[name])

    side_sign = 1.0 if name.startswith("left") else -1.0
    if "ThumbMetacarpal" in name:
        return [0.025 * side_sign, -0.01, 0.02]
    if "ThumbProximal" in name or "ThumbDistal" in name:
        return [0.025 * side_sign, 0.0, 0.0]
    if name.endswith("Proximal"):
        return [0.0, 0.0, 0.035]
    if name.endswith("Intermediate"):
        return [0.0, 0.0, 0.025]
    if name.endswith("Distal"):
        return [0.0, 0.0, 0.02]
    return [0.0, 0.0, 0.0]


def _segment_scale(name: str) -> list[float] | None:
    direct: dict[str, tuple[float, float, float]] = {
        "hips": (0.33, 0.23, 0.22),
        "spine": (0.30, 0.20, 0.20),
        "chest": (0.43, 0.28, 0.23),
        "upperChest": (0.45, 0.24, 0.23),
        "neck": (0.12, 0.15, 0.12),
        "head": (0.17, 0.24, 0.19),
        "leftUpperArm": (0.31, 0.13, 0.13),
        "rightUpperArm": (0.31, 0.13, 0.13),
        "leftLowerArm": (0.28, 0.10, 0.10),
        "rightLowerArm": (0.28, 0.10, 0.10),
        "leftHand": (0.18, 0.08, 0.04),
        "rightHand": (0.18, 0.08, 0.04),
        "leftUpperLeg": (0.18, 0.43, 0.18),
        "rightUpperLeg": (0.18, 0.43, 0.18),
        "leftLowerLeg": (0.14, 0.42, 0.14),
        "rightLowerLeg": (0.14, 0.42, 0.14),
        "leftFoot": (0.12, 0.08, 0.28),
        "rightFoot": (0.12, 0.08, 0.28),
        "leftToes": (0.11, 0.05, 0.10),
        "rightToes": (0.11, 0.05, 0.10),
        "jaw": (0.12, 0.06, 0.10),
    }
    if name in direct:
        return list(direct[name])
    if any(token in name for token in ("Thumb", "Index", "Middle", "Ring", "Little")):
        return [0.025, 0.025, 0.055]
    return None


def build_teacher_low_poly_gltf() -> dict[str, Any]:
    contract = build_teacher_avatar_contract()
    validate_teacher_avatar_contract(contract)

    bone_names = list(contract.human_bones)
    node_index = {name: index for index, name in enumerate(bone_names)}
    nodes: list[dict[str, Any]] = [
        {"name": name, "translation": _bone_translation(name), "children": []}
        for name in bone_names
    ]
    roots: list[int] = []

    for bone, parent in contract.bone_parents.items():
        if parent is None:
            roots.append(node_index[bone])
        else:
            nodes[node_index[parent]]["children"].append(node_index[bone])

    geometry_roles: list[tuple[str, str, list[float], list[float]]] = []
    for bone in bone_names:
        scale = _segment_scale(bone)
        if scale is not None:
            geometry_roles.append((f"GEO_{bone}", bone, [0.0, 0.0, 0.0], scale))

    geometry_roles.extend(
        [
            ("GEO_PENIS", "hips", [0.0, -0.05, 0.13], [0.045, 0.095, 0.045]),
            ("GEO_SCROTUM", "hips", [0.0, -0.09, 0.07], [0.07, 0.07, 0.06]),
            ("GEO_LEFT_TESTIS_VOLUME", "hips", [0.025, -0.09, 0.07], [0.03, 0.045, 0.03]),
            ("GEO_RIGHT_TESTIS_VOLUME", "hips", [-0.025, -0.09, 0.07], [0.03, 0.045, 0.03]),
            ("GEO_PERINEUM_REFERENCE", "hips", [0.0, -0.11, -0.04], [0.09, 0.03, 0.10]),
        ]
    )

    for geometry_name, parent_bone, translation, scale in geometry_roles:
        index = len(nodes)
        geometry_node: dict[str, Any] = {
            "name": geometry_name,
            "mesh": 0,
            "translation": translation,
            "scale": scale,
            "extras": {"anatomy_role": geometry_name.removeprefix("GEO_")},
        }
        if geometry_name == "GEO_head":
            geometry_node["weights"] = [0.0, 0.0]
            geometry_node["extras"]["expression_reference_targets"] = [
                "blinkReference",
                "happyReference",
            ]
        nodes.append(geometry_node)
        nodes[node_index[parent_bone]]["children"].append(index)

    for node in nodes:
        if node.get("children") == []:
            node.pop("children", None)

    raw_buffer, layout = _reference_buffer()
    encoded = base64.b64encode(raw_buffer).decode("ascii")

    buffer_view_names = ("positions", "indices", "uvs", "blink", "happy")
    buffer_views = [
        {
            "buffer": 0,
            "byteOffset": layout[name][0],
            "byteLength": layout[name][1],
            **(
                {"target": 34963}
                if name == "indices"
                else {"target": 34962}
            ),
        }
        for name in buffer_view_names
    ]

    blink_values = [component for delta in _BLINK_REFERENCE_DELTAS for component in delta]
    happy_values = [component for delta in _HAPPY_REFERENCE_DELTAS for component in delta]

    return {
        "asset": {
            "version": "2.0",
            "generator": "aion-astra-twin-embodiment/teacher-low-poly-v0.1",
        },
        "scene": 0,
        "scenes": [{"name": "ChatGPT Teacher Low Poly Reference", "nodes": roots}],
        "nodes": nodes,
        "buffers": [
            {
                "byteLength": len(raw_buffer),
                "uri": f"data:application/octet-stream;base64,{encoded}",
            }
        ],
        "bufferViews": buffer_views,
        "accessors": [
            {
                "bufferView": 0,
                "byteOffset": 0,
                "componentType": 5126,
                "count": len(_CUBE_POSITIONS),
                "type": "VEC3",
                "min": [-0.5, -0.5, -0.5],
                "max": [0.5, 0.5, 0.5],
            },
            {
                "bufferView": 1,
                "byteOffset": 0,
                "componentType": 5123,
                "count": len(_CUBE_INDICES),
                "type": "SCALAR",
                "min": [0],
                "max": [7],
            },
            {
                "bufferView": 2,
                "byteOffset": 0,
                "componentType": 5126,
                "count": len(_CUBE_UVS),
                "type": "VEC2",
                "min": [0.0, 0.0],
                "max": [1.0, 1.0],
            },
            {
                "bufferView": 3,
                "byteOffset": 0,
                "componentType": 5126,
                "count": len(_BLINK_REFERENCE_DELTAS),
                "type": "VEC3",
                "min": [0.0, min(blink_values), 0.0],
                "max": [0.0, max(blink_values), 0.0],
            },
            {
                "bufferView": 4,
                "byteOffset": 0,
                "componentType": 5126,
                "count": len(_HAPPY_REFERENCE_DELTAS),
                "type": "VEC3",
                "min": [min(happy_values), min(happy_values), 0.0],
                "max": [max(happy_values), max(happy_values), 0.0],
            },
        ],
        "materials": [
            {
                "name": "TeacherReferenceMaterial",
                "pbrMetallicRoughness": {
                    "baseColorFactor": [0.62, 0.62, 0.62, 1.0],
                    "metallicFactor": 0.0,
                    "roughnessFactor": 0.8,
                },
            }
        ],
        "meshes": [
            {
                "name": "UnitCubeReferenceMesh",
                "primitives": [
                    {
                        "attributes": {"POSITION": 0, "TEXCOORD_0": 2},
                        "indices": 1,
                        "material": 0,
                        "mode": 4,
                        "targets": [
                            {"POSITION": 3},
                            {"POSITION": 4},
                        ],
                    }
                ],
                "weights": [0.0, 0.0],
                "extras": {"targetNames": ["blinkReference", "happyReference"]},
            }
        ],
        "extras": {
            "body_id": contract.body_id,
            "status": "RENDERABLE_LOW_POLY_REFERENCE",
            "rig_mode": "SEGMENTED_HIERARCHICAL_REFERENCE",
            "coordinate_system": contract.coordinate_system,
            "linear_unit": contract.linear_unit,
            "initial_pose": contract.initial_pose,
            "facing": contract.facing,
            "anatomical_configuration": contract.anatomical_configuration,
            "renderable_mesh_status": "LOW_POLY_REFERENCE_MATERIALIZED",
            "reference_uv_status": "MATERIALIZED",
            "reference_morph_target_vertex_data_status": "MATERIALIZED",
            "continuous_production_mesh_status": "NOT_MATERIALIZED",
            "linear_blend_skin_weights_status": "NOT_MATERIALIZED",
            "production_morph_target_vertex_data_status": "NOT_MATERIALIZED",
            "production_texture_assets_status": "NOT_MATERIALIZED",
            "production_asset_status": "NOT_ESTABLISHED",
            "physical_body_claim": "NONE",
            "subjectivity_effect": "NONE",
            "sexual_function_status": "NOT_IMPLEMENTED",
            "intimate_interaction_status": "NOT_AUTHORIZED",
        },
    }


def build_teacher_low_poly_glb() -> bytes:
    payload = build_teacher_low_poly_gltf()
    json_payload = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    padding = (-len(json_payload)) % 4
    json_chunk = json_payload + (b" " * padding)

    total_length = 12 + 8 + len(json_chunk)
    header = struct.pack("<III", 0x46546C67, 2, total_length)
    chunk_header = struct.pack("<II", len(json_chunk), 0x4E4F534A)
    return header + chunk_header + json_chunk
