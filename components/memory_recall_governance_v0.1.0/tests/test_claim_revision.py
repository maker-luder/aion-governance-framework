from dataclasses import replace
import hashlib
import json
import sqlite3

import pytest

from aion_memory_recall import (
    ClaimRevisionService, EvidenceLink, EvidenceRelation, InferenceType,
    RecallRequest, ReviewDecision, verify_revision_history,
)
from aion_memory_recall.store import MemoryWriteDenied, SQLiteMemoryStore
import aion_memory_recall.revision as revision


STAMP = "2026-09-03T00:00:00+00:00"
REQUEST = RecallRequest("fixture-user", "AION", frozenset({"project", "restricted"}), frozenset(), frozenset({"research"}))


def memory(store, mid, **overrides):
    args = dict(memory_id=mid, namespace="research", user_id="fixture-user", agent_id="AION",
                content=f"synthetic claim {mid}", topics=("research",), access_scope=("project",),
                provenance_source="synthetic-fixture", provenance_verified=True,
                writeback_approved=True, recorded_at=STAMP)
    args.update(overrides)
    return store.write(**args)


def enroll(service, mid, deps=(), **kwargs):
    service.register(mid, claim_id=mid, inference_type=InferenceType.INFERENCE,
                     dependencies=deps, writeback_approved=True, **kwargs)


def evidence(mid="a", eid="e1", relation=EvidenceRelation.CONTRADICTS, **kwargs):
    args = dict(evidence_id=eid, target_memory_id=mid, source_id="fixture-source",
                locator="fixture:counterexample", content_sha256=hashlib.sha256(b"fixture evidence").hexdigest(),
                relation=relation, rationale="typed synthetic relation; not discovered semantically", provenance_verified=True)
    args.update(kwargs)
    return EvidenceLink(**args)


@pytest.fixture
def fixture(tmp_path):
    store = SQLiteMemoryStore(tmp_path / "memory.sqlite3")
    service = ClaimRevisionService(store, REQUEST, namespace="research")
    for mid in ("a", "b", "c", "unrelated"):
        memory(store, mid)
    enroll(service, "a")
    enroll(service, "b", ("a",))
    enroll(service, "c", ("b",))
    enroll(service, "unrelated")
    return store, service


def resolve(service, mid="a", **overrides):
    args = dict(decision=ReviewDecision.REVISE, replacement_content="narrower synthetic claim",
                reason="review explicitly limits the unsupported inference", reviewer_ref="fixture-reviewer",
                evidence_refs=("e1",), expected_event_hash=service.snapshot()["event_head"],
                recorded_at=STAMP, writeback_approved=True)
    args.update(overrides)
    return service.resolve(mid, **args)


def states(service):
    return {v["memory_id"]: v["status"] for v in service.snapshot()["versions"]}


def test_challenge_quarantines_transitive_dependents_not_unrelated(fixture):
    store, service = fixture
    assert service.add_evidence(evidence(), writeback_approved=True)
    assert states(service) == {"a": "CHALLENGED", "b": "DEPENDENCY_HOLD", "c": "DEPENDENCY_HOLD", "unrelated": "RECORDED"}
    assert [m.memory_id for m in store.recall(REQUEST)] == ["unrelated"]
    assert len(service.pending_reviews()) == 3
    assert verify_revision_history(service.snapshot())


@pytest.mark.parametrize("relation", [EvidenceRelation.IRRELEVANT, EvidenceRelation.SUPPORTS])
def test_noncontradictory_evidence_does_not_trigger_reopen(fixture, relation):
    store, service = fixture
    service.add_evidence(evidence(relation=relation), writeback_approved=True)
    assert len(store.recall(REQUEST)) == 4
    assert service.pending_reviews() == ()


def test_support_never_silently_clears_counterevidence(fixture):
    _, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    service.add_evidence(evidence(eid="support", relation=EvidenceRelation.SUPPORTS), writeback_approved=True)
    assert states(service)["a"] == "CHALLENGED"
    assert len(service.pending_reviews()) == 3


def test_idempotent_delivery_and_conflicting_id(fixture):
    _, service = fixture
    link = evidence()
    service.add_evidence(link, writeback_approved=True)
    before = service.snapshot()
    assert service.add_evidence(link, writeback_approved=True) is False
    assert before == service.snapshot()
    with pytest.raises(ValueError, match="collision"):
        service.add_evidence(replace(link, rationale="different"), writeback_approved=True)
    assert before == service.snapshot()


def test_repeated_source_not_promoted_to_independent_support(fixture):
    _, service = fixture
    for eid, source in (("s1", "same"), ("s2", "same"), ("s3", "mirror")):
        service.add_evidence(evidence(eid=eid, source_id=source, relation=EvidenceRelation.SUPPORTS), writeback_approved=True)
    data = service.snapshot()
    assert data["distinct_source_labels"] == 2
    assert data["distinct_content_digests"] == 1
    assert data["independent_support_count"] == "NOT_ESTABLISHED"


