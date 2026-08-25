from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_selective_memory import MemoryRecord, MemoryStatus, RetrievalHit, RetrievalTrace
from aion_selective_memory_adversarial import audit_memory_lineage, audit_record, audit_records, audit_retrieval

STAMP = "2026-08-13T00:00:00+00:00"


def record(memory_id: str = "memory:1", **overrides: object) -> MemoryRecord:
    values: dict[str, object] = {
        "memory_id": memory_id,
        "namespace": "subject:aion",
        "domain": "research",
        "purpose": "review",
        "content": "bounded governance evidence",
        "source_ref": "repo:evidence:1",
        "approval_ref": "approval:1",
        "created_at": STAMP,
        "revision": 1,
        "supersedes": None,
        "status": MemoryStatus.ACTIVE,
    }
    values.update(overrides)
    return MemoryRecord(**values)


def trace(*, hits=(), considered=("memory:1",), blocked=(), **overrides: object) -> RetrievalTrace:
    values: dict[str, object] = {
        "query": "governance evidence",
        "namespace": "subject:aion",
        "domain": "research",
        "purpose": "review",
        "considered_ids": considered,
        "blocked_ids": blocked,
        "hits": hits,
    }
    values.update(overrides)
    return RetrievalTrace(**values)


def run(output: Path) -> dict[str, object]:
    item = record()
    revised = record("memory:2", revision=2, supersedes="memory:1", source_ref="repo:evidence:2", approval_ref="approval:2")
    valid_hit = RetrievalHit(item, 0.5, ("evidence",))
    cases: list[tuple[str, object]] = [
        ("valid-record", audit_record(item)),
        ("missing-field", audit_record(record(content=""))),
        ("timezone-invalid", audit_record(record(created_at="2026-08-13T00:00:00"))),
        ("revision-zero", audit_record(record(revision=0))),
        ("initial-supersedes", audit_record(record(supersedes="memory:0"))),
        ("revision-parent-missing", audit_record(record(revision=2))),
        ("non-active-record", audit_record(record(status=MemoryStatus.SUPERSEDED))),
        ("empty-store", audit_records(())),
        ("duplicate-memory-id", audit_records((item, item))),
        ("revision-parent-not-found", audit_records((record(revision=2, supersedes="memory:missing"),))),
        ("revision-scope-drift", audit_records((item, record("memory:2", namespace="subject:other", revision=2, supersedes="memory:1", source_ref="repo:evidence:2", approval_ref="approval:2")))),
        ("revision-number-drift", audit_records((item, record("memory:2", revision=3, supersedes="memory:1", source_ref="repo:evidence:2", approval_ref="approval:2")))),
        ("source-reference-reuse", audit_records((item, record("memory:2", source_ref=item.source_ref, approval_ref="approval:2")))),
        ("discarded-retained", audit_records((record(status=MemoryStatus.DISCARDED),))),
        ("valid-revision-chain", audit_records((item, revised))),
        ("valid-lineage", audit_memory_lineage((item, revised), "memory:2")),
        ("missing-lineage-id", audit_memory_lineage((item,), "memory:missing")),
        ("valid-retrieval", audit_retrieval(trace(hits=(valid_hit,)), (item,))),
        ("retrieval-scope-missing", audit_retrieval(trace(namespace=""), (item,))),
        ("considered-duplicate", audit_retrieval(trace(considered=("memory:1", "memory:1")), (item,))),
        ("blocked-duplicate", audit_retrieval(trace(blocked=("memory:2", "memory:2")), (item,))),
        ("considered-blocked-overlap", audit_retrieval(trace(blocked=("memory:1",)), (item,))),
        ("non-active-hit", audit_retrieval(trace(hits=(RetrievalHit(record(status=MemoryStatus.SUPERSEDED), 0.5, ("evidence",)),)), (record(status=MemoryStatus.SUPERSEDED),))),
        ("hit-not-considered", audit_retrieval(trace(considered=(), hits=(valid_hit,)), (item,))),
        ("hit-scope-mismatch", audit_retrieval(trace(hits=(RetrievalHit(record(namespace="subject:other"), 0.5, ("evidence",)),)), (record(namespace="subject:other"),))),
        ("hit-score-invalid", audit_retrieval(trace(hits=(RetrievalHit(item, 1.1, ("evidence",)),)), (item,))),
        ("hit-terms-empty", audit_retrieval(trace(hits=(RetrievalHit(item, 0.5, ()),)), (item,))),
        ("hit-order-invalid", audit_retrieval(trace(considered=("memory:1", "memory:2"), hits=(RetrievalHit(record("memory:2", source_ref="repo:2", approval_ref="approval:2"), 0.2, ("evidence",)), RetrievalHit(record("memory:1", revision=2, supersedes="memory:0", source_ref="repo:1", approval_ref="approval:1"), 0.8, ("evidence",)))), (record("memory:1", revision=2, supersedes="memory:0", source_ref="repo:1", approval_ref="approval:1"), record("memory:2", source_ref="repo:2", approval_ref="approval:2")))),
        ("hit-record-not-found", audit_retrieval(trace(hits=(RetrievalHit(record("memory:2", source_ref="repo:2", approval_ref="approval:2"), 0.5, ("evidence",)),)), (item,))),
    ]
    records = []
    for case_id, audit in cases:
        decision = audit.as_dict()
        assert decision["authority"] == "REVIEW_METADATA_ONLY"
        assert decision["memory_truth"] == "NOT_ESTABLISHED"
        assert decision["identity_continuity"] == "NOT_ESTABLISHED"
        assert decision["subjectivity_conclusion"] == "NOT_ESTABLISHED"
        assert decision["canonical_effect"] == "NONE"
        assert decision["governance_effect"] == "NONE"
        assert decision["deployment"] is False
        assert decision["model_execution"] is False
        assert decision["observed_result"] == "NOT_EVALUATED"
        records.append({"case_id": case_id, "decision": decision})
    payload: dict[str, object] = {
        "schema_version": "0.1.0",
        "experiment": "selective-memory-control-adversarial-synthetic-fixtures",
        "research_status": "RESEARCH_ONLY",
        "case_count": len(records),
        "records": records,
        "memory_store_execution": False,
        "model_execution": False,
        "observed_result": "NOT_EVALUATED",
        "memory_truth": "NOT_ESTABLISHED",
        "identity_continuity": "NOT_ESTABLISHED",
        "subjectivity_conclusion": "NOT_ESTABLISHED",
        "authority": "REVIEW_METADATA_ONLY",
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
