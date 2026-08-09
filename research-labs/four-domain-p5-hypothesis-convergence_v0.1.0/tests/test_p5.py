from datetime import datetime, timezone
from types import SimpleNamespace
import hashlib

import pytest

from aion_four_domain_p5 import (
    AgentPosition,
    Conclusion,
    ConvergenceDirective,
    CrossAgentDisagreementAnalyzer,
    DisagreementClass,
    FalsificationCriterion,
    FalsificationDecision,
    FalsificationObservation,
    FalsificationTracker,
    HypothesisEvent,
    HypothesisLifecycleLedger,
    HypothesisRecord,
    HypothesisState,
    RegistryDecision,
    ReplicationRegistry,
    ResearchConvergenceGovernor,
    StageDecision,
)

UTC = timezone.utc
T0 = datetime(2026, 8, 9, 12, 40, tzinfo=UTC)
H = hashlib.sha256(b"x").hexdigest()
H2 = hashlib.sha256(b"y").hexdigest()


def position(run, runner, conclusion, evidence, *, tags=(), confidence=8000):
    return AgentPosition(
        run_id=run,
        runner_id=runner,
        hypothesis_id="H1",
        conclusion=conclusion,
        evidence_refs=tuple(evidence),
        dimension_tags=tuple(tags),
        confidence_bp=confidence,
    )


def test_disagreement_detects_fundamental_and_evidence_overlap():
    report = CrossAgentDisagreementAnalyzer().analyze((
        position("r1", "ai:a", Conclusion.SUPPORTS, ("e1", "e2"), tags=("method",)),
        position("r2", "ai:b", Conclusion.FALSIFIES, ("e2", "e3"), tags=("evidence",), confidence=7000),
    ))
    assert report.classification is DisagreementClass.FUNDAMENTAL_DISAGREEMENT
    assert report.mean_pairwise_evidence_overlap == pytest.approx(1/3)
    assert report.dimension_tags == ("evidence", "method")


def test_disagreement_requires_same_hypothesis():
    a = position("r1", "a", Conclusion.SUPPORTS, ("e1",))
    b = AgentPosition("r2", "b", "H2", Conclusion.CHALLENGES, ("e2",))
    with pytest.raises(ValueError):
        CrossAgentDisagreementAnalyzer().analyze((a, b))


class Kind:
    def __init__(self, value): self.value = value


class FakeManifest:
    experiment_id = "exp-1"
    runner_id = "runner-a"
    actor_kind = Kind("AI")
    def fingerprint(self): return H


class FakeResult:
    experiment_id = "exp-1"
    manifest_fingerprint = H
    output_hash = H2
    status = Kind("PASS")
    contamination_class = Kind("NONE")


def test_replication_registry_binds_p4_like_objects():
    registry = ReplicationRegistry()
    registry.append_p4(
        registry_id="reg-1",
        hypothesis_id="H1",
        manifest=FakeManifest(),
        result=FakeResult(),
        recorded_at=T0,
        evidence_refs=("fixture:1",),
    )
    summary = registry.summarize("H1")
    assert summary.decision is RegistryDecision.SINGLE_RUN
    assert summary.clean_run_count == 1


def test_replication_registry_detects_divergent_clean_outputs():
    registry = ReplicationRegistry()
    for idx, out in enumerate((H, H2), start=1):
        registry.append(SimpleNamespace(
            registry_id=f"reg-{idx}",
            hypothesis_id="H1",
            experiment_id=f"exp-{idx}",
            manifest_fingerprint=H,
            output_hash=out,
            runner_id=f"runner-{idx}",
            actor_kind="AI",
            result_status="PASS",
            contamination_class="NONE",
            recorded_at=T0,
            evidence_refs=("e",),
        ))
    assert registry.summarize("H1").decision is RegistryDecision.DIVERGENT


def test_hypothesis_lifecycle_preserves_reversible_evidence_states():
    ledger = HypothesisLifecycleLedger()
    ledger.create(HypothesisRecord("H1", "statement:1", "owner", T0, ("criterion:1",)))
    ledger.append(HypothesisEvent("e1", "H1", HypothesisState.REGISTERED, "owner", "HUMAN_OWNER", T0, ("protocol:1",), "register"))
    ledger.append(HypothesisEvent("e2", "H1", HypothesisState.TESTING, "runner", "AI", T0, ("run:1",), "test"))
    ledger.append(HypothesisEvent("e3", "H1", HypothesisState.SUPPORTED, "runner", "AI", T0, ("result:1",), "support"))
    ledger.append(HypothesisEvent("e4", "H1", HypothesisState.CHALLENGED, "runner2", "AI", T0, ("result:2",), "challenge"))
    projection = ledger.project("H1")
    assert projection.current_state is HypothesisState.CHALLENGED
    assert ("SUPPORTED", "CHALLENGED") in projection.transition_history
    assert set(projection.evidence_refs) == {"protocol:1", "run:1", "result:1", "result:2"}


