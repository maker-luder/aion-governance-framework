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
    ContrastAudit,
    ContrastSpec,
    MetricName,
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


def _request(**changes: object) -> LongitudinalClaimRequest:
    defaults = dict(
        claim_id="CLAIM-LONG-01",
        version=1,
        statement="A bounded synthetic contrast produced the preregistered metric observation.",
        provenance_record_id="claim-prov",
        claim_level=ClaimLevel.L0_OBSERVATION,
        evidence=(
            LongitudinalEvidenceInput(
                evidence_id="E-LONG-1",
                provenance_record_id="evidence-prov",
                relation=EvidenceRelation.SUPPORTS,
                publication_class=PublicationClass.SYNTHETIC,
                producer_ref="human-ai-longitudinal-study:C-MEMORY-01",
                runtime_or_context_ref="RUN-BASE->RUN-MEMORY",
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
    ledger.add(
        ContributionRecord(
            record_id="evidence-prov",
            proposition="Synthetic longitudinal contrast evidence.",
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
                evidence_id="E-LONG-1",
                kind=EvidenceKind.TEST_RESULT,
                reference="fixture:longitudinal-contrast",
                supports_claim=True,
            )
        ],
        final_qa_pass=True,
    )


def test_real_longitudinal_types_map_into_existing_claim_gate() -> None:
    mapping = build_longitudinal_claim_mapping(_spec(), _audit(), _request())
    assert mapping.hypothesis_id == "H-GROUNDING-01"
    assert mapping.contrast_id == "C-MEMORY-01"
    assert mapping.baseline_run_id == "RUN-BASE"
    assert mapping.intervention_run_id == "RUN-MEMORY"
    assert mapping.required_metrics == (MetricName.REGROUNDING_COST.value,)
    assert mapping.claim.subjectivity_claim is False
    assert mapping.claim.consciousness_claim is False
    assert mapping.canonical_effect == "NONE"

    assessment = assess_longitudinal_claim_mapping(
        mapping,
        ledger=_ledger(),
        lot=_lot(),
        repository_root=REPOSITORY_ROOT,
    )
    assert assessment.disposition is ClaimAdmissionDisposition.ADMISSIBLE_AS_BOUNDED_RESEARCH_RECORD
    assert assessment.scientific_disposition == "HOLD"
    assert assessment.subjectivity == "NOT_ESTABLISHED"
    assert assessment.consciousness == "NOT_ESTABLISHED"
    assert assessment.canonical_effect == "NONE"


def test_contrast_identity_mismatch_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="does not match"):
        build_longitudinal_claim_mapping(
            _spec(),
            _audit(contrast_id="OTHER-CONTRAST"),
            _request(),
        )


def test_structurally_inadmissible_contrast_cannot_enter_mapping() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="structurally inadmissible"):
        build_longitudinal_claim_mapping(
            _spec(),
            _audit(structurally_admissible=False),
            _request(),
        )


def test_metric_drift_between_spec_and_audit_fails_closed() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="exactly match"):
        build_longitudinal_claim_mapping(
            _spec(),
            _audit(observed_deltas=((MetricName.ERROR_DETECTION.value, 1.0),)),
            _request(),
        )


def test_bridge_does_not_infer_support_from_observation() -> None:
    request = _request(
        evidence=(
            LongitudinalEvidenceInput(
                evidence_id="E-LONG-1",
                provenance_record_id="evidence-prov",
                relation=EvidenceRelation.OBSERVES,
            ),
        )
    )
    with pytest.raises(LongitudinalClaimBridgeError, match="explicitly supporting"):
        build_longitudinal_claim_mapping(_spec(), _audit(), request)


def test_support_requires_exact_producer_and_runtime_context_refs() -> None:
    with pytest.raises(LongitudinalClaimBridgeError, match="producer_ref"):
        LongitudinalEvidenceInput(
            evidence_id="E-LONG-1",
            provenance_record_id="evidence-prov",
            relation=EvidenceRelation.SUPPORTS,
        )


def test_l3_is_not_admitted_without_explicit_intervention_sensitive_evidence() -> None:
    mapping = build_longitudinal_claim_mapping(
        _spec(),
        _audit(),
        _request(claim_level=ClaimLevel.L3_INTERVENTION_SENSITIVE_MECHANISM),
    )
    assessment = assess_longitudinal_claim_mapping(
        mapping,
        ledger=_ledger(),
        lot=_lot(),
        repository_root=REPOSITORY_ROOT,
    )
    assert assessment.disposition is ClaimAdmissionDisposition.HOLD
    assert "MECHANISM_PROMOTION_REQUIRES_INTERVENTION_SENSITIVE_EVIDENCE" in assessment.reasons


def test_private_evidence_remains_blocked_by_existing_gate() -> None:
    private = replace(
        _request().evidence[0],
        publication_class=PublicationClass.PRIVATE_TRANSCRIPT,
    )
    mapping = build_longitudinal_claim_mapping(
        _spec(),
        _audit(),
        _request(evidence=(private,)),
    )
    assessment = assess_longitudinal_claim_mapping(
        mapping,
        ledger=_ledger(),
        lot=_lot(),
        repository_root=REPOSITORY_ROOT,
    )
    assert assessment.disposition is ClaimAdmissionDisposition.HOLD
    assert "PRIVATE_TRANSCRIPT_NOT_PUBLISHABLE:E-LONG-1" in assessment.reasons


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
            _request(),
        )


def test_missing_evidence_provenance_is_still_rejected_by_existing_gate() -> None:
    mapping = build_longitudinal_claim_mapping(_spec(), _audit(), _request())
    empty_ledger = EpistemicProvenanceLedger()
    empty_ledger.add(
        ContributionRecord(
            record_id="claim-prov",
            proposition="Bounded longitudinal contrast claim.",
            origin=ContributionOrigin.AI_FORMALIZATION,
            layer=ClaimLayer.OBSERVATION,
        )
    )
    assessment = assess_longitudinal_claim_mapping(
        mapping,
        ledger=empty_ledger,
        lot=_lot(),
        repository_root=REPOSITORY_ROOT,
    )
    assert assessment.disposition is ClaimAdmissionDisposition.HOLD
    assert "INVALID_PROVENANCE:evidence-prov" in assessment.reasons
