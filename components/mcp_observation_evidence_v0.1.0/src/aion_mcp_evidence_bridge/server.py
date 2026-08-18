from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

from .models import EvidenceEnvelope, EvidenceProvenance, make_tool_call_id, utc_now
from .store import EvidenceStore

READ_ONLY_ANNOTATIONS = ToolAnnotations(
    read_only_hint=True,
    destructive_hint=False,
    idempotent_hint=True,
    open_world_hint=False,
)


def _fixture_path() -> Path:
    return Path(__file__).resolve().parents[2] / "fixtures" / "observation_records.json"


def _provenance(tool_name: str, evidence_source_class: str, source_id: str, source_timestamp: str) -> EvidenceProvenance:
    return EvidenceProvenance(
        evidence_source_class=evidence_source_class,
        source_id=source_id,
        source_timestamp=source_timestamp,
        retrieval_timestamp=utc_now(),
        tool_name=tool_name,
        tool_call_id=make_tool_call_id(),
        authority="NONE",
    )


def _envelope(
    *,
    tool_name: str,
    subject: str,
    data: Mapping[str, Any],
    found: bool,
    evidence_source_class: str,
    source_id: str,
    source_timestamp: str,
) -> dict[str, Any]:
    return EvidenceEnvelope(
        subject=subject,
        found=found,
        data=dict(data),
        provenance=_provenance(tool_name, evidence_source_class, source_id, source_timestamp),
    ).to_dict()


def build_server(store: EvidenceStore | None = None) -> MCPServer:
    """Build the Phase 1 evidence-only server.

    The default store is fixture-backed and contains no private conversation,
    live Runtime, memory-store, identity-store, or canonical-state handle.
    """

    source = store if store is not None else EvidenceStore.from_json(_fixture_path())
    server = MCPServer(
        name="aion-observation-evidence-bridge",
        title="AION / Astra Observation Evidence Bridge",
        description="Pure-read observation, provenance, boundary and nonclaims evidence bridge.",
        instructions=(
            "This is a Phase 1 evidence-only bridge. Retrieval is not natural recall, not accepted fact, "
            "not memory ownership, not identity authority, and not canonical state. The server has no write tools."
        ),
        version="0.1.0",
    )

    @server.tool(
        name="list_continuity_observations",
        title="List continuity observations",
        description="List explicit synthetic/public continuity observations without promoting them to fact.",
        annotations=READ_ONLY_ANNOTATIONS,
    )
    def list_continuity_observations() -> dict[str, Any]:
        records = source.list_continuity_observations()
        return _envelope(
            tool_name="list_continuity_observations",
            subject="CONTINUITY_OBSERVATIONS",
            data={"records": records, "count": len(records)},
            found=True,
            evidence_source_class="SYNTHETIC_FIXTURE",
            source_id="fixture:observation_records.json",
            source_timestamp="UNKNOWN",
        )

    @server.tool(
        name="get_continuity_observation",
        title="Get one continuity observation",
        description="Get one explicit observation by id; missing records fail closed.",
        annotations=READ_ONLY_ANNOTATIONS,
    )
    def get_continuity_observation(observation_id: str) -> dict[str, Any]:
        record = source.get_continuity_observation(observation_id)
        return _envelope(
            tool_name="get_continuity_observation",
            subject=f"CONTINUITY_OBSERVATION:{observation_id}",
            data={} if record is None else {"record": record},
            found=record is not None,
            evidence_source_class="SYNTHETIC_FIXTURE",
            source_id="fixture:observation_records.json",
            source_timestamp="UNKNOWN",
        )

    @server.tool(
        name="search_provenance_records",
        title="Search provenance records",
        description="Search explicit provenance records by a bounded text query.",
        annotations=READ_ONLY_ANNOTATIONS,
    )
    def search_provenance_records(query: str) -> dict[str, Any]:
        records = source.search_provenance_records(query)
        return _envelope(
            tool_name="search_provenance_records",
            subject="PROVENANCE_RECORDS",
            data={"query": query, "records": records, "count": len(records)},
            found=bool(records),
            evidence_source_class="SYNTHETIC_FIXTURE",
            source_id="fixture:observation_records.json",
            source_timestamp="UNKNOWN",
        )

    @server.tool(
        name="get_source_attribution",
        title="Get source attribution",
        description="Get explicit attribution metadata without inferring identity or authorship.",
        annotations=READ_ONLY_ANNOTATIONS,
    )
    def get_source_attribution(record_id: str) -> dict[str, Any]:
        record = source.get_source_attribution(record_id)
        return _envelope(
            tool_name="get_source_attribution",
            subject=f"SOURCE_ATTRIBUTION:{record_id}",
            data={} if record is None else {"record": record},
            found=record is not None,
            evidence_source_class="SYNTHETIC_FIXTURE",
            source_id="fixture:observation_records.json",
            source_timestamp="UNKNOWN",
        )

    @server.tool(
        name="get_research_boundary",
        title="Get research boundary",
        description="Return the Phase 1 allowed inputs, excluded inputs and prohibited operations.",
        annotations=READ_ONLY_ANNOTATIONS,
    )
    def get_research_boundary() -> dict[str, Any]:
        boundary = source.get_research_boundary()
        return _envelope(
            tool_name="get_research_boundary",
            subject="RESEARCH_BOUNDARY",
            data=boundary,
            found=True,
            evidence_source_class=str(boundary.get("evidence_source_class", "COMPOSITE_GOVERNANCE_RECORD")),
            source_id="fixture:observation_records.json#research_boundary",
            source_timestamp=str(boundary.get("source_timestamp", "UNKNOWN")),
        )

    @server.tool(
        name="get_current_nonclaims",
        title="Get current nonclaims",
        description="Return fixed subjectivity, identity, memory, runtime, deployment and canonical nonclaims.",
        annotations=READ_ONLY_ANNOTATIONS,
    )
    def get_current_nonclaims() -> dict[str, Any]:
        nonclaims = source.get_current_nonclaims()
        return _envelope(
            tool_name="get_current_nonclaims",
            subject="CURRENT_NONCLAIMS",
            data=nonclaims,
            found=True,
            evidence_source_class=str(nonclaims.get("evidence_source_class", "COMPOSITE_GOVERNANCE_RECORD")),
            source_id="fixture:observation_records.json#current_nonclaims",
            source_timestamp=str(nonclaims.get("source_timestamp", "UNKNOWN")),
        )

    return server


def main() -> None:
    """Run only local stdio transport; no HTTP/SSE/public deployment is configured."""

    build_server().run(transport="stdio")


if __name__ == "__main__":  # pragma: no cover
    main()
