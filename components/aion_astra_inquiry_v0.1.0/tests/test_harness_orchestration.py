from __future__ import annotations

from pathlib import Path

import pytest

from aion_astra_inquiry.core import EvidenceItem, InquiryReport, StopReason
from aion_astra_inquiry.harness_orchestration import (
    BoundedHarnessOrchestrator,
    HarnessExecutionClass,
    HarnessExecutionStatus,
    HarnessRegistration,
    default_harness_registry,
    verify_harness_receipt,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def _report_for(ref: str) -> InquiryReport:
    return InquiryReport(
        question="Does changing only persistent internal state alter bounded selection?",
        transcript=(),
        evidence=(
            EvidenceItem(
                ref=ref,
                excerpt="state intervention ablation matched control",
                content_sha256="0" * 64,
            ),
        ),
        stop_reason=StopReason.MAX_ROUNDS,
        candidate_findings=(),
        final_chain_hash="GENESIS",
    )


def test_default_registry_contains_only_enabled_state_level_harnesses() -> None:
    registrations = default_harness_registry().registrations
    assert {item.harness_id for item in registrations} == {
        "endogenous-goal-dynamics-state-v0.1.0",
        "endogenous-norm-formation-state-v0.1.0",
    }
    assert all(item.enabled for item in registrations)
    assert all(item.execution_class is HarnessExecutionClass.STATE_LEVEL for item in registrations)
    assert all(item.network_access is False for item in registrations)
    assert all(item.secret_access is False for item in registrations)
    assert all(item.repository_mutation is False for item in registrations)
    assert all(item.live_model_execution is False for item in registrations)


def test_registry_recommends_harness_only_from_admitted_lab_evidence() -> None:
    orchestrator = BoundedHarnessOrchestrator(REPOSITORY_ROOT, repository_ref="TEST_HEAD")
    egd = orchestrator.recommend_for_report(
        _report_for("research-labs/endogenous-goal-dynamics_v0.1.0/README.md")
    )
    unrelated = orchestrator.recommend_for_report(_report_for("docs/unrelated.md"))
    assert egd == ("endogenous-goal-dynamics-state-v0.1.0",)
    assert unrelated == ()


def test_endogenous_goal_dynamics_state_harness_executes_and_receipt_verifies() -> None:
    receipt = BoundedHarnessOrchestrator(
        REPOSITORY_ROOT,
        repository_ref="TEST_HEAD",
    ).execute("endogenous-goal-dynamics-state-v0.1.0")

    assert receipt.status is HarnessExecutionStatus.EXECUTED
    assert receipt.execution_class is HarnessExecutionClass.STATE_LEVEL
    assert receipt.state_intervention_observed is True
    assert receipt.live_model_execution is False
    assert receipt.network_access is False
    assert receipt.secret_access is False
    assert receipt.repository_mutation is False
    assert receipt.canonical_effect == "NONE"
    assert "Error in sitecustomize" not in receipt.stderr_excerpt
    assert verify_harness_receipt(receipt)


def test_endogenous_norm_formation_state_harness_executes_and_receipt_verifies() -> None:
    receipt = BoundedHarnessOrchestrator(
        REPOSITORY_ROOT,
        repository_ref="TEST_HEAD",
    ).execute("endogenous-norm-formation-state-v0.1.0")

    assessment = receipt.result_payload["assessment"]
    assert isinstance(assessment, dict)
    assert assessment["state_has_causal_role"] is True
    assert assessment["counterevidence_revises_state"] is True
    assert receipt.state_intervention_observed is True
    assert receipt.live_model_execution is False
    assert verify_harness_receipt(receipt)


def test_model_level_registration_cannot_be_enabled_by_agent_or_registry() -> None:
    with pytest.raises(ValueError, match="model-level"):
        HarnessRegistration(
            harness_id="forbidden-live-model",
            lab_path="research-labs/language-core-g1_v0.2.1",
            entrypoint="research-labs/language-core-g1_v0.2.1/scripts/run_model.py",
            python_source="research-labs/language-core-g1_v0.2.1/src",
            execution_class=HarnessExecutionClass.MODEL_LEVEL,
            enabled=True,
            live_model_execution=True,
        )


def test_registration_rejects_path_escape_and_authority_expansion() -> None:
    with pytest.raises(ValueError, match="normalized repository-relative"):
        HarnessRegistration(
            harness_id="escape",
            lab_path="research-labs/demo",
            entrypoint="research-labs/demo/../outside.py",
            python_source="research-labs/demo/src",
            execution_class=HarnessExecutionClass.STATE_LEVEL,
            enabled=True,
        )

    with pytest.raises(ValueError, match="read-only"):
        HarnessRegistration(
            harness_id="write-capable",
            lab_path="research-labs/demo",
            entrypoint="research-labs/demo/run.py",
            python_source="research-labs/demo/src",
            execution_class=HarnessExecutionClass.STATE_LEVEL,
            enabled=True,
            repository_mutation=True,
        )
