from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Iterable

from .teacher_anthropometry import (
    EXPECTED_MEASUREMENT_COUNT,
    TEACHER_ANTHROPOMETRY_PROFILE_ID,
    TEACHER_BODY_ID,
    build_teacher_anthropometry_profile,
)
from .teacher_avatar_bundle import build_teacher_reference_bundle_bytes


GENESIS_RECEIPT = "0" * 64


def _canonical_hash(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class TeacherEvidenceReceipt:
    index: int
    payload_sha256: str
    previous_receipt_sha256: str
    receipt_sha256: str


@dataclass(frozen=True, slots=True)
class TeacherAssetEvidenceStatus:
    reference_bundle_materialized: bool
    reference_file_count: int
    reference_bundle_sha256: str
    production_asset_verified: bool = False
    as_built_verified: bool = False
    physical_body_present: bool = False
    physical_sensors_present: bool = False
    physical_actuators_present: bool = False
    biological_realization: bool = False
    felt_body_sensation: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"
    consciousness: str = "NOT_ESTABLISHED"
    phenomenal_experience: str = "NOT_ESTABLISHED"
    action_authority: str = "NONE"
    canonical_effect: str = "NONE"
    deployment: bool = False

    def __post_init__(self) -> None:
        if self.reference_file_count <= 0:
            raise ValueError("reference bundle must contain files")
        if len(self.reference_bundle_sha256) != 64:
            raise ValueError("reference bundle sha256 required")
        if any(
            (
                self.production_asset_verified,
                self.as_built_verified,
                self.physical_body_present,
                self.physical_sensors_present,
                self.physical_actuators_present,
                self.biological_realization,
            )
        ):
            raise ValueError("physical/production realization is not established")
        if any(
            value != "NOT_ESTABLISHED"
            for value in (
                self.felt_body_sensation,
                self.subjectivity,
                self.consciousness,
                self.phenomenal_experience,
            )
        ):
            raise ValueError("phenomenal promotion is not established")
        if self.action_authority != "NONE":
            raise ValueError("Teacher reference body cannot grant action authority")
        if self.canonical_effect != "NONE" or self.deployment:
            raise ValueError("Teacher reference body must remain non-canonical and undeployed")


def build_teacher_asset_evidence_status() -> TeacherAssetEvidenceStatus:
    files, manifest = build_teacher_reference_bundle_bytes()
    bundle_payload = {
        "files": [
            {
                "filename": filename,
                "sha256": sha256(content).hexdigest(),
            }
            for filename, content in sorted(files.items())
        ],
        "manifest": manifest,
    }
    return TeacherAssetEvidenceStatus(
        reference_bundle_materialized=True,
        reference_file_count=len(files) + 1,
        reference_bundle_sha256=_canonical_hash(bundle_payload),
    )


def build_teacher_evidence_receipts(
    payloads: Iterable[object],
) -> tuple[TeacherEvidenceReceipt, ...]:
    previous = GENESIS_RECEIPT
    receipts: list[TeacherEvidenceReceipt] = []
    for index, payload in enumerate(payloads):
        payload_hash = _canonical_hash(payload)
        receipt_hash = _canonical_hash(
            {
                "index": index,
                "payload_sha256": payload_hash,
                "previous_receipt_sha256": previous,
            }
        )
        receipts.append(
            TeacherEvidenceReceipt(
                index=index,
                payload_sha256=payload_hash,
                previous_receipt_sha256=previous,
                receipt_sha256=receipt_hash,
            )
        )
        previous = receipt_hash
    return tuple(receipts)


def verify_teacher_evidence_receipts(
    payloads: Iterable[object],
    receipts: tuple[TeacherEvidenceReceipt, ...],
) -> bool:
    payload_tuple = tuple(payloads)
    if len(payload_tuple) != len(receipts):
        return False
    expected = build_teacher_evidence_receipts(payload_tuple)
    return expected == receipts


def teacher_integrity_probe() -> dict[str, object]:
    profile = build_teacher_anthropometry_profile()
    measurements = profile.measurement_map()
    if len(profile.measurements) != EXPECTED_MEASUREMENT_COUNT:
        raise ValueError("Teacher measurement count drift")
    if measurements["total_height"].nominal != 183.0:
        raise ValueError("Teacher height drift")
    if measurements["body_mass"].nominal != 84.0:
        raise ValueError("Teacher mass drift")

    asset = build_teacher_asset_evidence_status()
    payloads: tuple[object, ...] = (
        {
            "body_id": TEACHER_BODY_ID,
            "profile_id": TEACHER_ANTHROPOMETRY_PROFILE_ID,
            "measurements": profile.to_dict()["measurements"],
        },
        {
            "reference_bundle_sha256": asset.reference_bundle_sha256,
            "reference_file_count": asset.reference_file_count,
        },
        {
            "production_asset_verified": asset.production_asset_verified,
            "physical_body_present": asset.physical_body_present,
            "biological_realization": asset.biological_realization,
            "felt_body_sensation": asset.felt_body_sensation,
            "subjectivity": asset.subjectivity,
            "consciousness": asset.consciousness,
            "phenomenal_experience": asset.phenomenal_experience,
            "action_authority": asset.action_authority,
            "canonical_effect": asset.canonical_effect,
            "deployment": asset.deployment,
        },
    )
    receipts = build_teacher_evidence_receipts(payloads)
    if not verify_teacher_evidence_receipts(payloads, receipts):
        raise ValueError("Teacher evidence receipt verification failed")

    return {
        "body_id": TEACHER_BODY_ID,
        "anthropometry_profile_id": TEACHER_ANTHROPOMETRY_PROFILE_ID,
        "measurement_count": len(profile.measurements),
        "height_cm": measurements["total_height"].nominal,
        "mass_kg": measurements["body_mass"].nominal,
        "reference_bundle_materialized": asset.reference_bundle_materialized,
        "reference_file_count": asset.reference_file_count,
        "reference_bundle_sha256": asset.reference_bundle_sha256,
        "production_asset_verified": asset.production_asset_verified,
        "as_built_verified": asset.as_built_verified,
        "physical_body_present": asset.physical_body_present,
        "biological_realization": asset.biological_realization,
        "felt_body_sensation": asset.felt_body_sensation,
        "subjectivity": asset.subjectivity,
        "consciousness": asset.consciousness,
        "phenomenal_experience": asset.phenomenal_experience,
        "action_authority": asset.action_authority,
        "canonical_effect": asset.canonical_effect,
        "deployment": asset.deployment,
        "receipt_count": len(receipts),
        "final_receipt_sha256": receipts[-1].receipt_sha256,
    }
