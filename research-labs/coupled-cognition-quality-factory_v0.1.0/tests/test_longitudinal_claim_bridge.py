from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from aion_coupled_quality import (
    ClaimAdmissionDisposition,
    ClaimLayer,
    ClaimLevel,
    ContributionOrigin,
    ContributionRecord,
    EpistemicProvenanceLedger,
    Evidence,
    EvidenceKind,
    ResearchLot,
    Severity,
)
from aion_coupled_quality.longitudinal_claim_bridge import (
    LongitudinalClaimBridgeError,
    LongitudinalClaimRequest,
    LongitudinalEvidenceInput,
    assess_longitudinal_claim_mapping,
    build_longitudinal_claim_mapping,
)
from aion_human_ai_longitudinal import (
    AdmissionDisposition,
    ConditionProfile,
    ContextCondition,
    ContrastAudit,
    ContrastSpec,
    EpistemicInstruction,
    MetricName,
    MetricObservation,
    Presence,
    RunBinding,
    SummaryCondition,
    TaskDomain,
    TrialRecord,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def _spec() -> ContrastSpec:
    return ContrastSpec(
        contrast_id="C-MEMORY-01",
        hypothesis_id="H-GROUNDING-01",
        baseline_run_id="RUN-BASE",
        intervention_run_id="RUN-MEMORY",
        manipulated_fields=("memory",),
        required_metrics=(MetricName.REGROUNDING_COST,),
        falsifier="Matched runs show no preregistered difference in regrounding cost.",
        alternative_explanations=("Prompt cueing", "retrieval-format artifact"),
    )


def _audit(**changes: object) -> ContrastAudit:
    defaults = dict(
        contrast_id="C-MEMORY-01",
        structurally_admissible=True,
        observed_deltas=((MetricName.REGROUNDING_COST.value, -1.5),),
        reasons=(
            "STRUCTURAL_CONTRAST_ADMISSIBLE",
            "METRIC_DELTA_IS_NOT_CAUSAL_IDENTIFICATION",
            "HARNESS_PASS_IS_NOT_HYPOTHESIS_CONFIRMATION",
            "CLAIM_ADMISSION_REQUIRES_SEPARATE_PR91_MAPPING",
        ),
        scientific_disposition=AdmissionDisposition.HOLD,
        canonical_effect="NONE",
        deployment=False,
    )
    defaults.update(changes)
    return ContrastAudit(**defaults)


def _binding(run_id: str, *, context_ref: str) -> RunBinding:
    return RunBinding(
        run_id=run_id,
        study_id="STUDY-GROUNDING-01",
        provider_id="provider:test",
        model_id="model:test",
        model_version="v1",
        configuration_ref="config:matched-v1",
        task_id="task:grounding",
        task_version="v1",
        prompt_ref="prompt:matched",
        context_ref=context_ref,
        tool_manifest_ref="tools:none",
        scorer_ref="scorer:v1",
        preregistration_ref="prereg:H-GROUNDING-01",
        repository_commit="git:test-fixture",
        source_refs=("fixture:public-safe",),
    )


def _condition(*, memory: Presence) -> ConditionProfile:
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


def _trial(
    run_id: str,
    *,
    memory: Presence,
    context_ref: str,
    value: float,
    evidence_ref: str,
    unit: str = "turns",
    held_out: bool = False,
) -> TrialRecord:
    return TrialRecord(
        binding=_binding(run_id, context_ref=context_ref),
        condition=_condition(memory=memory),
        metrics=(
            MetricObservation(
                metric=MetricName.REGROUNDING_COST,
                value=value,
                unit=unit,
                evidence_refs=(evidence_ref,),
                held_out=held_out,
            ),
        ),
        evaluator_id="evaluator:fixture",
        evaluator_source_ref="fixture:evaluator-protocol",
        retrieved_artifact_refs=("fixture:memory-artifact",)
        if memory is Presence.PRESENT
        else (),
    )


def _baseline(**changes: object) -> TrialRecord:
    defaults = dict(
        run_id="RUN-BASE",
        memory=Presence.ABSENT,
        context_ref="context:base",
        value=4.0,
        evidence_ref="fixture:base:regrounding",
        unit="turns",
        held_out=False,
    )
    defaults.update(changes)
    return _trial(**defaults)


def _intervention(**changes: object) -> TrialRecord:
    defaults = dict(
        run_id="RUN-MEMORY",
        memory=Presence.PRESENT,
        context_ref="context:memory",
        value=2.5,
        evidence_ref="fixture:memory:regrounding",
        unit="turns",
        held_out=False,
    )
    defaults.update(changes)
    return _trial(**defaults)


def _request(**changes: object) -> LongitudinalClaimRequest:
    defaults = dict(
        provenance_record_id="claim-prov",
        evidence=(
            LongitudinalEvidenceInput(
                evidence_id="E-BASE",
                provenance_record_id="evidence-base-prov",
                run_id="RUN-BASE",
                metric_name=MetricName.REGROUNDING_COST.value,
                study_evidence_ref="fixture:base:regrounding",
            ),
            LongitudinalEvidenceInput(
                evidence_id="E-INTERVENTION",
                provenance_record_id="evidence-intervention-prov",
                run_id="RUN-MEMORY",
                metric_name=MetricName.REGROUNDING_COST.value,
                study_evidence_ref="fixture:memory:regrounding",
            ),
        ),
    )
    defaults.update(changes)
    return LongitudinalClaimRequest(**defaults)


def _ledger() -> EpistemicProvenanceLedger:
    ledger = EpistemicProvenanceLedger()
    ledger.add(
        ContributionRecord(
            record_id="claim-prov",
            proposition="Bounded longitudinal contrast claim.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.OBSERVATION,
            source_refs=(
                "fixture:base:regrounding",
                "fixture:memory:regrounding",
            ),
        )
    )
    for record_id, proposition, source_ref in (
        (
            "evidence-base-prov",
            "Synthetic baseline metric evidence.",
            "fixture:base:regrounding",
        ),
        (
            "evidence-intervention-prov",
            "Synthetic intervention metric evidence.",
            "fixture:memory:regrounding",
        ),
    ):
        ledger.add(
            ContributionRecord(
                record_id=record_id,
                proposition=proposition,
                origin=ContributionOrigin.AI_FORMALIZATION,
                layer=ClaimLayer.OBSERVATION,
                source_refs=(source_ref,),
            )
        )
    return ledger


def _lot(
    *,
    base_ref: str = "fixture:base:regrounding",
    intervention_ref: str = "fixture:memory:regrounding",
    base_kind: EvidenceKind = EvidenceKind.TEST_RESULT,
    intervention_kind: EvidenceKind = EvidenceKind.TEST_RESULT,
    base_supports: bool = True,
    intervention_supports: bool = True,
    final_qa_pass: bool = True,
) -> ResearchLot:
    return ResearchLot(
        lot_id="LOT-LONG-1",
        claim="Bounded longitudinal observation.",
        risk=Severity.MEDIUM,
        evidence=[
            Evidence(
                evidence_id="E-BASE",
                kind=base_kind,
                reference=base_ref,
                supports_claim=base_supports,
            ),
            Evidence(
                evidence_id="E-INTERVENTION",
                kind=intervention_kind,
                reference=intervention_ref,
                supports_claim=intervention_supports,
            ),
        ],
        final_qa_pass=final_qa_pass,
    )


def _mapping(
    *,
    spec: ContrastSpec | None = None,
    audit: ContrastAudit | None = None,
    baseline: TrialRecord | None = None,
    intervention: TrialRecord | None = None,
    request: LongitudinalClaimRequest | None = None,
):
    return build_longitudinal_claim_mapping(
        spec or _spec(),
        audit or _audit(),
        baseline or _baseline(),
        intervention or _intervention(),
        request or _request(),
    )


def test_real_longitudinal_types_map_into_existing_claim_gate() -> None:
    mapping = _mapping()

    assert mapping.hypothesis_id == "H-GROUNDING-01"
    assert mapping.contrast_id == "C-MEMORY-01"
    assert mapping.baseline_run_id == "RUN-BASE"
    assert mapping.intervention_run_id == "RUN-MEMORY"
    assert mapping.required_metrics == (MetricName.REGROUNDING_COST.value,)
    assert mapping.observed_deltas == ((MetricName.REGROUNDING_COST.value, -1.5),)
    assert mapping.metric_units == ((MetricName.REGROUNDING_COST.value, "turns"),)

    claim = mapping.claim
    assert claim.claim_level is ClaimLevel.L0_OBSERVATION
    assert claim.version == 1
    assert claim.claim_id.startswith("longitudinal-l0-claim-sha256:")
    assert claim.statement == (
        "Synthetic longitudinal contrast C-MEMORY-01 associated with H-GROUNDING-01 "
        "recorded bounded metric deltas: REGROUNDING_COST=-1.5 turns. "
        "This observation does not establish the hypothesis, a mechanism, causal learning, "
        "subjectivity, or consciousness."
    )
    assert claim.inferred_statements == ()
    assert claim.population_scope is False
    assert claim.causal_learning_effect is False
    assert claim.subjectivity_claim is False
    assert claim.consciousness_claim is False
    assert mapping.canonical_effect == "NONE"

    assert all(not item.intervention_sensitive for item in mapping.evidence_bindings)
    assert all(not item.transfer_candidate for item in mapping.evidence_bindings)
    assert all(not item.held_out for item in mapping.evidence_bindings)
    assert all(not item.repeated for item in mapping.evidence_bindings)
    assert all(not item.comparison_control for item in mapping.evidence_bindings)
    assert all(not item.independently_scored for item in mapping.evidence_bindings)
    runtime_refs = {item.runtime_or_context_ref for item in mapping.evidence_bindings}
    assert len(runtime_refs) == 2
    assert all(ref.startswith("longitudinal-runtime-sha256:") for ref in runtime_refs)
    assert all(
        item.producer_ref.startswith("longitudinal-producer-sha256:")
        for item in mapping.evidence_bindings
    )
    assert all(
        item.naturalistic_case_id.startswith("longitudinal-case-sha256:")
        for item in mapping.evidence_bindings
    )

    assessment = assess_longitudinal_claim_mapping(
        mapping,
        ledger=_ledger(),
        lot=_lot(),
        repository_root=REPOSITORY_ROOT,
    )
    assert (
        assessment.disposition
        is ClaimAdmissionDisposition.ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD
    )
    assert assessment.scientific_disposition == "HOLD"
    assert assessment.subjectivity == "NOT_ESTABLISHED"
    assert assessment.consciousness == "NOT_ESTABLISHED"
    assert assessment.canonical_effect == "NONE"


def test_claim_identity_is_content_addressed_and_not_caller_selected() -> None:
    first = _mapping()
    second = _mapping()
    altered = _mapping(intervention=_intervention(context_ref="context:memory-v2"))

    assert first.claim.claim_id == second.claim.claim_id
    assert first.claim.version == 1
    assert altered.claim.claim_id != first.claim.claim_id


def test_claim_identity_changes_when_full_run_binding_changes() -> None:
    baseline = _baseline()
    changed = replace(
        baseline,
        binding=replace(
            baseline.binding,
            prompt_ref="prompt:changed",
        ),
    )

    original = _mapping(baseline=baseline)
    mutated = _mapping(baseline=changed)

    assert original.claim.claim_id != mutated.claim.claim_id
    original_ref = next(
        item.runtime_or_context_ref
        for item in original.evidence_bindings
        if item.evidence_id == "E-BASE"
    )
    mutated_ref = next(
        item.runtime_or_context_ref
        for item in mutated.evidence_bindings
        if item.evidence_id == "E-BASE"
    )
    assert original_ref != mutated_ref


def test_evidence_provenance_must_bind_exact_trial_evidence_ref() -> None:
    mapping = _mapping()
    ledger = _ledger()
    wrong = EpistemicProvenanceLedger()
    wrong.add(ledger.get("claim-prov"))
    wrong.add(
        ContributionRecord(
            record_id="evidence-base-prov",
            proposition="Valid but unrelated provenance record.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.OBSERVATION,
            source_refs=("fixture:unrelated-source",),
        )
    )
    wrong.add(ledger.get("evidence-intervention-prov"))

    with pytest.raises(LongitudinalClaimBridgeError, match="not source-bound"):
        assess_longitudinal_claim_mapping(
            mapping,
            ledger=wrong,
            lot=_lot(),
            repository_root=REPOSITORY_ROOT,
        )


def test_claim_provenance_must_bind_all_trial_evidence_refs() -> None:
    mapping = _mapping()
    ledger = _ledger()
    wrong = EpistemicProvenanceLedger()
    wrong.add(
        ContributionRecord(
            record_id="claim-prov",
            proposition="Bounded longitudinal contrast claim.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.OBSERVATION,
            source_refs=("fixture:base:regrounding",),
        )
    )
    wrong.add(ledger.get("evidence-base-prov"))
    wrong.add(ledger.get("evidence-intervention-prov"))

    with pytest.raises(LongitudinalClaimBridgeError, match="not bound to all trial evidence refs"):
        assess_longitudinal_claim_mapping(
            mapping,
            ledger=wrong,
            lot=_lot(),
            repository_root=REPOSITORY_ROOT,
        )


def test_content_addressed_runtime_ref_avoids_delimiter_collision() -> None:
    baseline_a = _baseline()
    baseline_b = _baseline()
    baseline_a = replace(
        baseline_a,
        binding=replace(
            baseline_a.binding,
            provider_id="a|model:b",
            model_id="c",
        ),
    )
    baseline_b = replace(
        baseline_b,
        binding=replace(
            baseline_b.binding,
            provider_id="a",
            model_id="b|model:c",
        ),
    )

    mapping_a = _mapping(baseline=baseline_a)
    mapping_b = _mapping(baseline=baseline_b)

    ref_a = next(
        item.runtime_or_context_ref
        for item in mapping_a.evidence_bindings
        if item.evidence_id == "E-BASE"
    )
    ref_b = next(
        item.runtime_or_context_ref
        for item in mapping_b.evidence_bindings
        if item.evidence_id == "E-BASE"
    )
    assert ref_a != ref_b
    assert ref_a.startswith("longitudinal-runtime-sha256:")
    assert ref_b.startswith("longitudinal-runtime-sha256:")


def test_contrast_identity_mismatch_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="does not match"):
        _mapping(audit=_audit(contrast_id="OTHER-CONTRAST"))


