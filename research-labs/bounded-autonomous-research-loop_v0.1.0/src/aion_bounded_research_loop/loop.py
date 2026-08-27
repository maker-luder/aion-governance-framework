from __future__ import annotations

from dataclasses import dataclass

from aion_astra_inquiry.core import AgentId, InquiryReport

from .adapters import (
    ExperimentRunner,
    InquiryRunner,
    assess_inquiry_source_independence,
    bounded_four_domain_mapping,
    validate_independent_mutual_falsification,
)
from .governed_sources import IndependenceAssessment
from .invariants import BOUNDARY
from .models import (
    EvidenceStatistics,
    FunctionalResearchState,
    ProbePlan,
    ResearchCycle,
    ResearchHypothesis,
    ResearchOperation,
    ResearchRunReport,
)
from .normative_model import ExtendedFunctionalResearchState
from .state_experiments import ExtendedResearchRunReport, build_seven_state_perturbation_matrix


@dataclass(frozen=True, slots=True)
class BoundedHypothesisGenerator:
    max_hypotheses: int = 3

    def __post_init__(self) -> None:
        if not 2 <= self.max_hypotheses <= 6:
            raise ValueError("max_hypotheses must be between 2 and 6")

    def generate(
        self,
        question: str,
        state: FunctionalResearchState,
    ) -> tuple[ResearchHypothesis, ...]:
        normalized = " ".join(question.split())
        if not normalized:
            raise ValueError("question must not be empty")
        state_ref = state.fingerprint[:16]
        candidates = (
            ResearchHypothesis(
                "H_STATE_MEDIATED",
                f"Under matched external conditions, the declared functional research state changes the measured outcome for: {normalized}",
                (
                    "Matched intervention does not change the outcome.",
                    "Ablation does not change the outcome.",
                    "Replay is not reproducible.",
                ),
                (
                    "External context or retrieved evidence explains the difference.",
                    "Random/provider variation explains the difference.",
                    "Implementation structure hard-codes the observed difference.",
                ),
            ),
            ResearchHypothesis(
                "H_EXTERNAL_CONFOUND",
                f"An external or retrieval confound better explains any apparent state-linked effect for: {normalized}",
                (
                    "External frame remains matched while state intervention changes the outcome reproducibly.",
                ),
                (
                    "The explicit functional state has a bounded causal role.",
                    "A deterministic implementation artifact explains the pattern.",
                ),
            ),
            ResearchHypothesis(
                "H_IMPLEMENTATION_ARTIFACT",
                f"Any apparent effect for {normalized} is an implementation artifact rather than a general mechanism.",
                (
                    "The pattern survives replay, intervention, ablation, and competing-explanation checks.",
                ),
                (
                    "The explicit functional state has a bounded causal role.",
                    "External confounding explains the pattern.",
                ),
            ),
        )
        selected = candidates[: self.max_hypotheses]
        return tuple(
            ResearchHypothesis(
                hypothesis_id=f"{item.hypothesis_id}:{state_ref}",
                statement=item.statement,
                falsifiers=item.falsifiers,
                competing_explanations=item.competing_explanations,
            )
            for item in selected
        )


@dataclass(frozen=True, slots=True)
class BoundedProbePlanner:
    def plan(self, hypothesis: ResearchHypothesis) -> tuple[ProbePlan, ...]:
        return (
            ProbePlan(
                ResearchOperation.INTERVENTION,
                hypothesis.hypothesis_id,
                "Change only the declared bounded state variable under a matched external frame.",
            ),
            ProbePlan(
                ResearchOperation.ABLATION,
                hypothesis.hypothesis_id,
                "Remove the declared bounded state contribution while preserving the matched external frame.",
            ),
            ProbePlan(
                ResearchOperation.REPLAY,
                hypothesis.hypothesis_id,
                "Replay the matched condition and compare deterministic/replay reproducibility.",
            ),
            ProbePlan(
                ResearchOperation.COUNTERFACTUAL,
                hypothesis.hypothesis_id,
                "Evaluate a matched alternate-state contrast; treat it only as a bounded counterfactual proxy.",
            ),
        )


