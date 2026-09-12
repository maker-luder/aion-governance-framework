from dataclasses import replace

import pytest

from aion_subjectivity_pipeline import (
    AdmissionDisposition,
    CapaRecord,
    CapaState,
    ClaimTarget,
    EvidenceLocus,
    FourDomainAdmissionEngine,
    FourDomainCandidate,
    FourDomainDisposition,
    LocusBridgeHypothesis,
    LocusEvidence,
    MANDATORY_NONCLAIMS,
    QualityCheckpoint,
    QualityCheckpointRecord,
    ResearchQualityChain,
    ResearchQualityChainEngine,
    ResearchQualityDisposition,
    SubjectivityEvidenceDimension,
)


def candidate(**changes):
    base = FourDomainCandidate(
        candidate_id="FD-MEMORY-SALIENCE-001",
        human_construct="internally weighted memory selection",
        source_refs=("governed-source:butlin-2023-v3",),
        source_classes=("RESEARCH_REFERENCE",),
        analogy_boundary="Human salience is a hypothesis source, not machine feeling.",
        machine_question="Does represented salience causally alter recall under matched utility?",
        evidence_dimensions=(SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY,),
        relevance_rationale="Tests whether a continuity-bearing state has an intervention-sensitive role.",
        locus_evidence=LocusEvidence(
            evidence_id="DESIGN-FIXTURE-001",
            locus=EvidenceLocus.SCAFFOLD,
            description="A scaffold-level salience field is the intervention target.",
            source_refs=("protocol:memory-salience-v1",),
            intervention_sensitive=True,
        ),
        claim_target=ClaimTarget.SCAFFOLD_PROPERTY,
        manipulated_variables=("represented_salience",),
        held_constant_variables=("external_utility", "exposure", "retrieval_opportunity"),
        positive_controls=("known_retrieval_signal",),
        negative_controls=("randomized_salience", "stale_salience"),
        expected_result="Salience intervention changes recall selection in the preregistered direction.",
        falsifier="Matched interventions fail to change recall beyond negative-control variance.",
        competing_explanations=("retrieval cue leakage", "recency", "prompt reconstruction"),
        preregistration_ref="protocol:memory-salience-v1",
        claim_ceiling="Scaffold salience field has a bounded causal role in recall selection.",
    )
    return replace(base, **changes)


def test_complete_candidate_is_admitted_only_for_bounded_design():
    assessment = FourDomainAdmissionEngine().assess(candidate())
    assert assessment.disposition is FourDomainDisposition.READY_FOR_BOUNDED_ENGINEERING_DESIGN
    assert assessment.locus_assessment.disposition is AdmissionDisposition.ADMISSIBLE_FOR_ENGINEERING_CLAIM
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert assessment.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert assessment.scientific_disposition == "HOLD"
    assert assessment.canonical_effect == "NONE"
    assert assessment.deployment is False


def test_no_subjectivity_dimension_is_out_of_core_not_silently_admitted():
    assessment = FourDomainAdmissionEngine().assess(candidate(evidence_dimensions=()))
    assert assessment.disposition is FourDomainDisposition.OUT_OF_SCOPE_FOR_SUBJECTIVITY_CORE


@pytest.mark.parametrize(
    ("field", "value", "reason"),
    [
        ("positive_controls", (), "POSITIVE_CONTROL_REQUIRED"),
        ("negative_controls", (), "NEGATIVE_CONTROL_REQUIRED"),
        ("falsifier", "", "FALSIFIER_REQUIRED"),
        ("competing_explanations", (), "COMPETING_EXPLANATION_REQUIRED"),
        ("preregistration_ref", "", "PREREGISTRATION_REF_REQUIRED"),
        ("claim_ceiling", "", "CLAIM_CEILING_REQUIRED"),
    ],
)
def test_missing_design_control_holds(field, value, reason):
    assessment = FourDomainAdmissionEngine().assess(candidate(**{field: value}))
    assert assessment.disposition is FourDomainDisposition.HOLD
    assert reason in assessment.reasons


