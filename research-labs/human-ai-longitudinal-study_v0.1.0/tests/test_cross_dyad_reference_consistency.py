from __future__ import annotations

import json
from pathlib import Path


LAB_ROOT = Path(__file__).resolve().parents[1]


def _assert_single_payload_per_reference(
    packets: list[dict[str, object]],
    *,
    reference_key: str,
    payload_key: str,
) -> None:
    seen: dict[str, str] = {}
    for packet in packets:
        reference = packet[reference_key]
        payload = packet[payload_key]
        assert isinstance(reference, str)
        assert isinstance(payload, str)
        if reference in seen:
            assert seen[reference] == payload, (
                f"{reference_key} {reference!r} maps to multiple {payload_key} values"
            )
        else:
            seen[reference] = payload


def test_committed_condition_references_map_to_single_payload() -> None:
    fixture_path = LAB_ROOT / "fixtures" / "cross_dyad_condition_packets.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    packets = fixture["packets"]
    assert isinstance(packets, list)

    _assert_single_payload_per_reference(
        packets,
        reference_key="instruction_ref",
        payload_key="instruction_payload",
    )
    _assert_single_payload_per_reference(
        packets,
        reference_key="closure_rule_ref",
        payload_key="closure_rule_payload",
    )
