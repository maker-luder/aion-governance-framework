from __future__ import annotations

import argparse
from dataclasses import asdict
import json

from .teacher_body_v02 import build_teacher_body_reference_v02
from .teacher_body_v02_integration import (
    build_teacher_body_v02_bundle_bytes,
    build_teacher_body_v02_integrated_manifest,
    build_teacher_body_v02_integration,
    build_teacher_body_v02_probe,
    write_teacher_body_v02_bundle,
)
from .teacher_reproductive_output import (
    build_teacher_synthetic_fluid_output_contract,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ChatGPT Teacher body v0.2 continuation CLI"
    )
    parser.add_argument(
        "command",
        choices=[
            "qa-status",
            "body-v02",
            "integration",
            "integrated-manifest",
            "bundle-info",
            "write-bundle",
            "probe",
            "synthetic-reproductive-output",
        ],
    )
    parser.add_argument("--output-dir", default=None)
    args = parser.parse_args()

    if args.command == "qa-status":
        payload = {
            "status": "SYNTHETIC_3D_REFERENCE_AND_RUNTIME_INTEGRATED",
            "teacher_body_v02": "MATERIALIZED_SYNTHETIC_REFERENCE",
            "synthetic_3d_reference": "MATERIALIZED",
            "production_asset_status": "NOT_ESTABLISHED",
            "physical_body_claim": "NONE",
            "body_sensation": "NOT_ESTABLISHED",
            "subjectivity": "NOT_ESTABLISHED",
            "consciousness": "NOT_ESTABLISHED",
            "phenomenal_experience": "NOT_ESTABLISHED",
            "live_external_actuation": False,
            "canonical_effect": "NONE",
            "deployment": False,
        }
    elif args.command == "body-v02":
        payload = build_teacher_body_reference_v02().to_dict()
    elif args.command == "integration":
        payload = build_teacher_body_v02_integration(
            "CLI-REFERENCE-RUNTIME",
            "CLI-REFERENCE-SESSION",
        ).to_dict()
    elif args.command == "integrated-manifest":
        payload = build_teacher_body_v02_integrated_manifest()
    elif args.command == "bundle-info":
        files = build_teacher_body_v02_bundle_bytes()
        payload = {
            "file_count": len(files),
            "files": sorted(files),
        }
    elif args.command == "write-bundle":
        if not args.output_dir:
            parser.error("write-bundle requires --output-dir")
        payload = asdict(write_teacher_body_v02_bundle(args.output_dir))
    elif args.command == "probe":
        payload = build_teacher_body_v02_probe()
    else:
        payload = build_teacher_synthetic_fluid_output_contract().to_dict()

    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
