from pathlib import Path

from codex_male_embodiment.integrity import (
    build_snapshot_receipts,
    verify_snapshot_receipts,
)
from codex_male_embodiment.probe import run_probe


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "data/CODEX_SYNTHETIC_ANTHROPOMETRY_67_v0.1.json"
RIG = ROOT / "assets/codex_reference_rig.gltf"


def test_receipt_chain_detects_tampering() -> None:
    payloads = ("a", "b", "c")
    receipts = build_snapshot_receipts(payloads)
    assert verify_snapshot_receipts(payloads, receipts)
    assert not verify_snapshot_receipts(("a", "tampered", "c"), receipts)


def test_probe_is_deterministic_and_keeps_boundaries() -> None:
    first = run_probe(PROFILE, RIG)
    second = run_probe(PROFILE, RIG)
    assert first == second
    assert first["profile"]["height_cm"] == 175
    assert first["profile"]["mass_kg"] == 72
    assert first["profile"]["measurement_count"] == 67
    assert first["asset"]["status"] == "PROCEDURAL_RIG_REFERENCE"
    assert first["asset"]["actual_3d_mesh"] is False
    assert first["asset"]["physical_body_present"] is False
    assert first["boundaries"]["teacher_profile_state_shared"] is False
    assert first["boundaries"]["work_profile_state_shared"] is False
    assert first["boundaries"]["subjectivity"] == "NOT_ESTABLISHED"
    assert first["boundaries"]["action_authority"] == "NONE"
