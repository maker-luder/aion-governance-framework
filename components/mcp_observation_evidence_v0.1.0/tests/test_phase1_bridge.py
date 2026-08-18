from __future__ import annotations

import ast
import json
from pathlib import Path

import anyio
from mcp.client import Client

from aion_mcp_evidence_bridge import EvidenceStore, build_server
from aion_mcp_evidence_bridge.store import validate_external_source_admission

COMPONENT = Path(__file__).resolve().parents[1]
SRC = COMPONENT / "src" / "aion_mcp_evidence_bridge"
FIXTURE = COMPONENT / "fixtures" / "observation_records.json"
EXPECTED_TOOLS = {
    "list_continuity_observations",
    "get_continuity_observation",
    "search_provenance_records",
    "get_source_attribution",
    "get_research_boundary",
    "get_current_nonclaims",
}
FORBIDDEN_MODULES = {
    "aion_runtime",
    "astra_runtime",
    "aion_memory_recall",
    "individual_runtime_state",
}
FORBIDDEN_OPERATION_NAMES = {
    "create_memory",
    "update_identity",
    "promote_canonical",
    "merge_subjects",
    "write_relationship_state",
    "infer_subjectivity",
    "remember",
    "recall",
    "run_task",
}


def _json(result: object) -> dict[str, object]:
    structured = getattr(result, "structured_content", None)
    assert isinstance(structured, dict)
    return structured


def test_fixture_is_synthetic_or_public_only() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    public_records = json.dumps({"observations": payload["observations"], "attributions": payload["attributions"]}, sort_keys=True)
    assert "private conversation" not in public_records.casefold()
    assert "transcript" not in public_records.casefold()
    assert "memory database" not in public_records.casefold()
    assert "newsletter" not in public_records.casefold()
    for record in payload["observations"]:
        assert record["privacy_class"] in {"SYNTHETIC", "PUBLIC"}
        assert record["canonical_effect"] == "NONE"
        assert record["accepted_as_fact"] is False


def test_store_is_immutable_and_returns_defensive_copies() -> None:
    store = EvidenceStore.from_json(FIXTURE)
    first = store.list_continuity_observations()
    first[0]["label"] = "tampered"
    first[0]["evidence_refs"].append("tampered")
    second = store.list_continuity_observations()
    assert second[0]["label"] != "tampered"
    assert "tampered" not in second[0]["evidence_refs"]
    assert not any(name in dir(store) for name in FORBIDDEN_OPERATION_NAMES)


def test_source_modules_do_not_import_runtime_or_recall_modules() -> None:
    for path in SRC.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = {alias.name.split(".")[0] for alias in node.names}
                assert imported.isdisjoint(FORBIDDEN_MODULES)
            if isinstance(node, ast.ImportFrom):
                assert (node.module or "").split(".")[0] not in FORBIDDEN_MODULES
                assert all(alias.name not in FORBIDDEN_OPERATION_NAMES for alias in node.names)


def test_mcp_surface_is_exactly_closed_world_read_only() -> None:
    async def scenario() -> None:
        async with Client(build_server(EvidenceStore.from_json(FIXTURE))) as client:
            listed = await client.list_tools()
            by_name = {tool.name: tool for tool in listed.tools}
            assert set(by_name) == EXPECTED_TOOLS
            for tool in by_name.values():
                annotations = tool.annotations
                assert annotations is not None
                assert annotations.read_only_hint is True
                assert annotations.destructive_hint is False
                assert annotations.idempotent_hint is True
                assert annotations.open_world_hint is False
            resources = await client.list_resources()
            assert resources.resources == []

    anyio.run(scenario)


def test_list_and_get_return_provenance_source_flags_and_nonclaims() -> None:
    async def scenario() -> None:
        async with Client(build_server(EvidenceStore.from_json(FIXTURE))) as client:
            listed = _json(await client.call_tool("list_continuity_observations", {}))
            assert listed["accepted_as_fact"] is False
            assert listed["canonical_effect"] == "NONE"
            assert listed["memory_write"] == "NONE"
            assert listed["identity_authority"] == "NONE"
            assert listed["retrieval_mechanism"] == "MCP_EXTERNAL_RETRIEVAL"
            assert listed["recall_source"] == listed["retrieval_mechanism"]
            provenance = listed["provenance"]
            assert isinstance(provenance, dict)
            for field in (
                "source_type",
                "evidence_source_class",
                "retrieval_mechanism",
                "source_id",
                "source_timestamp",
                "retrieval_timestamp",
                "tool_name",
                "tool_call_id",
                "authority",
                "canonical_effect",
            ):
                assert provenance.get(field)
            assert provenance["source_type"] == provenance["evidence_source_class"]
            assert provenance["source_timestamp"] == "UNKNOWN"
            observations = listed["data"]["records"]
            assert len(observations) == 2

            one = _json(
                await client.call_tool(
                    "get_continuity_observation",
                    {"observation_id": "obs-synthetic-19-month-continuity-001"},
                )
            )
            record = one["data"]["record"]
            assert record["claim_level"] == "L0_OBSERVATION"
            assert record["privacy_class"] == "SYNTHETIC"
            assert record["accepted_as_fact"] is False
            assert record["nonclaims"]["identity_continuity"] == "NOT_ESTABLISHED"

    anyio.run(scenario)


