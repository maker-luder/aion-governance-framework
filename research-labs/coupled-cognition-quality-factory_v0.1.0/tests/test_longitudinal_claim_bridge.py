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
    EvidenceRelation,
    PublicationClass,
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
) -> TrialRecord:
    return TrialRecord(
        binding=_binding(run_id, context_ref=context_ref),
        condition=_condition(memory=memory),
        metrics=(
            MetricObservation(
                metric=MetricName.REGROUNDING_COST,
                value=value,
                unit="turns",
                evidence_refs=(evidence_ref,),
            ),
        ),
        evaluator_id="evaluator:fixture",
        evaluator_source_ref="fixture:evaluator-protocol",
        retrieved_artifact_refs=("fixture:memory-artifact",)
        if memory is Presence.PRESENT
        else (),
    )


def _baseline() -> TrialRecord:
    return _trial(
        "RUN-BASE",
        memory=Presence.ABSENT,
        context_ref="context:base",
        value=4.0,
        evidence_ref="fixture:base:regrounding",
    )


def _intervention() -> TrialRecord:
    return _trial(
        "RUN-MEMORY",
        memory=Presence.PRESENT,
        context_ref="context:memory",
        value=2.5,
        evidence_ref="fixture:memory:regrounding",
    )


def _request(**changes: object) -> LongitudinalClaimRequest:
    defaults = dict(
        claim_id="CLAIM-LONG-01",
        version=1,
        statement="A bounded synthetic contrast produced the preregistered metric observation.",
        provenance_record_id="claim-prov",
        claim_level=ClaimLevel.L0_OBSERVATION,
        evidence=(
            LongitudinalEvidenceInput(
                evidence_id="E-BASE",
                provenance_record_id="evidence-base-prov",
                relation=EvidenceRelation.SUPPORTS,
                run_id="RUN-BASE",
                metric_name=MetricName.REGROUNDING_COST.value,
                study_evidence_ref="fixture:base:regrounding",
                publication_class=PublicationClass.SYNTHETIC,
            ),
            LongitudinalEvidenceInput(
                evidence_id="E-INTERVENTION",
                provenance_record_id="evidence-intervention-prov",
                relation=EvidenceRelation.SUPPORTS,
                run_id="RUN-MEMORY",
                metric_name=MetricName.REGROUNDING_COST.value,
                study_evidence_ref="fixture:memory:regrounding",
                publication_class=PublicationClass.SYNTHETIC,
            ),
        ),
        inferred_statements=("The observation remains compatible with simpler explanations.",),
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


def _lot() -> ResearchLot:
    return ResearchLot(
        lot_id="LOT-LONG-1",
        claim="Bounded longitudinal observation.",
        risk=Severity.MEDIUM,
        evidence=[
            Evidence(
                evidence_id="E-BASE",
                kind=EvidenceKind.TEST_RESULT,
                reference="fixture:base:regrounding",
                supports_claim=True,
            ),
            Evidence(
                evidence_id="E-INTERVENTION",
                kind=EvidenceKind.TEST_RESULT,
                reference="fixture:memory:regrounding",
                supports_claim=True,
            ),
        ],
        final_qa_pass=True,
    )


def _mapping(request: LongitudinalClaimRequest | None = None):
    return build_longitudinal_claim_mapping(
        _spec(),
        _audit(),
        _baseline(),
        _intervention(),
        request or _request(),
    )


def test_real_longitudinal_types_map_into_existing_claim_gate() -> None:
    mapping = _mapping()
    assert mapping.hypothesis_id == "H-GROUNDING-01"
    assert mapping.contrast_id == "C-MEMORY-01"
    assert mapping.baseline_run_id == "RUN-BASE"
    assert mapping.intervention_run_id == "RUN-MEMORY"
    assert mapping.required_metrics == (MetricName.REGROUNDING_COST.value,)
    assert mapping.claim.subjectivity_claim is False
    assert mapping.claim.consciousness_claim is False
    assert mapping.canonical_effect == "NONE"
    assert mapping.claim.claim_level is ClaimLevel.L0_OBSERVATION
    assert mapping.claim.population_scope is False
    assert mapping.claim.causal_learning_effect is False
    assert mapping.claim.publication_class is PublicationClass.SYNTHETIC
    assert mapping.claim.statement == (
        "Longitudinal contrast C-MEMORY-01 recorded bounded metric deltas "
        "for hypothesis H-GROUNDING-01: REGROUNDING_COST=-1.5."
    )
    assert all(not item.intervention_sensitive for item in mapping.evidence_bindings)
    assert all(not item.transfer_candidate for item in mapping.evidence_bindings)
    assert all(not item.held_out for item in mapping.evidence_bindings)
    assert all(not item.repeated for item in mapping.evidence_bindings)
    assert all(not item.comparison_control for item in mapping.evidence_bindings)
    assert all(not item.independently_scored for item in mapping.evidence_bindings)
    assert {item.runtime_or_context_ref for item in mapping.evidence_bindings} == {
        (
            "provider:provider:test|model:model:test|version:v1|"
            "configuration:config:matched-v1|context:context:base|"
            "repo:git:test-fixture|run:RUN-BASE"
        ),
        (
            "provider:provider:test|model:model:test|version:v1|"
            "configuration:config:matched-v1|context:context:memory|"
            "repo:git:test-fixture|run:RUN-MEMORY"
        ),
    }

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
        build_longitudinal_claim_mapping(
            _spec(),
            _audit(contrast_id="OTHER-CONTRAST"),
            _baseline(),
            _intervention(),
            _request(),
        )


def test_run_binding_mismatch_fails_closed() -> None:
    wrong = _trial(
        "WRONG-RUN",
        memory=Presence.ABSENT,
        context_ref="context:base",
        value=4.0,
        evidence_ref="fixture:base:regrounding",
    )
    with pytest.raises(LongitudinalClaimBridgeError, match="baseline trial run_id"):
        build_longitudinal_claim_mapping(
            _spec(), _audit(), wrong, _intervention(), _request()
        )


def test_structurally_inadmissible_contrast_cannot_enter_mapping() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="structurally inadmissible"):
        build_longitudinal_claim_mapping(
            _spec(),
            _audit(structurally_admissible=False),
            _baseline(),
            _intervention(),
            _request(),
        )


