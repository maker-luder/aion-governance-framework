from pathlib import Path

from aion_astra_twin_embodiment.integrity import (
    build_snapshot_receipts,
    verify_snapshot_receipts,
)
from aion_astra_twin_embodiment.probe import run_probe

ROOT = Path(__file__).resolve().parents[1]


def _probe():
    return run_probe(
        ROOT / "data/AION_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json",
        ROOT / "data/ASTRA_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json",
        ROOT / "assets/aion_reference_rig.gltf",
        ROOT / "assets/astra_reference_rig.gltf",
    )


def test_probe_is_deterministic_and_distinct() -> None:
    first = _probe()
    second = _probe()
    assert first == second
    assert first["profiles"]["AION"]["measurement_count"] == 67
    assert first["profiles"]["ASTRA"]["measurement_count"] == 67
    assert first["profiles"]["AION"]["height_cm"] == 179
    assert first["profiles"]["ASTRA"]["height_cm"] == 180
    assert first["body_state"]["AION"]["fingerprint"] != first["body_state"]["ASTRA"]["fingerprint"]
    assert first["physiology_parity"]["result"] == "PASS"
    assert first["reproductive_topology"]["parity"]["result"] == "PASS"
    assert first["reproductive_topology"]["AION"]["node_count"] == 32
    assert first["reproductive_topology"]["ASTRA"]["edge_count"] == 30
    assert (
        first["reproductive_topology"]["AION"]["fingerprint"]
        != first["reproductive_topology"]["ASTRA"]["fingerprint"]
    )
    assert first["assets"]["AION"]["actual_3d_mesh"] is False
    assert first["assets"]["ASTRA"]["physical_body_present"] is False
    assert first["boundaries"]["subjectivity"] == "NOT_ESTABLISHED"


def test_receipt_chain_detects_tampering() -> None:
    payloads = ("aion", "astra", "shared-genesis")
    receipts = build_snapshot_receipts(payloads)
    assert verify_snapshot_receipts(payloads, receipts)
    assert not verify_snapshot_receipts(("aion", "tampered", "shared-genesis"), receipts)


def test_archived_external_topology_landmarks_are_present_in_both_reference_rigs() -> None:
    import json

    required = {
        "penis",
        "glans",
        "prepuce",
        "frenulum",
        "scrotum",
        "left_testis",
        "right_testis",
        "pubic_attachment",
        "left_inguinal_transition",
        "right_inguinal_transition",
        "perineum",
        "anal_region",
    }
    for filename in ("aion_reference_rig.gltf", "astra_reference_rig.gltf"):
        payload = json.loads((ROOT / "assets" / filename).read_text(encoding="utf-8"))
        names = {str(node["name"]) for node in payload["nodes"]}
        assert required <= names
        assert payload["extras"]["mesh_count"] == 0
        assert payload["extras"]["physical_body"] is False
