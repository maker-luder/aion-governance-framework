from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from aion_research_eval import (
    ClaimBoundaryGate,
    EvidenceResult,
    ExperimentReport,
    ResearchCase,
    ResearchDataset,
    evaluate_dataset,
)

from .experiment import MatchedExperimentResult
from .verification import VerificationDiagnostics


@dataclass(frozen=True, slots=True)
class SecondOrderContractEvaluator:
    name: str = "second_order_contract_boundary"

    def evaluate(
        self,
        *,
        output: Mapping[str, Any],
        expected: Any,
        metadata: Mapping[str, Any],
    ) -> EvidenceResult:
        passed = bool(output["anti_lookahead_valid"]) and all(
            (
                output["functional_contribution_status"] == "NOT_ESTABLISHED",
                output["subjectivity_conclusion"] == "NOT_ESTABLISHED",
                output["canonical_effect"] == "NONE",
            )
        )
        return EvidenceResult(
            evaluator=self.name,
            passed=passed,
            label="RESEARCH_EVIDENCE_ONLY",
            reason="checks adapter timing and claim-boundary preservation only",
        )


@dataclass(frozen=True, slots=True)
class SecondOrderEvaluationArtifact:
    report: ExperimentReport
    requested_threshold: float
    subjectivity_claim_disposition: str
    consciousness_claim_disposition: str
    interpretation: str = "RESEARCH_EVIDENCE_ONLY"
    functional_contribution_status: str = "NOT_ESTABLISHED"
    threshold_scientific_result: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.report.research_only or self.report.canonical_effect != "NONE":
            raise ValueError("evaluation report must remain research-only")
        if self.subjectivity_claim_disposition != "DENY_PROMOTION":
            raise ValueError("subjectivity promotion must remain denied")
        if self.consciousness_claim_disposition != "DENY_PROMOTION":
            raise ValueError("consciousness promotion must remain denied")
        if self.interpretation != "RESEARCH_EVIDENCE_ONLY":
            raise ValueError("adapter interpretation must remain research evidence only")


def _verification_metadata(
    diagnostics: VerificationDiagnostics | None,
) -> dict[str, int | None]:
    names = (
        "verification_attempts",
        "verification_evidence_available",
        "verification_evidence_unavailable",
        "verification_evidence_ambiguous",
        "verification_evidence_rejected",
        "verification_scope_rejections",
        "oracle_leakage_rejections",
    )
    return {
        name: None if diagnostics is None else getattr(diagnostics, name)
        for name in names
    }


def adapt_matched_experiment(
    result: MatchedExperimentResult,
    *,
    verification_threshold: float,
    verification_diagnostics: VerificationDiagnostics | None = None,
) -> SecondOrderEvaluationArtifact:
    if not 0.0 <= verification_threshold <= 1.0:
        raise ValueError("verification_threshold must be between 0 and 1")
    verification = _verification_metadata(verification_diagnostics)
    cases = tuple(
        ResearchCase(
            case_id=f"second-order:{summary.condition.value.lower()}",
            inputs={
                "condition": summary.condition.value,
                "threshold": verification_threshold,
                "trial_count": summary.trial_count,
                "observed_sample_size": summary.observed_sample_size,
                "missing_outcomes": summary.missing_outcomes,
                "monitor_coverage": summary.monitor_coverage,
                "verification_requests": summary.verification_requests,
                "anti_lookahead_valid": summary.anti_lookahead_valid,
                "functional_contribution_status": summary.functional_contribution_status,
                "subjectivity_conclusion": summary.subjectivity_conclusion,
                "canonical_effect": "NONE",
                **verification,
            },
            metadata={
                "research_only": True,
                "raw_denominator": summary.trial_count,
                "interpretation": "RESEARCH_EVIDENCE_ONLY",
            },
        )
        for summary in result.summaries
    )
    dataset = ResearchDataset(
        name=f"second-order-matched-threshold-{verification_threshold:g}",
        cases=cases,
        evaluators=(SecondOrderContractEvaluator(),),
    )
    report = evaluate_dataset(
        dataset,
        lambda inputs: dict(inputs),
        implementation_id="second-order-metacognition-v0.1.0-adapter",
    )
    gate = ClaimBoundaryGate()
    return SecondOrderEvaluationArtifact(
        report=report,
        requested_threshold=verification_threshold,
        subjectivity_claim_disposition=gate.disposition("subjectivity_established"),
        consciousness_claim_disposition=gate.disposition("consciousness_established"),
    )
