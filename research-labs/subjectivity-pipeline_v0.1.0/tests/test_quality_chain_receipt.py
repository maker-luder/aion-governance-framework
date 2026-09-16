from __future__ import annotations

from dataclasses import replace
import hashlib
from pathlib import Path
import subprocess

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
    build_repository_bound_quality_chain_receipt,
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


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), *args],
        text=True,
        encoding="utf-8",
    ).strip()


def repository_fixture(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    git(root, "config", "user.name", "Receipt Fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    contract_ref = "contracts/four_domain.py"
    contract_path = root / contract_ref
    contract_path.parent.mkdir(parents=True)
    contract_path.write_text("CANONICAL = True\n", encoding="utf-8")
    git(root, "add", contract_ref)
    git(root, "commit", "-qm", "fixture contract")
    return root, contract_ref


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


def test_repository_bound_receipt_resolves_head_tree_and_contract_from_git_objects(tmp_path: Path) -> None:
    root, contract_ref = repository_fixture(tmp_path)
    committed_bytes = b"CANONICAL = True\n"
    receipt = build_repository_bound_quality_chain_receipt(
        chain(),
        assessment(),
        repository_root=root,
        producer_contract_ref=contract_ref,
    )
    assert receipt.producer_git_head == git(root, "rev-parse", "HEAD")
    assert receipt.producer_tree_sha == git(root, "rev-parse", "HEAD^{tree}")
    assert receipt.producer_contract_sha256 == hashlib.sha256(committed_bytes).hexdigest()

    # Dirty working-tree bytes must not be silently attributed to the committed tree.
    (root / contract_ref).write_text("CANONICAL = False\n", encoding="utf-8")
    dirty_receipt = build_repository_bound_quality_chain_receipt(
        chain(),
        assessment(),
        repository_root=root,
        producer_contract_ref=contract_ref,
    )
    assert dirty_receipt.producer_contract_sha256 == hashlib.sha256(committed_bytes).hexdigest()
    assert dirty_receipt.producer_tree_sha == receipt.producer_tree_sha


def test_repository_bound_receipt_rejects_non_top_level_and_unsafe_contract_path(tmp_path: Path) -> None:
    root, contract_ref = repository_fixture(tmp_path)
    nested = root / "nested"
    nested.mkdir()
    with pytest.raises(QualityChainReceiptError, match="exact Git top-level"):
        build_repository_bound_quality_chain_receipt(
            chain(),
            assessment(),
            repository_root=nested,
            producer_contract_ref=contract_ref,
        )
    with pytest.raises(QualityChainReceiptError, match="safe repository-relative"):
        build_repository_bound_quality_chain_receipt(
            chain(),
            assessment(),
            repository_root=root,
            producer_contract_ref="../outside.py",
        )


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
