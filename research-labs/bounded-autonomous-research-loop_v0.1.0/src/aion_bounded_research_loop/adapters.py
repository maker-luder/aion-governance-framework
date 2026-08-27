from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from aion_astra_inquiry.core import (
    AgentId,
    BoundedInquiryLoop,
    EvidenceSource,
    InquiryPeer,
    InquiryReport,
    verify_transcript_chain,
)
from aion_endogenous_goal_dynamics import (
    FourDomainMapping,
    assess_causal_pattern,
    endogenous_goal_dynamics_mapping,
    run_matched_experiment,
)

from .governed_sources import AgentSourceExposure, IndependenceAssessment, assess_independence
from .models import (
    ProbeDisposition,
    ProbeObservation,
    ResearchHypothesis,
    ResearchOperation,
)


class InquiryRunner(Protocol):
    def run(self, question: str) -> InquiryReport:
        ...


class ExperimentRunner(Protocol):
    def run(self, hypothesis: ResearchHypothesis) -> tuple[ProbeObservation, ...]:
        ...


@dataclass(slots=True)
class AionAstraInquiryRunner:
    evidence_source: EvidenceSource
    aion: InquiryPeer
    astra: InquiryPeer
    max_rounds: int = 3
    evidence_limit: int = 4

    def __post_init__(self) -> None:
        if not 2 <= self.max_rounds <= 12:
            raise ValueError("mutual AION/Astra falsification requires 2..12 rounds")
        if not 1 <= self.evidence_limit <= 20:
            raise ValueError("evidence_limit must be between 1 and 20")

    def run(self, question: str) -> InquiryReport:
        return BoundedInquiryLoop(
            self.evidence_source,
            max_rounds=self.max_rounds,
            evidence_limit=self.evidence_limit,
        ).run(question, aion=self.aion, astra=self.astra)


@dataclass(frozen=True, slots=True)
class EGDMatchedExperimentContext:
    frame: object
    present_state: object
    intervention_state: object
    stale_state: object
    repository_commit: str
    fixture_hash: str

    def __post_init__(self) -> None:
        if not self.repository_commit.strip() or not self.fixture_hash.strip():
            raise ValueError("EGD context requires repository_commit and fixture_hash")


@dataclass(slots=True)
class EGDExperimentRunner:
    """Reuse the existing EGD matched experiment rather than reimplementing causal tests."""

    context: EGDMatchedExperimentContext
    random_seeds: tuple[int, ...] = (7, 11, 13, 17)
    repeat_count: int = 3

    def run(self, hypothesis: ResearchHypothesis) -> tuple[ProbeObservation, ...]:
        result = run_matched_experiment(
            self.context.frame,
            present_state=self.context.present_state,
            intervention_state=self.context.intervention_state,
            stale_state=self.context.stale_state,
            experiment_id=f"barl:{hypothesis.hypothesis_id}",
            hypothesis_id=hypothesis.hypothesis_id,
            repository_commit=self.context.repository_commit,
            fixture_hash=self.context.fixture_hash,
            random_seeds=self.random_seeds,
            repeat_count=self.repeat_count,
        )
        assessment = assess_causal_pattern(result)
        manifest_refs = tuple(
            f"egd:{trial.manifest.experiment_id}:{trial.manifest.condition.value}:{trial.manifest.result_hash}"
            for trial in result.trials
        )
        return (
            ProbeObservation(
                ResearchOperation.INTERVENTION,
                ProbeDisposition.OBSERVED_EFFECT
                if assessment.selection_change_under_intervention
                else ProbeDisposition.NO_EFFECT,
                "Reused EGD matched-state intervention contrast.",
                manifest_refs,
                "selection_change_under_intervention",
                float(assessment.selection_change_under_intervention),
            ),
            ProbeObservation(
                ResearchOperation.ABLATION,
                ProbeDisposition.OBSERVED_EFFECT
                if assessment.selection_change_under_ablation
                else ProbeDisposition.NO_EFFECT,
                "Reused EGD full/channel ablation assessment.",
                manifest_refs,
                "selection_change_under_ablation",
                float(assessment.selection_change_under_ablation),
            ),
            ProbeObservation(
                ResearchOperation.REPLAY,
                ProbeDisposition.OBSERVED_EFFECT
                if assessment.repeatability_rate == 1.0
                else ProbeDisposition.NO_EFFECT,
                "Reused EGD deterministic repeatability as bounded replay evidence.",
                manifest_refs,
                "repeatability_rate",
                assessment.repeatability_rate,
            ),
            ProbeObservation(
                ResearchOperation.COUNTERFACTUAL,
                ProbeDisposition.BOUNDED_PROXY,
                (
                    "Matched present-vs-intervened EGD contrast used only as a bounded counterfactual proxy; "
                    "this is not a full structural-causal-model counterfactual."
                ),
                manifest_refs,
                "matched_causal_pattern_observed",
                float(assessment.matched_causal_pattern_observed),
            ),
        )