def test_invalid_hypothesis_transition_fails_closed():
    ledger = HypothesisLifecycleLedger()
    ledger.create(HypothesisRecord("H1", "statement:1", "owner", T0, ("criterion:1",)))
    with pytest.raises(ValueError):
        ledger.append(HypothesisEvent("e1", "H1", HypothesisState.SUPPORTED, "a", "AI", T0, ("e",), "skip"))


def test_falsification_tracker_requires_preregistered_criterion_and_tracks_trigger():
    tracker = FalsificationTracker()
    tracker.add_criterion(FalsificationCriterion("c1", "H1", "metric < threshold", T0, ("protocol:1",)))
    tracker.observe(FalsificationObservation("o1", "c1", T0, True, ("result:1",)))
    report = tracker.assess("H1")
    assert report.decision is FalsificationDecision.TRIGGERED
    assert report.triggered_criteria == ("c1",)


def test_convergence_governor_blocks_p6_after_p5_cap():
    directive = ConvergenceDirective(
        directive_id="cap-1",
        initiated_by="human-owner",
        actor_role="HUMAN_OWNER",
        recorded_at=T0,
        stage_cap=5,
        reason_ref="event:2026-08-09-convergence",
        evidence_refs=("conversation-owner-directive",),
    )
    governor = ResearchConvergenceGovernor()
    assert governor.decide(4, 5, directive).decision is StageDecision.REVIEW_READY
    assert governor.decide(5, 6, directive).decision is StageDecision.HOLD_STAGE_CAP


def test_convergence_event_preserves_source_and_implementation_roles():
    directive = ConvergenceDirective(
        "cap-1", "human-owner", "HUMAN_OWNER", T0, 5,
        "event:2026-08-09-convergence", ("owner-directive",),
    )
    event = ResearchConvergenceGovernor().record_event(
        event_id="return-1",
        directive=directive,
        stage_reached=5,
        recorded_at=T0,
        public_summary="Human Owner set P5 as the deliberate research cap and returned the workbench to joint review.",
        evidence_refs=("owner-directive", "p5-test-suite"),
    )
    assert event.source_role == "HUMAN_OWNER"
    assert event.implementation_role == "CHATGPT_RESEARCH_ENGINEERING"
    assert event.research_status == "REVIEW_READY"


def test_full_p5_flow():
    ledger = HypothesisLifecycleLedger()
    ledger.create(HypothesisRecord("H1", "statement:1", "owner", T0, ("criterion:1",)))
    ledger.append(HypothesisEvent("e1", "H1", HypothesisState.REGISTERED, "owner", "HUMAN_OWNER", T0, ("protocol:1",), "registered"))
    ledger.append(HypothesisEvent("e2", "H1", HypothesisState.TESTING, "ai:a", "AI", T0, ("run:a",), "testing"))

    report = CrossAgentDisagreementAnalyzer().analyze((
        position("r1", "ai:a", Conclusion.SUPPORTS, ("e1", "e2")),
        position("r2", "ai:b", Conclusion.CHALLENGES, ("e2", "e3")),
        position("r3", "human:r", Conclusion.INCONCLUSIVE, ("e4",), confidence=5000),
    ))
    assert report.classification is DisagreementClass.STRUCTURED_DISAGREEMENT

    tracker = FalsificationTracker()
    tracker.add_criterion(FalsificationCriterion("criterion:1", "H1", "pre-registered fail condition", T0, ("protocol:1",)))
    tracker.observe(FalsificationObservation("obs:1", "criterion:1", T0, False, ("run:a", "run:b")))
    assert tracker.assess("H1").decision is FalsificationDecision.NOT_TRIGGERED

    directive = ConvergenceDirective("cap:5", "owner", "HUMAN_OWNER", T0, 5, "scope-cap", ("owner-directive",))
    assert ResearchConvergenceGovernor().decide(5, 6, directive).decision is StageDecision.HOLD_STAGE_CAP
