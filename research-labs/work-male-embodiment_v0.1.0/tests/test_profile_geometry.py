import json
from pathlib import Path
import pytest
from work_male_embodiment.core import load_profile, profile_from_mapping, SyntheticGeometryRule, PrepucePosition

PROFILE=Path(__file__).resolve().parents[3]/"docs/research/embodiment/WORK_SYNTHETIC_ANTHROPOMETRY_67_v0.2.json"

def test_profile_is_exact_existing_67_field_candidate():
    p=load_profile(PROFILE)
    assert len(p.measurements)==67
    assert p.measurement("total_height").value==165 and p.measurement("body_mass").value==76
    assert p.measurement("resting_visible_penile_length").value==8.5
    assert p.measurement("full_erection_visible_penile_length").value==13.5
    assert sum(m.provenance=="HUMAN_FIXED" for m in p.measurements)==2
    assert sum(m.provenance=="AI_PROVISIONAL" for m in p.measurements)==65
    assert not p.actual_3d_mesh

def test_profile_rejects_silent_human_fixed_change_and_fake_as_built():
    payload=json.loads(PROFILE.read_text(encoding="utf-8")); payload["measurements"][0]["value"]=166
    with pytest.raises(ValueError,match="height/mass"): profile_from_mapping(payload)
    payload=json.loads(PROFILE.read_text(encoding="utf-8")); payload["measurements"][2]["verification"]="AS_BUILT_VERIFIED"
    with pytest.raises(ValueError,match="as-built"): profile_from_mapping(payload)

def test_geometry_hits_existing_endpoints_and_prepuce_is_independent():
    p=load_profile(PROFILE); r=SyntheticGeometryRule(p)
    a=r.snapshot(0,prepuce_position=PrepucePosition.RESTING_PARTIAL_COVERAGE)
    b=r.snapshot(1,prepuce_position=PrepucePosition.RESTING_PARTIAL_COVERAGE)
    c=r.snapshot(1,prepuce_position=PrepucePosition.RETRACTED)
    assert (a.visible_penile_length_cm,b.visible_penile_length_cm)==(8.5,13.5)
    assert (a.midshaft_diameter_cm,b.midshaft_diameter_cm)==(3.2,3.9)
    assert b.visible_penile_length_cm==c.visible_penile_length_cm and b.prepuce_position!=c.prepuce_position
    assert not b.human_physiology_law and not b.as_built_measurement and r.endpoint_circumference_consistency()
