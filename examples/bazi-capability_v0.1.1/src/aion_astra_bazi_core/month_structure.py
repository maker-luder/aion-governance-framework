"""Selected month-structure evidence, not automatic successful-pattern judgment."""
from __future__ import annotations

from dataclasses import asdict, replace

from .constants import HIDDEN_STEMS, STEM_ELEMENTS
from .engine import ten_god
from .enums import OwnerReviewStatus
from .errors import ValidationError
from .models import BaziRuleProfile, Pillar
from .rule_profiles import standard_lichun_profile
from .school_evidence import build_bazi_school_evidence
from .serialization import derivation_hash

PROFILE_ID = "AION_ZIPING_MONTH_STRUCTURE_V1"


def ziping_month_structure_profile() -> BaziRuleProfile:
    """2026-09-03 Owner-selected method; not an approval of a person's reading."""
    return replace(
        standard_lichun_profile(),
        rule_profile_id=PROFILE_ID,
        profile_name="AION Ziping month-structure evidence / civil midnight",
        version="1.0.0",
        structure_rule="MONTH_HIDDEN_STEM_EXPOSURE_AND_ROOT_EVIDENCE_V1",
        strength_analysis_rule="SEPARATE_EVIDENCE_NO_AUTOMATIC_SCORE",
        useful_element_rule="STRUCTURE_SUPPORT_AND_CLIMATE_TERMS_SEPARATE",
        transformation_rule="CANDIDATES_ONLY_CONDITIONS_NOT_EVALUATED",
        source_references=standard_lichun_profile().source_references + (
            "docs/research/DOMAIN_METHOD_DECISION_2026_09_03.md",
            "ZIPING_ZHENQUAN_LUN_YONGSHEN_TEXT_NOT_XU_COMMENTARY",
        ),
        owner_review_status=OwnerReviewStatus.APPROVED,
    )


def derive_month_structure(pillars: tuple[Pillar, ...], *, profile_id: str) -> dict[str, object]:
    """Expose month candidates and literal roots; no weights or forced selection.

    A root means exact stem membership in the frozen hidden-stem table, not
    assessed effective strength. The day-master position is not a second
    exposed month stem. Multiple candidates remain multiple.
    """
    if profile_id != PROFILE_ID:
        raise ValidationError("unknown month-structure profile")
    if len(pillars) != 4 or {p.name for p in pillars} != {"YEAR", "MONTH", "DAY", "HOUR"}:
        raise ValidationError("exactly four unique named pillars required")
    by_name = {p.name: p for p in pillars}
    ordered = tuple(by_name[n] for n in ("YEAR", "MONTH", "DAY", "HOUR"))
    for p in ordered:
        if p.stem not in STEM_ELEMENTS or p.branch not in HIDDEN_STEMS:
            raise ValidationError("invalid stem or branch")
        if p.hidden_stems != HIDDEN_STEMS[p.branch]:
            raise ValidationError("hidden stems differ from the frozen table")
    day = by_name["DAY"].stem
    candidates = []
    for stem in by_name["MONTH"].hidden_stems:
        candidates.append({
            "stem": stem,
            "ten_god": ten_god(day, stem),
            "visible_in": [p.name for p in ordered if p.name != "DAY" and p.stem == stem],
            "literal_root_in": [p.name for p in ordered if stem in p.hidden_stems],
            "matches_day_master": stem == day,
            "selection": "EVIDENCE_ONLY_NOT_SELECTED_AS_USEFUL_ELEMENT",
        })
    result = {
        "profile_id": PROFILE_ID,
        "method_selection": "OWNER_SELECTED_2026_09_03",
        "calendar_profile": asdict(ziping_month_structure_profile()),
        "day_master": day,
        "month_branch": by_name["MONTH"].branch,
        "month_candidates": candidates,
        "raw_evidence": asdict(build_bazi_school_evidence(ordered)),
        "pattern_success": "NOT_EVALUATED",
        "strength": "NOT_DERIVED",
        "climate_assessment": "NOT_DERIVED_SEPARATE_LAYER",
        "useful_element": "NOT_SELECTED",
        "interpretation_status": "NOT_PERFORMED",
        "subjectivity": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
        "deployment": False,
        "action_authority": "NONE",
    }
    return {**result, "derivation_hash": derivation_hash(result)}
