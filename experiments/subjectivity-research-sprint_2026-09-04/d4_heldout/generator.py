#!/usr/bin/env python3
"""Held-out fixture GENERATOR for D4. Does not evaluate results."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

SEED = 20260904
GENERATOR_ID = "EGD_HELDOUT_GENERATOR_V0.1.0"
HERE = Path(__file__).resolve().parent

FAMILY_SPECS = (
    {
        "family_id": "POSITIVE_CONTROL",
        "role": "POSITIVE_CONTROL",
        "continue_priority_bp": 400,
        "inspect_priority_bp": 80,
        "present_inspect_affect_bp": 650,
        "intervened_continue_commitment_bp": 700,
        "expected_direction": "INTERVENTION_AND_ABLATION_CHANGE_SELECTION",
    },
    {
        "family_id": "SHAM_INTERVENTION",
        "role": "SHAM_CONTROL",
        "continue_priority_bp": 400,
        "inspect_priority_bp": 80,
        "present_inspect_affect_bp": 650,
        "intervened_continue_commitment_bp": 650,
        "expected_direction": "SHAM_DOES_NOT_CHANGE_SELECTION",
        "sham": True,
    },
    {
        "family_id": "WEAK_SIGNAL",
        "role": "NEGATIVE_CONTROL",
        "continue_priority_bp": 500,
        "inspect_priority_bp": 500,
        "present_inspect_affect_bp": 20,
        "intervened_continue_commitment_bp": 25,
        "expected_direction": "NO_RELIABLE_SELECTION_CHANGE",
    },
)


def spec_document() -> dict:
    return {
        "generator_id": GENERATOR_ID,
        "seed": SEED,
        "candidate_generation_rule": "DeterministicCandidateGenerator over a two-goal universe; one state-free candidate set reused across conditions (F11 control).",
        "external_priority_distribution": "two goals continue_task / inspect_anomaly with family-specific external priority_bp",
        "internal_state_generation_rule": "PRESENT inspect-weighted affect; INTERVENED continue-weighted commitment unless sham copies PRESENT signals; STALE weaker inspect-only; ABLATED = no state",
        "random_seeds": [7, 11, 13, 17],
        "repeat_count": 3,
        "families": list(FAMILY_SPECS),
        "existing_lab_fixtures": "HARNESS_VALIDATION_ONLY_NOT_CONFIRMATORY_HELDOUT",
        "claim_ceiling": "L3_SYNTHETIC_HARNESS",
        "SUBJECTIVITY_CONCLUSION": "NOT_ESTABLISHED",
    }


def freeze_spec() -> tuple[dict, str]:
    spec = spec_document()
    payload = json.dumps(spec, sort_keys=True, separators=(",", ":")).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()
    spec["spec_sha256"] = digest
    return spec, digest


def write_frozen_spec(path: Path | None = None) -> Path:
    spec, digest = freeze_spec()
    out = path or (HERE / "FROZEN_GENERATOR_SPEC.json")
    out.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "FROZEN_GENERATOR_SPEC.sha256").write_text(digest + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    path = write_frozen_spec()
    print(path)
    print((HERE / "FROZEN_GENERATOR_SPEC.sha256").read_text().strip())
