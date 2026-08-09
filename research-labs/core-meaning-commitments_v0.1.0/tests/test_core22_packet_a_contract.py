from __future__ import annotations

import json
from pathlib import Path


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "core22_packet_a.json"


def load_packet() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_packet_declares_exactly_ten_primitives() -> None:
    packet = load_packet()
    primitives = packet["primitives"]
    assert isinstance(primitives, list)
    assert len(primitives) == 10
    assert len({item["name"] for item in primitives}) == 10


def test_every_primitive_has_reconciliation_contract_fields() -> None:
    packet = load_packet()
    required = {
        "name",
        "research_anchors",
        "source_material",
        "disposition",
        "missing_fields",
        "non_claims",
        "test_targets",
    }
    for item in packet["primitives"]:
        assert required <= set(item)
        assert item["research_anchors"]
        assert item["disposition"]
        assert item["non_claims"]
        assert item["test_targets"]


def test_packet_has_no_runtime_or_canonical_effect() -> None:
    packet = load_packet()
    assert packet["canonical_effect"] == "NONE"
    assert packet["runtime_effect"] == "NONE"
    assert packet["mcp_effect"] == "NONE"
    assert packet["writeback_effect"] == "NONE"
    assert packet["new_core_constructs"] is False
    assert packet["ontology_promotion"] is False


def test_automatic_relevance_remains_off() -> None:
    packet = load_packet()
    assert packet["automatic_relevance"] is False
    relevance = next(item for item in packet["primitives"] if item["name"] == "ExplicitRelevanceBaseline")
    assert relevance["disposition"] == "REUSE_BASELINE"


def test_construct_20_21_22_are_not_overclaimed_as_implemented() -> None:
    packet = load_packet()
    by_name = {item["name"]: item for item in packet["primitives"]}
    assert by_name["ConflictRelationPrimitive"]["disposition"] == "REUSE_AS_PRIMITIVE_ONLY"
    assert "CONFLICT_RECORDED != CONSTRUCT_20_IMPLEMENTED" in by_name["ConflictRelationPrimitive"]["non_claims"]
    assert by_name["DeferredJudgmentRecordCandidate"]["disposition"] == "FIXTURE_ONLY_NOT_IMPLEMENTED"
    assert by_name["TemporalResolutionViewCandidate"]["disposition"] == "FIXTURE_ONLY_NOT_IMPLEMENTED"


def test_local_provenance_is_not_treated_as_full_construct_18() -> None:
    packet = load_packet()
    claim = next(item for item in packet["primitives"] if item["name"] == "CandidateClaimRecord")
    assert "full_construct_18_provenance" in claim["missing_fields"]


def test_fixture_only_candidates_are_explicitly_incomplete() -> None:
    packet = load_packet()
    by_name = {item["name"]: item for item in packet["primitives"]}
    deferred = by_name["DeferredJudgmentRecordCandidate"]
    temporal = by_name["TemporalResolutionViewCandidate"]
    assert "reopen_condition" in deferred["missing_fields"]
    assert "decision_lineage" in deferred["missing_fields"]
    assert "as_was_state" in temporal["missing_fields"]
    assert "transition_lineage" in temporal["missing_fields"]
    assert "current_retrospective_interpretation" in temporal["missing_fields"]
