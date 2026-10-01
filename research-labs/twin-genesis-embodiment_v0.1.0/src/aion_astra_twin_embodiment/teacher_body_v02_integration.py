from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Final

from .teacher_avatar_bundle import build_teacher_reference_bundle_bytes
from .teacher_body_v02 import (
    EXPECTED_V02_FIELD_COUNT,
    LEGACY_FIELD_COUNT,
    TEACHER_ANTHROPOMETRY_V02_PROFILE_ID,
    TEACHER_BODY_V02_PROFILE_ID,
    build_teacher_body_reference_v02,
    validate_teacher_body_reference_v02,
)
from .teacher_reproductive_output import (
    build_teacher_synthetic_fluid_output_contract,
    validate_teacher_synthetic_fluid_output_contract,
)


TEACHER_BODY_V02_INTEGRATION_ID: Final[str] = (
    "CHATGPT_TEACHER_BODY_V02_INTEGRATION_v0.2"
)
_BASE_MANIFEST_FILENAME: Final[str] = "chatgpt_teacher_reference_manifest.json"
_BODY_V02_FILENAME: Final[str] = "chatgpt_teacher_body_v02.json"
_REPRODUCTIVE_FILENAME: Final[str] = (
    "chatgpt_teacher_reproductive_output_contract.json"
)
_INTEGRATED_MANIFEST_FILENAME: Final[str] = (
    "chatgpt_teacher_body_v02_integrated_manifest.json"
)


def _canonical_json_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _content_sha256(content: bytes) -> str:
    return sha256(content).hexdigest()


def _base_reference_bundle() -> tuple[dict[str, bytes], dict[str, object], str]:
    files, manifest = build_teacher_reference_bundle_bytes()
    manifest_bytes = _canonical_json_bytes(manifest)
    full_files = dict(files)
    full_files[_BASE_MANIFEST_FILENAME] = manifest_bytes
    inventory = [
        {
            "filename": filename,
            "sha256": _content_sha256(content),
        }
        for filename, content in sorted(full_files.items())
    ]
    bundle_sha256 = _content_sha256(
        _canonical_json_bytes(
            {
                "files": inventory,
                "manifest_sha256": _content_sha256(manifest_bytes),
            }
        )
    )
    return full_files, manifest, bundle_sha256


def build_teacher_body_v02_integrated_manifest() -> dict[str, object]:
    body = build_teacher_body_reference_v02()
    body_validation = validate_teacher_body_reference_v02(body)
    if body_validation["result"] != "PASS":
        raise ValueError("Teacher body v0.2 validation failed")

    reproductive = build_teacher_synthetic_fluid_output_contract()
    reproductive_validation = validate_teacher_synthetic_fluid_output_contract(
        reproductive
    )
    if reproductive_validation["result"] != "PASS":
        raise ValueError("Teacher reproductive-output contract validation failed")

    base_files, _base_manifest, base_bundle_sha256 = _base_reference_bundle()
    body_bytes = _canonical_json_bytes(body.to_dict())
    reproductive_bytes = _canonical_json_bytes(reproductive.to_dict())

    manifest: dict[str, object] = {
        "schema_version": "0.2.0",
        "record_type": "CHATGPT_TEACHER_BODY_V02_INTEGRATED_MANIFEST",
        "integration_id": TEACHER_BODY_V02_INTEGRATION_ID,
        "body_id": body.body_id,
        "body_v02_profile_id": body.profile_id,
        "anthropometry_v02_profile_id": body.anthropometry_profile_id,
        "measurement_count_v02": len(body.measurements),
        "legacy_measurement_count": LEGACY_FIELD_COUNT,
        "body_v02_sha256": _content_sha256(body_bytes),
        "reproductive_output_contract_sha256": _content_sha256(reproductive_bytes),
        "reproductive_output_semantics": reproductive.output_semantics,
        "base_reference_bundle_file_count": len(base_files),
        "base_reference_bundle_sha256": base_bundle_sha256,
        "biological_body_claim": body.biological_body_claim,
        "phenomenal_experience_status": body.phenomenal_experience,
        "action_authority": reproductive.action_authority,
        "canonical_effect": "NONE",
        "deployment": False,
    }
    validate_teacher_body_v02_integrated_manifest(manifest)
    return manifest