def test_revision_preserves_content_history_and_does_not_release_dependents(fixture):
    store, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    new = resolve(service, inference_type=InferenceType.ANALOGY, assumptions=("not a diagnostic claim",))
    assert store.get("a").content == "synthetic claim a"
    assert store.get("a").superseded
    assert store.get(new).content == "narrower synthetic claim"
    assert states(service)[new] == "RECORDED"
    assert states(service)["b"] == states(service)["c"] == "DEPENDENCY_HOLD"
    assert {m.memory_id for m in store.recall(REQUEST)} == {new, "unrelated"}
    row = next(v for v in service.snapshot()["versions"] if v["memory_id"] == new)
    assert (row["version"], row["supersedes"], row["inference_type"]) == (2, "a", "ANALOGY")
    assert json.loads(row["assumptions_json"]) == ["not a diagnostic claim"]


def test_dependent_can_be_explicitly_rebased_after_parent_review(fixture):
    store, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    new_a = resolve(service)
    new_b = resolve(service, "b", dependencies=(new_a,), replacement_content="dependent reviewed against new premise")
    assert states(service)["b"] == "SUPERSEDED"
    assert states(service)["c"] == "DEPENDENCY_HOLD"
    assert new_b in {m.memory_id for m in store.recall(REQUEST)}


def test_retain_is_explicit_versioned_decision_not_auto_truth(fixture):
    store, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    new = resolve(service, decision=ReviewDecision.RETAIN, replacement_content=None)
    assert store.get(new).content == store.get("a").content
    assert service.snapshot()["subjectivity"] == "NOT_ESTABLISHED"
    assert store.get(new).canonical_effect == "NONE"


def test_withdraw_preserves_history_and_holds_descendants(fixture):
    store, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    assert resolve(service, decision=ReviewDecision.WITHDRAW, replacement_content=None) is None
    assert states(service)["a"] == "WITHDRAWN"
    assert store.get("a").content == "synthetic claim a"
    assert len(service.pending_reviews()) == 2


def test_second_challenge_and_second_revision(fixture):
    _, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    v2 = resolve(service)
    service.add_evidence(evidence(v2, "e2"), writeback_approved=True)
    v3 = resolve(service, v2, evidence_refs=("e2",), replacement_content="further narrowed")
    assert next(v for v in service.snapshot()["versions"] if v["memory_id"] == v3)["version"] == 3


def test_restart_preserves_queue_lineage_and_event_chain(fixture):
    store, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    reopened = ClaimRevisionService(SQLiteMemoryStore(store.path), REQUEST, namespace="research")
    assert service.snapshot() == reopened.snapshot()
    assert service.pending_reviews() == reopened.pending_reviews()
    assert verify_revision_history(reopened.snapshot())


def test_stale_review_rolls_back_without_successor(fixture):
    store, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    old = service.snapshot()["event_head"]
    service.add_evidence(evidence(eid="e2"), writeback_approved=True)
    before = service.snapshot()
    with pytest.raises(ValueError, match="stale review"):
        resolve(service, expected_event_hash=old)
    assert service.snapshot() == before
    assert len(store.list_for_identity(user_id=REQUEST.user_id, agent_id=REQUEST.agent_id)) == 4


def test_all_counterevidence_must_be_addressed(fixture):
    _, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    service.add_evidence(evidence(eid="e2"), writeback_approved=True)
    with pytest.raises(ValueError, match="all recorded counterevidence"):
        resolve(service)


@pytest.mark.parametrize("operation", ["register", "evidence", "resolve"])
def test_mutations_require_explicit_approval(fixture, operation):
    _, service = fixture
    before = service.snapshot()
    with pytest.raises(MemoryWriteDenied):
        if operation == "register":
            service.register("a", claim_id="a", inference_type=InferenceType.INFERENCE)
        elif operation == "evidence":
            service.add_evidence(evidence())
        else:
            resolve(service, writeback_approved=False)
    assert service.snapshot() == before


@pytest.mark.parametrize("field,value", [("agent_id", "Astra"), ("user_id", "other"), ("namespace", "other")])
def test_identity_namespace_isolation(fixture, field, value):
    store, service = fixture
    memory(store, "foreign", **{field: value})
    with pytest.raises(MemoryWriteDenied):
        enroll(service, "foreign")


def test_access_restrictions_and_no_scope_broadening(fixture):
    store, service = fixture
    memory(store, "restricted", access_scope=("restricted",))
    enroll(service, "restricted")
    memory(store, "public-derived", access_scope=("project",))
    with pytest.raises(MemoryWriteDenied, match="broaden"):
        enroll(service, "public-derived", ("restricted",))
    narrow = ClaimRevisionService(store, replace(REQUEST, requester_scopes=frozenset({"project"})), namespace="research")
    with pytest.raises(MemoryWriteDenied):
        narrow.snapshot()


@pytest.mark.parametrize("setter", ["set_conflict", "supersede", "tombstone"])
def test_legacy_setters_do_not_bypass_revision_protocol(fixture, setter):
    store, _ = fixture
    with pytest.raises(MemoryWriteDenied):
        getattr(store, setter)("a")


