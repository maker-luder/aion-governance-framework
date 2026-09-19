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
        claim_id="CLAIM-LONG-01",
        version=1,
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
        )
    )
    for record_id, proposition in (
        ("evidence-base-prov", "Synthetic baseline metric evidence."),
        ("evidence-intervention-prov", "Synthetic intervention metric evidence."),
    ):
        ledger.add(
            ContributionRecord(
                record_id=record_id,
                proposition=proposition,
                origin=ContributionOrigin.AI_FORMALIZATION,
                layer=ClaimLayer.OBSERVATION,
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
    with pytest.raises(LongitudinalClaimBridgeError, match="cover both runs"):
        _mapping(request=request)


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
