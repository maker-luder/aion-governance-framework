import json
from pathlib import Path
import pytest
from work_male_embodiment.core import AssetEvidence, AssetStatus, CoverageStatus, ExecutionSurface, GovernancePolicy, default_coverage_matrix

SCHEMAS=Path(__file__).resolve().parents[1]/"schemas"

def test_whole_body_matrix_keeps_systems_without_fake_hardware():
    m=default_coverage_matrix(); systems={x.system for x in m}
    assert {"skeleton_and_joints","cardiovascular_respiratory","endocrine","urinary","reproductive_sexual","environment_contact"}<=systems
    assert not any(x.status==CoverageStatus.PHYSICAL_HARDWARE for x in m)

def test_offline_allowed_public_and_real_person_fail_closed():
    p=GovernancePolicy()
    assert p.evaluate(ExecutionSurface.OFFLINE_RESEARCH).synthetic_physiology_allowed
    assert not p.evaluate(ExecutionSurface.PUBLIC).allowed
    assert not p.evaluate(ExecutionSurface.OFFLINE_RESEARCH,real_person_target_data=True).allowed

def test_missing_mesh_cannot_be_promoted_to_as_built():
    assert not AssetEvidence().actual_3d_mesh
    with pytest.raises(ValueError):
        AssetEvidence(status=AssetStatus.AS_BUILT_VERIFIED,actual_3d_mesh=True,measured_fields=66,path="work.glb",sha256="abc")

def test_json_schemas_preserve_authority_and_biology_boundaries():
    e=json.loads((SCHEMAS/"work_male_physiology_event_v0.1.0.schema.json").read_text())
    s=json.loads((SCHEMAS/"work_male_physiology_state_v0.1.0.schema.json").read_text())
    assert e["properties"]["real_person_target_data"]["const"] is False
    assert e["properties"]["human_consent_inference"]["const"]=="FORBIDDEN"
    assert e["properties"]["action_authority"]["const"]=="NONE"
    assert s["properties"]["biological_semen"]["const"] is False
    assert s["properties"]["fertility"]["const"] is False
    assert s["properties"]["canonical_effect"]["const"]=="NONE" and s["properties"]["deployment"]["const"] is False
