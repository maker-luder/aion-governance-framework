from datetime import datetime, timezone
import hashlib
import pytest

from aion_four_domain_p4 import (
    ActorKind,
    BenchmarkAccessPolicy,
    ContaminationClass,
    CrossAgentComparator,
    ExperimentManifest,
    ExperimentResult,
    NetworkMode,
    ObservationSourceClass,
    PublicObservationLedger,
    PublicObservationRecord,
    ReproductionDecision,
    ReproductionValidator,
    ResearchBundleExporter,
    ResultStatus,
    SearchExposure,
)

NOW = datetime(2026, 8, 9, 12, 20, tzinfo=timezone.utc)
INPUT = hashlib.sha256(b"fixture").hexdigest()
OUTPUT = hashlib.sha256(b"result").hexdigest()
EVIDENCE = hashlib.sha256(b"evidence").hexdigest()


def manifest(experiment_id="exp-1", runner="runner-A", env="py3.11-linux", *, network=NetworkMode.OFFLINE, policy=BenchmarkAccessPolicy.ISOLATED):
    return ExperimentManifest(
        experiment_id=experiment_id,
        protocol_version="P4-0.1",
        branch_name="review/four-domain-research-materialization",
        baseline_commit="e78fb97d39f592ed8b39dae73ed96c49faf6b3ce",
        runner_id=runner,
        actor_kind=ActorKind.AI,
        started_at=NOW,
        module_refs=("research-labs/four-domain-p3-resilience-experiments_v0.1.0",),
        fixture_refs=("fixture://p3/public",),
        network_mode=network,
        benchmark_access_policy=policy,
        environment_fingerprint=env,
        input_hash=INPUT,
        seed=7,
        benchmark_refs=("benchmark://synthetic-memory",),
    )


def result(m, output=OUTPUT, exposure=SearchExposure()):
    return ExperimentResult(
        experiment_id=m.experiment_id,
        manifest_fingerprint=m.fingerprint(),
        ended_at=NOW,
        status=ResultStatus.PASS,
        output_hash=output,
        evidence_refs=("evidence://trace",),
        search_exposure=exposure,
    )


def test_manifest_is_deterministic_and_research_only():
    m = manifest()
    assert len(m.fingerprint()) == 64
    assert m.fingerprint() == manifest().fingerprint()
    with pytest.raises(ValueError):
        ExperimentManifest(
            experiment_id="x", protocol_version="p", branch_name="b", baseline_commit="c",
            runner_id="r", actor_kind=ActorKind.HUMAN, started_at=NOW,
            module_refs=("m",), fixture_refs=("f",), network_mode=NetworkMode.OFFLINE,
            benchmark_access_policy=BenchmarkAccessPolicy.ISOLATED,
            environment_fingerprint="e", input_hash=INPUT, main_effect="WRITE",
        )


def test_offline_manifest_rejects_search_trace():
    with pytest.raises(ValueError):
        ExperimentManifest(
            experiment_id="x", protocol_version="p", branch_name="b", baseline_commit="c",
            runner_id="r", actor_kind=ActorKind.HUMAN, started_at=NOW,
            module_refs=("m",), fixture_refs=("f",), network_mode=NetworkMode.OFFLINE,
            benchmark_access_policy=BenchmarkAccessPolicy.ISOLATED,
            environment_fingerprint="e", input_hash=INPUT, search_trace_refs=("search://1",),
        )


def test_reproduction_exact_environment_variation_and_divergence():
    a = manifest()
    b = manifest("exp-2", "runner-B")
    assert ReproductionValidator().compare(a, result(a), b, result(b)).decision is ReproductionDecision.EXACT
    c = manifest("exp-3", "runner-C", env="py3.12-windows")
    assert ReproductionValidator().compare(a, result(a), c, result(c)).decision is ReproductionDecision.REPRODUCED_WITH_ENVIRONMENT_VARIATION
    d = manifest("exp-4", "runner-D")
    changed = hashlib.sha256(b"different").hexdigest()
    assert ReproductionValidator().compare(a, result(a), d, result(d, changed)).decision is ReproductionDecision.DIVERGED


def test_search_time_contamination_is_not_clean_reproduction():
    web = manifest("exp-web", "runner-W", network=NetworkMode.PUBLIC_WEB, policy=BenchmarkAccessPolicy.PUBLIC_SEARCH_ALLOWED)
    contaminated = result(web, exposure=SearchExposure(question_context_overlap=True, evidence_refs=("trace://q",)))
    report = ReproductionValidator().compare(web, contaminated, web, contaminated)
    assert report.decision is ReproductionDecision.CONTAMINATED
    assert contaminated.contamination_class is ContaminationClass.QUESTION_CONTEXT_LEAKAGE


def test_result_is_bound_to_manifest():
    a = manifest()
    b = manifest("exp-2")
    with pytest.raises(ValueError):
        ReproductionValidator().compare(a, result(b), b, result(b))


def test_cross_agent_comparison_preserves_runner_count():
    a = manifest("a", "human-owner")
    b = manifest("b", "ai-agent")
    comparison = CrossAgentComparator().compare(((a, result(a)), (b, result(b))))
    assert comparison.run_count == 2
    assert comparison.runner_count == 2
    assert comparison.exact_output_agreement == 1.0


def test_public_observation_rejects_private_material():
    ledger = PublicObservationLedger()
    record = PublicObservationRecord(
        observation_id="obs-public",
        source_class=ObservationSourceClass.PUBLIC_EVENT,
        source_ref="nvd://CVE-2026-example",
        observed_at=NOW,
        summary_ref="summary://public",
        evidence_hash=EVIDENCE,
        public_safe=True,
    )
    ledger.append(record)
    assert ledger.records() == (record,)
    with pytest.raises(ValueError):
        PublicObservationRecord(
            observation_id="obs-private",
            source_class=ObservationSourceClass.DAILY_LIFE_GENERALIZATION,
            source_ref="private://conversation",
            observed_at=NOW,
            summary_ref="summary://private",
            evidence_hash=EVIDENCE,
            public_safe=True,
            contains_private_conversation=True,
        )


def test_bundle_export_keeps_runner_and_contamination_provenance():
    m = manifest()
    bundle = ResearchBundleExporter().export(m, result(m))
    assert bundle.schema == "AION-RESEARCH-BUNDLE-0.1"
    assert bundle.runner_id == "runner-A"
    assert bundle.contamination_class == "NONE"