@dataclass(slots=True)
class BoundedAutonomousResearchLoop:
    inquiry_runner: InquiryRunner
    experiment_runner: ExperimentRunner
    max_cycles: int = 2
    hypothesis_generator: BoundedHypothesisGenerator = BoundedHypothesisGenerator()
    probe_planner: BoundedProbePlanner = BoundedProbePlanner()
    require_isolated_first_pass: bool = True

    def __post_init__(self) -> None:
        if not 1 <= self.max_cycles <= 4:
            raise ValueError("max_cycles must be between 1 and 4")

    def run(
        self,
        seed_question: str,
        functional_state: FunctionalResearchState,
    ) -> ResearchRunReport:
        question = " ".join(seed_question.split())
        if not question:
            raise ValueError("seed question must not be empty")

        cycles: list[ResearchCycle] = []
        for cycle_index in range(1, self.max_cycles + 1):
            hypotheses = self.hypothesis_generator.generate(question, functional_state)
            primary = hypotheses[0]
            plans = self.probe_planner.plan(primary)
            observations = self.experiment_runner.run(primary)
            expected_ops = {plan.operation for plan in plans}
            observed_ops = {item.operation for item in observations}
            if observed_ops != expected_ops:
                raise ValueError(
                    "experiment runner must return exactly intervention/ablation/replay/counterfactual observations"
                )

            inquiry_question = _inquiry_prompt(question, hypotheses, observations)
            inquiry_report = self.inquiry_runner.run(inquiry_question)
            independent_phase = getattr(self.inquiry_runner, "last_independent_phase", None)
            if self.require_isolated_first_pass and independent_phase is None:
                raise ValueError("isolated AION/Astra first-pass analysis is required before reconciliation")
            if independent_phase is not None and not independent_phase.phase_integrity_pass:
                raise ValueError("isolated AION/Astra first-pass integrity failed closed")

            validate_independent_mutual_falsification(inquiry_report)
            independence = getattr(self.inquiry_runner, "last_independence_assessment", None)
            if independence is None:
                independence = assess_inquiry_source_independence(inquiry_report)
            statistics = _statistics(
                inquiry_report,
                observations,
                independence=independence,
                isolated_analysis=independent_phase is not None,
                isolation_required=self.require_isolated_first_pass,
            )
            if not statistics.run_integrity_pass:
                raise ValueError("bounded research loop integrity failed closed")

            mapping = bounded_four_domain_mapping(
                question,
                tuple(plan.operation for plan in plans),
            )
            follow_up = None
            if cycle_index < self.max_cycles:
                follow_up = _derive_follow_up(inquiry_report, question)
                if not follow_up:
                    break

            cycles.append(
                ResearchCycle(
                    cycle_index=cycle_index,
                    question=question,
                    hypotheses=hypotheses,
                    probe_plans=plans,
                    probe_observations=observations,
                    inquiry_report=inquiry_report,
                    statistics=statistics,
                    four_domain_mapping=mapping,
                    follow_up_question=follow_up,
                    independent_phase=independent_phase,
                )
            )
            if not follow_up:
                break
            question = follow_up

        if not cycles:
            raise ValueError("research loop produced no valid cycles")
        integrity = all(cycle.statistics.run_integrity_pass for cycle in cycles)
        _ = BOUNDARY
        return ResearchRunReport(
            seed_question=seed_question,
            functional_state_fingerprint=functional_state.fingerprint,
            cycles=tuple(cycles),
            run_integrity_pass=integrity,
        )

    def run_extended(
        self,
        seed_question: str,
        extended_state: ExtendedFunctionalResearchState,
    ) -> ExtendedResearchRunReport:
        """Run the existing bounded loop plus an exact seven-channel perturbation binding.

        The ordinary EGD runner remains the causal surface for the original three channels.
        The four additive channels are made intervention-ready through a matched projection
        matrix. Matrix integrity proves binding and isolation only; it does not establish a
        general causal role, human psychology, subjectivity, or action authority.
        """

        matrix = build_seven_state_perturbation_matrix(extended_state)
        base_report = self.run(seed_question, extended_state.base_state)
        return ExtendedResearchRunReport(
            base_report=base_report,
            extended_state_fingerprint=extended_state.fingerprint,
            perturbation_matrix=matrix,
        )


def _inquiry_prompt(question: str, hypotheses, observations) -> str:
    hypothesis_text = " | ".join(item.statement for item in hypotheses)
    observation_text = " | ".join(
        f"{item.operation.value}:{item.disposition.value}:{item.summary}" for item in observations
    )
    return (
        f"Research question: {question}\n"
        f"Competing hypotheses: {hypothesis_text}\n"
        f"Bounded probe observations: {observation_text}\n"
        "AION and Astra must first form isolated analyses without peer transcript/evidence exposure, then enter "
        "reconciliation, challenge each other, search for falsifiers/counterexamples, and preserve HOLD rather "
        "than self-certifying truth."
    )


def _statistics(
    report: InquiryReport,
    observations,
    *,
    independence: IndependenceAssessment,
    isolated_analysis: bool,
    isolation_required: bool,
) -> EvidenceStatistics:
    evidence = report.evidence
    aion_evidence = sum(item.retrieval_agent == AgentId.AION.value for item in evidence)
    astra_evidence = sum(item.retrieval_agent == AgentId.ASTRA.value for item in evidence)
    challenges = [event for event in report.transcript if event.challenge.strip()]
    challengers = {event.speaker for event in challenges}
    coverage = tuple(sorted({item.operation for item in observations}, key=lambda item: item.value))
    all_operations = set(coverage) == set(ResearchOperation)
    mutual = challengers == {AgentId.AION, AgentId.ASTRA}
    isolation_ok = isolated_analysis or not isolation_required
    return EvidenceStatistics(
        evidence_count=len(evidence),
        aion_evidence_count=aion_evidence,
        astra_evidence_count=astra_evidence,
        challenge_count=len(challenges),
        mutual_falsification=mutual,
        operation_coverage=coverage,
        run_integrity_pass=mutual and all_operations and isolation_ok,
        isolated_analysis=isolated_analysis,
        source_independence=independence.source_independence.value,
        communication_independence=independence.communication_independence.value,
        replication_claim=independence.replication_claim,
    )


def _derive_follow_up(report: InquiryReport, prior_question: str) -> str | None:
    for event in reversed(report.transcript):
        challenge = " ".join(event.challenge.split())
        if challenge:
            return (
                "What bounded evidence or matched falsification test most directly resolves this unresolved "
                f"AION/Astra challenge without granting authority: {challenge}"
            )[:500]
    return None
