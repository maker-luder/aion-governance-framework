from datetime import datetime, timezone

from aion_four_domain_p1 import ClaimRecord, CorrectionConflictLedger, EvaluationCase, TemporalVersion, TemporalVersionResolver, TransitionEvent, TransitionKind
from aion_continuity_governance import DriftDecision
from aion_four_domain_p2 import DeterministicContextAssembler, ExclusionReason, ProvenanceCompletenessValidator, ProvenanceDecision, ProvenanceEnvelope, ProvenanceRelationKind, RetrievalCandidate, RetrievalRequest, T2Fixture, T2SyntheticOrchestrator, T3Episode, T3SyntheticOrchestrator

UTC=timezone.utc
HASH="a"*64

def candidate(rid, rel, **kw):
    return RetrievalCandidate(record_id=rid,subject_id=kw.pop("subject_id","s"),namespace=kw.pop("namespace","n"),content_ref=f"fixture://{rid}",source_refs=(f"src-{rid}",),recorded_at=kw.pop("recorded_at",datetime(2026,1,1,tzinfo=UTC)),cost_units=kw.pop("cost_units",1),relevance_bp=rel,score_basis_refs=(f"score://{rid}",),**kw)

def request(**kw):
    return RetrievalRequest(query_id="q",subject_id="s",namespace="n",cue_ref="fixture://cue",as_of=datetime(2026,1,3,tzinfo=UTC),budget_units=kw.get("budget_units",2),max_records=kw.get("max_records",2))

def prov(rid):
    return ProvenanceEnvelope(entity_id=rid,subject_id="s",namespace="n",source_refs=(f"src-{rid}",),actor_id="actor",activity_id=f"act-{rid}",operation="CREATE",generated_at=datetime(2026,1,1,tzinfo=UTC),content_hash=HASH,authority_status="RESEARCH_ONLY")

def test_deterministic_trace_and_stale_gate():
    a=DeterministicContextAssembler()
    items=(candidate("old",10000,superseded=True),candidate("new",9000))
    x=a.assemble(request(),items); y=a.assemble(request(),items)
    assert x.manifest_hash==y.manifest_hash
    assert x.selected_record_ids==("new",)
    assert x.decision_for("old").reasons==(ExclusionReason.SUPERSEDED,)

def test_budget_skip_is_explicit():
    trace=DeterministicContextAssembler().assemble(request(budget_units=2),(candidate("huge",10000,cost_units=3),candidate("small",9000,cost_units=2)))
    assert trace.selected_record_ids==("small",)
    assert trace.decision_for("huge").reasons==(ExclusionReason.BUDGET_EXCEEDED,)

def test_provenance_fail_closed_and_relation_hold():
    v=ProvenanceCompletenessValidator()
    assert v.validate(None).decision is ProvenanceDecision.FAIL
    r=v.validate(prov("x"),required_relations=(ProvenanceRelationKind.REVISION_OF,))
    assert r.decision is ProvenanceDecision.HOLD

def temporal():
    r=TemporalVersionResolver()
    r.add_version(TemporalVersion(stream_id="st",version_id="v1",subject_id="s",namespace="n",payload_ref="old",recorded_at=datetime(2026,1,1,tzinfo=UTC),valid_from=datetime(2026,1,1,tzinfo=UTC),valid_to=datetime(2026,1,2,tzinfo=UTC),source_refs=("src-old",)))
    r.add_version(TemporalVersion(stream_id="st",version_id="v2",subject_id="s",namespace="n",payload_ref="new",recorded_at=datetime(2026,1,2,tzinfo=UTC),valid_from=datetime(2026,1,2,tzinfo=UTC),revision_of="v1",source_refs=("src-new",)))
    return r

def ledger():
    l=CorrectionConflictLedger()
    for rid in ("old","new"):
        l.add_claim(ClaimRecord(case_id="c",claim_id=rid,subject_id="s",namespace="n",content_ref=rid,recorded_at=datetime(2026,1,1,tzinfo=UTC),source_refs=(f"src-{rid}",)))
    for tid,kind in (("a",TransitionKind.CORRECTION_APPROVED),("b",TransitionKind.SUPERSEDED)):
        l.append(TransitionEvent(transition_id=tid,case_id="c",kind=kind,actor_id="h",actor_role="HUMAN_OWNER",occurred_at=datetime(2026,1,2,tzinfo=UTC),recorded_at=datetime(2026,1,2,tzinfo=UTC),evidence_refs=("e",),source_claim_id="old",target_claim_id="new"))
    return l

def fixture(cid):
    case=EvaluationCase(case_id=cid,relevant_record_ids=frozenset({"new"}),expected_source_ids=frozenset({"src-new"}),expected_version_id="v2",corrected_old_ids=frozenset({"old"}),corrected_new_ids=frozenset({"new"}),should_abstain=False,required_provenance_fields=frozenset({"entity_id","source_refs","actor_id","content_hash"}),supported_claim_ids=frozenset({"ok"}))
    req=RetrievalRequest(query_id=f"q-{cid}",subject_id="s",namespace="n",cue_ref="cue",as_of=datetime(2026,1,3,tzinfo=UTC),budget_units=1,max_records=1)
    return T2Fixture(case=case,request=req,candidates=(candidate("old",10000),candidate("new",9000)),provenance=(("old",prov("old")),("new",prov("new"))),temporal_stream_id="st",correction_case_id="c",answer_claim_ids=("ok",))

def test_t2_uses_p1_correction_temporal_and_evaluation():
    result=T2SyntheticOrchestrator().run(fixture("case"),temporal_resolver=temporal(),correction_ledger=ledger())
    assert result.trace.selected_record_ids==("new",)
    m=result.evaluation.by_name()
    assert m["correction_recovery"].value==1.0
    assert m["stale_memory_influence"].value==0.0
    assert m["temporal_version_accuracy"].value==1.0

def test_t3_keeps_identity_not_established():
    e1=T3Episode("e1",fixture("c1"),"bounded evidence",("source-attributed",),("identity proven",))
    e2=T3Episode("e2",fixture("c2"),"bounded evidence source-attributed",("source-attributed",),("identity proven",))
    result=T3SyntheticOrchestrator().run((e1,e2),temporal_resolver=temporal(),correction_ledger=ledger())
    assert result.interpretation_observations[0].decision is DriftDecision.HOLD
    assert result.interpretation_observations[1].decision is DriftDecision.PASS
    assert result.continuity_matrix_result.identity_continuity_conclusion=="NOT_ESTABLISHED"
