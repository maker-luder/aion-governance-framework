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
    audit_fingerprint,
    payload_sha256,
)


SOURCE_PAYLOAD = "synthetic standards fixture v1"


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
        content_sha256=payload_sha256(SOURCE_PAYLOAD),
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


def audit_registry(*, sources: tuple[ExternalStandardSource, ...] | None = None, bindings: tuple[FourDomainStandardBinding, ...] | None = None):
    declared_sources = sources or (source(),)
    return FourDomainStandardsRegistry().audit(
        sources=declared_sources,
        source_payloads={item.standard_id: SOURCE_PAYLOAD for item in declared_sources},
        bindings=bindings or (binding(),),
        confounds=(confound(),),
        tev_vocabulary=vocabulary(),
    )


def test_complete_registry_is_structurally_admissible_with_nonclaims() -> None:
    audit = audit_registry()
    assert audit.structurally_admissible
    assert audit.tev_vocabulary_complete
    assert audit.model_invoked is False
    assert audit.evidence_admissibility == "PROCESS_CONTROL_ONLY"
    assert audit.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert audit.consciousness_conclusion == "NOT_ESTABLISHED"
    assert audit.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert audit.moral_status_conclusion == "NOT_ESTABLISHED"
    assert audit.scientific_disposition == "HOLD"
    assert audit.canonical_effect == "NONE"
    assert audit.deployment is False
    assert "SOURCE_CONTENT_HASHES_VERIFIED" in audit.reasons


def test_tev_vocabulary_cannot_collapse_or_omit_a_term() -> None:
    with pytest.raises(StandardsCrosswalkError, match="distinct and complete"):
        FourDomainStandardsRegistry().audit(
            sources=(source(),),
            source_payloads={source().standard_id: SOURCE_PAYLOAD},
            bindings=(binding(),),
            confounds=(confound(),),
            tev_vocabulary=vocabulary()[:-1],
        )


def test_unknown_standard_binding_fails_closed() -> None:
    with pytest.raises(StandardsCrosswalkError, match="unknown standard"):
        FourDomainStandardsRegistry().audit(
            sources=(source(),),
            source_payloads={source().standard_id: SOURCE_PAYLOAD},
            bindings=(replace(binding(), standard_id="UNKNOWN"),),
            confounds=(confound(),),
            tev_vocabulary=vocabulary(),
        )


def test_source_payload_hash_must_match_declared_digest() -> None:
    with pytest.raises(StandardsCrosswalkError, match="content hash mismatch"):
        FourDomainStandardsRegistry().audit(
            sources=(source(),),
            source_payloads={source().standard_id: "tampered standards fixture"},
            bindings=(binding(),),
            confounds=(confound(),),
            tev_vocabulary=vocabulary(),
        )


def test_every_source_requires_a_four_domain_binding() -> None:
    second = replace(
        source(),
        standard_id="STD-SYNTHETIC-002",
        title="Second fixture",
    )
    with pytest.raises(StandardsCrosswalkError, match="require Four-Domain bindings"):
        FourDomainStandardsRegistry().audit(
            sources=(source(), second),
            source_payloads={source().standard_id: SOURCE_PAYLOAD, second.standard_id: SOURCE_PAYLOAD},
            bindings=(binding(),),
            confounds=(confound(),),
            tev_vocabulary=vocabulary(),
        )


def test_human_construct_cannot_be_equivalence_or_subjectivity_proxy() -> None:
    with pytest.raises(StandardsCrosswalkError, match="cannot become"):
        replace(confound(), machine_equivalence=True)
    with pytest.raises(StandardsCrosswalkError, match="cannot become"):
        replace(confound(), subjectivity_proxy=True)


def test_competing_explanations_must_be_unique() -> None:
    with pytest.raises(StandardsCrosswalkError, match="must be unique"):
        replace(confound(), competing_explanations=("prompt cueing", "prompt cueing"))


def test_standard_source_content_is_immutably_bound() -> None:
    initial = source()
    changed = replace(initial, content_sha256=payload_sha256("changed fixture"))
    assert changed.content_sha256 != initial.content_sha256


def test_audit_fingerprint_binds_all_claim_boundary_fields() -> None:
    audit = audit_registry()
    assert audit_fingerprint(replace(audit, consciousness_conclusion="ESTABLISHED")) != audit_fingerprint(audit)
    assert audit_fingerprint(replace(audit, deployment=True)) != audit_fingerprint(audit)


def test_four_domain_fields_and_claim_ceiling_are_mandatory() -> None:
    with pytest.raises(StandardsCrosswalkError, match="machine_question_use"):
        replace(binding(), machine_question_use="")
    with pytest.raises(StandardsCrosswalkError, match="prohibited_promotion"):
        replace(binding(), prohibited_promotion="")
