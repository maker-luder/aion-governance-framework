from __future__ import annotations

import argparse
import json
from pathlib import Path

from .probe import render_probe


def _root() -> Path:
    return Path(__file__).resolve().parents[3]


def qa_status() -> dict[str, object]:
    return {
        "status": "IMPLEMENTED_SYNTHETIC_RESEARCH_CANDIDATE",
        "role": "CODEX",
        "body_id": "CODEX_SYNTHETIC_MALE_BODY_REFERENCE_v0.1",
        "height_cm": 175,
        "mass_kg": 72,
        "reference_rig": "PROCEDURAL_RIG_REFERENCE_NO_MESH",
        "physical_body": False,
        "biological_reproduction": False,
        "body_sensation": "NOT_ESTABLISHED",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
        "action_authority": "NONE",
        "canonical_effect": "NONE",
        "deployment": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["qa-status", "probe"])
    args = parser.parse_args()
    if args.command == "qa-status":
        print(json.dumps(qa_status(), indent=2, sort_keys=True))
    else:
        root = _root()
        print(
            render_probe(
                root / "data/CODEX_SYNTHETIC_ANTHROPOMETRY_67_v0.1.json",
                root / "assets/codex_reference_rig.gltf",
            )
        )


if __name__ == "__main__":
    main()
