from __future__ import annotations

from dataclasses import replace

import pytest

from aion_subjectivity_pipeline import (
    QualityCheckpoint,
    QualityCheckpointRecord,
    ResearchQualityAssessment,
    ResearchQualityChain,
    ResearchQualityDisposition,
)
from aion_subjectivity_pipeline.quality_receipt import (
    QualityChainReceiptError,
    build_research_quality_chain_receipt,
)


FINGERPRINT = "f" * 64


def chain() -> ResearchQualityChain:
    return ResearchQualityChain(
        chain_id="CHAIN-RECEIPT-001",
        candidate_id="CANDIDATE-001",
        candidate_fingerprint=FINGERPRINT,
        exact_source_state_ref="git:source-head",
        exact_runtime_ref="runtime:fixture-v1",
        checkpoints=tuple(
            QualityCheckpointRecord(
                checkpoint=checkpoint,
                input_refs=(f"input:{checkpoint.value}",),
                output_refs=(f"output:{checkpoint.value}",),
                passed=True,
            )
            for checkpoint in QualityCheckpoint
        ),
    )


def assessment() -> ResearchQualityAssessment:
    return ResearchQualityAssessment(
        chain_id="CHAIN-RECEIPT-001",
        disposition=ResearchQualityDisposition.READY_FOR_HUMAN_REVIEW,
        reasons=("fixture quality chain ready for bounded human review",),
    )


def test_receipt_is_content_addressed_and_preserves_nonclaims() -> None:
    receipt = build_research_quality_chain_receipt(
        chain(),
        assessment(),
        producer_git_head="1" * 40,
        producer_tree_sha="2" * 40,
        producer_contract_ref="research-labs/subjectivity-pipeline_v0.1.0/src/aion_subjectivity_pipeline/four_domain.py",
        producer_contract_sha256="3" * 64,
    )
    assert len(receipt.receipt_sha256) == 64
    assert len(receipt.checkpoint_set_sha256) == 64
    assert receipt.disposition == "READY_FOR_HUMAN_REVIEW"
    assert receipt.release_authority == "NONE"
    assert receipt.subjectivity_conclusion == "NOT_ESTABLISHED"
    assert receipt.phenomenal_experience_conclusion == "NOT_ESTABLISHED"
    assert receipt.scientific_disposition == "HOLD"
    assert receipt.canonical_effect == "NONE"
    assert receipt.deployment is False


def test_receipt_tampering_fails_closed() -> None:
    receipt = build_research_quality_chain_receipt(
        chain(),
        assessment(),
        producer_git_head="1" * 40,
        producer_tree_sha="2" * 40,
        producer_contract_ref="contract:four-domain",
        producer_contract_sha256="3" * 64,
    )
    with pytest.raises(QualityChainReceiptError, match="content digest mismatch"):
        replace(receipt, disposition="HOLD")


def test_receipt_cannot_upgrade_scientific_or_release_authority() -> None:
    with pytest.raises(QualityChainReceiptError, match="scientific validity"):
        build_research_quality_chain_receipt(
            chain(),
            replace(assessment(), scientific_disposition="VALIDATED"),
            producer_git_head="1" * 40,
            producer_tree_sha="2" * 40,
            producer_contract_ref="contract:four-domain",
            producer_contract_sha256="3" * 64,
        )
    with pytest.raises(QualityChainReceiptError, match="release authority"):
        build_research_quality_chain_receipt(
            chain(),
            replace(assessment(), release_authority="AUTOMATIC"),
            producer_git_head="1" * 40,
            producer_tree_sha="2" * 40,
            producer_contract_ref="contract:four-domain",
            producer_contract_sha256="3" * 64,
        )
