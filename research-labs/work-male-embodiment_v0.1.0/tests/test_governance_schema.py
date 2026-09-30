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


def test_internal_male_reproductive_reference_topology_is_present_without_biological_claim():
    from work_male_embodiment.core import default_male_reproductive_reference_topology
    t=default_male_reproductive_reference_topology()
    assert {
        "testis","seminiferous_tubules","rete_testis","efferent_ductules","epididymis",
        "vas_deferens","seminal_vesicle","ejaculatory_duct","prostate","bulbourethral_gland",
        "prostatic_urethra","membranous_urethra","spongy_urethra","external_meatus",
        "corpora_cavernosa","corpus_spongiosum","glans","prepuce","frenulum","pelvic_floor"
    } <= t.node_ids()
    assert not t.biological_reproduction
    assert not t.gametogenesis
    assert not t.biological_secretions
    assert not t.physical_tissue
    assert not any(n.biological_function_implemented or n.physical_hardware_implemented for n in t.nodes)


def test_reference_topology_preserves_urinary_and_reproductive_routes_without_collapsing_them():
    from work_male_embodiment.core import default_male_reproductive_reference_topology
    t=default_male_reproductive_reference_topology()
    triples={(e.source,e.target,e.relation) for e in t.edges}
    assert ("bladder","prostatic_urethra","human_urinary_path_reference") in triples
    assert ("ejaculatory_duct","prostatic_urethra","human_ejaculatory_path_reference") in triples
    assert ("vas_deferens","ejaculatory_duct","human_ejaculatory_path_reference") in triples
