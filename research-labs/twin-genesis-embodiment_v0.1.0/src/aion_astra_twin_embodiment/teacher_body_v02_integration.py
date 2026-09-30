from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Final

from .teacher_avatar_bundle import build_teacher_reference_bundle_bytes
from .teacher_avatar_validation import build_teacher_asset_manifest
from .teacher_body_runtime import (
    build_teacher_body_runtime_binding,
    validate_teacher_body_runtime_binding,
)
from .teacher_body_v02 import (
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
    "CHATGPT_TEACHER_BODY_V02_INTEGRATION_v0.1"
)
TEACHER_SYNTHETIC_REPRODUCTIVE_OUTPUT_CONTRACT_ID: Final[str] = (
    "CHATGPT_TEACHER_SYNTHETIC_REPRODUCTIVE_OUTPUT_v0.1"
)


def _canonical_json_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def _canonical_hash(payload: object) -> str:
    return sha256(_canonical_json_bytes(payload)).hexdigest()


def build_teacher_body_v02_json_payload() -> dict[str, object]:
    """Return the actual JSON-compatible v0.2 representation.

    The source dataclass intentionally uses tuples for immutable Python state.
    JSON persistence represents those sequences as arrays. Schema validation
    therefore targets this normalized representation rather than the in-memory
    dataclass container types.
    """
    encoded = _canonical_json_bytes(build_teacher_body_reference_v02().to_dict())
    payload = json.loads(encoded.decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Teacher body v0.2 JSON payload must be an object")
    return payload


@dataclass(frozen=True, slots=True)
class TeacherBodyV02Integration:
    integration_id: str
    base_binding_id: str
    runtime_id: str
    session_id: str
    body_id: str
    legacy_anthropometry_profile_id: str
    body_reference_profile_id: str
    anthropometry_profile_id_v02: str
    synthetic_reproductive_output_contract_id: str
    integrated_manifest_sha256: str
    synthetic_3d_reference_status: str = "MATERIALIZED"
    production_asset_status: str = "NOT_ESTABLISHED"
    live_external_actuation: bool = False
    physical_body_claim: str = "NONE"
    body_sensation_status: str = "NOT_ESTABLISHED"
    body_ownership_experience_status: str = "NOT_ESTABLISHED"
    subjectivity_status: str = "NOT_ESTABLISHED"
    consciousness_status: str = "NOT_ESTABLISHED"
    phenomenal_experience_status: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class TeacherBodyV02BundleReceipt:
    output_dir: str
    files: tuple[str, ...]
    file_sha256: tuple[tuple[str, str], ...]
    integrated_manifest_sha256: str
    bundle_status: str = "TEACHER_BODY_V02_REFERENCE_BUNDLE_MATERIALIZED"
    production_asset_status: str = "NOT_ESTABLISHED"
    physical_body_claim: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False


def build_teacher_reproductive_output_envelope() -> dict[str, object]:
    contract = build_teacher_synthetic_fluid_output_contract()
    validate_teacher_synthetic_fluid_output_contract(contract)
    return {
        "contract_id": TEACHER_SYNTHETIC_REPRODUCTIVE_OUTPUT_CONTRACT_ID,
        "contract": contract.to_dict(),
    }


def build_teacher_body_v02_integrated_manifest() -> dict[str, object]:
    body_v02 = build_teacher_body_reference_v02()
    validate_teacher_body_reference_v02(body_v02)
    body_payload = build_teacher_body_v02_json_payload()
    reproductive = build_teacher_reproductive_output_envelope()
    legacy_manifest = build_teacher_asset_manifest()

    body_bytes = _canonical_json_bytes(body_payload)
    reproductive_bytes = _canonical_json_bytes(reproductive)
    legacy_manifest_bytes = _canonical_json_bytes(legacy_manifest)

    return {
        "schema_version": "0.1.0",
        "record_type": "CHATGPT_TEACHER_BODY_V02_INTEGRATED_MANIFEST",
        "integration_id": TEACHER_BODY_V02_INTEGRATION_ID,
        "body_id": body_v02.body_id,
        "body_reference_profile_id": body_v02.profile_id,
        "anthropometry_profile_id_v02": body_v02.anthropometry_profile_id,
        "measurement_slot_count": len(body_v02.measurements),
        "synthetic_reproductive_output_contract_id": (
            TEACHER_SYNTHETIC_REPRODUCTIVE_OUTPUT_CONTRACT_ID
        ),
        "body_reference_sha256": sha256(body_bytes).hexdigest(),
        "synthetic_reproductive_output_sha256": sha256(
            reproductive_bytes
        ).hexdigest(),
        "legacy_asset_manifest_sha256": sha256(
            legacy_manifest_bytes
        ).hexdigest(),
        "legacy_asset_artifact_count": len(legacy_manifest["artifacts"]),
        "synthetic_3d_reference_status": "MATERIALIZED",
        "production_asset_status": "NOT_ESTABLISHED",
        "physical_body_claim": "NONE",
        "biological_body_claim": "NONE",
        "biological_semen": False,
        "sperm_or_gametes": False,
        "fertility": False,
        "body_sensation_status": "NOT_ESTABLISHED",
        "body_ownership_experience_status": "NOT_ESTABLISHED",
        "subjectivity_status": "NOT_ESTABLISHED",
        "consciousness_status": "NOT_ESTABLISHED",
        "phenomenal_experience_status": "NOT_ESTABLISHED",
        "live_external_actuation": False,
        "canonical_effect": "NONE",
        "deployment": False,
    }


def build_teacher_body_v02_integration(
    runtime_id: str,
    session_id: str,
) -> TeacherBodyV02Integration:
    base = build_teacher_body_runtime_binding(runtime_id, session_id)
    validate_teacher_body_runtime_binding(base)

    body_v02 = build_teacher_body_reference_v02()
    validate_teacher_body_reference_v02(body_v02)

    reproductive = build_teacher_synthetic_fluid_output_contract()
    validate_teacher_synthetic_fluid_output_contract(reproductive)

    manifest = build_teacher_body_v02_integrated_manifest()
    integration = TeacherBodyV02Integration(
        integration_id=TEACHER_BODY_V02_INTEGRATION_ID,
        base_binding_id=base.binding_id,
        runtime_id=base.runtime_id,
        session_id=base.session_id,
        body_id=base.body_id,
        legacy_anthropometry_profile_id=base.anthropometry_profile_id,
        body_reference_profile_id=body_v02.profile_id,
        anthropometry_profile_id_v02=body_v02.anthropometry_profile_id,
        synthetic_reproductive_output_contract_id=(
            TEACHER_SYNTHETIC_REPRODUCTIVE_OUTPUT_CONTRACT_ID
        ),
        integrated_manifest_sha256=_canonical_hash(manifest),
    )
    validate_teacher_body_v02_integration(integration)
    return integration


def validate_teacher_body_v02_integration(
    integration: TeacherBodyV02Integration,
) -> dict[str, str]:
    if integration.integration_id != TEACHER_BODY_V02_INTEGRATION_ID:
        raise ValueError("Teacher body v0.2 integration id drift")

    base = build_teacher_body_runtime_binding(
        integration.runtime_id,
        integration.session_id,
    )
    validate_teacher_body_runtime_binding(base)
    if integration.base_binding_id != base.binding_id:
        raise ValueError("Teacher body v0.2 base binding drift")
    if integration.body_id != base.body_id:
        raise ValueError("Teacher body v0.2 body id drift")
    if integration.legacy_anthropometry_profile_id != base.anthropometry_profile_id:
        raise ValueError("Teacher legacy anthropometry binding drift")

    body_v02 = build_teacher_body_reference_v02()
    validate_teacher_body_reference_v02(body_v02)
    if integration.body_reference_profile_id != TEACHER_BODY_V02_PROFILE_ID:
        raise ValueError("Teacher body v0.2 profile binding drift")
    if integration.body_reference_profile_id != body_v02.profile_id:
        raise ValueError("Teacher body v0.2 profile materialization mismatch")
    if integration.anthropometry_profile_id_v02 != TEACHER_ANTHROPOMETRY_V02_PROFILE_ID:
        raise ValueError("Teacher v0.2 anthropometry binding drift")
    if integration.anthropometry_profile_id_v02 != body_v02.anthropometry_profile_id:
        raise ValueError("Teacher v0.2 anthropometry materialization mismatch")

    reproductive = build_teacher_synthetic_fluid_output_contract()
    validate_teacher_synthetic_fluid_output_contract(reproductive)
    if integration.synthetic_reproductive_output_contract_id != (
        TEACHER_SYNTHETIC_REPRODUCTIVE_OUTPUT_CONTRACT_ID
    ):
        raise ValueError("Teacher synthetic reproductive-output binding drift")

    expected_manifest_hash = _canonical_hash(
        build_teacher_body_v02_integrated_manifest()
    )
    if integration.integrated_manifest_sha256 != expected_manifest_hash:
        raise ValueError("Teacher body v0.2 integrated manifest hash drift")

    if integration.synthetic_3d_reference_status != "MATERIALIZED":
        raise ValueError("Teacher synthetic 3D reference status drift")
    if integration.production_asset_status != "NOT_ESTABLISHED":
        raise ValueError("Teacher integration cannot claim a production asset")
    if integration.live_external_actuation:
        raise ValueError("Teacher integration cannot self-enable external actuation")
    if integration.physical_body_claim != "NONE":
        raise ValueError("Teacher integration cannot claim a physical body")
    if any(
        value != "NOT_ESTABLISHED"
        for value in (
            integration.body_sensation_status,
            integration.body_ownership_experience_status,
            integration.subjectivity_status,
            integration.consciousness_status,
            integration.phenomenal_experience_status,
        )
    ):
        raise ValueError("Teacher integration cannot establish phenomenal states")
    if integration.canonical_effect != "NONE" or integration.deployment:
        raise ValueError("Teacher integration must remain non-canonical and undeployed")

    return {
        "result": "PASS",
        "legacy_teacher_values_preserved": "PASS",
        "body_v02_binding": "PASS",
        "synthetic_reproductive_output_binding": "PASS",
        "integrated_manifest_binding": "PASS",
        "synthetic_3d_reference": "MATERIALIZED",
        "physical_body_claim": "NONE",
        "phenomenal_nonclaim": "PASS",
    }


def build_teacher_body_v02_bundle_bytes() -> dict[str, bytes]:
    legacy_files, legacy_manifest = build_teacher_reference_bundle_bytes()
    files = dict(legacy_files)
    files["chatgpt_teacher_reference_manifest.json"] = _canonical_json_bytes(
        legacy_manifest
    )
    files["chatgpt_teacher_body_reference_v02.json"] = _canonical_json_bytes(
        build_teacher_body_v02_json_payload()
    )
    files[
        "chatgpt_teacher_synthetic_reproductive_output_v01.json"
    ] = _canonical_json_bytes(build_teacher_reproductive_output_envelope())
    files["chatgpt_teacher_body_v02_integrated_manifest.json"] = (
        _canonical_json_bytes(build_teacher_body_v02_integrated_manifest())
    )
    return files


def write_teacher_body_v02_bundle(
    output_dir: str | Path,
) -> TeacherBodyV02BundleReceipt:
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    if not target.is_dir():
        raise ValueError("Teacher body v0.2 bundle output must be a directory")

    files = build_teacher_body_v02_bundle_bytes()
    file_hashes: list[tuple[str, str]] = []
    for filename, content in sorted(files.items()):
        path = target / filename
        path.write_bytes(content)
        reread = path.read_bytes()
        digest = sha256(reread).hexdigest()
        if digest != sha256(content).hexdigest():
            raise ValueError(f"Teacher body v0.2 bundle write drift: {filename}")
        file_hashes.append((filename, digest))

    manifest_name = "chatgpt_teacher_body_v02_integrated_manifest.json"
    manifest_hash = dict(file_hashes)[manifest_name]
    receipt = TeacherBodyV02BundleReceipt(
        output_dir=str(target),
        files=tuple(sorted(files)),
        file_sha256=tuple(file_hashes),
        integrated_manifest_sha256=manifest_hash,
    )
    verify_teacher_body_v02_bundle(target, receipt)
    return receipt


def verify_teacher_body_v02_bundle(
    output_dir: str | Path,
    receipt: TeacherBodyV02BundleReceipt,
) -> dict[str, str]:
    target = Path(output_dir)
    if not target.is_dir():
        raise ValueError("Teacher body v0.2 verification target must be a directory")
    if Path(receipt.output_dir).resolve() != target.resolve():
        raise ValueError("Teacher body v0.2 receipt output directory mismatch")

    hashes = dict(receipt.file_sha256)
    if len(hashes) != len(receipt.file_sha256):
        raise ValueError("Teacher body v0.2 receipt contains duplicate files")
    if set(hashes) != set(receipt.files):
        raise ValueError("Teacher body v0.2 receipt inventory mismatch")

    for filename, expected in sorted(hashes.items()):
        if Path(filename).name != filename:
            raise ValueError("Teacher body v0.2 receipt filename must be a basename")
        path = target / filename
        if not path.is_file():
            raise ValueError(f"Teacher body v0.2 bundle file missing: {filename}")
        actual = sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Teacher body v0.2 bundle hash mismatch: {filename}")

    manifest_name = "chatgpt_teacher_body_v02_integrated_manifest.json"
    if hashes.get(manifest_name) != receipt.integrated_manifest_sha256:
        raise ValueError("Teacher body v0.2 integrated manifest receipt mismatch")

    return {
        "result": "PASS",
        "file_inventory": "PASS",
        "file_hashes": "PASS",
        "integrated_manifest_hash": "PASS",
        "body_v02": "PRESENT",
        "synthetic_reproductive_output": "PRESENT",
    }


def build_teacher_body_v02_probe() -> dict[str, object]:
    integration = build_teacher_body_v02_integration(
        "TEACHER-V02-PROBE-RUNTIME",
        "TEACHER-V02-PROBE-SESSION",
    )
    body_v02 = build_teacher_body_reference_v02()
    reproductive = build_teacher_synthetic_fluid_output_contract()
    bundle = build_teacher_body_v02_bundle_bytes()
    return {
        "integration": integration.to_dict(),
        "measurement_slot_count": len(body_v02.measurements),
        "synthetic_reproductive_output": reproductive.to_dict(),
        "bundle_file_count": len(bundle),
        "bundle_sha256": sha256(
            b"".join(
                filename.encode("utf-8") + sha256(content).digest()
                for filename, content in sorted(bundle.items())
            )
        ).hexdigest(),
        "boundaries": {
            "teacher_profile_is_work_profile": False,
            "physical_body_claim": "NONE",
            "biological_semen": False,
            "sperm_or_gametes": False,
            "fertility": False,
            "body_sensation": "NOT_ESTABLISHED",
            "subjectivity": "NOT_ESTABLISHED",
            "consciousness": "NOT_ESTABLISHED",
            "phenomenal_experience": "NOT_ESTABLISHED",
            "live_external_actuation": False,
            "canonical_effect": "NONE",
            "deployment": False,
        },
    }
