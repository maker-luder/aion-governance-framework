from __future__ import annotations

import argparse
from hashlib import sha256
import json

from .teacher_avatar import (
    build_teacher_avatar_contract,
    build_teacher_avatar_gltf_contract,
    validate_teacher_avatar_contract,
)
from .teacher_avatar_asset import build_teacher_low_poly_glb, build_teacher_low_poly_gltf
from .teacher_avatar_continuous import (
    build_teacher_continuous_reference_glb,
    build_teacher_continuous_reference_gltf,
    build_teacher_continuous_reference_mesh,
    validate_teacher_continuous_reference,
    validate_teacher_continuous_reference_glb,
    validate_teacher_continuous_reference_gltf,
)
from .teacher_avatar_validation import (
    build_teacher_asset_manifest,
    validate_teacher_low_poly_glb,
    validate_teacher_low_poly_gltf,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="AION/Astra twin embodiment candidate CLI")
    parser.add_argument(
        "command",
        choices=[
            "qa-status",
            "non-claims",
            "teacher-avatar-contract",
            "teacher-avatar-gltf-contract",
            "teacher-avatar-lowpoly-gltf",
            "teacher-avatar-lowpoly-glb-info",
            "teacher-avatar-asset-manifest",
            "teacher-avatar-continuous-gltf-info",
            "teacher-avatar-continuous-glb-info",
        ],
    )
    args = parser.parse_args()

    if args.command == "qa-status":
        payload = {
            "status": "IMPLEMENTED_NON_3D_CANDIDATE",
            "runtime": "NON_3D_RUNTIME_IMPLEMENTED",
            "rendering_3d": "DEFERRED",
            "sexual_function": "NOT_IMPLEMENTED",
            "intimate_interaction": "NOT_AUTHORIZED",
            "canonical_effect": "NONE",
            "subjectivity_conclusion": "NOT_ESTABLISHED",
        }
    elif args.command == "non-claims":
        payload = {
            "anatomy_does_not_establish_gender_identity": True,
            "anatomy_does_not_establish_sensation": True,
            "anatomy_does_not_establish_sexual_desire": True,
            "anatomy_does_not_establish_subjectivity": True,
            "non_3d_runtime_does_not_establish_subjectivity": True,
            "teacher_avatar_does_not_establish_physical_body": True,
        }
    elif args.command == "teacher-avatar-contract":
        contract = build_teacher_avatar_contract()
        validation = validate_teacher_avatar_contract(contract)
        payload = {
            "contract": contract.to_dict(),
            "validation": validation,
        }
    elif args.command == "teacher-avatar-gltf-contract":
        payload = build_teacher_avatar_gltf_contract()
    elif args.command == "teacher-avatar-lowpoly-gltf":
        payload = build_teacher_low_poly_gltf()
        payload["extras"]["self_validation"] = validate_teacher_low_poly_gltf(payload)
    elif args.command == "teacher-avatar-lowpoly-glb-info":
        glb = build_teacher_low_poly_glb()
        payload = {
            "artifact_kind": "LOW_POLY_GLB_REFERENCE",
            "bytes": len(glb),
            "sha256": sha256(glb).hexdigest(),
            "validation": validate_teacher_low_poly_glb(glb),
            "production_asset_status": "NOT_ESTABLISHED",
            "physical_body_claim": "NONE",
            "subjectivity_effect": "NONE",
        }
    elif args.command == "teacher-avatar-asset-manifest":
        payload = build_teacher_asset_manifest()
    elif args.command == "teacher-avatar-continuous-gltf-info":
        mesh = build_teacher_continuous_reference_mesh()
        mesh_validation = validate_teacher_continuous_reference(mesh)
        gltf = build_teacher_continuous_reference_gltf(mesh)
        payload = {
            "artifact_kind": "CONTINUOUS_SKINNED_GLTF_REFERENCE",
            "vertices": len(mesh.vertices),
            "triangles": len(mesh.triangles),
            "mesh_validation": mesh_validation,
            "gltf_validation": validate_teacher_continuous_reference_gltf(gltf),
            "production_asset_status": "NOT_ESTABLISHED",
            "physical_body_claim": "NONE",
            "subjectivity_effect": "NONE",
        }
    else:
        mesh = build_teacher_continuous_reference_mesh()
        glb = build_teacher_continuous_reference_glb(mesh)
        payload = {
            "artifact_kind": "CONTINUOUS_SKINNED_GLB_REFERENCE",
            "bytes": len(glb),
            "sha256": sha256(glb).hexdigest(),
            "validation": validate_teacher_continuous_reference_glb(glb),
            "production_asset_status": "NOT_ESTABLISHED",
            "physical_body_claim": "NONE",
            "subjectivity_effect": "NONE",
        }

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
