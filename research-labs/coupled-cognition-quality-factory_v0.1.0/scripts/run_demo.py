from aion_coupled_quality import (
    CounterDisposition,
    CounterEvidenceItem,
    Evidence,
    EvidenceKind,
    FactoryStage,
    QualityFactory,
    ResearchLot,
    Severity,
)

lot = ResearchLot(lot_id="DEMO-001", claim="A jointly developed claim", risk=Severity.HIGH)
f = QualityFactory(lot)
for s in (FactoryStage.IQC, FactoryStage.HYPOTHESIS, FactoryStage.AI_WORK, FactoryStage.HUMAN_REVIEW, FactoryStage.IPQC, FactoryStage.COUNTEREVIDENCE, FactoryStage.IMPLEMENT, FactoryStage.VERIFY, FactoryStage.FINAL_QA):
    f.transition(s)
f.record_pair_judgment(human_approved=True, ai_supported=True)
f.set_falsifier("Independent counterexample breaks the prediction")
f.add_evidence(Evidence("T-1", EvidenceKind.TEST_RESULT, "tests/independent.json", True, True))
f.add_counterevidence(CounterEvidenceItem("CE-1", "evidence/negative-case.md", "Alternative causal explanation"))
f.dispose_counterevidence("CE-1", CounterDisposition.ACCEPTED)
print(f.final_qa())
print(f.release())
print(f.snapshot())
