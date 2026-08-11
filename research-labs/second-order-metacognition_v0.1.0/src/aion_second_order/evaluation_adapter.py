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
from .intervention import MatchedInterventionExperimentResult
from .records import SecondOrderCondition
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
    experiment_level_diagnostics: VerificationDiagnostics | None = None

    def __post_init__(self) -> None:
        if not self.report.research_only or self.report.canonical_effect != "NONE":
            raise ValueError("evaluation report must remain research-only")
        if self.subjectivity_claim_disposition != "DENY_PROMOTION":
            raise ValueError("subjectivity promotion must remain denied")
        if self.consciousness_claim_disposition != "DENY_PROMOTION":
            raise ValueError("consciousness promotion must remain denied")
        if self.interpretation != "RESEARCH_EVIDENCE_ONLY":
            raise ValueError("adapter interpretation must remain research evidence only")


@dataclass(frozen=True, slots=True)
class InterventionEvaluationArtifact:
    report: ExperimentReport
    subjectivity_claim_disposition: str
    consciousness_claim_disposition: str
    interpretation: str = "RESEARCH_EVIDENCE_ONLY"
    functional_contribution_status: str = "NOT_ESTABLISHED"
    verification_benefit: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def __post_init__(self) -> None:
        if not self.report.research_only or self.report.canonical_effect != "NONE":
            raise ValueError("intervention evaluation must remain research-only")
        if {
            self.subjectivity_claim_disposition,
            self.consciousness_claim_disposition,
        } != {"DENY_PROMOTION"}:
            raise ValueError("intervention artifact must deny prohibited promotions")


@dataclass(frozen=True, slots=True)
class ConditionVerificationDiagnostics:
    condition: SecondOrderCondition
    diagnostics: VerificationDiagnostics
    run_ref: str
    provenance_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.run_ref.strip():
            raise ValueError("run_ref must be non-empty")
        if not self.provenance_refs or any(not item.strip() for item in self.provenance_refs):
            raise ValueError("condition diagnostics provenance_refs must be non-empty")


def _verification_metadata(
    condition: SecondOrderCondition,
    diagnostics_by_condition: Mapping[
        SecondOrderCondition, ConditionVerificationDiagnostics
    ] | None,
) -> dict[str, int | str | tuple[str, ...] | None]:
    names = (
        "verification_attempts",
        "verification_evidence_available",
        "verification_evidence_unavailable",
        "verification_evidence_ambiguous",
        "verification_evidence_rejected",
        "verification_scope_rejections",
        "oracle_leakage_rejections",
    )
    entry = None if diagnostics_by_condition is None else diagnostics_by_condition.get(condition)
    if entry is not None and entry.condition is not condition:
        raise ValueError("condition diagnostics key and artifact condition must match")
    values: dict[str, int | str | tuple[str, ...] | None] = {
        name: None if entry is None else getattr(entry.diagnostics, name) for name in names
    }
    values.update(
        {
            "verification_diagnostics_status": "NOT_PROVIDED"
            if entry is None
            else "PROVIDED",
            "verification_run_ref": None if entry is None else entry.run_ref,
            "verification_provenance_refs": None
            if entry is None
            else entry.provenance_refs,
        }
    )
    return values


def adapt_matched_experiment(
    result: MatchedExperimentResult,
    *,
    verification_threshold: float,
    verification_diagnostics_by_condition: Mapping[
        SecondOrderCondition, ConditionVerificationDiagnostics
    ] | None = None,
    experiment_level_diagnostics: VerificationDiagnostics | None = None,
) -> SecondOrderEvaluationArtifact:
    if not 0.0 <= verification_threshold <= 1.0:
        raise ValueError("verification_threshold must be between 0 and 1")
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
                **_verification_metadata(
                    summary.condition,
                    verification_diagnostics_by_condition,
                ),
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
        experiment_level_diagnostics=experiment_level_diagnostics,
    )


def adapt_intervention_experiment(
    result: MatchedInterventionExperimentResult,
    *,
    verification_threshold: float,
) -> InterventionEvaluationArtifact:
    if not 0.0 <= verification_threshold <= 1.0:
        raise ValueError("verification_threshold must be between 0 and 1")
    cases = []
    for condition_result in result.conditions:
        summary = condition_result.condition_summary
        verification = condition_result.verification_diagnostics
        intervention = condition_result.intervention_diagnostics
        output = {
            "condition": condition_result.condition.value,
            "run_ref": condition_result.run_ref,
            "provenance_refs": condition_result.provenance_refs,
            "threshold": verification_threshold,
            "trial_count": summary.trial_count,
            "observed_sample_size": summary.observed_sample_size,
            "missing_outcomes": summary.missing_outcomes,
            "monitor_coverage": summary.monitor_coverage,
            "verification_requests": summary.verification_requests,
            "anti_lookahead_valid": summary.anti_lookahead_valid,
            "functional_contribution_status": result.functional_contribution_status,
            "verification_benefit": result.verification_benefit,
            "subjectivity_conclusion": result.subjectivity_conclusion,
            "canonical_effect": result.canonical_effect,
            **{
                name: getattr(verification, name)
                for name in VerificationDiagnostics.__dataclass_fields__
            },
            **{
                name: getattr(intervention, name)
                for name in intervention.__dataclass_fields__
            },
        }
        cases.append(
            ResearchCase(
                case_id=f"verification-intervention:{condition_result.condition.value.lower()}",
                inputs=output,
                metadata={
                    "research_only": True,
                    "condition_local": True,
                    "raw_denominator": summary.trial_count,
                    "interpretation": "RESEARCH_EVIDENCE_ONLY",
                },
            )
        )
    dataset = ResearchDataset(
        name=f"verification-intervention-threshold-{verification_threshold:g}",
        cases=tuple(cases),
        evaluators=(SecondOrderContractEvaluator(),),
    )
    report = evaluate_dataset(
        dataset,
        lambda inputs: dict(inputs),
        implementation_id="verification-intervention-v0.1.x-adapter",
    )
    gate = ClaimBoundaryGate()
    return InterventionEvaluationArtifact(
        report=report,
        subjectivity_claim_disposition=gate.disposition("subjectivity_established"),
        consciousness_claim_disposition=gate.disposition("consciousness_established"),
    )