def test_database_guard_and_immutable_content(fixture):
    store, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    with store._session() as db:
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("UPDATE memory_records SET conflict=0 WHERE memory_id='a'")
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("UPDATE memory_records SET content='changed' WHERE memory_id='a'")


def test_new_claim_cannot_reuse_challenged_premise(fixture):
    store, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    memory(store, "new")
    with pytest.raises(ValueError, match="dependencies must be active"):
        enroll(service, "new", ("a",))


def test_cycles_and_unknown_dependencies_rejected(fixture):
    store, service = fixture
    memory(store, "new")
    with pytest.raises(KeyError):
        enroll(service, "new", ("missing",))
    # A logical self-reference is rejected even if it names an older version.
    with store._session() as db:
        with pytest.raises(ValueError, match="cycle"):
            service._dependencies(db, ("c",), store.get("a"), "a")


@pytest.mark.parametrize("budget", ["MAX_EVENTS", "MAX_VERSIONS", "MAX_EVIDENCE"])
def test_budget_exhaustion_is_atomic(fixture, monkeypatch, budget):
    store, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    before = service.snapshot()
    original_limit = getattr(revision, budget)
    monkeypatch.setattr(revision, budget, 0)
    with pytest.raises(ValueError, match="budget"):
        if budget == "MAX_EVIDENCE":
            service.add_evidence(evidence(eid="e2"), writeback_approved=True)
        else:
            resolve(service)
    # Hardened reads also reject databases exceeding the active limit. Restore
    # the injected test limit before comparing the unchanged persisted state.
    monkeypatch.setattr(revision, budget, original_limit)
    assert before == service.snapshot()
    assert len(store.list_for_identity(user_id=REQUEST.user_id, agent_id=REQUEST.agent_id)) == 4


@pytest.mark.parametrize("value", [0, 65, True, 1.5])
def test_queue_limits(fixture, value):
    with pytest.raises(ValueError):
        fixture[1].pending_reviews(limit=value)


def test_tampered_event_chain_detected(fixture):
    data = fixture[1].snapshot()
    data["events"][0]["payload_json"] = '{}'
    assert not verify_revision_history(data)


def test_unknown_or_irrelevant_review_evidence_rejected(fixture):
    _, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    service.add_evidence(evidence(eid="noise", relation=EvidenceRelation.IRRELEVANT), writeback_approved=True)
    for refs in (("missing",), ("noise",)):
        with pytest.raises(ValueError, match="relevant"):
            resolve(service, evidence_refs=refs)


def test_stale_evidence_target_never_silently_redirected(fixture):
    _, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    resolve(service)
    with pytest.raises(ValueError, match="stale target"):
        service.add_evidence(evidence(eid="later"), writeback_approved=True)


@pytest.mark.parametrize("kwargs", [dict(provenance_verified=False), dict(provenance_verified=1),
                                   dict(content_sha256="bad"), dict(relation="CONTRADICTS"), dict(rationale="")])
def test_evidence_validation(kwargs):
    with pytest.raises((ValueError, MemoryWriteDenied)):
        evidence(**kwargs)


def test_connections_close_without_cyclic_garbage_collection(tmp_path):
    import gc

    path = tmp_path / "closed.sqlite3"
    gc.disable()
    try:
        store = SQLiteMemoryStore(path)
        memory(store, "x")
        service = ClaimRevisionService(store, REQUEST, namespace="research")
        enroll(service, "x")
        service.snapshot()
        service.pending_reviews()
        store.get("x")
        store.recall(REQUEST)
        # Windows rejects unlinking an open SQLite handle. This stays inside tmp_path.
        path.unlink()
        assert not path.exists()
    finally:
        gc.enable()


def test_concurrent_evidence_commits_have_no_lost_update(fixture):
    from concurrent.futures import ThreadPoolExecutor

    store, service = fixture
    other = ClaimRevisionService(SQLiteMemoryStore(store.path), REQUEST, namespace="research")
    with ThreadPoolExecutor(max_workers=2) as pool:
        calls = [pool.submit(s.add_evidence, evidence(eid=eid), writeback_approved=True)
                 for s, eid in ((service, "e1"), (other, "e2"))]
        assert all(call.result() for call in calls)
    snapshot = service.snapshot()
    assert len(snapshot["evidence"]) == 2
    assert verify_revision_history(snapshot)
    assert len(service.pending_reviews()) == 3


@pytest.mark.parametrize("overrides", [dict(recorded_at="2026-09-03"), dict(inference_type=""),
                                      dict(replacement_content="synthetic claim a"), dict(reason=""),
                                      dict(evidence_refs=()), dict(decision="REVISE")])
def test_invalid_reviews_do_not_mutate(fixture, overrides):
    _, service = fixture
    service.add_evidence(evidence(), writeback_approved=True)
    before = service.snapshot()
    with pytest.raises(ValueError):
        resolve(service, **overrides)
    assert before == service.snapshot()
