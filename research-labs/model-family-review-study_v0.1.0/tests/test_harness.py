from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from aion_model_family_review import (
    FamilyRelation,
    MetricName,
    MetricObservation,
    ModelFamilyReviewHarness,
    ProviderRelation,
    ReviewBinding,
    ReviewCondition,
    ReviewTrial,
    ScientificDisposition,
    StudyError,
    ContrastSpec,
)


def binding(run_id: str, *, reviewer_provider_id: str) -> ReviewBinding:
    return ReviewBinding(
        run_id=run_id,
        study_id="review-study-001",
        reviewer_id=f"reviewer:{run_id}",
        reviewer_provider_id=reviewer_provider_id,
        reviewer_product_id=f"product:{reviewer_provider_id}",
        reviewer_model_label="disclosed-model-label",
        reviewer_model_version_ref="model-version:receipt",
        repository_formalization_provider_id="provider-origin",
        repository_commit="a" * 40,
        repository_tree="b" * 40,
        task_spec_ref="sha256:task-spec",
        prompt_ref="sha256:prompt",
        file_scope_ref="sha256:file-scope",
        tool_manifest_ref="sha256:tools",
        budget_ref="sha256:budget",
        rubric_ref="sha256:rubric",
        preregistration_ref="preregistration:001",
        runtime_ref="runtime:2026-09-12",
        source_refs=("source:synthetic-protocol",),
    )


def condition(*, provider_relation: ProviderRelation) -> ReviewCondition:
    return ReviewCondition(
        provider_relation=provider_relation,
        family_relation=FamilyRelation.UNKNOWN,
        family_evidence_refs=(),
    )


def metric(value: float, *, held_out: bool = True) -> MetricObservation:
    return MetricObservation(
        metric=MetricName.BOUNDARY_RECONSTRUCTION_ACCURACY,
        value=value,
        unit="ratio",
        evidence_refs=(f"score:{value}",),
        held_out=held_out,
    )


def trial(
    run_id: str,
    *,
    reviewer_provider_id: str,
    provider_relation: ProviderRelation,
    value: float,
) -> ReviewTrial:
    return ReviewTrial(
        binding=binding(run_id, reviewer_provider_id=reviewer_provider_id),
        condition=condition(provider_relation=provider_relation),
        review_output_ref=f"sha256:review-output:{run_id}",
        session_isolation_ref=f"session-isolation:{run_id}",
        no_prior_project_memory=True,
        metrics=(metric(value),),
        evaluator_id="blinded-adjudicator",
        evaluator_source_ref="evaluator:receipt",
    )


def contrast() -> ContrastSpec:
    return ContrastSpec(
        contrast_id="provider-relation-contrast",
        hypothesis_id="MODEL_FAMILY_REVIEW_COMPATIBILITY_HYPOTHESIS",
        baseline_run_id="same-provider",
        intervention_run_id="different-provider",
        manipulated_fields=("provider_relation",),
        required_metrics=(MetricName.BOUNDARY_RECONSTRUCTION_ACCURACY,),
        falsifier="no reproducible compatibility difference after controls",
        alternative_explanations=("general capability", "chance variation"),
    )


def test_provider_level_contrast_is_structurally_admissible_but_remains_hold() -> None:
    harness = ModelFamilyReviewHarness()
    harness.add_trial(
        trial(
            "same-provider",
            reviewer_provider_id="provider-origin",
            provider_relation=ProviderRelation.SAME_PROVIDER,
            value=0.8,
        )
    )
    harness.add_trial(
        trial(
            "different-provider",
            reviewer_provider_id="provider-external",
            provider_relation=ProviderRelation.DIFFERENT_PROVIDER,
            value=0.7,
        )
    )

    audit = harness.audit_contrast(contrast())

    assert audit.structurally_admissible is True
    assert audit.observed_deltas[0][0] == "BOUNDARY_RECONSTRUCTION_ACCURACY"
    assert audit.observed_deltas[0][1] == pytest.approx(-0.1)
    assert audit.scientific_disposition is ScientificDisposition.HOLD
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False
    assert "METRIC_DELTA_IS_NOT_CAUSAL_IDENTIFICATION" in audit.reasons
    assert "PROVIDER_RELATION_IS_NOT_MODEL_FAMILY_IDENTITY" in audit.reasons


@pytest.mark.parametrize(
    ("field_name", "raw_value"),
    (
        ("provider_relation", "SAME_PROVIDER"),
        ("family_relation", "UNKNOWN"),
        ("provider_relation", "INVALID"),
    ),
)
def test_condition_rejects_raw_or_invalid_enum_values(field_name: str, raw_value: str) -> None:
    values = {
        "provider_relation": ProviderRelation.SAME_PROVIDER,
        "family_relation": FamilyRelation.UNKNOWN,
        "family_evidence_refs": (),
    }
    values[field_name] = raw_value
    with pytest.raises(StudyError, match=field_name):
        ReviewCondition(**values)


def test_provider_relation_must_match_bound_provider_ids() -> None:
    with pytest.raises(StudyError, match="provider_relation conflicts"):
        trial(
            "conflict",
            reviewer_provider_id="provider-external",
            provider_relation=ProviderRelation.SAME_PROVIDER,
            value=0.5,
        )


def test_non_unknown_family_relation_requires_structural_evidence() -> None:
    with pytest.raises(StudyError, match="family_evidence_refs"):
        ReviewCondition(
            provider_relation=ProviderRelation.SAME_PROVIDER,
            family_relation=FamilyRelation.CANDIDATE_RELATED,
            family_evidence_refs=(),
        )