def test_metric_drift_between_spec_and_audit_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="exactly match"):
        build_longitudinal_claim_mapping(
            _spec(),
            _audit(observed_deltas=((MetricName.ERROR_DETECTION.value, 1.0),)),
            _baseline(),
            _intervention(),
            _request(),
        )


def test_evidence_must_bind_to_actual_trial_metric_reference() -> None:
    bad = replace(
        _request().evidence[0],
        study_evidence_ref="fixture:not-from-trial",
    )
    request = _request(evidence=(bad, _request().evidence[1]))
    with pytest.raises(LongitudinalClaimBridgeError, match="not bound to trial metric evidence"):
        build_longitudinal_claim_mapping(
            _spec(), _audit(), _baseline(), _intervention(), request
        )


def test_support_must_cover_both_runs_for_required_metric() -> None:
    request = _request(evidence=(_request().evidence[1],))
    with pytest.raises(LongitudinalClaimBridgeError, match="cover both runs"):
        build_longitudinal_claim_mapping(
            _spec(), _audit(), _baseline(), _intervention(), request
        )


def test_non_support_trial_relation_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="SUPPORTS only"):
        replace(
            _request().evidence[0],
            relation=EvidenceRelation.OBSERVES,
        )


@pytest.mark.parametrize(
    "claim_level",
    (
        ClaimLevel.L1_REPEATABLE_BEHAVIOR,
        ClaimLevel.L2_STATE_ASSOCIATION,
        ClaimLevel.L3_INTERVENTION_SENSITIVE_MECHANISM,
        ClaimLevel.L4_ROBUST_REPLICATION,
        ClaimLevel.L5_SUBJECTIVITY_NOT_AUTOMATICALLY_ESTABLISHED,
    ),
)
def test_bridge_v01_rejects_claim_levels_above_l0(claim_level: ClaimLevel) -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="L0 observation records only"):
        _request(claim_level=claim_level)


@pytest.mark.parametrize(
    "field_name",
    (
        "intervention_sensitive",
        "transfer_candidate",
        "held_out",
        "repeated",
        "comparison_control",
        "independently_scored",
    ),
)
def test_advanced_evidence_qualification_flags_fail_closed(field_name: str) -> None:
    changes = {field_name: True}
    with pytest.raises(LongitudinalClaimBridgeError, match="advanced evidence qualification"):
        LongitudinalEvidenceInput(
            evidence_id="E-ADVANCED",
            provenance_record_id="evidence-base-prov",
            relation=EvidenceRelation.SUPPORTS,
            run_id="RUN-BASE",
            metric_name=MetricName.REGROUNDING_COST.value,
            study_evidence_ref="fixture:base:regrounding",
            **changes,
        )


def test_replication_qualification_refs_fail_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="replication qualification"):
        LongitudinalEvidenceInput(
            evidence_id="E-REPLICATION",
            provenance_record_id="evidence-base-prov",
            relation=EvidenceRelation.SUPPORTS,
            run_id="RUN-BASE",
            metric_name=MetricName.REGROUNDING_COST.value,
            study_evidence_ref="fixture:base:regrounding",
            replication_source_ref="fixture:replication",
            replication_provenance_record_id="replication-prov",
        )


@pytest.mark.parametrize(
    ("population_scope", "causal_learning_effect"),
    ((True, False), (False, True), (True, True)),
)
def test_population_and_causal_learning_promotion_fail_closed(
    population_scope: bool,
    causal_learning_effect: bool,
) -> None:
    with pytest.raises(
        LongitudinalClaimBridgeError,
        match="cannot promote population or causal-learning scope",
    ):
        _request(
            population_scope=population_scope,
            causal_learning_effect=causal_learning_effect,
        )


def test_non_synthetic_trial_evidence_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="SYNTHETIC trial evidence only"):
        replace(
            _request().evidence[0],
            publication_class=PublicationClass.PRIVATE_TRANSCRIPT,
        )


def test_non_synthetic_claim_publication_class_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="emits SYNTHETIC claims only"):
        _request(publication_class=PublicationClass.PUBLIC_SAFE)


def test_caller_statement_cannot_override_bounded_observation_statement() -> None:
    request = _request(statement="This proves the hypothesis and subjectivity.")
    mapping = _mapping(request)
    assert "proves the hypothesis" not in mapping.claim.statement
    assert mapping.claim.statement.startswith("Longitudinal contrast C-MEMORY-01 recorded bounded metric deltas")


@pytest.mark.parametrize(
    ("canonical_effect", "deployment"),
    (("PROMOTE", False), ("NONE", True)),
)
def test_harness_cannot_smuggle_authority_into_claim_mapping(
    canonical_effect: str,
    deployment: bool,
) -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="canonical or deployment"):
        build_longitudinal_claim_mapping(
            _spec(),
            _audit(canonical_effect=canonical_effect, deployment=deployment),
            _baseline(),
            _intervention(),
            _request(),
        )


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
