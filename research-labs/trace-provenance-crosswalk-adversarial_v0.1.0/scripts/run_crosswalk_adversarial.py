from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_trace_crosswalk import AIONTraceEvent, TracePolicy
from aion_trace_crosswalk_adversarial import CrosswalkEntry, audit_event_batch, audit_source_entries, audit_source_entry, audit_trace_crosswalk


def event(event_id: str = "event:1", **overrides: object) -> AIONTraceEvent:
    values: dict[str, object] = {
        "session_id": "session:1",
        "user_id": "user:1",
        "agent_name": "agent:research",
        "span_kind": "CHAIN",
        "runtime_event_id": event_id,
        "subject_id": "subject:1",
        "input_value": "private-input",
        "output_value": "private-output",
        "tool_name": "read_file",
        "tool_parameters": "path=fixture",
        "retrieval_documents": ("doc:1",),
        "evaluation_name": "bounded-check",
        "evaluation_score": 0.5,
        "evaluation_label": "review",
        "evaluation_explanation": "synthetic",
        "graph_node_id": "node:1",
        "graph_parent_id": None,
        "metadata": {"fixture": True},
        "source_ref": "repo:fixture@abc123",
        "approval_ref": "approval:1",
        "canonical_effect": "NONE",
    }
    values.update(overrides)
    return AIONTraceEvent(**values)


def entry(entry_id: str = "entry:1", **overrides: object) -> CrosswalkEntry:
    values: dict[str, object] = {
        "entry_id": entry_id,
        "source_ref": "repo:fixture@abc123",
        "source_kind": "Repository Evidence",
        "what": "trace contract",
        "who": "Manus",
        "where": "research-labs/trace-provenance-crosswalk_v0.1.0",
        "when": "2026-08-13",
        "method": "read-only source inspection",
        "authority": "Repository Evidence",
        "transformation": "crosswalk to review metadata",
        "currentness": "CURRENT",
        "target_field": "session.id",
        "evidence_reused": True,
        "new_evidence_claimed": False,
    }
    values.update(overrides)
    return CrosswalkEntry(**values)


def run(output: Path) -> dict[str, object]:
    cases: list[tuple[str, object]] = [
        ("valid-trace", audit_trace_crosswalk(event())),
        ("raw-input-policy", audit_trace_crosswalk(event(), TracePolicy(include_input_value=True))),
        ("raw-output-policy", audit_trace_crosswalk(event(), TracePolicy(include_output_value=True))),
        ("tool-parameters-policy", audit_trace_crosswalk(event(), TracePolicy(include_tool_parameters=True))),
        ("graph-self-parent", audit_trace_crosswalk(event(graph_parent_id="node:1"))),
        ("blank-source-ref", audit_trace_crosswalk(event(source_ref=" "))),
        ("blank-approval-ref", audit_trace_crosswalk(event(approval_ref=" "))),
        ("external-import", audit_trace_crosswalk(event(), external_attributes={"session.id": "external:1", "evaluation.score": 0.4, "vendor.extra": "retained"})),
        ("external-aion-namespace", audit_trace_crosswalk(event(), external_attributes={"aion.subject_id": "subject:other"})),
        ("external-invalid-score", audit_trace_crosswalk(event(), external_attributes={"evaluation.score": "not-a-number"})),
        ("external-out-of-range-score", audit_trace_crosswalk(event(), external_attributes={"evaluation.score": 2.0})),
        ("empty-trace-batch", audit_event_batch(())),
        ("duplicate-trace-ids", audit_event_batch((event("event:1"), event("event:1")))),
        ("valid-trace-batch", audit_event_batch((event("event:1"), event("event:2")))),
        ("valid-source-entry", audit_source_entry(entry())),
        ("missing-attribution", audit_source_entry(entry(where=""))),
        ("unknown-source-kind", audit_source_entry(entry(source_kind="Unknown Actor"))),
        ("unknown-currentness", audit_source_entry(entry(currentness="FRESH"))),
        ("reused-marked-new", audit_source_entry(entry(new_evidence_claimed=True))),
        ("stale-source-entry", audit_source_entry(entry(currentness="STALE"))),
        ("empty-crosswalk", audit_source_entries(())),
        ("duplicate-crosswalk-ids", audit_source_entries((entry(), entry()))),
        ("missing-crosswalk-ref", audit_source_entries((entry(source_ref=""),))),
        ("historical-crosswalk", audit_source_entries((entry(currentness="HISTORICAL"),))),
        ("valid-crosswalk", audit_source_entries((entry(), entry("entry:2", target_field="agent.name")))),
    ]
    records = []
    for case_id, audit in cases:
        decision = audit.as_dict()
        assert decision["authority"] == "EXTERNAL_OBSERVATION_ONLY"
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "trace-provenance-crosswalk-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "trace_execution": False,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "authority": "EXTERNAL_OBSERVATION_ONLY",
        "canonical_effect": "NONE",
        "governance_effect": "NONE",
        "deployment": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(run(args.output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