def test_queries_fail_closed_and_boundary_tools_are_non_mutating() -> None:
    async def scenario() -> None:
        store = EvidenceStore.from_json(FIXTURE)
        before = store.list_continuity_observations()
        async with Client(build_server(store)) as client:
            missing = _json(
                await client.call_tool(
                    "get_continuity_observation",
                    {"observation_id": "missing"},
                )
            )
            assert missing["found"] is False
            assert missing["data"] == {}
            assert missing["canonical_effect"] == "NONE"

            provenance = _json(
                await client.call_tool(
                    "search_provenance_records",
                    {"query": "public repository"},
                )
            )
            assert provenance["found"] is True
            assert provenance["data"]["count"] == 1

            attribution = _json(
                await client.call_tool(
                    "get_source_attribution",
                    {"record_id": "prov-public-repository-main-001"},
                )
            )
            assert attribution["found"] is True
            assert attribution["data"]["record"]["authority"] == "NONE"

            boundary = _json(await client.call_tool("get_research_boundary", {}))
            assert "call_existing_runtime_recall" in boundary["data"]["prohibited_operations"]
            assert "PRIVATE_CONVERSATION_BULK_INGEST" in boundary["data"]["excluded_inputs"]
            assert boundary["data"]["canonical_effect"] == "NONE"
            assert boundary["provenance"]["evidence_source_class"] == "COMPOSITE_GOVERNANCE_RECORD"
            assert boundary["provenance"]["source_timestamp"] == "UNKNOWN"

            nonclaims = _json(await client.call_tool("get_current_nonclaims", {}))
            assert nonclaims["data"]["subjectivity_conclusion"] == "NOT_ESTABLISHED"
            assert nonclaims["data"]["identity_continuity_conclusion"] == "NOT_ESTABLISHED"
            assert nonclaims["data"]["live_runtime_effect"] == "NONE"
            assert nonclaims["provenance"]["evidence_source_class"] == "COMPOSITE_GOVERNANCE_RECORD"
            assert nonclaims["provenance"]["source_timestamp"] == "UNKNOWN"

        assert store.list_continuity_observations() == before

    anyio.run(scenario)


def test_provenance_authority_and_executor_are_separated() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    records = {item["record_id"]: item for item in payload["provenance_records"]}

    owner = records["prov-human-owner-mcp-phase1-authorization-001"]
    teacher = records["prov-chatgpt-teacher-mcp-phase1-formalization-001"]
    executor = records["prov-manus-implementation-executor-unknown-001"]

    assert owner["source_type"] == "HUMAN_OWNER_AUTHORIZATION"
    assert owner["authority"] == "APPROVE_SCOPE"
    assert owner["source_timestamp"] == "UNKNOWN"
    assert teacher["source_type"] == "CHATGPT_TEACHER_FORMALIZATION"
    assert teacher["authority"] == "PROPOSE_REVIEW"
    assert teacher["source_timestamp"] == "UNKNOWN"
    assert owner["source_type"] != teacher["source_type"]
    assert executor["evidence_source_class"] == "TASK_EXECUTION_PROVENANCE"
    assert executor["orchestrator"] == "MANUS"
    assert executor["implementation_executor"] == "UNKNOWN"
    assert executor["source_timestamp"] == "UNKNOWN"


def test_retrieval_mechanism_and_evidence_source_class_are_distinct() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    for observation in payload["observations"]:
        assert observation["retrieval_mechanism"] == "MCP_EXTERNAL_RETRIEVAL"
        assert observation["evidence_source_class"] == "SYNTHETIC_FIXTURE"
        assert observation["retrieval_mechanism"] != observation["evidence_source_class"]


def test_external_source_admission_fails_closed_without_question_or_metadata() -> None:
    missing = validate_external_source_admission({"source_id": "https://example.invalid"})
    assert missing["admission"] == "HOLD_OR_DROP"
    assert set(missing["missing_fields"]) == {
        "existing_question",
        "provenance",
        "source_scope",
        "evidence_role",
    }
    assert missing["ingested"] is False
    assert missing["canonical_effect"] == "NONE"
    assert missing["subjectivity_evidence_weight"] == 0


def test_external_source_admission_is_metadata_only_and_rejects_bulk_ingest() -> None:
    candidate = {
        "existing_question": "Does an official document clarify the external-context/memory boundary?",
        "provenance": "official-source-reference",
        "source_scope": "OFFICIAL_EXTERNAL_DOCUMENTATION",
        "evidence_role": "BOUNDARY_REFERENCE",
        "bulk_ingest": True,
    }
    result = validate_external_source_admission(candidate)
    assert result["admission"] == "HOLD_OR_DROP"
    assert result["bulk_ingest"] is True
    assert result["ingested"] is False
    assert result["canonical_effect"] == "NONE"
