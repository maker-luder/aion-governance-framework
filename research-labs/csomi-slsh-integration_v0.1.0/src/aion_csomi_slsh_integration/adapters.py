from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .authority import ReadOnlyAuthority, _git

CSOMI_CONTROL_FIXTURE = (
    "research-labs/cross-substrate-other-minds-inference_v0.1.0/fixtures/"
    "csomi_positive_negative_controls_v0.1.0.json"
)


def _read_json_at_ref(root: Path, resolved_ref: str, path: str) -> tuple[dict[str, Any], str]:
    raw = _git(root, "show", f"{resolved_ref}:{path}").encode("utf-8")
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw).hexdigest()


def build_adapter_inventory(root: Path, authority: ReadOnlyAuthority) -> dict[str, Any]:
    packet = authority.packet
    claims = packet.get("claim_records", [])
    channels = packet.get("evidence_channels", [])
    disanalogies = packet.get("disanalogy_matrix", [])
    falsifiers = packet.get("falsifier_matrix", packet.get("falsifiers", []))
    controls = packet.get("controls", [])
    auxiliary_artifacts: list[dict[str, str]] = []

    if authority.spec.framework == "CSOMI":
        fixture, fixture_hash = _read_json_at_ref(
            root, authority.resolved_ref, CSOMI_CONTROL_FIXTURE
        )
        controls = fixture.get("positive_controls", []) + fixture.get("negative_controls", [])
        auxiliary_artifacts.append(
            {
                "path": CSOMI_CONTROL_FIXTURE,
                "sha256": fixture_hash,
                "role": "CONTROL_IDENTIFIER_ONLY",
            }
        )

    return {
        "framework": authority.spec.framework,
        "authority_sha": authority.spec.authority_sha,
        "packet_id": packet.get("packet_id"),
        "claim_ids": sorted(item.get("id") for item in claims if item.get("id")),
        "evidence_channel_ids": sorted(item.get("id") for item in channels if item.get("id")),
        "disanalogy_ids": sorted(item.get("id") for item in disanalogies if item.get("id")),
        "control_ids": sorted(
            item.get("id", item.get("control_id"))
            for item in controls
            if item.get("id", item.get("control_id"))
        ),
        "falsifier_ids": sorted(item.get("id") for item in falsifiers if item.get("id")),
        "auxiliary_artifacts": auxiliary_artifacts,
        "semantic_projection": "IDENTIFIERS_AND_LINEAGE_ONLY",
        "no_source_claim_projection": True,
        "read_only": True,
    }