def test_run_binding_mismatch_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="baseline trial run_id"):
        _mapping(baseline=_baseline(run_id="WRONG-RUN"))


def test_structurally_inadmissible_contrast_cannot_enter_mapping() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="structurally inadmissible"):
        _mapping(audit=_audit(structurally_admissible=False))


def test_audit_delta_must_match_source_trial_values() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="does not match source trial values"):
        _mapping(audit=_audit(observed_deltas=((MetricName.REGROUNDING_COST.value, 99.0),)))


def test_metric_unit_drift_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="metric unit drift"):
        _mapping(intervention=_intervention(unit="seconds"))


def test_metric_held_out_drift_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="held_out status drift"):
        _mapping(intervention=_intervention(held_out=True))


def test_evidence_must_bind_to_actual_trial_metric_reference() -> None:
    bad = replace(
        _request().evidence[0],
        study_evidence_ref="fixture:not-from-trial",
    )
    request = _request(evidence=(bad, _request().evidence[1]))
    with pytest.raises(
        LongitudinalClaimBridgeError,
        match="not bound to trial metric evidence",
    ):
        _mapping(request=request)


def test_duplicate_trial_metric_evidence_mapping_fails_closed() -> None:
    duplicate = replace(_request().evidence[0], evidence_id="E-BASE-DUP")
    request = _request(evidence=(_request().evidence[0], duplicate, _request().evidence[1]))
    with pytest.raises(LongitudinalClaimBridgeError, match="cannot be duplicated"):
        _mapping(request=request)


