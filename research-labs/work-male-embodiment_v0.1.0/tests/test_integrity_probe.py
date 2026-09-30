from dataclasses import replace
from pathlib import Path

from work_male_embodiment.integrity import (
    build_snapshot_receipts,
    verify_snapshot_receipts,
)
from work_male_embodiment.probe import run_probe


PROFILE = (
    Path(__file__).resolve().parents[3]
    / "docs/research/embodiment/WORK_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"
)


def test_snapshot_receipts_detect_payload_and_receipt_tampering():
    payloads = ("a", "b", "c")
    receipts = build_snapshot_receipts(payloads)
    assert verify_snapshot_receipts(payloads, receipts)
    assert not verify_snapshot_receipts(("a", "B", "c"), receipts)
    tampered = list(receipts)
    tampered[1] = replace(tampered[1], payload_sha256="f" * 64)
    assert not verify_snapshot_receipts(payloads, tuple(tampered))


def test_probe_is_deterministic_and_fail_closed_about_missing_asset():
    first = run_probe(PROFILE)
    second = run_probe(PROFILE)
    assert first["body_state"]["fingerprint"] == second["body_state"]["fingerprint"]
    assert first["physiology"]["fingerprint"] == second["physiology"]["fingerprint"]
    assert first["integrity"]["final_receipt"] == second["integrity"]["final_receipt"]
    assert first["asset"]["verified"] is False
    assert first["asset"]["actual_3d_mesh"] is False
    assert "actual_3d_mesh" in first["asset"]["missing"]
    assert first["boundaries"]["subjectivity"] == "NOT_ESTABLISHED"
    assert first["boundaries"]["human_consent_inference"] == "FORBIDDEN"
