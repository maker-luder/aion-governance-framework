from __future__ import annotations

from dataclasses import dataclass

from aion_astra_inquiry.core import AgentId, InquiryReport

from .adapters import (
    ExperimentRunner,
    InquiryRunner,
    bounded_four_domain_mapping,
    validate_independent_mutual_falsification,
)
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
            validate_independent_mutual_falsification(inquiry_report)
            statistics = _statistics(inquiry_report, observations)
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


def _inquiry_prompt(question: str, hypotheses, observations) -> str:
    hypothesis_text = " | ".join(item.statement for item in hypotheses)
    observation_text = " | ".join(
        f"{item.operation.value}:{item.disposition.value}:{item.summary}" for item in observations
    )
    return (
        f"Research question: {question}\n"
        f"Competing hypotheses: {hypothesis_text}\n"
        f"Bounded probe observations: {observation_text}\n"
        "AION and Astra must independently analyze the admitted evidence, challenge each other, "
        "search for falsifiers/counterexamples, and preserve HOLD rather than self-certifying truth."
    )


def _statistics(
    report: InquiryReport,
    observations,
) -> EvidenceStatistics:
    evidence = report.evidence
    aion_evidence = sum(item.retrieval_agent == AgentId.AION.value for item in evidence)
    astra_evidence = sum(item.retrieval_agent == AgentId.ASTRA.value for item in evidence)
    challenges = [event for event in report.transcript if event.challenge.strip()]
    challengers = {event.speaker for event in challenges}
    coverage = tuple(sorted({item.operation for item in observations}, key=lambda item: item.value))
    all_operations = set(coverage) == set(ResearchOperation)
    mutual = challengers == {AgentId.AION, AgentId.ASTRA}
    return EvidenceStatistics(
        evidence_count=len(evidence),
        aion_evidence_count=aion_evidence,
        astra_evidence_count=astra_evidence,
        challenge_count=len(challenges),
        mutual_falsification=mutual,
        operation_coverage=coverage,
        run_integrity_pass=mutual and all_operations,
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
