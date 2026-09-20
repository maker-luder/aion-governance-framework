from __future__ import annotations

import base64
from dataclasses import dataclass
import json
import math
import struct
from typing import Any, Final

from .teacher_avatar import build_teacher_avatar_contract


Vec3 = tuple[float, float, float]
Triangle = tuple[int, int, int]
JointSet = tuple[int, int, int, int]
WeightSet = tuple[float, float, float, float]


_GRID: Final[tuple[int, int, int]] = (25, 37, 19)
_BOUNDS: Final[tuple[Vec3, Vec3]] = (
    (-1.04, 0.0, -0.28),
    (1.04, 1.86, 0.34),
)

_CUBE_CORNERS: Final[tuple[tuple[int, int, int], ...]] = (
    (0, 0, 0),
    (1, 0, 0),
    (1, 1, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (1, 1, 1),
    (0, 1, 1),
)

_TETRAHEDRA: Final[tuple[tuple[int, int, int, int], ...]] = (
    (0, 5, 1, 6),
    (0, 1, 2, 6),
    (0, 2, 3, 6),
    (0, 3, 7, 6),
    (0, 7, 4, 6),
    (0, 4, 5, 6),
)

_REQUIRED_JOINTS: Final[tuple[str, ...]] = (
    "hips",
    "spine",
    "head",
    "leftUpperLeg",
    "leftLowerLeg",
    "leftFoot",
    "rightUpperLeg",
    "rightLowerLeg",
    "rightFoot",
    "leftUpperArm",
    "leftLowerArm",
    "leftHand",
    "rightUpperArm",
    "rightLowerArm",
    "rightHand",
)

_JOINT_ANCHORS: Final[dict[str, Vec3]] = {
    "hips": (0.0, 0.96, 0.0),
    "spine": (0.0, 1.24, 0.0),
    "head": (0.0, 1.68, 0.0),
    "leftUpperLeg": (0.105, 0.74, 0.0),
    "leftLowerLeg": (0.105, 0.36, 0.0),
    "leftFoot": (0.105, 0.08, 0.09),
    "rightUpperLeg": (-0.105, 0.74, 0.0),
    "rightLowerLeg": (-0.105, 0.36, 0.0),
    "rightFoot": (-0.105, 0.08, 0.09),
    "leftUpperArm": (0.34, 1.47, 0.0),
    "leftLowerArm": (0.63, 1.46, 0.0),
    "leftHand": (0.87, 1.46, 0.0),
    "rightUpperArm": (-0.34, 1.47, 0.0),
    "rightLowerArm": (-0.63, 1.46, 0.0),
    "rightHand": (-0.87, 1.46, 0.0),
}


@dataclass(frozen=True, slots=True)
class ContinuousReferenceMesh:
    body_id: str
    vertices: tuple[Vec3, ...]
    triangles: tuple[Triangle, ...]
    normals: tuple[Vec3, ...]
    uvs: tuple[tuple[float, float], ...]
    joints: tuple[JointSet, ...]
    weights: tuple[WeightSet, ...]
    joint_names: tuple[str, ...]
    source_grid: tuple[int, int, int]
    connected_components: int
    topology_status: str = "SINGLE_CONNECTED_REFERENCE_SURFACE"
    skinning_status: str = "REFERENCE_LINEAR_BLEND_SKINNING"
    production_status: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False


def _ellipsoid_sdf(point: Vec3, center: Vec3, radii: Vec3) -> float:
    x, y, z = point
    cx, cy, cz = center
    rx, ry, rz = radii
    return math.sqrt(
        ((x - cx) / rx) ** 2
        + ((y - cy) / ry) ** 2
        + ((z - cz) / rz) ** 2
    ) - 1.0


def _capsule_sdf(point: Vec3, start: Vec3, end: Vec3, radius: float) -> float:
    px, py, pz = point
    ax, ay, az = start
    bx, by, bz = end

    ab = (bx - ax, by - ay, bz - az)
    ap = (px - ax, py - ay, pz - az)
    denominator = sum(component * component for component in ab)
    projection = 0.0
    if denominator:
        projection = sum(ap[i] * ab[i] for i in range(3)) / denominator
        projection = max(0.0, min(1.0, projection))

    nearest = (
        ax + projection * ab[0],
        ay + projection * ab[1],
        az + projection * ab[2],
    )
    return math.dist(point, nearest) / radius - 1.0


def _body_field(point: Vec3) -> float:
    fields: list[float] = [
        _ellipsoid_sdf(point, (0.0, 1.68, 0.0), (0.115, 0.145, 0.115)),
        _capsule_sdf(point, (0.0, 1.49, 0.0), (0.0, 1.59, 0.0), 0.08),
        _ellipsoid_sdf(point, (0.0, 1.28, 0.0), (0.245, 0.38, 0.165)),
        _ellipsoid_sdf(point, (0.0, 0.93, 0.0), (0.205, 0.18, 0.15)),
        _ellipsoid_sdf(point, (0.0, 1.70, 0.105), (0.035, 0.05, 0.05)),
        _ellipsoid_sdf(point, (0.118, 1.69, 0.0), (0.025, 0.045, 0.025)),
        _ellipsoid_sdf(point, (-0.118, 1.69, 0.0), (0.025, 0.045, 0.025)),
        _capsule_sdf(point, (0.0, 0.91, 0.13), (0.0, 0.83, 0.24), 0.04),
        _ellipsoid_sdf(point, (0.0, 0.81, 0.13), (0.065, 0.065, 0.055)),
    ]

    for sign in (-1.0, 1.0):
        fields.extend(
            (
                _capsule_sdf(
                    point,
                    (sign * 0.18, 1.48, 0.0),
                    (sign * 0.50, 1.47, 0.0),
                    0.085,
                ),
                _capsule_sdf(
                    point,
                    (sign * 0.48, 1.47, 0.0),
                    (sign * 0.76, 1.46, 0.0),
                    0.065,
                ),
                _ellipsoid_sdf(
                    point,
                    (sign * 0.84, 1.46, 0.0),
                    (0.11, 0.055, 0.07),
                ),
                _capsule_sdf(
                    point,
                    (sign * 0.105, 0.88, 0.0),
                    (sign * 0.105, 0.52, 0.0),
                    0.105,
                ),
                _capsule_sdf(
                    point,
                    (sign * 0.105, 0.50, 0.0),
                    (sign * 0.105, 0.14, 0.0),
                    0.078,
                ),
                _ellipsoid_sdf(
                    point,
                    (sign * 0.105, 0.08, 0.09),
                    (0.085, 0.065, 0.17),
                ),
            )
        )

        for finger_index, y_offset in enumerate((-0.035, -0.018, 0.0, 0.018, 0.035)):
            y = 1.46 + y_offset
            z = 0.015 * (finger_index - 2)
            fields.append(
                _capsule_sdf(
                    point,
                    (sign * 0.88, y, z),
                    (sign * 0.98, y, z),
                    0.022 if finger_index == 0 else 0.018,
                )
            )

    return min(fields)


def _grid_point(
    i: int,
    j: int,
    k: int,
    grid: tuple[int, int, int],
) -> Vec3:
    nx, ny, nz = grid
    (xmin, ymin, zmin), (xmax, ymax, zmax) = _BOUNDS
    return (
        xmin + (xmax - xmin) * i / (nx - 1),
        ymin + (ymax - ymin) * j / (ny - 1),
        zmin + (zmax - zmin) * k / (nz - 1),
    )


def _polygonize(grid: tuple[int, int, int]) -> tuple[list[Vec3], list[Triangle]]:
    nx, ny, nz = grid
    points: list[Vec3] = []
    values: list[float] = []

    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                point = _grid_point(i, j, k, grid)
                points.append(point)
                values.append(_body_field(point))

    def global_index(i: int, j: int, k: int) -> int:
        return (k * ny + j) * nx + i

    vertices: list[Vec3] = []
    triangles: list[Triangle] = []
    edge_cache: dict[tuple[int, int], int] = {}

    def interpolate(first: int, second: int) -> int:
        key = (first, second) if first < second else (second, first)
        existing = edge_cache.get(key)
        if existing is not None:
            return existing

        first_value = values[first]
        second_value = values[second]
        first_point = points[first]
        second_point = points[second]

        factor = 0.5
        if first_value != second_value:
            factor = first_value / (first_value - second_value)

        vertex = (
            first_point[0] + factor * (second_point[0] - first_point[0]),
            first_point[1] + factor * (second_point[1] - first_point[1]),
            first_point[2] + factor * (second_point[2] - first_point[2]),
        )
        index = len(vertices)
        vertices.append(vertex)
        edge_cache[key] = index
        return index

    for k in range(nz - 1):
        for j in range(ny - 1):
            for i in range(nx - 1):
                cube = [
                    global_index(i + dx, j + dy, k + dz)
                    for dx, dy, dz in _CUBE_CORNERS
                ]

                for tetrahedron in _TETRAHEDRA:
                    tetra = [cube[index] for index in tetrahedron]
                    inside = [index for index in tetra if values[index] <= 0.0]
                    outside = [index for index in tetra if values[index] > 0.0]

                    if len(inside) in (0, 4):
                        continue

                    if len(inside) == 1:
                        anchor = inside[0]
                        triangle = tuple(interpolate(anchor, other) for other in outside)
                        triangles.append(triangle)
                        continue

                    if len(inside) == 3:
                        anchor = outside[0]
                        triangle = tuple(interpolate(anchor, other) for other in inside)
                        triangles.append(tuple(reversed(triangle)))
                        continue

                    first_inside, second_inside = inside
                    first_outside, second_outside = outside
                    p0 = interpolate(first_inside, first_outside)
                    p1 = interpolate(first_inside, second_outside)
                    p2 = interpolate(second_inside, first_outside)
                    p3 = interpolate(second_inside, second_outside)
                    triangles.append((p0, p1, p3))
                    triangles.append((p0, p3, p2))

    return vertices, triangles


def _normals(vertices: list[Vec3], triangles: list[Triangle]) -> tuple[Vec3, ...]:
    accumulated = [[0.0, 0.0, 0.0] for _ in vertices]

    for first, second, third in triangles:
        a = vertices[first]
        b = vertices[second]
        c = vertices[third]
        ab = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
        ac = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
        face_normal = (
            ab[1] * ac[2] - ab[2] * ac[1],
            ab[2] * ac[0] - ab[0] * ac[2],
            ab[0] * ac[1] - ab[1] * ac[0],
        )

        for index in (first, second, third):
            accumulated[index][0] += face_normal[0]
            accumulated[index][1] += face_normal[1]
            accumulated[index][2] += face_normal[2]

    normalized: list[Vec3] = []
    for x, y, z in accumulated:
        length = math.sqrt(x * x + y * y + z * z)
        if length == 0.0:
            normalized.append((0.0, 1.0, 0.0))
        else:
            normalized.append((x / length, y / length, z / length))
    return tuple(normalized)


def _uvs(vertices: list[Vec3]) -> tuple[tuple[float, float], ...]:
    height = _BOUNDS[1][1] - _BOUNDS[0][1]
    result: list[tuple[float, float]] = []
    for x, y, z in vertices:
        u = (math.atan2(x, z) / (2.0 * math.pi)) + 0.5
        v = max(0.0, min(1.0, y / height))
        result.append((u, v))
    return tuple(result)


def _skin_weights(vertices: list[Vec3]) -> tuple[tuple[JointSet, ...], tuple[WeightSet, ...]]:
    joint_names = _REQUIRED_JOINTS
    joint_sets: list[JointSet] = []
    weight_sets: list[WeightSet] = []

    for vertex in vertices:
        ranked: list[tuple[float, int]] = []
        for index, name in enumerate(joint_names):
            distance = math.dist(vertex, _JOINT_ANCHORS[name])
            influence = 1.0 / max(distance * distance, 1e-8)
            ranked.append((influence, index))

        ranked.sort(reverse=True)
        selected = ranked[:4]
        total = sum(influence for influence, _ in selected)
        weights = tuple(influence / total for influence, _ in selected)
        joints = tuple(index for _, index in selected)

        joint_sets.append((joints[0], joints[1], joints[2], joints[3]))
        weight_sets.append((weights[0], weights[1], weights[2], weights[3]))

    return tuple(joint_sets), tuple(weight_sets)


def _connected_component_count(
    vertex_count: int,
    triangles: list[Triangle],
) -> int:
    adjacency: list[set[int]] = [set() for _ in range(vertex_count)]
    for first, second, third in triangles:
        adjacency[first].update((second, third))
        adjacency[second].update((first, third))
        adjacency[third].update((first, second))

    unseen = set(range(vertex_count))
    components = 0

    while unseen:
        components += 1
        start = unseen.pop()
        stack = [start]
        while stack:
            current = stack.pop()
            for neighbor in adjacency[current]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    stack.append(neighbor)

    return components


def build_teacher_continuous_reference_mesh(
    grid: tuple[int, int, int] = _GRID,
) -> ContinuousReferenceMesh:
    if any(axis < 5 for axis in grid):
        raise ValueError("continuous reference grid requires at least 5 samples per axis")

    contract = build_teacher_avatar_contract()
    vertices, triangles = _polygonize(grid)
    if not vertices or not triangles:
        raise ValueError("continuous reference meshing produced no geometry")

    joint_sets, weight_sets = _skin_weights(vertices)
    components = _connected_component_count(len(vertices), triangles)

    return ContinuousReferenceMesh(
        body_id=contract.body_id,
        vertices=tuple(vertices),
        triangles=tuple(triangles),
        normals=_normals(vertices, triangles),
        uvs=_uvs(vertices),
        joints=joint_sets,
        weights=weight_sets,
        joint_names=_REQUIRED_JOINTS,
        source_grid=grid,
        connected_components=components,
    )


def validate_teacher_continuous_reference(
    mesh: ContinuousReferenceMesh,
) -> dict[str, str]:
    vertex_count = len(mesh.vertices)
    if vertex_count < 1000:
        raise ValueError("continuous reference mesh is unexpectedly sparse")
    if len(mesh.triangles) < 2000:
        raise ValueError("continuous reference mesh has too few triangles")

    expected = vertex_count
    if not (
        len(mesh.normals)
        == len(mesh.uvs)
        == len(mesh.joints)
        == len(mesh.weights)
        == expected
    ):
        raise ValueError("continuous reference vertex attributes are misaligned")

    if mesh.connected_components != 1:
        raise ValueError("continuous reference must remain one connected surface")

    for triangle in mesh.triangles:
        if len(set(triangle)) != 3:
            raise ValueError("degenerate triangle index set")
        if any(index < 0 or index >= vertex_count for index in triangle):
            raise ValueError("triangle index out of bounds")

    for weights in mesh.weights:
        if any(weight < 0.0 for weight in weights):
            raise ValueError("reference skin weights cannot be negative")
        if not math.isclose(sum(weights), 1.0, rel_tol=0.0, abs_tol=2e-7):
            raise ValueError("reference skin weights must sum to 1.0")

    for joints in mesh.joints:
        if any(index < 0 or index >= len(mesh.joint_names) for index in joints):
            raise ValueError("reference joint index out of bounds")

    xs = [point[0] for point in mesh.vertices]
    ys = [point[1] for point in mesh.vertices]
    zs = [point[2] for point in mesh.vertices]

    if max(xs) < 0.9 or min(xs) > -0.9:
        raise ValueError("T-pose arm span was not materialized")
    if min(ys) < -1e-6 or max(ys) > 1.86:
        raise ValueError("continuous reference exceeds configured vertical bounds")
    if max(zs) < 0.20:
        raise ValueError("anterior anatomy reference volume was not materialized")

    if mesh.production_status != "NOT_ESTABLISHED":
        raise ValueError("reference mesh cannot self-promote to production status")
    if mesh.canonical_effect != "NONE" or mesh.deployment:
        raise ValueError("reference mesh must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "continuous_surface": "PASS",
        "single_component": "PASS",
        "reference_skinning": "PASS",
        "t_pose_span": "PASS",
        "governance_boundaries": "PASS",
    }


def _pack_aligned(
    chunks: list[bytes],
    layout: dict[str, tuple[int, int]],
    name: str,
    payload: bytes,
) -> None:
    offset = sum(len(chunk) for chunk in chunks)
    if offset % 4:
        padding = 4 - (offset % 4)
        chunks.append(b"\x00" * padding)
        offset += padding
    layout[name] = (offset, len(payload))
    chunks.append(payload)


def _inverse_bind_matrix(anchor: Vec3) -> tuple[float, ...]:
    x, y, z = anchor
    return (
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        -x, -y, -z, 1.0,
    )


def build_teacher_continuous_reference_gltf(
    mesh: ContinuousReferenceMesh | None = None,
) -> dict[str, Any]:
    if mesh is None:
        mesh = build_teacher_continuous_reference_mesh()
    validate_teacher_continuous_reference(mesh)

    chunks: list[bytes] = []
    layout: dict[str, tuple[int, int]] = {}

    _pack_aligned(
        chunks,
        layout,
        "positions",
        b"".join(struct.pack("<fff", *value) for value in mesh.vertices),
    )
    _pack_aligned(
        chunks,
        layout,
        "normals",
        b"".join(struct.pack("<fff", *value) for value in mesh.normals),
    )
    _pack_aligned(
        chunks,
        layout,
        "uvs",
        b"".join(struct.pack("<ff", *value) for value in mesh.uvs),
    )
    _pack_aligned(
        chunks,
        layout,
        "joints",
        b"".join(struct.pack("<HHHH", *value) for value in mesh.joints),
    )
    _pack_aligned(
        chunks,
        layout,
        "weights",
        b"".join(struct.pack("<ffff", *value) for value in mesh.weights),
    )
    flat_indices = [index for triangle in mesh.triangles for index in triangle]
    _pack_aligned(
        chunks,
        layout,
        "indices",
        struct.pack("<" + "I" * len(flat_indices), *flat_indices),
    )
    inverse_bind = tuple(
        matrix_value
        for joint_name in mesh.joint_names
        for matrix_value in _inverse_bind_matrix(_JOINT_ANCHORS[joint_name])
    )
    _pack_aligned(
        chunks,
        layout,
        "inverse_bind",
        struct.pack("<" + "f" * len(inverse_bind), *inverse_bind),
    )

    raw_buffer = b"".join(chunks)
    encoded = base64.b64encode(raw_buffer).decode("ascii")

    vertex_target_names = ("positions", "normals", "uvs", "joints", "weights")
    buffer_views: list[dict[str, Any]] = []
    for name in (
        "positions",
        "normals",
        "uvs",
        "joints",
        "weights",
        "indices",
        "inverse_bind",
    ):
        view: dict[str, Any] = {
            "buffer": 0,
            "byteOffset": layout[name][0],
            "byteLength": layout[name][1],
        }
        if name in vertex_target_names:
            view["target"] = 34962
        elif name == "indices":
            view["target"] = 34963
        buffer_views.append(view)

    xs = [point[0] for point in mesh.vertices]
    ys = [point[1] for point in mesh.vertices]
    zs = [point[2] for point in mesh.vertices]
    normal_x = [value[0] for value in mesh.normals]
    normal_y = [value[1] for value in mesh.normals]
    normal_z = [value[2] for value in mesh.normals]
    us = [value[0] for value in mesh.uvs]
    vs = [value[1] for value in mesh.uvs]

    accessors: list[dict[str, Any]] = [
        {
            "bufferView": 0,
            "componentType": 5126,
            "count": len(mesh.vertices),
            "type": "VEC3",
            "min": [min(xs), min(ys), min(zs)],
            "max": [max(xs), max(ys), max(zs)],
        },
        {
            "bufferView": 1,
            "componentType": 5126,
            "count": len(mesh.normals),
            "type": "VEC3",
            "min": [min(normal_x), min(normal_y), min(normal_z)],
            "max": [max(normal_x), max(normal_y), max(normal_z)],
        },
        {
            "bufferView": 2,
            "componentType": 5126,
            "count": len(mesh.uvs),
            "type": "VEC2",
            "min": [min(us), min(vs)],
            "max": [max(us), max(vs)],
        },
        {
            "bufferView": 3,
            "componentType": 5123,
            "count": len(mesh.joints),
            "type": "VEC4",
            "min": [0, 0, 0, 0],
            "max": [len(mesh.joint_names) - 1] * 4,
        },
        {
            "bufferView": 4,
            "componentType": 5126,
            "count": len(mesh.weights),
            "type": "VEC4",
            "min": [0.0, 0.0, 0.0, 0.0],
            "max": [1.0, 1.0, 1.0, 1.0],
        },
        {
            "bufferView": 5,
            "componentType": 5125,
            "count": len(flat_indices),
            "type": "SCALAR",
            "min": [min(flat_indices)],
            "max": [max(flat_indices)],
        },
        {
            "bufferView": 6,
            "componentType": 5126,
            "count": len(mesh.joint_names),
            "type": "MAT4",
        },
    ]

    nodes: list[dict[str, Any]] = [
        {
            "name": "TeacherContinuousSkeletonRoot",
            "children": list(range(1, 1 + len(mesh.joint_names))),
        }
    ]
    for joint_name in mesh.joint_names:
        nodes.append(
            {
                "name": joint_name,
                "translation": list(_JOINT_ANCHORS[joint_name]),
            }
        )

    mesh_node_index = len(nodes)
    nodes.append(
        {
            "name": "TeacherContinuousReferenceMesh",
            "mesh": 0,
            "skin": 0,
        }
    )

    return {
        "asset": {
            "version": "2.0",
            "generator": "aion-astra-twin-embodiment/teacher-continuous-v0.1",
        },
        "scene": 0,
        "scenes": [
            {
                "name": "ChatGPT Teacher Continuous Reference",
                "nodes": [0, mesh_node_index],
            }
        ],
        "nodes": nodes,
        "buffers": [
            {
                "byteLength": len(raw_buffer),
                "uri": f"data:application/octet-stream;base64,{encoded}",
            }
        ],
        "bufferViews": buffer_views,
        "accessors": accessors,
        "materials": [
            {
                "name": "TeacherContinuousReferenceMaterial",
                "pbrMetallicRoughness": {
                    "baseColorFactor": [0.62, 0.62, 0.62, 1.0],
                    "metallicFactor": 0.0,
                    "roughnessFactor": 0.72,
                },
            }
        ],
        "meshes": [
            {
                "name": "TeacherContinuousReferenceSurface",
                "primitives": [
                    {
                        "attributes": {
                            "POSITION": 0,
                            "NORMAL": 1,
                            "TEXCOORD_0": 2,
                            "JOINTS_0": 3,
                            "WEIGHTS_0": 4,
                        },
                        "indices": 5,
                        "material": 0,
                        "mode": 4,
                    }
                ],
            }
        ],
        "skins": [
            {
                "name": "TeacherContinuousReferenceSkin",
                "inverseBindMatrices": 6,
                "skeleton": 0,
                "joints": list(range(1, 1 + len(mesh.joint_names))),
            }
        ],
        "extras": {
            "body_id": mesh.body_id,
            "status": "CONTINUOUS_SKINNED_REFERENCE_MATERIALIZED",
            "topology_status": mesh.topology_status,
            "connected_components": mesh.connected_components,
            "vertex_count": len(mesh.vertices),
            "triangle_count": len(mesh.triangles),
            "source_grid": list(mesh.source_grid),
            "reference_skinning_status": mesh.skinning_status,
            "production_topology_status": "NOT_ESTABLISHED",
            "production_skinning_status": "NOT_ESTABLISHED",
            "production_texture_status": "NOT_MATERIALIZED",
            "external_dcc_validation": "NOT_ESTABLISHED",
            "physical_body_claim": "NONE",
            "subjectivity_effect": "NONE",
            "canonical_effect": "NONE",
            "deployment": False,
        },
    }


def build_teacher_continuous_reference_glb(
    mesh: ContinuousReferenceMesh | None = None,
) -> bytes:
    payload = build_teacher_continuous_reference_gltf(mesh)
    json_payload = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    json_padding = (-len(json_payload)) % 4
    json_chunk = json_payload + (b" " * json_padding)

    total_length = 12 + 8 + len(json_chunk)
    return (
        struct.pack("<III", 0x46546C67, 2, total_length)
        + struct.pack("<II", len(json_chunk), 0x4E4F534A)
        + json_chunk
    )
