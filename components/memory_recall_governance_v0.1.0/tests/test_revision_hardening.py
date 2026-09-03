"""Bounded adversarial behavior tests; all databases are pytest disposable fixtures."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import gc
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from threading import Barrier
import types

import pytest

from aion_memory_recall import ClaimRevisionService, EvidenceRelation, ReviewDecision, verify_revision_history
from aion_memory_recall.revision import _hash, _json
from aion_memory_recall.revision_integrity import bounded_dag, canonical_payload, identifier, strict_json
from aion_memory_recall.store import MemoryWriteDenied, SQLiteMemoryStore
import aion_memory_recall.revision as revision
from test_claim_revision import REQUEST, STAMP, enroll, evidence, memory, resolve, states
from test_claim_revision import fixture as _shared_fixture


@pytest.fixture
def fixture(tmp_path):
    return _shared_fixture.__wrapped__(tmp_path)


ROOT = Path(__file__).resolve().parents[3]
BASE = "4b77b2be69c7721da4e93465b7feb0c3a2aec265"


def dump(store):
    with store._session() as db:
        return tuple(db.iterdump())


def make_graph(tmp_path, graph):
    store = SQLiteMemoryStore(tmp_path / "graph.sqlite3")
    service = ClaimRevisionService(store, REQUEST, namespace="research")
    for node, parents in graph.items():
        memory(store, node)
        enroll(service, node, parents)
    return store, service


@pytest.mark.parametrize("graph,affected", [
    ({"a": (), "b": ("a",), "x": ()}, {"a", "b"}),
    ({"a": (), "b": ("a",), "c": ("b",), "x": ()}, {"a", "b", "c"}),
    ({"a": (), "b": ("a",), "c": ("a",), "x": ()}, {"a", "b", "c"}),
    ({"a": (), "b": ("a",), "c": ("a",), "d": ("b", "c"), "x": ()}, {"a", "b", "c", "d"}),
    ({"a": (), "x": (), "b": ("a", "x")}, {"a", "b"}),
])
def test_graph_shapes_and_exact_unrelated_preservation(tmp_path, graph, affected):
    store, service = make_graph(tmp_path, graph)
    service.add_evidence(evidence(), writeback_approved=True)
    assert {mid for mid, status in states(service).items() if status != "RECORDED"} == affected
    assert {m.memory_id for m in store.recall(REQUEST)} == set(graph) - affected
    before = service.snapshot()
    assert service.add_evidence(evidence(), writeback_approved=True) is False
    assert before == service.snapshot()


@pytest.mark.parametrize("wide", [False, True])
def test_deep_and_wide_bounded_service_graph(tmp_path, wide):
    graph = {"a": ()}
    for i in range(1, 18):
        graph[f"n{i}"] = ("a" if wide or i == 1 else f"n{i-1}",)
    store, service = make_graph(tmp_path, graph)
    service.add_evidence(evidence(), writeback_approved=True)
    assert len(service.pending_reviews(limit=32)) == len(graph)
    assert store.recall(REQUEST) == []


@pytest.mark.parametrize("graph", [{"a": ("a",)}, {"a": ("b",), "b": ("a",)},
                                    {"a": ("c",), "b": ("a",), "c": ("b",)}])
def test_explicit_cycle_policy(graph):
    with pytest.raises(ValueError, match="cycle"):
        bounded_dag(graph, max_nodes=256, max_edges=1024, max_depth=64, max_parents=16)


@pytest.mark.parametrize("depth", [63, 64, 65])
def test_real_depth_limit_minus_at_plus(depth):
    graph = {"n0": ()} | {f"n{i}": (f"n{i-1}",) for i in range(1, depth+1)}
    if depth <= revision.MAX_DEPTH:
        assert len(bounded_dag(graph,max_nodes=256,max_edges=1024,max_depth=64,max_parents=16)) == depth+1
    else:
        with pytest.raises(ValueError, match="depth budget"):
            bounded_dag(graph,max_nodes=256,max_edges=1024,max_depth=64,max_parents=16)


@pytest.mark.parametrize("nodes", [255, 256, 257])
def test_real_node_limit_minus_at_plus(nodes):
    graph = {f"n{i}": () for i in range(nodes)}
    if nodes <= revision.MAX_VERSIONS:
        assert len(bounded_dag(graph,max_nodes=256,max_edges=1024,max_depth=64,max_parents=16)) == nodes
    else:
        with pytest.raises(ValueError, match="node budget"):
            bounded_dag(graph,max_nodes=256,max_edges=1024,max_depth=64,max_parents=16)


@pytest.mark.parametrize("parents", [15, 16, 17])
def test_dependency_edge_limit_minus_at_plus(parents):
    graph = {f"n{i}": () for i in range(parents)}
    graph["dependent"] = tuple(graph)
    if parents <= 16:
        bounded_dag(graph,max_nodes=256,max_edges=1024,max_depth=64,max_parents=16)
    else:
        with pytest.raises(ValueError, match="edge budget"):
            bounded_dag(graph,max_nodes=256,max_edges=1024,max_depth=64,max_parents=16)


@pytest.mark.parametrize("edge_count", [1023, 1024, 1025])
def test_total_edge_limit_minus_at_plus(edge_count):
    graph = {f"p{i}": () for i in range(16)}
    remaining = edge_count
    for i in range(65):
        parents = tuple(f"p{j}" for j in range(min(16, remaining)))
        graph[f"c{i}"] = parents
        remaining -= len(parents)
    if edge_count <= 1024:
        bounded_dag(graph,max_nodes=256,max_edges=1024,max_depth=64,max_parents=16)
    else:
        with pytest.raises(ValueError, match="edge budget"):
            bounded_dag(graph,max_nodes=256,max_edges=1024,max_depth=64,max_parents=16)


class InjectedFault(RuntimeError):
    pass


class FailingConnection:
    def __init__(self, inner, fragment, occurrence):
        self.inner, self.fragment, self.occurrence = inner, fragment, occurrence
        self.hits = 0

    def execute(self, sql, *args):
        result = self.inner.execute(sql, *args)
        if self.fragment in sql:
            self.hits += 1
            if self.hits == self.occurrence:
                raise InjectedFault("injected after " + self.fragment)
        return result

    def __getattr__(self, name):
        return getattr(self.inner, name)


@pytest.mark.parametrize("fragment,occurrence,operation", [
    ("INSERT INTO claim_evidence",1,"evidence"),
    ("UPDATE claim_versions SET status",1,"evidence"),
    ("UPDATE memory_records SET conflict",2,"evidence"),
    ("INSERT INTO claim_revision_events",1,"evidence"),
    ("INSERT INTO memory_records",1,"review"),
    ("INSERT INTO claim_versions",1,"review"),
    ("UPDATE memory_records SET superseded",1,"review"),
    ("INSERT INTO claim_revision_events",1,"review"),
])
def test_injected_sql_stage_failure_rolls_back_every_table(fixture, monkeypatch, fragment, occurrence, operation):
    store, service = fixture
    if operation == "review":
        service.add_evidence(evidence(),writeback_approved=True)
    before = dump(store)
    token = service.snapshot()["event_head"]
    connect = store._connect
    with monkeypatch.context() as m:
        m.setattr(store,"_connect",lambda: FailingConnection(connect(),fragment,occurrence))
        with pytest.raises(InjectedFault):
            if operation == "evidence":
                service.add_evidence(evidence(),writeback_approved=True)
            else:
                # Pass all inputs directly; snapshot is not part of the injected write.
                service.resolve("a",decision=ReviewDecision.REVISE,replacement_content="changed",reason="fixture",
                                reviewer_ref="review",evidence_refs=("e1",),expected_event_hash=token,
                                recorded_at=STAMP,writeback_approved=True)
    assert dump(store) == before
    assert verify_revision_history(service.snapshot())


def test_failure_before_and_after_event_append_is_atomic(fixture, monkeypatch):
    store, service = fixture
    original = service._append
    for after in (False, True):
        before = dump(store)
        def fail(db,payload):
            if after:
                original(db,payload)
            raise InjectedFault("event stage")
        with monkeypatch.context() as m:
            m.setattr(service,"_append",fail)
            with pytest.raises(InjectedFault):
                service.add_evidence(evidence(),writeback_approved=True)
        assert dump(store) == before


def race(functions):
    barrier = Barrier(len(functions))
    def call(fn):
        barrier.wait(timeout=10)
        try:
            return ("OK",fn())
        except (ValueError,sqlite3.IntegrityError) as exc:
            return ("REJECTED",str(exc))
    with ThreadPoolExecutor(max_workers=len(functions)) as pool:
        futures = [pool.submit(call,fn) for fn in functions]
        return [future.result(timeout=30) for future in futures]


@pytest.mark.parametrize("different", [False,True])
def test_same_evidence_id_competing_writers(fixture,different):
    store, service = fixture
    other = ClaimRevisionService(SQLiteMemoryStore(store.path),REQUEST,namespace="research")
    left=evidence(); right=replace(left,rationale="different") if different else left
    result=race([lambda: service.add_evidence(left,writeback_approved=True),lambda: other.add_evidence(right,writeback_approved=True)])
    assert sum(kind=="OK" for kind,_ in result)==(1 if different else 2)
    if not different:
        assert sorted(value for _,value in result)==[False,True]
    snapshot=service.snapshot()
    assert len(snapshot['evidence'])==1 and len(snapshot['events'])==5


def test_competing_successors_never_fork(fixture):
    store, service = fixture
    service.add_evidence(evidence(),writeback_approved=True)
    token=service.snapshot()['event_head']
    other=ClaimRevisionService(SQLiteMemoryStore(store.path),REQUEST,namespace='research')
    results=race([lambda: resolve(service,expected_event_hash=token,replacement_content='left'),
                  lambda: resolve(other,expected_event_hash=token,replacement_content='right')])
    assert sorted(kind for kind,_ in results)==['OK','REJECTED']
    versions=[v for v in service.snapshot()['versions'] if v['claim_id']=='a']
    assert [v['version'] for v in versions]==[1,2]
    assert verify_revision_history(service.snapshot())


def test_historical_version_binding_requires_each_revalidation(fixture):
    _,service=fixture
    service.add_evidence(evidence(),writeback_approved=True)
    a2=resolve(service)
    b=next(v for v in service.snapshot()['versions'] if v['memory_id']=='b')
    assert json.loads(b['dependencies_json'])==['a']
    with pytest.raises(ValueError):
        resolve(service,'b',dependencies=('a',))
    b2=resolve(service,'b',dependencies=(a2,),replacement_content='b rechecked')
    assert states(service)['c']=='DEPENDENCY_HOLD'
    c2=resolve(service,'c',dependencies=(b2,),replacement_content='c rechecked')
    assert states(service)[c2]=='RECORDED'
    assert service.pending_reviews()==()


@pytest.mark.parametrize('decision',list(ReviewDecision))
def test_full_support_challenge_review_reopen_lifecycle(fixture,decision):
    store,service=fixture
    service.add_evidence(evidence(eid='support',relation=EvidenceRelation.SUPPORTS),writeback_approved=True)
    service.add_evidence(evidence(),writeback_approved=True)
    content='revised' if decision is ReviewDecision.REVISE else None
    resolve(service,decision=decision,replacement_content=content)
    before=service.snapshot()
    reopened=ClaimRevisionService(SQLiteMemoryStore(store.path),REQUEST,namespace='research')
    assert before==reopened.snapshot()
    assert store.get('a').content=='synthetic claim a'
    assert {e['evidence_id'] for e in before['evidence']}=={'support','e1'}
    assert states(reopened)['b']==states(reopened)['c']=='DEPENDENCY_HOLD'


def test_declared_lineage_and_two_retrieving_agents(fixture):
    _,service=fixture
    for eid,source,parents,agent in [('paper-a','paper',(),'AION'),('paper-b','paper',(),'Astra'),
                                   ('news','news',('paper',),'AION'),('blog','blog',('news',),'Astra')]:
        service.add_evidence(evidence(eid=eid,source_id=source,derived_from=parents,retrieval_agent=agent,
                                     retrieval_event_id='retrieval-'+eid,publisher='fixture publisher'),writeback_approved=True)
    snapshot=service.snapshot()
    assert snapshot['declared_source_lineage_roots']=={'blog':['paper'],'news':['paper'],'paper':['paper']}
    assert len(snapshot['content_duplicate_groups'][0]['evidence_ids'])==4
    assert snapshot['independent_support_count']=='NOT_ESTABLISHED'
    assert snapshot['automatic_source_independence_judgment'] is False


def test_source_lineage_cycles_reject_atomically(fixture):
    store,service=fixture
    service.add_evidence(evidence(eid='e1',source_id='source-a',derived_from=('source-b',)),writeback_approved=True)
    before=dump(store)
    with pytest.raises(ValueError,match='cycle'):
        service.add_evidence(evidence(eid='e2',source_id='source-b',derived_from=('source-a',)),writeback_approved=True)
    assert before==dump(store)


def test_canonical_unicode_newlines_times_and_dict_order():
    left={'content':'cafe\u0301\r\nsecond','recorded_at':'2026-09-03T08:00:00+08:00','n':1,'ok':True,'optional':None}
    right={'optional':None,'ok':True,'n':1,'recorded_at':STAMP,'content':'caf\u00e9\nsecond'}
    assert _hash(canonical_payload(left))==_hash(canonical_payload(right))
    assert _hash(canonical_payload({'values':[1,2]}))!=_hash(canonical_payload({'values':[2,1]}))
    assert _hash(canonical_payload({'n':True}))!=_hash(canonical_payload({'n':1}))
    assert _hash(canonical_payload({}))!=_hash(canonical_payload({'n':None}))


@pytest.mark.parametrize('value',[set([1,2]),float('nan'),1.5,b'bytes'])
def test_ambiguous_canonical_types_reject(value):
    with pytest.raises(ValueError):
        canonical_payload({'value':value})


@pytest.mark.parametrize('bad',['','a\x00b','x\ny','x\u202ey','cafe\u0301','x'*201])
def test_identifier_rejection(bad):
    with pytest.raises(ValueError):
        identifier(bad)


@pytest.mark.parametrize('raw',['{"a":1,"a":2}','{"a":NaN}'])
def test_ambiguous_json_rejection(raw):
    with pytest.raises(ValueError):
        strict_json(raw)


def test_reference_insertion_order_and_original_wording(tmp_path):
    heads=[]
    for index,deps in enumerate([('p','q'),('q','p')]):
        folder=tmp_path/str(index);folder.mkdir()
        store,service=make_graph(folder,{'p':(),'q':()})
        text='cafe\u0301\r\nsecond' if index==0 else 'caf\u00e9\nsecond'
        memory(store,'a',content=text,recorded_at='2026-09-03T08:00:00+08:00' if index==0 else STAMP)
        enroll(service,'a',deps)
        heads.append(service.snapshot()['event_head'])
        assert store.get('a').content==text
    assert heads[0]==heads[1]


@pytest.mark.parametrize('budget,allowed',[('MAX_EVENTS',5),('MAX_EVIDENCE',2),('MAX_VERSIONS',5)])
def test_transaction_limits_below_at_above(fixture,monkeypatch,budget,allowed):
    store,service=fixture
    with monkeypatch.context() as m:
        m.setattr(revision,budget,allowed)
        if budget=='MAX_VERSIONS':
            memory(store,'new');enroll(service,'new')
            memory(store,'excess');before=dump(store)
            with pytest.raises(ValueError,match='budget'):
                enroll(service,'excess')
        else:
            repetitions=allowed-4 if budget=='MAX_EVENTS' else allowed
            for i in range(repetitions):
                service.add_evidence(evidence(eid=f'e{i}'),writeback_approved=True)
            before=dump(store)
            with pytest.raises(ValueError,match='budget'):
                service.add_evidence(evidence(eid='excess'),writeback_approved=True)
        assert dump(store)==before


@pytest.mark.parametrize('affected_limit',[2,3,4])
def test_affected_count_limit_boundaries(fixture,monkeypatch,affected_limit):
    store,service=fixture
    before=dump(store)
    monkeypatch.setattr(revision,'MAX_AFFECTED',affected_limit)
    if affected_limit<3:
        with pytest.raises(ValueError,match='affected'):
            service.add_evidence(evidence(),writeback_approved=True)
        assert dump(store)==before
    else:
        service.add_evidence(evidence(),writeback_approved=True)
        assert len(service.pending_reviews())==3


def test_event_byte_budget_atomicity(fixture,monkeypatch):
    store,service=fixture
    before=dump(store)
    with store._session() as db:
        used=db.execute('SELECT sum(length(cast(payload_json AS BLOB))) FROM claim_revision_events').fetchone()[0]
    monkeypatch.setattr(revision,'MAX_HISTORY_BYTES',used+1)
    with pytest.raises(ValueError,match='byte budget'):
        service.add_evidence(evidence(),writeback_approved=True)
    assert before==dump(store)


@pytest.fixture(scope='module')
def baseline_store_class():
    # Trusted, exact Git source is executed solely to produce disposable old-schema DBs.
    path='components/memory_recall_governance_v0.1.0/src/aion_memory_recall/store.py'
    raw=subprocess.check_output(['git','-c','core.autocrlf=false','show',BASE+':'+path],cwd=ROOT)
    module=types.ModuleType('aion_memory_recall._baseline_migration_fixture')
    sys.modules[module.__name__]=module
    exec(compile(raw,path,'exec'),module.__dict__)
    yield module.SQLiteMemoryStore
    del sys.modules[module.__name__]


@pytest.mark.parametrize('populated',[False,True])
def test_actual_baseline_database_open_is_additive_idempotent(tmp_path,baseline_store_class,populated):
    path=tmp_path/'baseline.sqlite3'
    old=baseline_store_class(path)
    if populated:
        for mid in ('normal','conflicted','tombstoned','superseded','other'):
            memory(old,mid,agent_id='Astra' if mid=='other' else 'AION')
        old.set_conflict('conflicted');old.tombstone('tombstoned');old.supersede('superseded')
    with sqlite3.connect(path) as db:
        original=db.execute('SELECT * FROM memory_records ORDER BY memory_id').fetchall()
    db.close()
    gc.collect()  # Only historical fixture connections lack explicit closing.
    store=SQLiteMemoryStore(path)
    service=ClaimRevisionService(store,REQUEST,namespace='research')
    assert service.snapshot()['events']==[]
    before=dump(store)
    ClaimRevisionService(SQLiteMemoryStore(path),REQUEST,namespace='research')
    assert before==dump(store)
    with store._session() as db:
        actual=[tuple(row) for row in db.execute('SELECT * FROM memory_records ORDER BY memory_id')]
        assert actual==original
    if populated:
        assert [m.memory_id for m in store.recall(REQUEST)]==['normal']
        enroll(service,'normal')
        assert states(service)['normal']=='RECORDED'
        for mid in ('conflicted','tombstoned','superseded'):
            with pytest.raises(ValueError):
                enroll(service,mid)


def test_downgrade_read_only_not_write_safe(fixture,baseline_store_class):
    store,service=fixture
    old=baseline_store_class(store.path)
    assert {m.memory_id for m in old.recall(REQUEST)}=={'a','b','c','unrelated'}
    # Demonstrate why baseline writes must not be used on a revision-managed DB.
    old.set_conflict('a')
    with pytest.raises(ValueError,match='flag/status'):
        service.snapshot()
    gc.collect()


@pytest.mark.parametrize('setter',['set_conflict','supersede','tombstone'])
@pytest.mark.parametrize('managed',['a','b','retired'])
def test_legacy_setter_matrix_is_not_a_bypass(fixture,setter,managed):
    store,service=fixture
    service.add_evidence(evidence(),writeback_approved=True)
    if managed=='retired':
        resolve(service);managed='a'
    before=dump(store)
    with pytest.raises(MemoryWriteDenied):
        getattr(store,setter)(managed)
    assert before==dump(store)
    memory(store,'legacy')
    getattr(store,setter)('legacy')


@pytest.mark.parametrize('corruption', ['cycle','missing','event','flags','schema'])
def test_manual_corruption_rejected_without_repair(fixture,corruption):
    store,service=fixture
    with store._session() as db:
        if corruption=='cycle':
            db.execute("UPDATE claim_versions SET dependencies_json='[\"c\"]' WHERE memory_id='a'")
        elif corruption=='missing':
            db.execute("UPDATE claim_versions SET dependencies_json='[\"missing\"]' WHERE memory_id='b'")
        elif corruption=='event':
            db.execute("UPDATE claim_revision_events SET event_hash='broken' WHERE sequence=1")
        elif corruption=='flags':
            db.execute("UPDATE memory_records SET conflict=1 WHERE memory_id='a'")
        else:
            db.execute('ALTER TABLE claim_evidence ADD COLUMN unexpected TEXT')
    before=dump(store)
    with pytest.raises(ValueError):
        service.add_evidence(evidence(),writeback_approved=True)
    assert before==dump(store)
    with pytest.raises(ValueError):
        ClaimRevisionService(SQLiteMemoryStore(store.path),REQUEST,namespace='research')


@pytest.mark.parametrize('gc_enabled',[False,True])
def test_repeated_connections_and_transaction_exception_close_immediately(tmp_path,gc_enabled):
    previous=gc.isenabled()
    (gc.enable if gc_enabled else gc.disable)()
    try:
        for i in range(4):
            path=tmp_path/f'close-{i}.sqlite3'
            store=SQLiteMemoryStore(path)
            memory(store,'a')
            service=ClaimRevisionService(store,REQUEST,namespace='research');enroll(service,'a')
            with pytest.raises(InjectedFault):
                with service._transaction(True) as db:
                    db.execute("UPDATE memory_records SET conflict=1 WHERE memory_id='a'")
                    raise InjectedFault()
            service.snapshot();service.pending_reviews()
            path.unlink()
            assert not path.exists()
    finally:
        (gc.enable if previous else gc.disable)()


def test_sql_metacharacters_are_data_not_commands(tmp_path):
    store=SQLiteMemoryStore(tmp_path/'sql.sqlite3')
    mid="x'); DROP TABLE memory_records;--"
    memory(store,mid)
    service=ClaimRevisionService(store,REQUEST,namespace='research');enroll(service,mid)
    service.add_evidence(evidence(mid),writeback_approved=True)
    assert store.get(mid).memory_id==mid
    assert len(service.snapshot()['versions'])==1


def test_hash_match_is_not_semantic_or_tamper_proof(fixture):
    _,service=fixture
    data=service.snapshot()
    previous='GENESIS'
    for event in data['events']:
        payload=json.loads(event['payload_json'])
        payload['attacker_rewrites_entire_history']=True
        event['payload_json']=_json(payload)
        event['previous_hash']=previous
        event['event_hash']=_hash({'sequence':event['sequence'],'previous_hash':previous,'payload':payload})
        previous=event['event_hash']
    data['event_head']=previous
    assert verify_revision_history(data)  # No trusted external anchor/signature was supplied.
    assert data['subjectivity']==data['consciousness']==data['identity_continuity']=='NOT_ESTABLISHED'


def test_subprocess_restart_replay():
    command=[sys.executable,'-B',str(ROOT/'scripts/probe_claim_revision.py'),'--mode','revision']
    a=subprocess.run(command,capture_output=True,text=True,check=True)
    b=subprocess.run(command,capture_output=True,text=True,check=True)
    assert json.loads(a.stdout)==json.loads(b.stdout)


@pytest.mark.parametrize('damage',['all-events','suffix','evidence-row'])
def test_projection_damage_rejected_even_with_valid_remaining_hashes(fixture,damage):
    store,service=fixture
    service.add_evidence(evidence(),writeback_approved=True)
    with store._session() as db:
        if damage=='all-events':
            db.execute('DELETE FROM claim_revision_events')
        elif damage=='suffix':
            db.execute('DELETE FROM claim_revision_events WHERE sequence=(SELECT max(sequence) FROM claim_revision_events)')
        else:
            db.execute('DELETE FROM claim_evidence')
    before=dump(store)
    with pytest.raises(ValueError,match='projection'):
        service.snapshot()
    assert dump(store)==before


def test_schema_failure_rolls_back_additive_tables(tmp_path):
    store=SQLiteMemoryStore(tmp_path/'malformed.sqlite3')
    with store._session() as db:
        db.execute('CREATE TABLE claim_versions(memory_id TEXT, status TEXT)')
    before=dump(store)
    with pytest.raises(ValueError,match='schema'):
        ClaimRevisionService(store,REQUEST,namespace='research')
    assert dump(store)==before


@pytest.mark.parametrize('field,value',[('user_id','another-user'),('agent_id','Astra'),('namespace','elsewhere')])
def test_cross_identity_registration_fails_without_partial_revision(tmp_path,field,value):
    store=SQLiteMemoryStore(tmp_path/'identity.sqlite3')
    memory(store,'a',**{field:value})
    service=ClaimRevisionService(store,REQUEST,namespace='research')
    before=dump(store)
    with pytest.raises(MemoryWriteDenied):
        enroll(service,'a')
    assert dump(store)==before


def test_conflicting_declared_lineage_rolls_back(fixture):
    store,service=fixture
    service.add_evidence(evidence(derived_from=('paper-a',)),writeback_approved=True)
    before=dump(store)
    with pytest.raises(ValueError,match='conflicting'):
        service.add_evidence(evidence(eid='e2',derived_from=('paper-b',)),writeback_approved=True)
    assert dump(store)==before


def test_actual_pre_hardening_events_preserve_hashes_and_extend_v2(tmp_path):
    path='components/memory_recall_governance_v0.1.0/src/aion_memory_recall/revision.py'
    raw=subprocess.check_output(['git','show','fd8f0964d621fdea0e5fb3e202775b4feaccc067:'+path],cwd=ROOT)
    name='aion_memory_recall._pre_hardening_fixture'
    module=types.ModuleType(name);sys.modules[name]=module
    try:
        exec(compile(raw,path,'exec'),module.__dict__)
        store=SQLiteMemoryStore(tmp_path/'v1.sqlite3')
        old=module.ClaimRevisionService(store,REQUEST,namespace='research')
        for mid,parents in [('a',()),('b',('a',)),('c',('b',))]:
            memory(store,mid)
            old.register(mid,claim_id=mid,inference_type=module.InferenceType.INFERENCE,
                         dependencies=parents,writeback_approved=True)
        def old_evidence(mid,eid):
            return module.EvidenceLink(eid,mid,'source','fixture:paper','a'*64,
                                       module.EvidenceRelation.CONTRADICTS,'counterexample',True)
        old.add_evidence(old_evidence('b','e-b'),writeback_approved=True)
        old.resolve('b',decision=module.ReviewDecision.WITHDRAW,reason='bounded withdrawal',
                    reviewer_ref='fixture',evidence_refs=('e-b',),expected_event_hash=old.snapshot()['event_head'],
                    recorded_at=STAMP,writeback_approved=True)
        old.add_evidence(old_evidence('a','e-a'),writeback_approved=True)
        events=old.snapshot()['events']
        service=ClaimRevisionService(store,REQUEST,namespace='research')
        assert service.snapshot()['events']==events
        assert not service.add_evidence(evidence('a','e-a',source_id='source',locator='fixture:paper',
                                               content_sha256='a'*64,rationale='counterexample'),writeback_approved=True)
        service.add_evidence(evidence('a','new-evidence'),writeback_approved=True)
        after=service.snapshot()
        assert after['events'][:-1]==events
        assert json.loads(after['events'][-1]['payload_json'])['canonicalization']=='CLAIM_REVISION_V2'
        assert after==ClaimRevisionService(SQLiteMemoryStore(store.path),REQUEST,namespace='research').snapshot()
    finally:
        del sys.modules[name]