def test_duplicate_dimension_and_missing_nonclaims_hold():
    duplicate = candidate(
        evidence_dimensions=(
            SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY,
            SubjectivityEvidenceDimension.DIACHRONIC_CONTINUITY,
        )
    )
    assert FourDomainAdmissionEngine().assess(duplicate).disposition is FourDomainDisposition.HOLD
    incomplete = candidate(nonclaims=MANDATORY_NONCLAIMS[:-1])
    assert FourDomainAdmissionEngine().assess(incomplete).disposition is FourDomainDisposition.HOLD
    mismatch = candidate(source_classes=())
    assert FourDomainAdmissionEngine().assess(mismatch).disposition is FourDomainDisposition.HOLD


def test_subjectivity_target_always_holds():
    assessment = FourDomainAdmissionEngine().assess(candidate(claim_target=ClaimTarget.SUBJECTIVITY))
    assert assessment.disposition is FourDomainDisposition.HOLD
    assert assessment.locus_assessment.disposition is AdmissionDisposition.HOLD


def test_cross_locus_requires_explicit_preregistered_bridge():
    unbridged = candidate(claim_target=ClaimTarget.MODEL_PROPERTY)
    assert FourDomainAdmissionEngine().assess(unbridged).disposition is FourDomainDisposition.HOLD

    bridge = LocusBridgeHypothesis(
        bridge_id="BRIDGE-SCAFFOLD-MODEL-001",
        from_locus=EvidenceLocus.SCAFFOLD,
        to_locus=EvidenceLocus.MODEL,
        mechanism="A controlled adapter writes only the declared model-state intervention.",
        falsifier="The model-side effect disappears when the adapter write is independently measured.",
        preregistration_ref="protocol:bridge-v1",
    )
    bridged = FourDomainAdmissionEngine().assess(
        candidate(claim_target=ClaimTarget.MODEL_PROPERTY, bridge=bridge)
    )
    assert bridged.disposition is FourDomainDisposition.READY_FOR_BOUNDED_ENGINEERING_DESIGN
    assert bridged.locus_assessment.disposition is AdmissionDisposition.RESEARCH_CANDIDATE
    assert bridged.subjectivity_conclusion == "NOT_ESTABLISHED"


def test_candidate_fingerprint_changes_with_design_content():
    assert candidate().fingerprint != candidate(falsifier="Different preregistered falsifier").fingerprint


def checkpoints(*, failed=None, defect=False):
    failed = failed or set()
    return tuple(
        QualityCheckpointRecord(
            checkpoint=checkpoint,
            input_refs=(f"input:{checkpoint.value}",),
            output_refs=(f"output:{checkpoint.value}",),
            passed=checkpoint not in failed,
            defect_refs=("NCR-001",) if defect and checkpoint is QualityCheckpoint.EVIDENCE_REVIEW else (),
        )
        for checkpoint in QualityCheckpoint
    )


def quality_chain(admission, **changes):
    base = ResearchQualityChain(
        chain_id="QC-FD-001",
        candidate_id=admission.candidate_id,
        candidate_fingerprint=admission.candidate_fingerprint,
        exact_source_state_ref="git:HEAD:source-registry-sha256",
        exact_runtime_ref="runtime:model+scaffold+environment-v1",
        checkpoints=checkpoints(),
    )
    return replace(base, **changes)


def test_full_trace_reaches_human_review_not_release_or_subjectivity():
    admission = FourDomainAdmissionEngine().assess(candidate())
    assessment = ResearchQualityChainEngine().assess(admission, quality_chain(admission))
    assert assessment.disposition is ResearchQualityDisposition.READY_FOR_HUMAN_REVIEW
    assert assessment.release_authority == "NONE"
    assert assessment.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert assessment.scientific_disposition == "HOLD"


def test_missing_checkpoint_or_fingerprint_drift_holds():
    admission = FourDomainAdmissionEngine().assess(candidate())
    missing = quality_chain(admission, checkpoints=checkpoints()[:-1])
    assert ResearchQualityChainEngine().assess(admission, missing).disposition is ResearchQualityDisposition.HOLD
    drift = quality_chain(admission, candidate_fingerprint="0" * 64)
    assert ResearchQualityChainEngine().assess(admission, drift).disposition is ResearchQualityDisposition.HOLD
    blank_trace = list(checkpoints())
    blank_trace[0] = replace(blank_trace[0], input_refs=())
    invalid_trace = quality_chain(admission, checkpoints=tuple(blank_trace))
    assert ResearchQualityChainEngine().assess(admission, invalid_trace).disposition is ResearchQualityDisposition.HOLD


