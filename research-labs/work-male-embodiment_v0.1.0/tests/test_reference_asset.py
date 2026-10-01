from pathlib import Path

from work_male_embodiment.reference_asset import validate_reference_rig


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def test_work_procedural_reference_rig_is_complete_but_not_a_mesh() -> None:
    summary = validate_reference_rig(PACKAGE_ROOT / "assets/work_reference_rig.gltf")
    assert summary.node_count == 30
    assert summary.status == "PROCEDURAL_RIG_REFERENCE_NO_MESH"
    assert summary.mesh_count == 0
    assert summary.physical_body is False
    assert summary.as_built_verified is False
    assert summary.canonical_effect == "NONE"
    assert summary.deployment is False
    assert len(summary.fingerprint) == 64