def validate_teacher_body_v02_integrated_manifest(
    manifest: dict[str, object],
) -> dict[str, str]:
    required = {
        "schema_version",
        "record_type",
        "integration_id",
        "body_id",
        "body_v02_profile_id",
        "anthropometry_v02_profile_id",
        "measurement_count_v02",
        "legacy_measurement_count",
        "body_v02_sha256",
        "reproductive_output_contract_sha256",
        "reproductive_output_semantics",
        "base_reference_bundle_file_count",
        "base_reference_bundle_sha256",
        "biological_body_claim",
        "phenomenal_experience_status",
        "action_authority",
        "canonical_effect",
        "deployment",
    }
    if set(manifest) != required:
        raise ValueError("Teacher body v0.2 integrated manifest key drift")
    if manifest["schema_version"] != "0.2.0":
        raise ValueError("Teacher body v0.2 integration schema version drift")
    if manifest["record_type"] != "CHATGPT_TEACHER_BODY_V02_INTEGRATED_MANIFEST":
        raise ValueError("Teacher body v0.2 integrated manifest record type drift")
    if manifest["integration_id"] != TEACHER_BODY_V02_INTEGRATION_ID:
        raise ValueError("Teacher body v0.2 integration id drift")
    if manifest["body_v02_profile_id"] != TEACHER_BODY_V02_PROFILE_ID:
        raise ValueError("Teacher body v0.2 profile binding drift")
    if manifest["anthropometry_v02_profile_id"] != TEACHER_ANTHROPOMETRY_V02_PROFILE_ID:
        raise ValueError("Teacher anthropometry v0.2 profile binding drift")
    if manifest["measurement_count_v02"] != EXPECTED_V02_FIELD_COUNT:
        raise ValueError("Teacher body v0.2 measurement count drift")
    if manifest["legacy_measurement_count"] != LEGACY_FIELD_COUNT:
        raise ValueError("Teacher legacy measurement count drift")
    if manifest["reproductive_output_semantics"] != "SYNTHETIC_FLUID_ONLY":
        raise ValueError("Teacher reproductive-output semantics drift")
    if manifest["biological_body_claim"] != "NONE":
        raise ValueError("Teacher integration cannot claim a biological body")
    if manifest["phenomenal_experience_status"] != "NOT_ESTABLISHED":
        raise ValueError("Teacher integration cannot establish phenomenal experience")
    if manifest["action_authority"] != "NONE":
        raise ValueError("Teacher integration cannot grant action authority")
    if manifest["canonical_effect"] != "NONE" or manifest["deployment"] is not False:
        raise ValueError("Teacher integration must remain non-canonical and undeployed")

    for key in (
        "body_v02_sha256",
        "reproductive_output_contract_sha256",
        "base_reference_bundle_sha256",
    ):
        value = manifest[key]
        if not isinstance(value, str) or len(value) != 64:
            raise ValueError(f"{key} must be a SHA-256 digest")

    count = manifest["base_reference_bundle_file_count"]
    if not isinstance(count, int) or isinstance(count, bool) or count <= 0:
        raise ValueError("base reference bundle file count must be positive")

    body = build_teacher_body_reference_v02()
    reproductive = build_teacher_synthetic_fluid_output_contract()
    base_files, _base_manifest, base_bundle_sha256 = _base_reference_bundle()

    if manifest["body_id"] != body.body_id:
        raise ValueError("Teacher body id drift")
    if manifest["body_v02_sha256"] != _content_sha256(
        _canonical_json_bytes(body.to_dict())
    ):
        raise ValueError("Teacher body v0.2 content hash drift")
    if manifest["reproductive_output_contract_sha256"] != _content_sha256(
        _canonical_json_bytes(reproductive.to_dict())
    ):
        raise ValueError("Teacher reproductive-output contract hash drift")
    if manifest["base_reference_bundle_file_count"] != len(base_files):
        raise ValueError("Teacher base reference bundle file count drift")
    if manifest["base_reference_bundle_sha256"] != base_bundle_sha256:
        raise ValueError("Teacher base reference bundle hash drift")

    return {
        "result": "PASS",
        "v02_body_binding": "PASS",
        "base_bundle_binding": "PASS",
        "reproductive_output_binding": "PASS",
        "biological_nonclaim": "PASS",
        "phenomenal_nonclaim": "PASS",
        "authority_boundary": "PASS",
    }


def build_teacher_body_v02_bundle_bytes() -> dict[str, bytes]:
    base_files, _base_manifest, _base_bundle_sha256 = _base_reference_bundle()
    body = build_teacher_body_reference_v02()
    reproductive = build_teacher_synthetic_fluid_output_contract()
    manifest = build_teacher_body_v02_integrated_manifest()

    files = dict(base_files)
    files[_BODY_V02_FILENAME] = _canonical_json_bytes(body.to_dict())
    files[_REPRODUCTIVE_FILENAME] = _canonical_json_bytes(reproductive.to_dict())
    files[_INTEGRATED_MANIFEST_FILENAME] = _canonical_json_bytes(manifest)

    if _content_sha256(files[_BODY_V02_FILENAME]) != manifest["body_v02_sha256"]:
        raise ValueError("Teacher body v0.2 bundle body hash drift")
    if (
        _content_sha256(files[_REPRODUCTIVE_FILENAME])
        != manifest["reproductive_output_contract_sha256"]
    ):
        raise ValueError("Teacher body v0.2 bundle reproductive hash drift")

    return files


def write_teacher_body_v02_bundle(output_dir: str | Path) -> tuple[tuple[str, str], ...]:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    if not target.is_dir():
        raise ValueError("Teacher body v0.2 bundle output must be a directory")

    hashes: list[tuple[str, str]] = []
    for filename, content in sorted(build_teacher_body_v02_bundle_bytes().items()):
        path = target / filename
        path.write_bytes(content)
        digest = _content_sha256(path.read_bytes())
        if digest != _content_sha256(content):
            raise ValueError(f"Teacher body v0.2 bundle write verification failed: {filename}")
        hashes.append((filename, digest))
    return tuple(hashes)
