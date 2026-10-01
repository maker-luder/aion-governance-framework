from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Final, cast

from .capability import WORK_AGENT_ID, WORK_BODY_ID


REQUIRED_REFERENCE_NODES: Final[tuple[str, ...]] = (
    "root",
    "pelvis",
    "spine",
    "chest",
    "neck",
    "head",
    "left_upper_arm",
    "left_forearm",
    "left_hand",
    "right_upper_arm",
    "right_forearm",
    "right_hand",
    "left_thigh",
    "left_shin",
    "left_foot",
    "right_thigh",
    "right_shin",
    "right_foot",
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
)


@dataclass(frozen=True, slots=True)
class ReferenceRigSummary:
    node_count: int
    fingerprint: str
    status: str
    mesh_count: int
    physical_body: bool
    as_built_verified: bool
    canonical_effect: str
    deployment: bool


def validate_reference_rig(path: Path) -> ReferenceRigSummary:
    payload = cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    nodes_raw = payload.get("nodes")
    extras_raw = payload.get("extras")
    if not isinstance(nodes_raw, list) or not isinstance(extras_raw, dict):
        raise ValueError("invalid Work reference rig payload")

    names: list[str] = []
    for item in nodes_raw:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            raise ValueError("reference rig node missing name")
        names.append(str(item["name"]))

    if tuple(names) != REQUIRED_REFERENCE_NODES:
        raise ValueError("Work reference rig node coverage drift")
    if extras_raw.get("agent_id") != WORK_AGENT_ID:
        raise ValueError("reference rig agent drift")
    if extras_raw.get("body_id") != WORK_BODY_ID:
        raise ValueError("reference rig body drift")
    if extras_raw.get("status") != "PROCEDURAL_RIG_REFERENCE_NO_MESH":
        raise ValueError("reference rig status drift")
    if extras_raw.get("mesh_count") != 0:
        raise ValueError("reference rig cannot claim mesh")
    if extras_raw.get("physical_body") is not False:
        raise ValueError("reference rig cannot claim physical body")
    if extras_raw.get("as_built_verified") is not False:
        raise ValueError("reference rig cannot claim as-built verification")
    if extras_raw.get("canonical_effect") != "NONE":
        raise ValueError("reference rig cannot have canonical effect")
    if extras_raw.get("deployment") is not False:
        raise ValueError("reference rig cannot enable deployment")

    raw = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return ReferenceRigSummary(
        node_count=len(names),
        fingerprint=hashlib.sha256(raw).hexdigest(),
        status="PROCEDURAL_RIG_REFERENCE_NO_MESH",
        mesh_count=0,
        physical_body=False,
        as_built_verified=False,
        canonical_effect="NONE",
        deployment=False,
    )