def test_support_must_cover_both_runs_for_required_metric() -> None:
    request = _request(evidence=(_request().evidence[1],))
    with pytest.raises(LongitudinalClaimBridgeError, match="cover every trial metric evidence ref"):
        _mapping(request=request)


def test_all_trial_metric_evidence_refs_must_be_mapped() -> None:
    baseline = _baseline()
    metric = baseline.metrics[0]
    baseline = replace(
        baseline,
        metrics=(
            replace(
                metric,
                evidence_refs=(
                    "fixture:base:regrounding",
                    "fixture:base:secondary",
                ),
            ),
        ),
    )
    with pytest.raises(
        LongitudinalClaimBridgeError,
        match="cover every trial metric evidence ref",
    ):
        _mapping(baseline=baseline)


@pytest.mark.parametrize(
    ("canonical_effect", "deployment"),
    (("PROMOTE", False), ("NONE", True)),
)
def test_harness_cannot_smuggle_authority_into_claim_mapping(
    canonical_effect: str,
    deployment: bool,
) -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="canonical or deployment"):
        _mapping(audit=_audit(canonical_effect=canonical_effect, deployment=deployment))


def test_quality_lot_reference_must_match_trial_evidence_ref() -> None:
    mapping = _mapping()
    with pytest.raises(LongitudinalClaimBridgeError, match="reference mismatch"):
        assess_longitudinal_claim_mapping(
            mapping,
            ledger=_ledger(),
            lot=_lot(base_ref="fixture:unrelated"),
            repository_root=REPOSITORY_ROOT,
        )


