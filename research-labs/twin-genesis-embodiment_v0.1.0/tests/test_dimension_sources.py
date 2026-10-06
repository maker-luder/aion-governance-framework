from __future__ import annotations

from aion_astra_twin_embodiment.dimension_sources import (
    build_dimension_source_manifest,
    source_map,
    validate_dimension_source_manifest,
)


def test_source_manifest_separates_primary_tiger_and_practitioner_sources():
    result = validate_dimension_source_manifest()
    assert result["result"] == "PASS"
    assert int(result["primary_tiger_source_count"]) >= 6
    assert int(result["community_practitioner_source_count"]) >= 5


def test_practitioner_sources_do_not_claim_tiger_biology():
    sources = build_dimension_source_manifest()
    practitioners = [source for source in sources if source.source_class == "COMMUNITY_PRACTITIONER"]
    assert practitioners
    for source in practitioners:
        assert "tiger_biology" in source.does_not_support


def test_usfws_source_is_explicitly_forensic_not_live_normal_range():
    source = source_map()["USFWS_YATES_2005_TIGER_GENITAL_ID"]
    assert source.source_class == "INSTITUTIONAL_FORENSICS"
    assert "live_penile_normal_range" in source.does_not_support