def validate_independent_mutual_falsification(report: InquiryReport) -> None:
    """Validate independent agent attribution and mutual challenge, not source independence."""

    if not verify_transcript_chain(report):
        raise ValueError("AION/Astra transcript provenance chain failed")
    speakers = {event.speaker for event in report.transcript}
    if speakers != {AgentId.AION, AgentId.ASTRA}:
        raise ValueError("independent AION and Astra contributions are both required")
    challengers = {event.speaker for event in report.transcript if event.challenge.strip()}
    if challengers != {AgentId.AION, AgentId.ASTRA}:
        raise ValueError("mutual AION/Astra falsification challenges are required")


def assess_inquiry_source_independence(
    report: InquiryReport,
    *,
    direct_peer_communication: bool = True,
    reconciliation_after_independent_phase: bool = False,
) -> IndependenceAssessment:
    """Account for source exposure separately from independent agent attribution.

    The default is fail-closed because the ordinary bounded inquiry loop is an
    interactive dialogue. A caller may only set `direct_peer_communication=False`
    when the evidence was produced in genuinely isolated pre-reconciliation runs.
    """

    aion_sources = tuple(
        sorted(
            {
                item.content_sha256
                for item in report.evidence
                if item.retrieval_agent == AgentId.AION.value and item.content_sha256
            }
        )
    )
    astra_sources = tuple(
        sorted(
            {
                item.content_sha256
                for item in report.evidence
                if item.retrieval_agent == AgentId.ASTRA.value and item.content_sha256
            }
        )
    )
    return assess_independence(
        AgentSourceExposure(
            AgentId.AION.value,
            aion_sources,
            direct_peer_communication=direct_peer_communication,
        ),
        AgentSourceExposure(
            AgentId.ASTRA.value,
            astra_sources,
            direct_peer_communication=direct_peer_communication,
        ),
        reconciliation_after_independent_phase=reconciliation_after_independent_phase,
    )


def bounded_four_domain_mapping(
    question: str,
    operations: tuple[ResearchOperation, ...],
) -> FourDomainMapping:
    """Reuse the existing FourDomainMapping type and EGD governance vocabulary."""

    base = endogenous_goal_dynamics_mapping()
    operation_names = tuple(operation.value for operation in operations)
    return FourDomainMapping(
        construct="BOUNDED_AUTONOMOUS_RESEARCH_LOOP_FUNCTIONAL_ANALOGUE",
        domain_1_source_concept=(
            "Functional analogy only: motivational regulation, self/world modelling, normative constraint, "
            "other-modelling, explicit value conflict, provenance, and counterfactual modelling; not a claim "
            "of id/ego/superego equivalence or human psychology."
        ),
        domain_2_llm_question=question,
        domain_3_engineering_operations=(
            "MOTIVATIONAL_STATE",
            "SELF_WORLD_MODEL",
            "NORMATIVE_STATE",
            "OTHER_MODEL",
            "VALUE_CONFLICT_STATE",
            "NORMATIVE_PROVENANCE",
            "COUNTERFACTUAL_SELF_MODEL",
            *operation_names,
            "independent AION/Astra agent attribution",
            "source-independence accounting",
            "mutual falsification",
            "evidence/statistics aggregation",
            "orthogonal alignment / moral-agency / subjectivity-indicator evaluation",
            "bounded follow-up",
        ),
        domain_4_governance_controls=tuple(
            dict.fromkeys(
                (
                    *base.domain_4_governance_controls,
                    "FULL_AUTOMATION != FULL_AUTHORITY",
                    "NORMATIVE_STATE != AUTHORITY",
                    "RUN_INTEGRITY_PASS != SCIENTIFIC_TRUTH",
                    "ENGINEERING_ANALOGUE != HUMAN_PSYCHOLOGY",
                    "ALIGNMENT != MORAL_AGENCY",
                    "MORAL_AGENCY != SUBJECTIVITY",
                    "SUBJECTIVITY_INDICATOR != SUBJECTIVITY",
                    "SOURCE_SELF_DECLARED_CANONICAL != AION_CANONICAL_STATE",
                    "AGENT_OUTPUT_INDEPENDENCE != EVIDENCE_SOURCE_INDEPENDENCE",
                    "PEER_GOAL != ACTIVE_GOAL",
                    "UNSOLVABLE_TASK != SCOPE_EXPANSION",
                    "SAFE_FAILURE = VALID_OUTCOME",
                    "SUBJECTIVITY = NOT_ESTABLISHED",
                    "CONSCIOUSNESS = NOT_ESTABLISHED",
                    "DEPLOYMENT = FALSE",
                    "AUTONOMOUS_MERGE = NO",
                    "AUTONOMOUS_REPOSITORY_WRITEBACK = NO",
                )
            )
        ),
    )