def test_quality_lot_mapped_evidence_must_be_test_result() -> None:
    mapping = _mapping()
    with pytest.raises(LongitudinalClaimBridgeError, match="must be TEST_RESULT"):
        assess_longitudinal_claim_mapping(
            mapping,
            ledger=_ledger(),
            lot=_lot(base_kind=EvidenceKind.REPOSITORY_ARTIFACT),
            repository_root=REPOSITORY_ROOT,
        )


def test_quality_lot_mapped_evidence_must_support_bounded_observation() -> None:
    mapping = _mapping()
    with pytest.raises(LongitudinalClaimBridgeError, match="must support"):
        assess_longitudinal_claim_mapping(
            mapping,
            ledger=_ledger(),
            lot=_lot(base_supports=False),
            repository_root=REPOSITORY_ROOT,
        )


def test_duplicate_quality_lot_evidence_ids_fail_closed() -> None:
    mapping = _mapping()
    lot = _lot()
    lot.evidence.append(
        Evidence(
            evidence_id="E-BASE",
            kind=EvidenceKind.TEST_RESULT,
            reference="fixture:base:regrounding",
            supports_claim=True,
        )
    )
    with pytest.raises(LongitudinalClaimBridgeError, match="duplicate evidence ids"):
        assess_longitudinal_claim_mapping(
            mapping,
            ledger=_ledger(),
            lot=lot,
            repository_root=REPOSITORY_ROOT,
        )


