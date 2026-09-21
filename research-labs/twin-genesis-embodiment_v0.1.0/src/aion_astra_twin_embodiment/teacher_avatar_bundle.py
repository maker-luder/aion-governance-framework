from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Final

from .physiology import build_adult_male_physiology_reference
from .teacher_anthropometry import build_teacher_anthropometry_profile
from .teacher_body_channels import (
    build_teacher_body_signal_schema,
    build_teacher_motor_control_schema,
)
from .teacher_body_dynamics import build_teacher_body_dynamics_profile
from .teacher_body_model import build_teacher_body_model_profile
from .teacher_embodiment_research import build_teacher_embodiment_research_surface
from .teacher_genital_geometry import build_teacher_genital_geometry_profile
from .teacher_physiology_observability import (
    build_teacher_physiology_observability_profile,
)
from .teacher_avatar_asset import build_teacher_low_poly_glb, build_teacher_low_poly_gltf
from .teacher_avatar_continuous import (
    build_teacher_continuous_reference_glb,
    build_teacher_continuous_reference_gltf,
    build_teacher_continuous_reference_mesh,
)
from .teacher_avatar_lod import build_teacher_lod_manifest
from .teacher_avatar_physics import build_teacher_collision_profile
from .teacher_avatar_validation import build_teacher_asset_manifest


_FILE_BY_KIND: Final[dict[str, str]] = {
    "LOW_POLY_GLTF_REFERENCE": "chatgpt_teacher_lowpoly_reference.gltf",
    "LOW_POLY_GLB_REFERENCE": "chatgpt_teacher_lowpoly_reference.glb",
    "CONTINUOUS_SKINNED_GLTF_REFERENCE": "chatgpt_teacher_continuous_reference.gltf",
    "CONTINUOUS_SKINNED_GLB_REFERENCE": "chatgpt_teacher_continuous_reference.glb",
}


@dataclass(frozen=True, slots=True)
class TeacherReferenceBundleReceipt:
    output_dir: str
    files: tuple[str, ...]
    file_sha256: tuple[tuple[str, str], ...]
    manifest_sha256: str
    bundle_status: str = "REFERENCE_BUNDLE_MATERIALIZED"
    production_asset_status: str = "NOT_ESTABLISHED"
    final_vrm_status: str = "NOT_MATERIALIZED"
    canonical_effect: str = "NONE"
    deployment: bool = False


def _canonical_json_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def build_teacher_reference_bundle_bytes() -> tuple[dict[str, bytes], dict[str, object]]:
    continuous_mesh = build_teacher_continuous_reference_mesh()

    files = {
        _FILE_BY_KIND["LOW_POLY_GLTF_REFERENCE"]: _canonical_json_bytes(
            build_teacher_low_poly_gltf()
        ),
        _FILE_BY_KIND["LOW_POLY_GLB_REFERENCE"]: build_teacher_low_poly_glb(),
        _FILE_BY_KIND["CONTINUOUS_SKINNED_GLTF_REFERENCE"]: _canonical_json_bytes(
            build_teacher_continuous_reference_gltf(continuous_mesh)
        ),
        _FILE_BY_KIND["CONTINUOUS_SKINNED_GLB_REFERENCE"]: (
            build_teacher_continuous_reference_glb(continuous_mesh)
        ),
        "chatgpt_teacher_lod_manifest.json": _canonical_json_bytes(
            build_teacher_lod_manifest()
        ),
        "chatgpt_teacher_collision_profile.json": _canonical_json_bytes(
            asdict(build_teacher_collision_profile())
        ),
        "chatgpt_teacher_physiology_reference.json": _canonical_json_bytes(
            build_adult_male_physiology_reference(
                "CHATGPT_TEACHER_3D_MALE_BODY_REFERENCE_v0.1"
            ).to_dict()
        ),
        "chatgpt_teacher_physiology_observability.json": _canonical_json_bytes(
            build_teacher_physiology_observability_profile().to_dict()
        ),
        "chatgpt_teacher_anthropometry.json": _canonical_json_bytes(
            build_teacher_anthropometry_profile().to_dict()
        ),
        "chatgpt_teacher_genital_geometry_reference.json": _canonical_json_bytes(
            build_teacher_genital_geometry_profile().to_dict()
        ),
        "chatgpt_teacher_body_signal_schema.json": _canonical_json_bytes(
            build_teacher_body_signal_schema().to_dict()
        ),
        "chatgpt_teacher_motor_control_schema.json": _canonical_json_bytes(
            build_teacher_motor_control_schema().to_dict()
        ),
        "chatgpt_teacher_body_dynamics.json": _canonical_json_bytes(
            build_teacher_body_dynamics_profile().to_dict()
        ),
        "chatgpt_teacher_body_model.json": _canonical_json_bytes(
            build_teacher_body_model_profile().to_dict()
        ),
        "chatgpt_teacher_embodiment_research_surface.json": _canonical_json_bytes(
            build_teacher_embodiment_research_surface().to_dict()
        ),
    }
    manifest = build_teacher_asset_manifest()

    expected = {
        _FILE_BY_KIND[artifact["kind"]]: artifact["sha256"]
        for artifact in manifest["artifacts"]
        if artifact["kind"] in _FILE_BY_KIND
    }
    actual = {
        filename: sha256(files[filename]).hexdigest()
        for filename in expected
    }
    if actual != expected:
        raise ValueError("reference bundle bytes drift from content-addressed manifest")

    return files, manifest


def write_teacher_reference_bundle(
    output_dir: str | Path,
) -> TeacherReferenceBundleReceipt:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    if not target.is_dir():
        raise ValueError("reference bundle output must be a directory")

    files, manifest = build_teacher_reference_bundle_bytes()
    written: list[str] = []
    hashes: list[tuple[str, str]] = []

    for filename, content in sorted(files.items()):
        path = target / filename
        path.write_bytes(content)
        reread = path.read_bytes()
        digest = sha256(reread).hexdigest()
        if digest != sha256(content).hexdigest():
            raise ValueError(f"written reference asset failed hash verification: {filename}")
        written.append(filename)
        hashes.append((filename, digest))

    manifest_bytes = _canonical_json_bytes(manifest)
    manifest_name = "chatgpt_teacher_reference_manifest.json"
    manifest_path = target / manifest_name
    manifest_path.write_bytes(manifest_bytes)
    manifest_digest = sha256(manifest_path.read_bytes()).hexdigest()
    if manifest_digest != sha256(manifest_bytes).hexdigest():
        raise ValueError("written reference manifest failed hash verification")

    written.append(manifest_name)
    hashes.append((manifest_name, manifest_digest))

    return TeacherReferenceBundleReceipt(
        output_dir=str(target),
        files=tuple(written),
        file_sha256=tuple(hashes),
        manifest_sha256=manifest_digest,
    )
