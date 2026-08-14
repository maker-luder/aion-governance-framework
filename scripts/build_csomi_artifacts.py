#!/usr/bin/env python3
"""Materialize reviewer-facing CSOMI artifact subsets from the canonical packet."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = ROOT / "research-workbench/cross-substrate-other-minds-inference-2026-08-14/CSOMI_PACKET_V0.1.0.json"
OUT = ROOT / "research-labs/cross-substrate-other-minds-inference_v0.1.0/artifacts"


def write(name: str, payload: dict) -> None:
    target = OUT / name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    packet = json.loads(PACKET.read_text(encoding="utf-8"))
    identity = {
        "schema_version": packet["schema_version"],
        "packet_id": packet["packet_id"],
        "milestone": packet["milestone"],
        "branch": packet["branch"],
        "base_head": packet["base_head"],
    }
    write("CSOMI_CLAIM_RECORD_V0.1.0.json", {**identity, "claim_records": packet["claim_records"]})
    write("CSOMI_EVIDENCE_MATRIX_V0.1.0.json", {**identity, "evidence_channels": packet["evidence_channels"], "evidence_matrix": packet["evidence_matrix"]})
    write("CSOMI_DISANALOGY_MATRIX_V0.1.0.json", {**identity, "disanalogy_matrix": packet["disanalogy_matrix"]})
    write("CSOMI_FALSIFIER_MATRIX_V0.1.0.json", {**identity, "falsifier_matrix": packet["falsifier_matrix"]})
    write("CSOMI_VERTICAL_SLICE_V0.1.0.json", {**identity, "vertical_slice": packet["vertical_slice"]})
    print(f"materialized CSOMI artifacts={5}")


if __name__ == "__main__":
    main()
