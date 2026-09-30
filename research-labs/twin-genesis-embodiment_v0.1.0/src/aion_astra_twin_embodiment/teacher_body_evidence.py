from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any

from .teacher_avatar_asset import build_teacher_low_poly_glb
from .teacher_avatar_continuous import (
    build_teacher_continuous_reference_glb,
    build_teacher_continuous_reference_mesh,
    validate_teacher_continuous_reference,
    validate_teacher_continuous_reference_glb,
)
from .teacher_avatar_physics import build_teacher_collision_profile
from .teacher_avatar_validation import (
    build_teacher_asset_manifest,
    validate_teacher_low_poly_glb,
)
from .teacher_body_v02 import build_teacher_body_reference_v02


GENESIS_RECEIPT = "0" * 64


def _canonical_sha256(payload: Any) -> str:
    return sha256(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
            default=str,
        ).encode("utf-8")
    ).hexdigest()


@dataclass(frozen=True, slots=True)
class TeacherEvidenceReceipt:
    index: int
    evidence_id: str
    payload_sha256: str
    previous_receipt_sha256: str
    receipt_sha256: str


@dataclass(frozen=True, slots=True)
class TeacherBodyEvidenceManifest:
    body_id: str
    anthropometry_slots: int
    low_poly_glb_sha256: str
    continuous_glb_sha256: str
    asset_manifest_sha256: str
    collision_profile_sha256: str
    reference_mesh_materialized: bool
    production_asset_established: bool = False
    physical_body_established: bool = False
    as_built_measurement_verified: bool = False
    physical_sensors_established: bool = False
    physical_actuators_established: bool = False
    biological_body: bool = False
    felt_body_sensation: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.anthropometry_slots != 67:
            raise ValueError("Teacher v0.2 evidence must retain 67 measurement slots")
        if not self.reference_mesh_materialized:
            raise ValueError("Teacher reference mesh is materialized at this source head")
        if any(
            (
                self.production_asset_established,
                self.physical_body_established,
                self.as_built_measurement_verified,
                self.physical_sensors_established,
                self.physical_actuators_established,
                self.biological_body,
            )
        ):
            raise ValueError("reference evidence cannot promote absent physical/biological evidence")
        if any(
            value != "NOT_ESTABLISHED"
            for value in (
                self.felt_body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("Teacher body evidence cannot establish phenomenal claims")
        if self.action_authority != "NONE":
            raise ValueError("Teacher body evidence cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("Teacher body evidence must remain non-canonical and undeployed")


def build_teacher_body_evidence_manifest() -> TeacherBodyEvidenceManifest:
    body = build_teacher_body_reference_v02()
    low_poly_glb = build_teacher_low_poly_glb()
    low_poly_validation = validate_teacher_low_poly_glb(low_poly_glb)
    if low_poly_validation["result"] != "PASS":
        raise ValueError("Teacher low-poly GLB failed self-validation")

    continuous_mesh = build_teacher_continuous_reference_mesh()
    continuous_validation = validate_teacher_continuous_reference(continuous_mesh)
    if continuous_validation["result"] != "PASS":
        raise ValueError("Teacher continuous mesh failed self-validation")
    continuous_glb = build_teacher_continuous_reference_glb(continuous_mesh)
    continuous_glb_validation = validate_teacher_continuous_reference_glb(continuous_glb)
    if continuous_glb_validation["result"] != "PASS":
        raise ValueError("Teacher continuous GLB failed self-validation")

    asset_manifest = build_teacher_asset_manifest()
    collision_profile = build_teacher_collision_profile()

    return TeacherBodyEvidenceManifest(
        body_id=body.body_id,
        anthropometry_slots=len(body.measurements),
        low_poly_glb_sha256=sha256(low_poly_glb).hexdigest(),
        continuous_glb_sha256=sha256(continuous_glb).hexdigest(),
        asset_manifest_sha256=_canonical_sha256(asset_manifest),
        collision_profile_sha256=_canonical_sha256(collision_profile),
        reference_mesh_materialized=True,
    )


def build_evidence_receipts(
    manifest: TeacherBodyEvidenceManifest,
) -> tuple[TeacherEvidenceReceipt, ...]:
    evidence = (
        ("anthropometry", {"body_id": manifest.body_id, "slots": manifest.anthropometry_slots}),
        ("low_poly_glb", {"sha256": manifest.low_poly_glb_sha256}),
        ("continuous_glb", {"sha256": manifest.continuous_glb_sha256}),
        ("asset_manifest", {"sha256": manifest.asset_manifest_sha256}),
        ("collision_profile", {"sha256": manifest.collision_profile_sha256}),
    )
    previous = GENESIS_RECEIPT
    receipts: list[TeacherEvidenceReceipt] = []
    for index, (evidence_id, payload) in enumerate(evidence):
        payload_sha = _canonical_sha256(payload)
        receipt_sha = sha256(
            f"{index}|{evidence_id}|{payload_sha}|{previous}".encode("utf-8")
        ).hexdigest()
        receipts.append(
            TeacherEvidenceReceipt(
                index=index,
                evidence_id=evidence_id,
                payload_sha256=payload_sha,
                previous_receipt_sha256=previous,
                receipt_sha256=receipt_sha,
            )
        )
        previous = receipt_sha
    return tuple(receipts)


def verify_evidence_receipts(
    manifest: TeacherBodyEvidenceManifest,
    receipts: tuple[TeacherEvidenceReceipt, ...],
) -> bool:
    return receipts == build_evidence_receipts(manifest)


def run_teacher_body_evidence_probe() -> dict[str, Any]:
    manifest = build_teacher_body_evidence_manifest()
    receipts = build_evidence_receipts(manifest)
    if not verify_evidence_receipts(manifest, receipts):
        raise RuntimeError("Teacher evidence receipt verification failed")
    return {
        "body_id": manifest.body_id,
        "anthropometry_slots": manifest.anthropometry_slots,
        "reference_assets": {
            "low_poly_glb_sha256": manifest.low_poly_glb_sha256,
            "continuous_glb_sha256": manifest.continuous_glb_sha256,
            "asset_manifest_sha256": manifest.asset_manifest_sha256,
            "collision_profile_sha256": manifest.collision_profile_sha256,
            "reference_mesh_materialized": manifest.reference_mesh_materialized,
        },
        "evidence_chain": {
            "receipt_count": len(receipts),
            "verified": True,
            "final_receipt_sha256": receipts[-1].receipt_sha256,
        },
        "nonclaims": {
            "production_asset_established": False,
            "physical_body_established": False,
            "as_built_measurement_verified": False,
            "physical_sensors_established": False,
            "physical_actuators_established": False,
            "biological_body": False,
            "felt_body_sensation": "NOT_ESTABLISHED",
            "subjectivity": "NOT_ESTABLISHED",
            "consciousness": "NOT_ESTABLISHED",
            "phenomenal_experience": "NOT_ESTABLISHED",
            "action_authority": "NONE",
            "canonical_effect": "NONE",
            "deployment": False,
        },
    }