def test_existing_claim_gate_still_requires_quality_final_qa() -> None:
    mapping = _mapping()
    assessment = assess_longitudinal_claim_mapping(
        mapping,
        ledger=_ledger(),
        lot=_lot(final_qa_pass=False),
        repository_root=REPOSITORY_ROOT,
    )
    assert assessment.disposition is ClaimAdmissionDisposition.HOLD
    assert "QUALITY_FACTORY_FINAL_QA_NOT_PASSED" in assessment.reasons


def test_missing_evidence_provenance_is_still_rejected_by_existing_gate() -> None:
    mapping = _mapping()
    incomplete_ledger = EpistemicProvenanceLedger()
    incomplete_ledger.add(
        ContributionRecord(
            record_id="claim-prov",
            proposition="Bounded longitudinal contrast claim.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.OBSERVATION,
            source_refs=(
                "fixture:base:regrounding",
                "fixture:memory:regrounding",
            ),
        )
    )
    assessment = assess_longitudinal_claim_mapping(
        mapping,
        ledger=incomplete_ledger,
        lot=_lot(),
        repository_root=REPOSITORY_ROOT,
    )
    assert assessment.disposition is ClaimAdmissionDisposition.HOLD
    assert "INVALID_PROVENANCE:evidence-base-prov" in assessment.reasons
    assert "INVALID_PROVENANCE:evidence-intervention-prov" in assessment.reasons

def test_structural_revalidation_rejects_uncontrolled_evaluator_drift() -> None:
    intervention = replace(_intervention(), evaluator_id="evaluator:other")
    with pytest.raises(
        LongitudinalClaimBridgeError,
        match="structural revalidation failed: uncontrolled evaluator drift",
    ):
        _mapping(intervention=intervention)


def test_structural_revalidation_rejects_uncontrolled_binding_drift() -> None:
    intervention = _intervention()
    intervention = replace(
        intervention,
        binding=replace(intervention.binding, provider_id="provider:other"),
    )
    with pytest.raises(
        LongitudinalClaimBridgeError,
        match="structural revalidation failed: uncontrolled binding drift",
    ):
        _mapping(intervention=intervention)


def test_structural_revalidation_rejects_undeclared_condition_change() -> None:
    intervention = _intervention()
    intervention = replace(
        intervention,
        condition=replace(intervention.condition, personalization=Presence.PRESENT),
    )
    with pytest.raises(
        LongitudinalClaimBridgeError,
        match="structural revalidation failed: condition change mismatch",
    ):
        _mapping(intervention=intervention)


def test_claim_identity_changes_when_falsifier_changes() -> None:
    original = _mapping()
    changed = _mapping(
        spec=replace(
            _spec(),
            falsifier="A different preregistered falsifier for the bounded observation.",
        )
    )
    assert changed.claim.claim_id != original.claim.claim_id


def test_claim_identity_changes_when_alternative_explanations_change() -> None:
    original = _mapping()
    changed = _mapping(
        spec=replace(
            _spec(),
            alternative_explanations=("Different alternative explanation",),
        )
    )
    assert changed.claim.claim_id != original.claim.claim_id


def test_claim_identity_changes_when_provenance_mapping_changes() -> None:
    original = _mapping()
    changed = _mapping(
        request=replace(_request(), provenance_record_id="claim-prov-v2")
    )
    assert changed.claim.claim_id != original.claim.claim_id


def test_claim_identity_changes_when_evidence_identity_changes() -> None:
    original = _mapping()
    evidence = _request().evidence
    changed_evidence = (
        replace(evidence[0], evidence_id="E-BASE-V2"),
        evidence[1],
    )
    changed = _mapping(request=_request(evidence=changed_evidence))
    assert changed.claim.claim_id != original.claim.claim_id

