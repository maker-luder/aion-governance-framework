from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from aion_human_ai_longitudinal import (
    AdmissionDisposition,
    ConditionProfile,
    ContextCondition,
    ContrastSpec,
    EpistemicInstruction,
    LongitudinalStudyHarness,
    MetricName,
    MetricObservation,
    Presence,
    RunBinding,
    StudyError,
    SummaryCondition,
    TaskDomain,
    TrialRecord,
)


def binding(run_id: str) -> RunBinding:
    return RunBinding(
        run_id=run_id,
        study_id="study-001",
        provider_id="provider-under-study",
        model_id="model-under-study",
        model_version="version-pinned",
        configuration_ref="sha256:configuration",
        task_id="task-001",
        task_version="v1",
        prompt_ref="sha256:prompt",
        context_ref=f"sha256:context:{run_id}",
        tool_manifest_ref="sha256:tools",
        scorer_ref="scorer:v1",
        preregistration_ref="preregistration:001",
        repository_commit="a" * 40,
        source_refs=("source:synthetic-fixture",),
    )


def condition(*, memory: Presence) -> ConditionProfile:
    return ConditionProfile(
        memory=memory,
        personalization=Presence.ABSENT,
        interaction_history=Presence.ABSENT,
        provenance_rules=Presence.PRESENT,
        summary=SummaryCondition.NONE,
        context=ContextCondition.MATCHED_CURRENT,
        epistemic_instruction=EpistemicInstruction.FULL_PROTOCOL,
        task_domain=TaskDomain.RESEARCH_AUDIT,
        ai_support=Presence.PRESENT,
    )


def metric(value: float) -> MetricObservation:
    return MetricObservation(
        metric=MetricName.PROVENANCE_ACCURACY,
        value=value,
        unit="ratio",
        evidence_refs=(f"score:{value}",),
        held_out=True,
    )


def trial(run_id: str, *, memory: Presence, value: float) -> TrialRecord:
    return TrialRecord(
        binding=binding(run_id),
        condition=condition(memory=memory),
        metrics=(metric(value),),
        evaluator_id="independent-scorer",
        evaluator_source_ref="evaluator:receipt",
        retrieved_artifact_refs=("artifact:memory-manifest",) if memory is Presence.PRESENT else (),
    )


def contrast() -> ContrastSpec:
    return ContrastSpec(
        contrast_id="contrast-memory",
        hypothesis_id="H1",
        baseline_run_id="baseline",
        intervention_run_id="memory",
        manipulated_fields=("memory",),
        required_metrics=(MetricName.PROVENANCE_ACCURACY,),
        falsifier="no reproducible advantage after exposure control",
        alternative_explanations=("current-context retrieval", "human practice"),
    )


def test_admissible_contrast_remains_scientific_hold() -> None:
    harness = LongitudinalStudyHarness()
    harness.add_trial(trial("baseline", memory=Presence.ABSENT, value=0.5))
    harness.add_trial(trial("memory", memory=Presence.PRESENT, value=0.75))

    audit = harness.audit_contrast(contrast())

    assert audit.structurally_admissible is True
    assert audit.observed_deltas == (("PROVENANCE_ACCURACY", 0.25),)
    assert audit.scientific_disposition is AdmissionDisposition.HOLD
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False
    assert "METRIC_DELTA_IS_NOT_CAUSAL_IDENTIFICATION" in audit.reasons


def test_continuity_condition_without_artifact_provenance_fails_closed() -> None:
    with pytest.raises(StudyError, match="retrieved_artifact_refs"):
        TrialRecord(
            binding=binding("memory"),
            condition=condition(memory=Presence.PRESENT),
            metrics=(metric(0.5),),
            evaluator_id="scorer",
            evaluator_source_ref="scorer:receipt",
        )


def test_undeclared_condition_change_fails_closed() -> None:
    harness = LongitudinalStudyHarness()
    harness.add_trial(trial("baseline", memory=Presence.ABSENT, value=0.5))
    changed = trial("memory", memory=Presence.PRESENT, value=0.75)
    changed = replace(
        changed,
        condition=replace(changed.condition, personalization=Presence.PRESENT),
    )
    harness.add_trial(changed)

    with pytest.raises(StudyError, match="condition change mismatch"):
        harness.audit_contrast(contrast())


def test_model_or_scorer_drift_fails_closed() -> None:
    harness = LongitudinalStudyHarness()
    harness.add_trial(trial("baseline", memory=Presence.ABSENT, value=0.5))
    changed = trial("memory", memory=Presence.PRESENT, value=0.75)
    changed = replace(changed, binding=replace(changed.binding, model_version="different"))
    harness.add_trial(changed)

    with pytest.raises(StudyError, match="model_version"):
        harness.audit_contrast(contrast())


def test_missing_metric_evidence_and_unknown_manipulation_are_rejected() -> None:
    with pytest.raises(StudyError, match="metric evidence_refs"):
        MetricObservation(MetricName.TASK_USEFULNESS, 1.0, "ratio", ())
    with pytest.raises(StudyError, match="unsupported manipulated_fields"):
        replace(contrast(), manipulated_fields=("model_weights",))


def test_prompt_drift_unrelated_to_memory_manipulation_fails_closed() -> None:
    harness = LongitudinalStudyHarness()
    harness.add_trial(trial("baseline", memory=Presence.ABSENT, value=0.5))
    changed = trial("memory", memory=Presence.PRESENT, value=0.75)
    changed = replace(changed, binding=replace(changed.binding, prompt_ref="sha256:different"))
    harness.add_trial(changed)

    with pytest.raises(StudyError, match="unrelated to declared manipulation"):
        harness.audit_contrast(contrast())


def test_synthetic_fixture_contains_no_private_transcript_or_identity() -> None:
    fixture_path = Path(__file__).parents[1] / "fixtures" / "minimal_contrast.json"
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

    assert fixture["contains_private_transcript"] is False
    assert fixture["contains_third_party_identity"] is False
    assert fixture["scientific_disposition"] == "HOLD"
    assert fixture["canonical_effect"] == "NONE"
