import pytest
from aion_coupled_quality import (
    CounterDisposition, CounterEvidenceItem, Evidence, EvidenceKind,
    FactoryStage, QualityError, QualityFactory, ResearchLot, Severity,
)


def _factory(risk=Severity.MEDIUM):
    return QualityFactory(ResearchLot(lot_id="R-001", claim="candidate claim", risk=risk))


def _qualified(factory):
    factory.set_falsifier("Fails if independent evidence contradicts the causal prediction")
    factory.add_evidence(Evidence("E1", EvidenceKind.TEST_RESULT, "tests/result.json", True, True))
    factory.add_counterevidence(CounterEvidenceItem("C1", "sources/counter.md", "alternative explanation"))
    factory.dispose_counterevidence("C1", CounterDisposition.ACCEPTED)


def test_mutual_agreement_is_not_enough_for_release():
    f = _factory()
    f.record_pair_judgment(human_approved=True, ai_supported=True)
    f.set_falsifier("can be disproven")
    f.add_counterevidence(CounterEvidenceItem("C1", "counter/ref", "challenge"))
    f.dispose_counterevidence("C1", CounterDisposition.ACCEPTED)
    assert f.final_qa() is False
    assert "NO_INDEPENDENT_EVIDENCE" in f.snapshot()["events"][-1]


def test_counterevidence_route_is_mandatory():
    f = _factory()
    f.set_falsifier("can be disproven")
    f.add_evidence(Evidence("E1", EvidenceKind.TEST_RESULT, "tests/result.json", True, True))
    assert f.final_qa() is False
    assert "NO_COUNTEREVIDENCE_ROUTE" in f.snapshot()["events"][-1]


def test_open_counterevidence_blocks_release():
    f = _factory()
    f.set_falsifier("can be disproven")
    f.add_evidence(Evidence("E1", EvidenceKind.TEST_RESULT, "tests/result.json", True, True))
    f.add_counterevidence(CounterEvidenceItem("C1", "counter/ref", "challenge"))
    assert f.final_qa() is False
    assert "OPEN_COUNTEREVIDENCE" in f.snapshot()["events"][-1]


def test_model_output_cannot_satisfy_independent_evidence():
    f = _factory()
    f.set_falsifier("can be disproven")
    f.add_evidence(Evidence("E1", EvidenceKind.MODEL_OUTPUT, "model/output.json", True, True))
    f.add_counterevidence(CounterEvidenceItem("C1", "counter/ref", "challenge"))
    f.dispose_counterevidence("C1", CounterDisposition.ACCEPTED)
    assert f.final_qa() is False


def test_capa_applied_is_not_capa_verified():
    f = _factory()
    _qualified(f)
    f.open_ncr("NCR-1", "claim overstates evidence", Severity.HIGH)
    f.contain_ncr("NCR-1", "human and AI mutually reinforced an unsupported inference")
    f.plan_capa("NCR-1", "add independent counterevidence and lower claim strength")
    f.apply_capa("NCR-1")
    assert f.final_qa() is False
    assert "OPEN_NCR_CAPA" in f.snapshot()["events"][-1]


def test_verified_capa_can_close_ncr():
    f = _factory()
    _qualified(f)
    f.open_ncr("NCR-1", "unsupported inference", Severity.HIGH)
    f.contain_ncr("NCR-1", "confirmation loop")
    f.plan_capa("NCR-1", "retest with counterexample corpus")
    f.apply_capa("NCR-1")
    f.verify_capa("NCR-1", ("tests/counterexample-regression.json",))
    f.close_ncr("NCR-1")
    assert f.final_qa() is True


def test_high_risk_requires_test_or_primary_independent_evidence():
    f = _factory(Severity.HIGH)
    f.set_falsifier("can be disproven")
    f.add_evidence(Evidence("E1", EvidenceKind.EXTERNAL_SECONDARY, "review/paper.md", True, True))
    f.add_counterevidence(CounterEvidenceItem("C1", "counter/ref", "challenge"))
    f.dispose_counterevidence("C1", CounterDisposition.REBUTTED_WITH_EVIDENCE, resolution_evidence_refs=("review/paper.md",))
    assert f.final_qa() is False
    assert "HIGH_RISK_NO_TEST_OR_PRIMARY" in f.snapshot()["events"][-1]


def test_full_factory_can_release_when_gates_are_satisfied():
    f = _factory(Severity.HIGH)
    for stage in (FactoryStage.IQC, FactoryStage.HYPOTHESIS, FactoryStage.AI_WORK, FactoryStage.HUMAN_REVIEW, FactoryStage.IPQC, FactoryStage.COUNTEREVIDENCE, FactoryStage.IMPLEMENT, FactoryStage.VERIFY, FactoryStage.FINAL_QA):
        f.transition(stage)
    f.record_pair_judgment(human_approved=True, ai_supported=True)
    _qualified(f)
    assert f.final_qa() is True
    assert f.release() == FactoryStage.RELEASED


def test_release_fails_closed_when_ncr_open():
    f = _factory()
    for stage in (FactoryStage.IQC, FactoryStage.HYPOTHESIS, FactoryStage.AI_WORK, FactoryStage.HUMAN_REVIEW, FactoryStage.IPQC, FactoryStage.COUNTEREVIDENCE, FactoryStage.IMPLEMENT, FactoryStage.VERIFY, FactoryStage.FINAL_QA):
        f.transition(stage)
    _qualified(f)
    f.open_ncr("NCR-OPEN", "missing provenance", Severity.CRITICAL)
    assert f.release() == FactoryStage.HOLD


def test_rebutting_counterevidence_requires_resolution_evidence():
    f = _factory()
    f.add_counterevidence(CounterEvidenceItem("C1", "counter/ref", "challenge"))
    with pytest.raises(QualityError):
        f.dispose_counterevidence("C1", CounterDisposition.REBUTTED_WITH_EVIDENCE)


def test_factory_cannot_grant_canonical_or_deployment_authority():
    with pytest.raises(QualityError):
        QualityFactory(ResearchLot(lot_id="X", claim="x", deployment=True))


def test_inherited_provider_prohibition_lock_is_preserved():
    from aion_coupled_quality import ProhibitedProviderError, assert_provider_allowed
    for identifier in ("Claude", "Anthropic", "vendor:Anthropic:model:Claude"):
        with pytest.raises(ProhibitedProviderError):
            assert_provider_allowed(identifier)
    assert assert_provider_allowed("local-test-model") == "local-test-model"
