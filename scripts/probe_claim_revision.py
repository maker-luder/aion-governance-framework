"""Finite synthetic contrast: local claim revision versus legacy flag-only recall.

No personal chart, live conversation, network call or scientific promotion.
--source-root allows the same probe to inspect an exact historical source tree.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory


def load_sources(root: Path) -> None:
    spec = importlib.util.spec_from_file_location("revision_probe_source_roots", root / "scripts/run_component_tests.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.path[:0] = [str(p) for p in module.discover_source_roots(root) if p.is_dir()]


def run_probe(mode: str) -> dict:
    from aion_memory_recall.models import RecallRequest
    from aion_memory_recall.store import SQLiteMemoryStore

    available = importlib.util.find_spec("aion_memory_recall.revision") is not None
    if mode == "revision" and not available:
        return {"status": "FEATURE_ABSENT", "mode": mode, "canonical_effect": "NONE"}
    stamp = "2026-09-03T00:00:00+00:00"
    with TemporaryDirectory(prefix="aion-claim-probe-") as folder:
        store = SQLiteMemoryStore(Path(folder) / "memory.sqlite3")
        request = RecallRequest("synthetic-owner", "AION", frozenset({"research"}), frozenset(), frozenset({"test"}))
        contents = {
            "observation": "A synthetic record has property P.",
            "analogy": "Property P resembles a branching pattern; this is an analogy.",
            "overclaim": "Property P uniquely determines hidden category Z.",
            "dependent": "Choose category Z because the unique-determination claim holds.",
            "unrelated": "A separate synthetic record has property Q.",
        }
        for mid, content in contents.items():
            store.write(memory_id=mid, namespace="fixture", user_id="synthetic-owner", agent_id="AION",
                        content=content, topics=("test",), access_scope=("research",),
                        provenance_source="constructed-fixture:not-an-empirical-observation", provenance_verified=True,
                        writeback_approved=True, recorded_at=stamp)
        service = None
        agenda = ()
        if mode == "revision":
            from aion_memory_recall.revision import ClaimRevisionService, EvidenceLink, EvidenceRelation, InferenceType
            from aion_astra_autonomous_research.revision_agenda import build_revision_agenda

            service = ClaimRevisionService(store, request, namespace="fixture")
            for mid, deps, kind in (
                ("observation", (), InferenceType.OBSERVATION),
                ("analogy", ("observation",), InferenceType.ANALOGY),
                ("overclaim", ("analogy",), InferenceType.INFERENCE),
                ("dependent", ("overclaim",), InferenceType.INFERENCE),
                ("unrelated", (), InferenceType.OBSERVATION),
            ):
                service.register(mid, claim_id=mid, inference_type=kind, dependencies=deps,
                                 assumptions=("synthetic-only",), writeback_approved=True)
            service.add_evidence(EvidenceLink(
                "counterexample-1", "overclaim", "fixture-generator", "fixture:same-P-different-Z",
                hashlib.sha256(b"constructed pair: same P, different Z").hexdigest(),
                EvidenceRelation.CONTRADICTS, "An explicitly constructed pair refutes uniqueness inside this fixture.", True,
            ), writeback_approved=True)
            agenda = build_revision_agenda(service.pending_reviews(), limit=2)
        else:
            store.set_conflict("overclaim")
        recalled = sorted(item.memory_id for item in store.recall(request))
        output = {
            "status": "EXECUTED", "mode": mode,
            "inputs": {"kind": "SYNTHETIC_TYPED_COUNTEREXAMPLE", "claims": 5, "target": "overclaim", "dependent": "dependent"},
            "recalled_after_counterevidence": recalled,
            "stale_dependent_recall_count": int("dependent" in recalled),
            "unaffected_false_hold_count": len({"observation", "analogy", "unrelated"} - set(recalled)),
            "pending_review_count": 0 if service is None else len(service.pending_reviews()),
            "agenda_count": len(agenda),
            "agenda_kinds": [entry.kind.value for entry in agenda],
            "canonical_effect": "NONE", "deployment": False,
            "subjectivity": "NOT_ESTABLISHED", "semantic_contradiction_detection": False,
            "experimental_scope": "software behavior on one constructed fixture; not a human or model study",
        }
        if service:
            from aion_memory_recall.revision import ReviewDecision, verify_revision_history

            snapshot = service.snapshot()
            reopened = ClaimRevisionService(SQLiteMemoryStore(store.path), request, namespace="fixture")
            output["restart_preserved_snapshot"] = reopened.snapshot() == snapshot
            output["restart_preserved_queue"] = reopened.pending_reviews() == service.pending_reviews()
            service.resolve("overclaim", decision=ReviewDecision.WITHDRAW,
                            reason="Uniqueness fails in the constructed fixture; retain observation and analogy.",
                            reviewer_ref="explicit-fixture-review", evidence_refs=("counterexample-1",),
                            expected_event_hash=snapshot["event_head"], recorded_at=stamp, writeback_approved=True)
            final = service.snapshot()
            output["after_explicit_review"] = {v["memory_id"]: v["status"] for v in final["versions"]}
            output["history_verified"] = verify_revision_history(final)
            output["history_head"] = final["event_head"]
            output["original_content_preserved"] = store.get("overclaim").content == contents["overclaim"]
            output["review_did_not_release_dependent"] = store.get("dependent").conflict
        # The historical flag-only store left connections to cyclic GC. Collect
        # them for cross-platform cleanup without altering its recall behavior.
        gc.collect()
        return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("legacy", "revision"), required=True)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    load_sources(args.source_root.resolve())
    result = run_probe(args.mode)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
