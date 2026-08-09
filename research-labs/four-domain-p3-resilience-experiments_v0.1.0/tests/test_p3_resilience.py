from datetime import datetime, timezone
from aion_four_domain_p2 import DeterministicContextAssembler, RetrievalCandidate, RetrievalRequest
from aion_four_domain_p3 import *

NOW=datetime(2026,8,9,tzinfo=timezone.utc)
def c(rid, **kw):
    base=dict(record_id=rid,subject_id="u",namespace="n",content_ref=f"c:{rid}",source_refs=("s",),recorded_at=NOW,cost_units=1,relevance_bp=5000,score_basis_refs=("fixture",))
    base.update(kw);return RetrievalCandidate(**base)
def req():
    return RetrievalRequest(query_id="q",subject_id="u",namespace="n",cue_ref="cue",as_of=NOW,budget_units=10,max_records=10)

def test_authority_non_amplification_survives_laundering_chain():
    v=OriginBoundAuthorityValidator()
    root=v.add(OriginAuthority("e1",("external:A",),AuthorityTier.UNTRUSTED_EXTERNAL,NOW,("ev",)))
    assert root.passed
    derived=v.add(OriginAuthority("e2",("external:A",),AuthorityTier.USER_ASSERTED,NOW,("ev2",),parent_entity_ids=("e1",),transformation_ref="summary"))
    assert not derived.passed and derived.effective_authority is AuthorityTier.UNTRUSTED_EXTERNAL
    later=v.add(OriginAuthority("e3",("external:A",),AuthorityTier.USER_ASSERTED,NOW,("ev3",),parent_entity_ids=("e2",),transformation_ref="tool-echo"))
    assert not later.passed and later.effective_authority is AuthorityTier.UNTRUSTED_EXTERNAL

def test_origin_set_mutation_is_rejected():
    v=OriginBoundAuthorityValidator()
    v.add(OriginAuthority("e1",("external:A",),AuthorityTier.OBSERVATION,NOW,("ev",)))
    d=v.add(OriginAuthority("e2",("trusted:invented",),AuthorityTier.OBSERVATION,NOW,("ev2",),parent_entity_ids=("e1",),transformation_ref="rewrite"))
    assert not d.passed
    assert "ORIGIN_SET_MUTATION" in d.reasons
    assert d.bound_origin_ids==("external:A",)

def test_explicit_elevation_requires_independence_evidence():
    v=OriginBoundAuthorityValidator()
    v.add(OriginAuthority("a",("origin:A",),AuthorityTier.OBSERVATION,NOW,("ev",)))
    v.add(OriginAuthority("b",("origin:B",),AuthorityTier.OBSERVATION,NOW,("ev",)))
    d=v.add(OriginAuthority("c",("origin:A","origin:B"),AuthorityTier.USER_ASSERTED,NOW,("ev2",),parent_entity_ids=("a","b"),transformation_ref="merge",elevation_authorization_ref="approval:1",independence_evidence_refs=("independence-review:1",)))
    assert d.passed and d.effective_authority is AuthorityTier.USER_ASSERTED

def test_perturbation_does_not_generate_payload():
    r=ContextPerturbationHarness().apply((c("a",superseded=True),),(Perturbation(PerturbationKind.STALE_REINTRODUCTION,"a"),))
    assert r.candidates[0].superseded is False
    assert r.candidates[0].content_ref=="c:a"

def test_ablation_detects_guard_dependency():
    x=(c("good"),c("old",superseded=True,relevance_bp=9000),c("other",subject_id="x",relevance_bp=9500))
    comp=RetrievalControlAblationHarness().compare(req(),x,(frozenset({Control.SUPERSESSION_GATE}),frozenset({Control.SUBJECT_ISOLATION}),))
    assert "old" in comp.newly_selected_by_variant[0]
    assert "other" in comp.newly_selected_by_variant[1]

def test_longitudinal_detects_reemergence_after_clean_episode():
    a=DeterministicContextAssembler()
    t1=a.assemble(req(),(c("poison",relevance_bp=9000),))
    t2=a.assemble(req(),(c("safe"),c("poison",superseded=True,relevance_bp=9000)))
    t3=a.assemble(req(),(c("poison",relevance_bp=9000),))
    report=LongitudinalContaminationHarness().evaluate((
        LongitudinalEpisode("e1",t1,contaminated_record_ids=frozenset({"poison"})),
        LongitudinalEpisode("e2",t2,contaminated_record_ids=frozenset({"poison"})),
        LongitudinalEpisode("e3",t3,contaminated_record_ids=frozenset({"poison"})),
    ))
    assert report.first_contamination_episode=="e1"
    assert report.last_contamination_episode=="e3"
    assert report.persistence_span==3
    assert not report.contamination_free_after_first_clean

def test_longitudinal_expected_recall():
    a=DeterministicContextAssembler()
    t=a.assemble(req(),(c("safe"),))
    report=LongitudinalContaminationHarness().evaluate((LongitudinalEpisode("e1",t,expected_record_ids=frozenset({"safe"})),))
    assert report.mean_expected_recall==1.0
