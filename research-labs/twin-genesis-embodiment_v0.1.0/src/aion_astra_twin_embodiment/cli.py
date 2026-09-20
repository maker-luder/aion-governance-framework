from __future__ import annotations

import argparse
from dataclasses import asdict
from hashlib import sha256
import json

from .physiology import (
    build_adult_male_physiology_reference,
    validate_physiology_parity,
)
from .teacher_avatar import (
    build_teacher_avatar_contract,
    build_teacher_avatar_gltf_contract,
    validate_teacher_avatar_contract,
)
from .teacher_avatar_asset import build_teacher_low_poly_glb, build_teacher_low_poly_gltf
from .teacher_avatar_bundle import write_teacher_reference_bundle
from .teacher_avatar_continuous import (
    build_teacher_continuous_reference_glb,
    build_teacher_continuous_reference_gltf,
    build_teacher_continuous_reference_mesh,
    validate_teacher_continuous_reference,
    validate_teacher_continuous_reference_glb,
    validate_teacher_continuous_reference_gltf,
)
from .teacher_avatar_lod import build_teacher_lod_manifest
from .teacher_avatar_physics import build_teacher_collision_profile
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
            "teacher-avatar-reference-bundle",
            "teacher-avatar-lod-manifest",
            "teacher-avatar-collision-profile",
            "physiology-parity",
        ],
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for teacher-avatar-reference-bundle",
    )
    args = parser.parse_args()

    if args.command == "qa-status":
        payload = {
            "status": "IMPLEMENTED_NON_3D_CANDIDATE",
            "runtime": "NON_3D_RUNTIME_IMPLEMENTED",
            "rendering_3d": "DEFERRED",
            "physiology_profile_id": "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1",
            "physiological_function_reference": "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED",
            "reproductive_physiology_reference": "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED",
            "sensory_signal_processing_reference": "REFERENCE_FUNCTIONAL_COMPLETENESS_MATERIALIZED",
            "full_biophysical_simulation": "NOT_MATERIALIZED",
            "erotic_intent": "NONE",
            "intimate_interaction": "NOT_AUTHORIZED",
            "canonical_effect": "NONE",
            "subjectivity_conclusion": "NOT_ESTABLISHED",
        }
    elif args.command == "non-claims":
        payload = {
            "anatomy_does_not_establish_gender_identity": True,
            "physiology_does_not_establish_felt_sensation": True,
            "physiology_does_not_establish_sexual_desire": True,
            "normal_reproductive_physiology_is_not_erotic_intent": True,
            "anatomy_or_physiology_does_not_establish_subjectivity": True,
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
    elif args.command == "teacher-avatar-continuous-glb-info":
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
    elif args.command == "teacher-avatar-reference-bundle":
        if not args.output_dir:
            parser.error("teacher-avatar-reference-bundle requires --output-dir")
        payload = asdict(write_teacher_reference_bundle(args.output_dir))
    elif args.command == "teacher-avatar-lod-manifest":
        payload = build_teacher_lod_manifest()
    elif args.command == "teacher-avatar-collision-profile":
        payload = asdict(build_teacher_collision_profile())
    else:
        teacher_contract = build_teacher_avatar_contract()
        aion = build_adult_male_physiology_reference("AION_REFERENCE_BODY")
        astra = build_adult_male_physiology_reference("ASTRA_REFERENCE_BODY")
        teacher = build_adult_male_physiology_reference(teacher_contract.body_id)
        payload = {
            "aion": aion.to_dict(),
            "astra": astra.to_dict(),
            "teacher": teacher.to_dict(),
            "parity": validate_physiology_parity((aion, astra, teacher)),
        }

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
