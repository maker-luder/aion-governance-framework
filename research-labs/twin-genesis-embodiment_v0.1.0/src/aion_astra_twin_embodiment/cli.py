from __future__ import annotations

import argparse
import json
from pathlib import Path

from .probe import run_probe


def _root() -> Path:
    return Path(__file__).resolve().parents[2]


def qa_status() -> dict[str, object]:
    return {
        "status": "IMPLEMENTED_SYNTHETIC_REFERENCE_EXTENSION_PENDING_REVIEW",
        "aion_body": "AION_3D_MALE_BODY_REFERENCE_v0.1",
        "astra_body": "ASTRA_3D_MALE_BODY_REFERENCE_v0.3",
        "aion_anthropometry_fields": 67,
        "astra_anthropometry_fields": 67,
        "whole_body_systems": 19,
        "physiology_profile": "ADULT_MALE_PHYSIOLOGY_REFERENCE_v0.1",
        "procedural_rig_reference": True,
        "actual_3d_mesh": False,
        "physical_body": False,
        "body_sensation": "NOT_ESTABLISHED",
        "body_ownership_experience": "NOT_ESTABLISHED",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
        "action_authority": "NONE",
        "canonical_effect": "NONE",
        "deployment": False,
    }


def _probe() -> dict[str, object]:
    root = _root()
    return run_probe(
        root / "data/AION_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json",
        root / "data/ASTRA_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json",
        root / "assets/aion_reference_rig.gltf",
        root / "assets/astra_reference_rig.gltf",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="AION/Astra twin embodiment candidate CLI")
    parser.add_argument("command", choices=["qa-status", "probe", "non-claims"])
    args = parser.parse_args()

    if args.command == "qa-status":
        payload: dict[str, object] = qa_status()
    elif args.command == "probe":
        payload = _probe()
    else:
        payload = {
            "shared_genesis_does_not_establish_shared_identity": True,
            "anatomy_does_not_establish_gender_identity": True,
            "signal_does_not_establish_sensation": True,
            "physiology_does_not_establish_desire": True,
            "body_state_does_not_establish_body_ownership": True,
            "runtime_binding_does_not_establish_subjectivity": True,
            "procedural_rig_does_not_establish_physical_body": True,
        }
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
