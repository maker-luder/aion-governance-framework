from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json

from aion_four_domain_p5 import (
    AgentPosition,
    Conclusion,
    ConvergenceDirective,
    CrossAgentDisagreementAnalyzer,
    FalsificationCriterion,
    FalsificationObservation,
    FalsificationTracker,
    HypothesisEvent,
    HypothesisLifecycleLedger,
    HypothesisRecord,
    HypothesisState,
    ReplicationEntry,
    ReplicationRegistry,
    ResearchConvergenceGovernor,
)

NOW = datetime(2026, 8, 9, 12, 40, tzinfo=timezone.utc)

ledger = HypothesisLifecycleLedger()
ledger.create(HypothesisRecord(
    "H-P5-DEMO",
    "statement:cross-agent-result-stability",
    "human-owner",
    NOW,
    ("criterion:divergence-threshold",),
))
ledger.append(HypothesisEvent(
    "event:registered", "H-P5-DEMO", HypothesisState.REGISTERED,
    "human-owner", "HUMAN_OWNER", NOW, ("protocol:p5-demo",), "preregister-demo"
))
ledger.append(HypothesisEvent(
    "event:testing", "H-P5-DEMO", HypothesisState.TESTING,
    "research-runner", "AI", NOW, ("run:demo",), "start-demo"
))

disagreement = CrossAgentDisagreementAnalyzer().analyze((
    AgentPosition(
        "run:a", "ai:a", "H-P5-DEMO", Conclusion.SUPPORTS,
        ("evidence:shared", "evidence:a"), dimension_tags=("interpretation",), confidence_bp=8000
    ),
    AgentPosition(
        "run:b", "ai:b", "H-P5-DEMO", Conclusion.CHALLENGES,
        ("evidence:shared", "evidence:b"), dimension_tags=("evidence",), confidence_bp=6500
    ),
))

registry = ReplicationRegistry()
for index, (runner, payload) in enumerate((("ai:a", b"result-a"), ("ai:b", b"result-b")), start=1):
    registry.append(ReplicationEntry(
        registry_id=f"registry:{index}",
        hypothesis_id="H-P5-DEMO",
        experiment_id="experiment:p5-demo",
        manifest_fingerprint=hashlib.sha256(b"manifest").hexdigest(),
        output_hash=hashlib.sha256(payload).hexdigest(),
        runner_id=runner,
        actor_kind="AI",
        result_status="PASS",
        contamination_class="NONE",
        recorded_at=NOW,
        evidence_refs=(f"run:{runner}",),
    ))
replication = registry.summarize("H-P5-DEMO")

tracker = FalsificationTracker()
tracker.add_criterion(FalsificationCriterion(
    "criterion:divergence-threshold", "H-P5-DEMO",
    "pre-registered divergence condition", NOW, ("protocol:p5-demo",)
))
tracker.observe(FalsificationObservation(
    "obs:demo", "criterion:divergence-threshold", NOW, False, ("run:a", "run:b")
))
falsification = tracker.assess("H-P5-DEMO")

directive = ConvergenceDirective(
    "directive:p5-cap",
    "human-owner",
    "HUMAN_OWNER",
    NOW,
    5,
    "event:2026-08-09-p5-convergence",
    ("owner-directive",),
)
governor = ResearchConvergenceGovernor()
p6_gate = governor.decide(5, 6, directive)
return_event = governor.record_event(
    event_id="event:return-to-review",
    directive=directive,
    stage_reached=5,
    recorded_at=NOW,
    public_summary="P5 completed; Human Owner returns the research workbench to joint review.",
    evidence_refs=("owner-directive", "p5-full-demo"),
)

output = {
    "hypothesis_state": ledger.project("H-P5-DEMO").current_state.value,
    "disagreement_class": disagreement.classification.value,
    "evidence_overlap": disagreement.mean_pairwise_evidence_overlap,
    "replication_decision": replication.decision.value,
    "falsification_decision": falsification.decision.value,
    "p6_gate": p6_gate.decision.value,
    "research_status": return_event.research_status,
    "main_effect": return_event.main_effect,
}
print(json.dumps(output, sort_keys=True))
