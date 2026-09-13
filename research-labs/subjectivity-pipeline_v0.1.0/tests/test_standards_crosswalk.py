from __future__ import annotations

from dataclasses import replace

import pytest

from aion_subjectivity_pipeline import (
    ExternalStandardSource,
    FourDomainStandardBinding,
    FourDomainStandardsRegistry,
    StandardContributionRole,
    StandardsCrosswalkError,
    SubjectivityConfoundRecord,
    TevvDefinition,
    TevvTerm,
    payload_sha256,
)


def source() -> ExternalStandardSource:
    return ExternalStandardSource(
        standard_id="STD-SYNTHETIC-001",
        title="Synthetic quality and evidence vocabulary fixture",
        issuing_body="SYNTHETIC_FIXTURE",
        version_or_date="v1",
        locator="fixture:standards-crosswalk-v1",
        accessed_on="2026-09-13",
        contribution_roles=(
            StandardContributionRole.VOCABULARY,
            StandardContributionRole.PROCESS_CONTROL,
            StandardContributionRole.EVIDENCE_QUALITY,
            StandardContributionRole.CLAIM_LIMIT,
        ),
        content_sha256=payload_sha256("synthetic standards fixture v1"),
    )


def binding() -> FourDomainStandardBinding:
    return FourDomainStandardBinding(
        binding_id="BIND-001",
        standard_id="STD-SYNTHETIC-001",
        human_construct_use="Use human-side construct only as a hypothesis source.",
        machine_question_use="State an ontology-neutral machine question.",
        engineering_operation_use="Bind intervention, control, measurement, and falsifier.",
        governance_interpretation_use="Apply evidence ceiling and locus boundary.",
        permitted_claim="The declared process control is structurally satisfied.",
        prohibited_promotion="Process conformance does not establish subjectivity.",
    )


def confound() -> SubjectivityConfoundRecord:
    return SubjectivityConfoundRecord(
        confound_id="CONF-001",
        human_construct="human autobiographical continuity",
        machine_operationalization="availability of a versioned event-history fixture",
        competing_explanations=("retrieval reconstruction", "prompt cueing", "fixed policy"),
    )


def vocabulary() -> tuple[TevvDefinition, ...]:
    return (
        TevvDefinition(TevvTerm.TEST, "Did a bounded component produce the expected result?", "Declared oracle passes."),
        TevvDefinition(TevvTerm.EVALUATION, "How does observed performance compare with criteria?", "Criteria and uncertainty are reported."),
        TevvDefinition(TevvTerm.VERIFICATION, "Was the system built according to specified requirements?", "Specified requirements are traceably checked."),
        TevvDefinition(TevvTerm.VALIDATION, "Does the tested system support the intended use claim?", "Use-context evidence supports only the declared ceiling."),
    )


def test_complete_registry_is_structurally_admissible_with_nonclaims() -> None:
    audit = FourDomainStandardsRegistry().audit(
        sources=(source(),), bindings=(binding(),), confounds=(confound(),), tev_vocabulary=vocabulary()
    )
    assert audit.structurally_admissible
    assert audit.tev_vocabulary_complete
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.consciousness_conclusion == "NOT_ESTABLISHED"
    assert audit.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert audit.moral_status_conclusion == "NOT_ESTABLISHED"
    assert audit.scientific_disposition == "HOLD"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False


def test_tev_vocabulary_cannot_collapse_or_omit_a_term() -> None:
    with pytest.raises(StandardsCrosswalkError, match="distinct and complete"):
        FourDomainStandardsRegistry().audit(
            sources=(source(),), bindings=(binding(),), confounds=(confound(),), tev_vocabulary=vocabulary()[:-1]
        )


def test_unknown_standard_binding_fails_closed() -> None:
    with pytest.raises(StandardsCrosswalkError, match="unknown standard"):
        FourDomainStandardsRegistry().audit(
            sources=(source(),),
            bindings=(replace(binding(), standard_id="UNKNOWN"),),
            confounds=(confound(),),
            tev_vocabulary=vocabulary(),
        )


def test_human_construct_cannot_be_equivalence_or_subjectivity_proxy() -> None:
    with pytest.raises(StandardsCrosswalkError, match="cannot become"):
        replace(confound(), machine_equivalence=True)
    with pytest.raises(StandardsCrosswalkError, match="cannot become"):
        replace(confound(), subjectivity_proxy=True)


def test_standard_source_content_is_immutably_bound() -> None:
    initial = source()
    changed = replace(initial, content_sha256=payload_sha256("changed fixture"))
    assert changed.content_sha256 != initial.content_sha256


def test_four_domain_fields_and_claim_ceiling_are_mandatory() -> None:
    with pytest.raises(StandardsCrosswalkError, match="machine_question_use"):
        replace(binding(), machine_question_use="")
    with pytest.raises(StandardsCrosswalkError, match="prohibited_promotion"):
        replace(binding(), prohibited_promotion="")
