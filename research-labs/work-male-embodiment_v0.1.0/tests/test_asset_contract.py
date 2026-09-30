import pytest

from work_male_embodiment.asset_contract import (
    AssetCandidateEvidence,
    AssetFormat,
    VerificationState,
    build_asset_contract,
    verify_asset_candidate,
)


IDS = tuple(f"m{i}" for i in range(67))


def test_asset_contract_requires_all_geometry_rig_and_verification_surfaces():
    contract = build_asset_contract(IDS)
    ok, missing = verify_asset_candidate(contract, AssetCandidateEvidence())
    assert not ok
    assert {
        "actual_3d_mesh",
        "67_measurements_verified",
        "rig_nodes",
        "joint_limits",
        "collision_geometry",
        "mass_properties",
        "skinning",
        "external_geometry_nodes",
        "prepuce_mobility_geometry",
    } <= set(missing)


def test_unverified_asset_cannot_smuggle_mesh_evidence():
    with pytest.raises(ValueError, match="unverified asset"):
        AssetCandidateEvidence(
            status=VerificationState.REQUIRED_UNVERIFIED,
            asset_format=AssetFormat.GLTF,
        )


def test_mesh_claim_requires_path_format_and_sha():
    with pytest.raises(ValueError, match="mesh claim"):
        AssetCandidateEvidence(
            status=VerificationState.CANDIDATE_PRESENT,
            actual_3d_mesh=True,
        )
