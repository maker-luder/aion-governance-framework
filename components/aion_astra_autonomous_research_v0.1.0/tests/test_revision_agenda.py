from dataclasses import replace
import importlib.util
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "components/memory_recall_governance_v0.1.0/src"))

from aion_memory_recall import ClaimStatus, RevisionRequest  # noqa: E402
from aion_astra_autonomous_research import AgendaKind, build_revision_agenda  # noqa: E402


def pending():
    return RevisionRequest("claim", "memory", 1, ClaimStatus.CHALLENGED, ("e1",), ("p1",), "a" * 64)


def test_adapter_uses_existing_agenda_kind_and_provenance():
    request = pending()
    result = build_revision_agenda((request,))
    assert result[0].kind is AgendaKind.CONTRADICTION
    assert set(result[0].source_refs) == {"memory:memory", "revision-head:" + "a" * 64, "evidence:e1", "premise:p1"}
    assert result == build_revision_agenda((request,))
    assert result != build_revision_agenda((replace(request, expected_event_hash="b" * 64),))


def test_adapter_is_bounded_and_order_independent():
    requests = tuple(replace(pending(), memory_id=f"m{index}") for index in range(5))
    assert len(build_revision_agenda(requests, limit=2)) == 2
    assert build_revision_agenda(requests, limit=2) == build_revision_agenda(tuple(reversed(requests)), limit=2)
    assert build_revision_agenda(()) == ()


@pytest.mark.parametrize("limit", [0, 21, True, 1.5])
def test_invalid_budget(limit):
    with pytest.raises(ValueError):
        build_revision_agenda((pending(),), limit=limit)


@pytest.mark.parametrize("requests", [(pending(), pending()), (replace(pending(), status=ClaimStatus.RECORDED),), ("untyped",)])
def test_invalid_input(requests):
    with pytest.raises(ValueError):
        build_revision_agenda(requests)


def test_actual_legacy_contrast_restart_and_deterministic_replay():
    spec = importlib.util.spec_from_file_location("probe_claim_revision", ROOT / "scripts/probe_claim_revision.py")
    probe = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(probe)
    legacy = probe.run_probe("legacy")
    revised = probe.run_probe("revision")
    assert legacy["stale_dependent_recall_count"] == 1
    assert revised["stale_dependent_recall_count"] == 0
    assert revised["unaffected_false_hold_count"] == 0
    assert revised["pending_review_count"] == revised["agenda_count"] == 2
    assert revised["restart_preserved_queue"] and revised["restart_preserved_snapshot"]
    assert revised["history_verified"] and revised["original_content_preserved"]
    assert revised["review_did_not_release_dependent"]
    assert revised == probe.run_probe("revision")


@pytest.mark.parametrize('count',[19,20,21])
def test_output_budget_boundaries_are_deterministic(count):
    requests=tuple(replace(pending(),memory_id=f'm{i}') for i in range(count))
    assert len(build_revision_agenda(requests,limit=20))==min(count,20)


@pytest.mark.parametrize('count',[63,64,65])
def test_input_budget_boundaries(count):
    requests=tuple(replace(pending(),memory_id=f'm{i}') for i in range(count))
    if count>64:
        with pytest.raises(ValueError):
            build_revision_agenda(requests)
    else:
        assert len(build_revision_agenda(requests,limit=20))==20


def test_upstream_counterevidence_and_adapter_failure_do_not_mutate(tmp_path,monkeypatch):
    import hashlib
    import socket
    import subprocess
    import aion_astra_autonomous_research.revision_agenda as adapter
    from aion_memory_recall import ClaimRevisionService, EvidenceLink, EvidenceRelation, InferenceType, RecallRequest
    from aion_memory_recall.store import SQLiteMemoryStore

    def forbidden(*args,**kwargs):
        raise AssertionError('adapter attempted external execution')

    store=SQLiteMemoryStore(tmp_path/'agenda.sqlite3')
    request=RecallRequest('fixture-user','AION',frozenset({'research'}),frozenset(),frozenset({'research'}))
    service=ClaimRevisionService(store,request,namespace='research')
    for mid,parents in [('a',()),('b',('a',))]:
        store.write(memory_id=mid,namespace='research',user_id='fixture-user',agent_id='AION',content='fixture',
                    topics=('research',),access_scope=('research',),provenance_source='fixture',provenance_verified=True,
                    writeback_approved=True,recorded_at='2026-09-03T00:00:00Z')
        service.register(mid,claim_id=mid,inference_type=InferenceType.INFERENCE,dependencies=parents,writeback_approved=True)
    service.add_evidence(EvidenceLink('counter','a','source','fixture:paper',hashlib.sha256(b'e').hexdigest(),
                                      EvidenceRelation.CONTRADICTS,'caller supplied',True),writeback_approved=True)
    before=service.snapshot()
    requests=service.pending_reviews()
    downstream=next(r for r in requests if r.memory_id=='b')
    assert downstream.counterevidence_refs==('counter',) and downstream.affected_by==('a',)
    monkeypatch.setattr(socket,'socket',forbidden)
    monkeypatch.setattr(subprocess,'Popen',forbidden)
    entries=adapter.build_revision_agenda((downstream,))
    assert {'counterevidence:counter','affected-by:a','premise:a','revision-head:'+before['event_head']}.issubset(entries[0].source_refs)
    assert 'version 1' in entries[0].question and 'DEPENDENCY_HOLD' in entries[0].question
    assert before==service.snapshot()
    monkeypatch.setattr(adapter,'AgendaEntry',forbidden)
    with pytest.raises(AssertionError):
        adapter.build_revision_agenda(requests)
    assert before==service.snapshot()  # Agenda is derived after commit, not a separate durable insert.
