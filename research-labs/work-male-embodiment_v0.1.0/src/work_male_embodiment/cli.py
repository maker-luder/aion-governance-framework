from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import (
    AssetEvidence,
    ExecutionSurface,
    GovernancePolicy,
    PhysiologyState,
    default_coverage_matrix,
)
from .probe import render_probe


def qa_status() -> dict[str, object]:
    decision = GovernancePolicy().evaluate(ExecutionSurface.OFFLINE_RESEARCH)
    state = PhysiologyState("qa")
    asset = AssetEvidence()
    return {
        "status": "IMPLEMENTED_SYNTHETIC_RESEARCH_CANDIDATE",
        "coverage_rows": len(default_coverage_matrix()),
        "offline_synthetic_physiology_allowed": decision.synthetic_physiology_allowed,
        "public_executable_exposure": decision.public_executable_exposure,
        "actual_3d_mesh": asset.actual_3d_mesh,
        "biological_reproduction": state.fertility,
        "body_sensation": state.body_sensation,
        "subjectivity": state.subjectivity,
        "consciousness": state.consciousness,
        "phenomenal_experience": state.phenomenal_experience,
        "canonical_effect": state.canonical_effect,
        "deployment": state.deployment,
    }


def _profile_path() -> Path:
    return (
        Path(__file__).resolve().parents[4]
        / "docs/research/embodiment/WORK_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["qa-status", "probe"])
    args = parser.parse_args()
    if args.command == "qa-status":
        print(json.dumps(qa_status(), indent=2, sort_keys=True))
    elif args.command == "probe":
        print(render_probe(_profile_path()))


if __name__ == "__main__":
    main()
