import hashlib
import json
from pathlib import Path

import pytest

from codex_male_embodiment.asset_contract import (
    AssetCandidateEvidence,
    AssetFormat,
    VerificationState,
    build_asset_contract,
    verify_asset_candidate,
)
from codex_male_embodiment.core import load_profile


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "data/CODEX_SYNTHETIC_ANTHROPOMETRY_67_v0.1.json"
RIG = ROOT / "assets/codex_reference_rig.gltf"


def _rig_evidence() -> AssetCandidateEvidence:
    raw = RIG.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    external = {"penis", "glans", "prepuce", "frenulum", "scrotum"}
    names = [str(item["name"]) for item in payload["nodes"]]
    return AssetCandidateEvidence(
        status=VerificationState.PROCEDURAL_RIG_REFERENCE,
        asset_format=AssetFormat.GLTF,
        asset_path=str(RIG),
        sha256=hashlib.sha256(raw).hexdigest(),
        rig_nodes_present=tuple(name for name in names if name not in external),
        external_geometry_nodes_present=tuple(name for name in names if name in external),
    )


def test_reference_rig_is_present_but_not_a_mesh() -> None:
    profile = load_profile(PROFILE)
    contract = build_asset_contract(tuple(item.id for item in profile.measurements))
    evidence = _rig_evidence()
    ok, missing = verify_asset_candidate(contract, evidence)
    assert not ok
    assert "rig_nodes" not in missing
    assert "external_geometry_nodes" not in missing
    assert "actual_3d_mesh" in missing
    assert "collision_geometry" in missing
    assert evidence.actual_3d_mesh is False
    assert evidence.physical_body_present is False


def test_rig_reference_cannot_be_promoted_to_physical_body() -> None:
    evidence = _rig_evidence()
    with pytest.raises(ValueError, match="physical/as-built"):
        AssetCandidateEvidence(
            status=evidence.status,
            asset_format=evidence.asset_format,
            asset_path=evidence.asset_path,
            sha256=evidence.sha256,
            rig_nodes_present=evidence.rig_nodes_present,
            external_geometry_nodes_present=evidence.external_geometry_nodes_present,
            physical_body_present=True,
        )
