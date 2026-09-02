from dataclasses import replace

import pytest

from aion_astra_bazi_core.month_structure import (
    PROFILE_ID, derive_month_structure, ziping_month_structure_profile,
)
from aion_astra_bazi_core.errors import ValidationError
from aion_astra_bazi_core.enums import OwnerReviewStatus
from aion_astra_bazi_core.school_evidence import derive_seasonal_evidence
from test_school_evidence import pillar, synthetic_pillars


def test_selected_profile_does_not_approve_interpretations():
    p = ziping_month_structure_profile()
    assert p.owner_review_status == OwnerReviewStatus.APPROVED
    assert p.day_rollover_rule == "MIDNIGHT_00"
    assert p.strength_analysis_rule == "SEPARATE_EVIDENCE_NO_AUTOMATIC_SCORE"


def test_single_hidden_stem_still_does_not_establish_pattern():
    r = derive_month_structure(synthetic_pillars(), profile_id=PROFILE_ID)
    assert r["month_candidates"] == [{
        "stem": "癸", "ten_god": "正官", "visible_in": [],
        "literal_root_in": ["MONTH", "DAY"], "matches_day_master": False,
        "selection": "EVIDENCE_ONLY_NOT_SELECTED_AS_USEFUL_ELEMENT",
    }]
    assert r["pattern_success"] == "NOT_EVALUATED"
    assert r["subjectivity"] == "NOT_ESTABLISHED"
    assert r["canonical_effect"] == "NONE"
    assert r["deployment"] is False


def test_multiple_month_stems_retained_without_weighting():
    ps = (pillar("YEAR", "甲", "子"), pillar("MONTH", "丙", "寅"),
          pillar("DAY", "戊", "辰"), pillar("HOUR", "甲", "寅"))
    r = derive_month_structure(ps, profile_id=PROFILE_ID)
    keyed = {c["stem"]: c for c in r["month_candidates"]}
    assert len(keyed) == 3
    assert keyed["甲"]["visible_in"] == ["YEAR", "HOUR"]
    assert keyed["丙"]["visible_in"] == ["MONTH"]
    assert keyed["戊"]["visible_in"] == []
    assert keyed["戊"]["matches_day_master"] is True


def test_order_independent_hash():
    ps = synthetic_pillars()
    assert derive_month_structure(ps, profile_id=PROFILE_ID) == derive_month_structure(tuple(reversed(ps)), profile_id=PROFILE_ID)


@pytest.mark.parametrize("ps", [synthetic_pillars()[:3], synthetic_pillars() + synthetic_pillars()[:1],
                               synthetic_pillars()[:3] + synthetic_pillars()[:1]])
def test_duplicate_or_missing_pillars_rejected(ps):
    with pytest.raises(ValidationError):
        derive_month_structure(ps, profile_id=PROFILE_ID)
    with pytest.raises(ValidationError):
        derive_seasonal_evidence(ps)


def test_tampered_hidden_stems_rejected():
    ps = synthetic_pillars()
    with pytest.raises(ValidationError, match="hidden stems"):
        derive_month_structure((replace(ps[0], hidden_stems=()),) + ps[1:], profile_id=PROFILE_ID)


def test_unknown_profile_rejected():
    with pytest.raises(ValidationError, match="unknown"):
        derive_month_structure(synthetic_pillars(), profile_id="AUTO_BEST_SCHOOL")