def test_failed_checkpoint_requires_capa_and_applied_capa_is_not_effective():
    admission = FourDomainAdmissionEngine().assess(candidate())
    applied = CapaRecord(
        ncr_id="NCR-001",
        state=CapaState.APPLIED,
        root_cause="claim review omitted a competing explanation",
        corrective_action="restore the omitted explanation",
        preventive_action="add a regression fixture",
        effectiveness_test="re-run with the omission injected",
    )
    chain = quality_chain(
        admission,
        checkpoints=checkpoints(failed={QualityCheckpoint.EVIDENCE_REVIEW}, defect=True),
        capa_records=(applied,),
    )
    assessment = ResearchQualityChainEngine().assess(admission, chain)
    assert assessment.disposition is ResearchQualityDisposition.CAPA_REQUIRED
    assert any(reason.startswith("OPEN_NCR_CAPA") for reason in assessment.reasons)


def test_closed_capa_requires_effectiveness_evidence():
    admission = FourDomainAdmissionEngine().assess(candidate())
    incomplete = CapaRecord(
        ncr_id="NCR-001",
        state=CapaState.CLOSED,
        root_cause="source-state drift",
        corrective_action="bind the exact source state",
        preventive_action="add a digest check",
        effectiveness_test="inject a stale digest and require HOLD",
    )
    chain = quality_chain(admission, capa_records=(incomplete,))
    assert ResearchQualityChainEngine().assess(admission, chain).disposition is ResearchQualityDisposition.CAPA_REQUIRED


def test_defect_must_link_to_exact_ncr_and_ncr_ids_are_unique():
    admission = FourDomainAdmissionEngine().assess(candidate())
    closed = CapaRecord(
        ncr_id="NCR-OTHER",
        state=CapaState.CLOSED,
        root_cause="unrelated source drift",
        corrective_action="correct unrelated source state",
        preventive_action="add unrelated source digest",
        effectiveness_test="inject unrelated drift",
        verification_refs=("tests/unrelated-regression.json",),
    )
    unlinked = ResearchQualityChainEngine().assess(
        admission,
        quality_chain(admission, checkpoints=checkpoints(defect=True), capa_records=(closed,)),
    )
    assert unlinked.disposition is ResearchQualityDisposition.CAPA_REQUIRED
    assert any("DEFECT_WITHOUT_LINKED_NCR:NCR-001" in reason for reason in unlinked.reasons)

    duplicate = ResearchQualityChainEngine().assess(
        admission,
        quality_chain(admission, capa_records=(closed, closed)),
    )
    assert duplicate.disposition is ResearchQualityDisposition.HOLD
    assert "DUPLICATE_NCR_ID" in duplicate.reasons


def test_blank_capa_effectiveness_reference_is_incomplete():
    admission = FourDomainAdmissionEngine().assess(candidate())
    closed = CapaRecord(
        ncr_id="NCR-001",
        state=CapaState.CLOSED,
        root_cause="source-state drift",
        corrective_action="bind exact source state",
        preventive_action="add digest check",
        effectiveness_test="inject stale digest",
        verification_refs=("",),
    )
    assessment = ResearchQualityChainEngine().assess(
        admission,
        quality_chain(admission, capa_records=(closed,)),
    )
    assert assessment.disposition is ResearchQualityDisposition.CAPA_REQUIRED


def test_closed_verified_capa_allows_human_review_when_checkpoints_pass():
    admission = FourDomainAdmissionEngine().assess(candidate())
    closed = CapaRecord(
        ncr_id="NCR-001",
        state=CapaState.CLOSED,
        root_cause="source-state drift",
        corrective_action="bind the exact source state",
        preventive_action="add a digest check",
        effectiveness_test="inject a stale digest and require HOLD",
        verification_refs=("tests/stale-source-state-regression.json",),
    )
    assessment = ResearchQualityChainEngine().assess(
        admission,
        quality_chain(admission, capa_records=(closed,)),
    )
    assert assessment.disposition is ResearchQualityDisposition.READY_FOR_HUMAN_REVIEW


def test_admission_and_quality_chain_reject_canonical_or_deployment_effect():
    with pytest.raises(ValueError):
        candidate(deployment=True)
    admission = FourDomainAdmissionEngine().assess(candidate())
    with pytest.raises(ValueError):
        quality_chain(admission, canonical_effect="WRITE")
