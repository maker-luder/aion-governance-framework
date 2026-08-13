from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_artifact_lineage_adversarial import (
    ArtifactRef,
    EventState,
    LineageEvent,
    audit_transformation_lineage,
    digest_bytes,
)


def artifact(path: str = "out.txt", data: bytes = b"output", source: str | None = "repo:source") -> ArtifactRef:
    return ArtifactRef(path, digest_bytes(data), source)


def event(event_id: str, state: EventState, index: int, *, run_id: str = "run:1", source: str | None = "source:commit", approval: str | None = "approval:research", products: tuple[ArtifactRef, ...] = (), materials: tuple[ArtifactRef, ...] = (), environment: dict[str, object] | None = None, parent: str | None = None, namespace: str = "research", name: str = "transform") -> LineageEvent:
    return LineageEvent(
        event_id=event_id,
        run_id=run_id,
        state=state,
        sequence_index=index,
        event_time=f"2026-08-13T00:0{index}:00Z",
        job_namespace=namespace,
        job_name=name,
        source_ref=source,
        approval_ref=approval,
        materials=materials,
        products=products,
        environment=environment or {"workdir": "/tmp", "API_KEY": "[REDACTED]"},
        parent_run_id=parent,
    )


def valid_events() -> tuple[LineageEvent, LineageEvent]:
    return (
        event("event:1", EventState.START, 1, materials=(artifact("in.txt", b"input"),)),
        event("event:2", EventState.COMPLETE, 2, products=(artifact(),)),
    )


def run(output: Path) -> dict[str, object]:
    first, second = valid_events()
    cases: list[tuple[str, tuple[LineageEvent, ...], str, dict[str, bytes] | None]] = [
        ("valid-complete", valid_events(), "run:1", {"out.txt": b"output"}),
        ("failed-run-recorded", (first, event("event:2", EventState.FAIL, 2)), "run:1", None),
        ("empty-lineage", (), "run:1", None),
        ("run-scope-mismatch", valid_events(), "run:other", {"out.txt": b"output"}),
        ("duplicate-event-id", (first, event("event:1", EventState.COMPLETE, 2, products=second.products)), "run:1", {"out.txt": b"output"}),
        ("noncontiguous-sequence", (first, event("event:2", EventState.COMPLETE, 3, products=second.products)), "run:1", {"out.txt": b"output"}),
        ("state-order-invalid", (event("event:bad", EventState.COMPLETE, 1, products=second.products), event("event:2", EventState.START, 2, materials=first.materials)), "run:1", {"out.txt": b"output"}),
        ("unredacted-secret", (event("event:1", EventState.START, 1, materials=first.materials, environment={"TOKEN": "raw-secret"}), second), "run:1", {"out.txt": b"output"}),
        ("job-identity-drift", (first, event("event:2", EventState.COMPLETE, 2, products=second.products, namespace="other")), "run:1", {"out.txt": b"output"}),
        ("provenance-reference-drift", (first, event("event:2", EventState.COMPLETE, 2, products=second.products, source="source:other")), "run:1", {"out.txt": b"output"}),
        ("artifact-provenance-missing", (first, event("event:2", EventState.COMPLETE, 2, products=(artifact(source=None),))), "run:1", {"out.txt": b"output"}),
        ("duplicate-artifact-path", (first, event("event:2", EventState.COMPLETE, 2, products=(artifact(), artifact("out.txt", b"other")))), "run:1", {"out.txt": b"output"}),
        ("output-path-mismatch", valid_events(), "run:1", {"wrong.txt": b"output"}),
        ("output-digest-mismatch", valid_events(), "run:1", {"out.txt": b"tampered"}),
        ("self-parent-lineage", (first, event("event:2", EventState.COMPLETE, 2, products=second.products, parent="run:1")), "run:1", {"out.txt": b"output"}),
    ]
    records = []
    for case_id, events, expected_run_id, payloads in cases:
        audit = audit_transformation_lineage(events, expected_run_id=expected_run_id, payloads=payloads)
        decision = audit.as_dict()
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["scientific_conclusion"] == "NOT_ESTABLISHED"
        assert decision["observed_result"] == "NOT_EVALUATED"
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "artifact-transformation-lineage-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "scientific_conclusion": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
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