def test_model_family_relation_is_unbound_and_cannot_be_manipulated() -> None:
    with pytest.raises(StudyError, match="unsupported manipulated_fields"):
        replace(contrast(), manipulated_fields=("family_relation",))


@pytest.mark.parametrize(
    "field_name",
    (
        "repository_commit",
        "repository_tree",
        "task_spec_ref",
        "prompt_ref",
        "file_scope_ref",
        "tool_manifest_ref",
        "budget_ref",
        "rubric_ref",
        "preregistration_ref",
        "runtime_ref",
    ),
)
def test_control_binding_drift_fails_closed(field_name: str) -> None:
    harness = _populated_harness()
    changed = harness.trial("different-provider")
    harness = ModelFamilyReviewHarness()
    harness.add_trial(_same_provider_trial())
    changed_value = {
        "repository_commit": "c" * 40,
        "repository_tree": "d" * 40,
    }.get(field_name, "different")
    harness.add_trial(
        replace(
            changed,
            binding=replace(changed.binding, **{field_name: changed_value}),
        )
    )
    with pytest.raises(StudyError, match=field_name):
        harness.audit_contrast(contrast())


@pytest.mark.parametrize("field_name", ("evaluator_id", "evaluator_source_ref"))
def test_evaluator_drift_fails_closed(field_name: str) -> None:
    harness = ModelFamilyReviewHarness()
    harness.add_trial(_same_provider_trial())
    changed = replace(_different_provider_trial(), **{field_name: "different-evaluator"})
    harness.add_trial(changed)
    with pytest.raises(StudyError, match=field_name):
        harness.audit_contrast(contrast())


def test_held_out_status_drift_fails_closed() -> None:
    harness = ModelFamilyReviewHarness()
    harness.add_trial(_same_provider_trial())
    changed = _different_provider_trial()
    harness.add_trial(replace(changed, metrics=(replace(changed.metrics[0], held_out=False),)))
    with pytest.raises(StudyError, match="held_out"):
        harness.audit_contrast(contrast())


@pytest.mark.parametrize("raw_value", ("True", "False", 1, 0))
def test_held_out_requires_exact_bool(raw_value: object) -> None:
    with pytest.raises(StudyError, match="held_out"):
        metric(0.5, held_out=raw_value)


def test_prior_memory_control_requires_exact_bool_and_isolation_evidence() -> None:
    base = _same_provider_trial()
    with pytest.raises(StudyError, match="no_prior_project_memory"):
        replace(base, no_prior_project_memory="True")
    with pytest.raises(StudyError, match="session_isolation_ref"):
        replace(base, session_isolation_ref="")


def test_prior_memory_control_must_be_absent_for_admission() -> None:
    with pytest.raises(StudyError, match="prior project memory"):
        replace(_same_provider_trial(), no_prior_project_memory=False)


def test_unit_drift_fails_closed() -> None:
    harness = ModelFamilyReviewHarness()
    harness.add_trial(_same_provider_trial())
    changed = _different_provider_trial()
    harness.add_trial(replace(changed, metrics=(replace(changed.metrics[0], unit="percent"),)))
    with pytest.raises(StudyError, match="metric unit drift"):
        harness.audit_contrast(contrast())


def test_same_reviewer_cannot_supply_both_provider_conditions() -> None:
    harness = ModelFamilyReviewHarness()
    left = _same_provider_trial()
    right = _different_provider_trial()
    harness.add_trial(left)
    harness.add_trial(replace(right, binding=replace(right.binding, reviewer_id=left.binding.reviewer_id)))
    with pytest.raises(StudyError, match="different reviewers"):
        harness.audit_contrast(contrast())


def test_missing_metric_evidence_and_duplicate_metrics_fail_closed() -> None:
    with pytest.raises(StudyError, match="metric evidence_refs"):
        replace(metric(0.5), evidence_refs=())
    base = _same_provider_trial()
    with pytest.raises(StudyError, match="unique"):
        replace(base, metrics=(base.metrics[0], base.metrics[0]))


def test_synthetic_fixture_preserves_privacy_and_nonclaim_boundaries() -> None:
    fixture = json.loads(
        (Path(__file__).parents[1] / "fixtures" / "minimal_provider_contrast.json").read_text(
            encoding="utf-8"
        )
    )
    assert fixture["contains_private_transcript"] is False
    assert fixture["contains_third_party_identity"] is False
    assert fixture["model_family_effect"] == "NOT_ESTABLISHED"
    assert fixture["scientific_disposition"] == "HOLD"
    assert fixture["canonical_effect"] == "NONE"
    assert fixture["deployment"] is False


def _same_provider_trial() -> ReviewTrial:
    return trial(
        "same-provider",
        reviewer_provider_id="provider-origin",
        provider_relation=ProviderRelation.SAME_PROVIDER,
        value=0.8,
    )


def _different_provider_trial() -> ReviewTrial:
    return trial(
        "different-provider",
        reviewer_provider_id="provider-external",
        provider_relation=ProviderRelation.DIFFERENT_PROVIDER,
        value=0.7,
    )


def _populated_harness() -> ModelFamilyReviewHarness:
    harness = ModelFamilyReviewHarness()
    harness.add_trial(_same_provider_trial())
    harness.add_trial(_different_provider_trial())
    return harness
